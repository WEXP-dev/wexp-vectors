#!/usr/bin/env python3
"""Validate the WEXP Core-01 public vector set.

Kept separate from ``validate_vectors.py`` on purpose. That script validates the
Core-00 envelope, whose schema is closed and whose shape Core-01 does not share;
folding two envelopes into one validator would mean loosening the Core-00 one.

Checks, all fail-closed:

* every vector, the descriptor and the profile validate against their schemas;
* every ``bound_files`` digest matches the file on disk, and the set is exactly
  the set of vector files present;
* the profile digest declared by the descriptor matches the profile;
* the bundled specification copy matches the digest the descriptor declares, so
  the set is provably bound to those exact specification bytes offline;
* each vector agrees with the descriptor on candidate identity, with the profile
  on harness label, and with its profile binding on requirement ids, source
  fixture and classification.

It reports the vector-set identity but asserts nothing about engine behaviour:
expectations come from the specification, never from an implementation.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - dependency is declared in requirements
    print(
        "FAIL: the jsonschema package is required; install requirements-validator.txt",
        file=sys.stderr,
    )
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
SET_ROOT = ROOT / "vectors" / "WEXP-CORE-01-VECTORS-001"
SCHEMA_ROOT = ROOT / "schema"


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8") + b"\n").hexdigest()


def load(path: Path) -> tuple[dict, str]:
    """One read: the digest and the parsed value describe the same bytes."""
    buffer = path.read_bytes()
    return json.loads(buffer.decode("utf-8")), hashlib.sha256(buffer).hexdigest()


def main() -> int:
    errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    schemas = {}
    for name in ("descriptor", "profile", "vector"):
        schemas[name] = json.loads((SCHEMA_ROOT / f"core-01-{name}.schema.json").read_bytes())
        Draft202012Validator.check_schema(schemas[name])

    descriptor, _ = load(SET_ROOT / "descriptor.json")
    profile, profile_sha = load(SET_ROOT / "profile.json")

    for name, value in (("descriptor", descriptor), ("profile", profile)):
        for problem in Draft202012Validator(schemas[name]).iter_errors(value):
            errors.append(f"{name}: {problem.message}")

    check(
        descriptor["profile"]["sha256"] == profile_sha,
        f"profile digest mismatch: declared {descriptor['profile']['sha256']}, observed {profile_sha}",
    )
    check(
        SET_ROOT.name == descriptor["candidate_id"],
        f"directory {SET_ROOT.name!r} must equal candidate_id {descriptor['candidate_id']!r}",
    )

    authority = descriptor["authority"]
    spec = SET_ROOT / authority["snapshot_path"]
    if not spec.is_file():
        errors.append(f"declared specification copy is missing: {authority['snapshot_path']}")
    else:
        spec_bytes = spec.read_bytes()
        check(
            hashlib.sha256(spec_bytes).hexdigest() == authority["xml_sha256"],
            "bundled specification copy does not match the declared XML digest",
        )
        check(
            len(spec_bytes) == authority["xml_bytes"],
            f"bundled specification copy is {len(spec_bytes)} bytes, declared {authority['xml_bytes']}",
        )

    declared = {entry["path"]: entry for entry in descriptor["bound_files"]}
    present = {f"vectors/{p.name}" for p in (SET_ROOT / "vectors").glob("*.json")}
    check(
        set(declared) == present,
        f"bound_files and vector files disagree: only-declared={sorted(set(declared) - present)}, "
        f"only-present={sorted(present - set(declared))}",
    )

    entries: list[list[str]] = []
    for relative in sorted(set(declared) & present):
        vector, vector_sha = load(SET_ROOT / relative)
        for problem in Draft202012Validator(schemas["vector"]).iter_errors(vector):
            errors.append(f"{relative}: {problem.message}")
        check(
            vector_sha == declared[relative]["sha256"],
            f"{relative}: digest mismatch: declared {declared[relative]['sha256']}, observed {vector_sha}",
        )
        check(
            vector["candidate_id"] == descriptor["candidate_id"],
            f"{relative}: declares candidate {vector['candidate_id']!r}",
        )
        check(
            vector["harness_representation"] == profile["harness"]["label"],
            f"{relative}: harness representation does not match the profile harness label",
        )
        check(
            vector["snapshot"]["xml_sha256"] == authority["xml_sha256"],
            f"{relative}: snapshot digest does not match the descriptor authority",
        )
        binding = profile["vector_bindings"].get(vector["vector_id"])
        if binding is None:
            errors.append(f"{relative}: no binding in the profile")
        else:
            for field in ("requirement_ids", "source_fixture", "classification"):
                check(
                    vector[field] == binding[field],
                    f"{relative}: {field} disagrees between the vector and the profile binding",
                )
        entries.append([vector["vector_id"], vector_sha])

    if errors:
        for message in errors:
            print(f"FAIL: {message}", file=sys.stderr)
        return 1

    print(f"PASS: {len(entries)} vector(s) in {descriptor['candidate_id']}")
    print(f"  specification   {authority['snapshot_id']} sha256={authority['xml_sha256']}")
    print(f"  profile         {profile['profile_id']} sha256={profile_sha}")
    print(f"  vector set      {canonical_sha256(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
