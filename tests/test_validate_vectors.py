from __future__ import annotations

import ast
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
            "requirements",
            "vectors",
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

    def report(self) -> VALIDATOR.ValidationReport:
        return VALIDATOR.validate_repository(self.root)

    def errors(self) -> str:
        return "\n".join(self.report().errors)

    def write_json(self, relative_path: str, value: object) -> None:
        destination = self.root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def load_json(self, relative_path: str) -> dict[str, object]:
        value = json.loads((self.root / relative_path).read_text(encoding="utf-8"))
        self.assertIsInstance(value, dict)
        return value

    def test_candidate_repository_is_valid(self) -> None:
        report = self.report()
        self.assertEqual([], report.errors)
        self.assertEqual(8, report.vector_count)
        self.assertEqual(7, report.core_vector_count)
        self.assertEqual(7, report.candidate_count)
        self.assertEqual(0, report.released_count)
        self.assertEqual(6, report.requirement_count)
        self.assertEqual(1, report.schema_example_count)

    def test_validator_does_not_import_reference_implementation(self) -> None:
        source = VALIDATOR_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        self.assertNotIn("wexp_ref", imported_roots)

    def test_duplicate_document_and_vector_id_are_rejected(self) -> None:
        shutil.copy2(
            self.root / "vectors/core-00/WEXP-CORE-00-V0001.json",
            self.root / "vectors/core-00/copy.json",
        )
        errors = self.errors()
        self.assertIn("duplicate vector document content", errors)
        self.assertIn("duplicate vector_id", errors)

    def test_duplicate_json_member_is_rejected(self) -> None:
        destination = self.root / "vectors/core-00/duplicate-key.json"
        destination.write_text(
            '{"vector_id":"WEXP-CORE-00-V0098",'
            '"vector_id":"WEXP-CORE-00-V0099"}\n',
            encoding="utf-8",
        )
        self.assertIn("duplicate JSON member 'vector_id'", self.errors())

    def test_revision_scoped_requirement_id_is_required(self) -> None:
        vector_path = "vectors/core-00/WEXP-CORE-00-V0001.json"
        vector = self.load_json(vector_path)
        vector["requirement_ids"] = ["WEXP-CORE-REQ-0001"]
        self.write_json(vector_path, vector)
        self.assertIn("invalid requirement ID 'WEXP-CORE-REQ-0001'", self.errors())

    def test_unknown_reviewed_requirement_is_rejected(self) -> None:
        vector_path = "vectors/core-00/WEXP-CORE-00-V0001.json"
        vector = self.load_json(vector_path)
        vector["requirement_ids"] = ["WEXP-CORE-00-REQ-9999"]
        self.write_json(vector_path, vector)
        self.assertIn("unknown reviewed requirement", self.errors())

    def test_unreviewed_requirement_is_rejected(self) -> None:
        registry_path = "requirements/core-00.json"
        registry = self.load_json(registry_path)
        requirements = registry["requirements"]
        self.assertIsInstance(requirements, list)
        requirements[0]["review_status"] = "ambiguous"
        requirements[0]["vector_eligibility"] = False
        self.write_json(registry_path, registry)
        errors = self.errors()
        self.assertIn("requirement is not ready for vectors", errors)
        self.assertIn("requirement is not vector-eligible", errors)

    def test_unused_requirement_is_rejected(self) -> None:
        for path in sorted((self.root / "vectors/core-00").glob("*.json")):
            vector = json.loads(path.read_text(encoding="utf-8"))
            vector["requirement_ids"] = [
                item
                for item in vector["requirement_ids"]
                if item != "WEXP-CORE-00-REQ-0005"
            ]
            if not vector["requirement_ids"]:
                vector["requirement_ids"] = ["WEXP-CORE-00-REQ-0006"]
            self.write_json(path.relative_to(self.root).as_posix(), vector)
        self.assertIn("WEXP-CORE-00-REQ-0005", self.errors())

    def test_core_source_hash_mismatch_is_rejected(self) -> None:
        vector_path = "vectors/core-00/WEXP-CORE-00-V0001.json"
        vector = self.load_json(vector_path)
        vector["specification"]["sha256"] = "0" * 64
        self.write_json(vector_path, vector)
        self.assertIn("Core source identity mismatch", self.errors())

    def test_non_normative_harness_shape_is_enforced(self) -> None:
        vector_path = "vectors/core-00/WEXP-CORE-00-V0001.json"
        vector = self.load_json(vector_path)
        vector["input"]["prior_checks"]["signature"] = "unchecked"
        self.write_json(vector_path, vector)
        self.assertIn("test-harness schema error", self.errors())
        self.assertIn("'valid' was expected", self.errors())

    def test_unknown_extension_names_must_be_unique(self) -> None:
        vector_path = "vectors/core-00/WEXP-CORE-00-V0007.json"
        vector = self.load_json(vector_path)
        vector["input"]["unknown_extensions"] = [
            {"name": "slice-unknown", "critical": False},
            {"name": "slice-unknown", "critical": True},
        ]
        self.write_json(vector_path, vector)
        self.assertIn(
            "duplicate unknown extension name 'slice-unknown'",
            self.errors(),
        )

    def test_manifest_hash_mismatch_is_rejected(self) -> None:
        manifest_path = "manifests/vectors.json"
        manifest = self.load_json(manifest_path)
        manifest["schemas"]["vector_envelope"]["sha256"] = "0" * 64
        self.write_json(manifest_path, manifest)
        self.assertIn("sha256 mismatch for schema/vector.schema.json", self.errors())

    def test_manifest_rejects_unsafe_paths(self) -> None:
        manifest_path = "manifests/vectors.json"
        for unsafe_path in ("../vector.json", "/vector.json", "vectors\\vector.json"):
            with self.subTest(unsafe_path=unsafe_path):
                manifest = self.load_json(manifest_path)
                manifest["vectors"][1]["path"] = unsafe_path
                self.write_json(manifest_path, manifest)
                self.assertIn("unsafe or non-canonical path", self.errors())
                shutil.copy2(
                    REPOSITORY_ROOT / manifest_path,
                    self.root / manifest_path,
                )

    def test_manifest_rejects_released_entry_in_candidate_package(self) -> None:
        manifest_path = "manifests/vectors.json"
        manifest = self.load_json(manifest_path)
        manifest["vectors"][1]["status"] = "released"
        self.write_json(manifest_path, manifest)
        self.assertIn("status must be 'candidate'", self.errors())

    def test_unlisted_vector_file_is_rejected(self) -> None:
        source = self.root / "vectors/core-00/WEXP-CORE-00-V0001.json"
        value = json.loads(source.read_text(encoding="utf-8"))
        value["vector_id"] = "WEXP-CORE-00-V0099"
        self.write_json("vectors/core-00/WEXP-CORE-00-V0099.json", value)
        self.assertIn("unlisted vector file", self.errors())

    def test_core_vector_filename_must_match_vector_id(self) -> None:
        source = self.root / "vectors/core-00/WEXP-CORE-00-V0001.json"
        destination = self.root / "vectors/core-00/misnamed.json"
        source.rename(destination)
        self.assertIn("path must match its revision-scoped vector ID", self.errors())

    def test_invalid_envelope_schema_is_reported_without_crashing(self) -> None:
        schema_path = "schema/vector.schema.json"
        schema = self.load_json(schema_path)
        schema["type"] = "not-a-json-schema-type"
        self.write_json(schema_path, schema)
        self.assertIn("invalid JSON Schema", self.errors())

    def test_invalid_harness_schema_is_reported_without_crashing(self) -> None:
        schema_path = "schema/core-00-test-harness.schema.json"
        schema = self.load_json(schema_path)
        schema["type"] = "not-a-json-schema-type"
        self.write_json(schema_path, schema)
        self.assertIn("invalid JSON Schema", self.errors())

    def test_fixed_manifest_files_must_not_be_symbolic_links(self) -> None:
        for relative_path, expected_error in (
            ("VERSION", "VERSION must not be a symbolic link"),
            (
                "manifests/vectors.json",
                "manifest must not be a symbolic link",
            ),
            (
                "requirements/core-00.json",
                "requirement registry must not be a symbolic link",
            ),
            (
                "schema/vector.schema.json",
                "schema must not be a symbolic link",
            ),
        ):
            with self.subTest(relative_path=relative_path):
                original = self.root / relative_path
                replacement = original.with_name(original.name + ".target")
                original.rename(replacement)
                original.symlink_to(replacement.name)
                self.assertIn(expected_error, self.errors())
                original.unlink()
                replacement.rename(original)

    def test_vector_roots_must_not_be_symbolic_links(self) -> None:
        original = self.root / "vectors"
        replacement = self.root / "vectors.target"
        original.rename(replacement)
        original.symlink_to(replacement.name, target_is_directory=True)
        self.assertIn("vector root must not be a symbolic link: vectors", self.errors())


if __name__ == "__main__":
    unittest.main()
