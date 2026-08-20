from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_core01_vectors.py"
SET_ROOT = ROOT / "vectors" / "WEXP-CORE-01-VECTORS-001"


def run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_core01_vectors.py")],
        capture_output=True, text=True, cwd=root,
    )


class Core01VectorSetTest(unittest.TestCase):
    def test_repository_set_validates(self) -> None:
        result = run(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: 16 vector(s)", result.stdout)

    def test_declared_vector_set_identity_is_stable(self) -> None:
        manifest = json.loads((ROOT / "manifests" / "core-01-vectors.json").read_bytes())
        self.assertIn(manifest["vector_set_sha256"], run(ROOT).stdout)


class TamperTest(unittest.TestCase):
    """Every mutation must be caught. A corpus that validates after its
    expectations were edited would certify nothing."""

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        for name in ("scripts", "schema", "vectors", "manifests"):
            shutil.copytree(ROOT / name, self.root / name)
        self.set_root = self.root / "vectors" / "WEXP-CORE-01-VECTORS-001"

    def _rejects(self) -> None:
        result = run(self.root)
        self.assertEqual(result.returncode, 1, f"expected rejection, got:\n{result.stdout}")

    def _edit(self, relative: str, mutate) -> None:
        path = self.set_root / relative
        payload = json.loads(path.read_bytes())
        mutate(payload)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def test_baseline_copy_validates(self) -> None:
        self.assertEqual(run(self.root).returncode, 0)

    def test_edited_expectation_is_rejected(self) -> None:
        self._edit(
            "vectors/WEXP-CORE-01-Q001-TV-0006.json",
            lambda v: v["expected"].__setitem__("asserted_claim_supported", True),
        )
        self._rejects()

    def test_edited_specification_copy_is_rejected(self) -> None:
        spec = self.set_root / "spec" / "draft-sergeev-wexp-core-01.xml"
        spec.write_bytes(spec.read_bytes() + b"<!-- -->")
        self._rejects()

    def test_one_byte_mutation_is_rejected(self) -> None:
        vector = self.set_root / "vectors" / "WEXP-CORE-01-Q001-TV-0001.json"
        original = vector.read_bytes()
        indentation = original.index(b"\n  ") + 1
        mutated = original[:indentation] + b"\t" + original[indentation + 1 :]
        self.assertEqual(len(original), len(mutated))
        self.assertEqual(1, sum(left != right for left, right in zip(original, mutated)))
        vector.write_bytes(mutated)

        result = run(self.root)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("digest mismatch", result.stderr)

    def test_line_ending_only_change_is_rejected(self) -> None:
        vector = self.set_root / "vectors" / "WEXP-CORE-01-Q001-TV-0001.json"
        original = vector.read_bytes()
        self.assertNotIn(b"\r\n", original)
        mutated = original.replace(b"\n", b"\r\n")
        self.assertNotEqual(original, mutated)
        vector.write_bytes(mutated)

        result = run(self.root)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("digest mismatch", result.stderr)

    def test_removed_vector_is_rejected(self) -> None:
        (self.set_root / "vectors" / "WEXP-CORE-01-Q001-TV-0001.json").unlink()
        self._rejects()

    def test_binding_disagreement_is_rejected(self) -> None:
        self._edit(
            "vectors/WEXP-CORE-01-Q001-TV-0003.json",
            lambda v: v.__setitem__("source_fixture", "C99"),
        )
        self._rejects()


if __name__ == "__main__":
    unittest.main()
