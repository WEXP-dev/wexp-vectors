from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate_vectors.py"
MODULE_SPEC = importlib.util.spec_from_file_location("validate_vectors", VALIDATOR_PATH)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:  # pragma: no cover
    raise RuntimeError(f"cannot import validator from {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = VALIDATOR
MODULE_SPEC.loader.exec_module(VALIDATOR)


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
        self.root.mkdir()
        for relative_directory in (
            "schema",
            "examples",
            "manifests",
        ):
            shutil.copytree(
                REPOSITORY_ROOT / relative_directory,
                self.root / relative_directory,
            )
        shutil.copy2(REPOSITORY_ROOT / "VERSION", self.root / "VERSION")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def errors(self) -> list[str]:
        return VALIDATOR.validate_repository(self.root).errors

    def write_json(self, relative_path: str, value: object) -> None:
        destination = self.root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def load_example(self) -> dict[str, object]:
        return json.loads(
            (self.root / "examples/non-normative-schema-example.json").read_text(
                encoding="utf-8"
            )
        )

    def test_public_infrastructure_repository_is_valid(self) -> None:
        report = VALIDATOR.validate_repository(self.root)
        self.assertEqual([], report.errors)
        self.assertEqual(1, report.vector_count)
        self.assertEqual(1, report.schema_example_count)
        self.assertEqual(0, report.interop_count)

    def test_duplicate_document_and_vector_id_are_rejected(self) -> None:
        shutil.copy2(
            self.root / "examples/non-normative-schema-example.json",
            self.root / "examples/duplicate.json",
        )
        errors = "\n".join(self.errors())
        self.assertIn("duplicate vector document content", errors)
        self.assertIn("duplicate vector_id", errors)

    def test_duplicate_json_member_is_rejected(self) -> None:
        destination = self.root / "examples/duplicate-key.json"
        destination.write_text(
            '{"vector_id":"WEXP-EXAMPLE-V0002",'
            '"vector_id":"WEXP-EXAMPLE-V0003"}\n',
            encoding="utf-8",
        )
        self.assertIn("duplicate JSON member 'vector_id'", "\n".join(self.errors()))

    def test_requirement_id_format_is_checked_explicitly(self) -> None:
        vector = self.load_example()
        vector.update(
            {
                "vector_id": "WEXP-CORE-V0001",
                "specification": "core",
                "classification": "positive",
                "requirement_ids": ["NOT-A-REQUIREMENT-ID"],
                "description": "Synthetic validator test fixture; not a protocol vector.",
            }
        )
        self.write_json("vectors/bad-requirement.json", vector)
        self.assertIn("invalid requirement ID", "\n".join(self.errors()))

    def test_interop_requires_mapping_and_rejects_floating_revision(self) -> None:
        vector = {
            "vector_id": "WEXP-INTEROP-V0001",
            "specification": "interop",
            "requirement_ids": [],
            "description": "Synthetic validator test fixture; not an interop claim.",
            "classification": "interop",
            "input": {"fixture": True},
            "expected": {"validator_fixture": True},
            "external_specifications": [
                {
                    "identity": "synthetic-test-document",
                    "relationship": "MAPPING",
                    "revision_kind": "tag",
                    "exact_revision": "HEAD"
                }
            ],
            "assumptions": ["Synthetic validation fixture only"]
        }
        self.write_json("vectors/floating-interop.json", vector)
        errors = "\n".join(self.errors())
        self.assertIn("must declare mapping_id", errors)
        self.assertIn("uses floating revision 'HEAD'", errors)

    def test_manifest_hash_mismatch_is_rejected(self) -> None:
        manifest_path = self.root / "manifests/vectors.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["schema"]["sha256"] = "0" * 64
        self.write_json("manifests/vectors.json", manifest)
        self.assertIn("schema sha256 mismatch", "\n".join(self.errors()))

    def test_invalid_json_schema_is_reported_without_crashing(self) -> None:
        schema_path = self.root / "schema/vector.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["type"] = "not-a-json-schema-type"
        self.write_json("schema/vector.schema.json", schema)
        self.assertIn("invalid JSON Schema", "\n".join(self.errors()))


if __name__ == "__main__":
    unittest.main()
