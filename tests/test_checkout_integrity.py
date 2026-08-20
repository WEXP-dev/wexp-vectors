from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# These pathspecs mirror the explicit canonical-byte inventory and
# .gitattributes. Vector-set contents are protected independent of extension;
# the other rules are deliberately scoped to the proven files.
PRESERVED_PATHSPECS = (
    ":(glob)manifests/*.json",
    "requirements/core-00.json",
    ":(glob)schema/*.json",
    "examples/non-normative-schema-example.json",
    "vectors",
    ":(glob)evidence/core-01-set-002/*.json",
    "provenance/PUBLIC-GENESIS.json",
)


def git(*arguments: str, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=text,
    )


def tracked_preserved_paths() -> list[str]:
    result = git("ls-files", "-z", "--", *PRESERVED_PATHSPECS)
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


class CheckoutIntegrityTest(unittest.TestCase):
    def test_every_preserved_path_disables_git_text_conversion(self) -> None:
        paths = tracked_preserved_paths()
        self.assertGreater(len(paths), 0)
        result = git("check-attr", "text", "--", *paths, text=True)
        attributes = {}
        for line in result.stdout.splitlines():
            path, attribute, value = line.rsplit(": ", 2)
            self.assertEqual(attribute, "text")
            attributes[path] = value

        self.assertEqual(set(paths), set(attributes))
        self.assertEqual(
            {},
            {path: value for path, value in attributes.items() if value != "unset"},
        )

    def test_worktree_preserves_canonical_git_blob_bytes(self) -> None:
        paths = tracked_preserved_paths()
        self.assertGreater(len(paths), 0)
        mismatches = []
        for relative_path in paths:
            canonical = git("cat-file", "blob", f"HEAD:{relative_path}").stdout
            observed = (ROOT / relative_path).read_bytes()
            if observed != canonical:
                mismatches.append(relative_path)
        self.assertEqual([], mismatches, "checkout changed canonical repository bytes")


if __name__ == "__main__":
    unittest.main()
