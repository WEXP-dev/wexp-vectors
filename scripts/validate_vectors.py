#!/usr/bin/env python3
"""Validate this repository's WEXP vector package and integrity index.

This tool checks repository structure and traceability. It does not implement
WEXP, determine protocol conformance, or make the test harness normative.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover - exercised by CLI environments
    raise SystemExit(
        "The jsonschema package is required. Install the packages listed in "
        "requirements-validator.txt."
    ) from exc


MANIFEST_PATH = PurePosixPath("manifests/vectors.json")
ENVELOPE_SCHEMA_PATH = PurePosixPath("schema/vector.schema.json")
HARNESS_SCHEMA_PATH = PurePosixPath("schema/core-00-test-harness.schema.json")
REQUIREMENTS_PATH = PurePosixPath("requirements/core-00.json")
EXAMPLE_PATH = PurePosixPath("examples/non-normative-schema-example.json")
VECTOR_ROOTS = (PurePosixPath("vectors"), PurePosixPath("examples"))

CORE_DOCUMENT = "draft-sergeev-wexp-core"
CORE_REVISION = "00"
CORE_XML_SHA256 = (
    "6cd8b680059cc81e1ec4c84737d9319ee242ef63e89c57de497bd57ede08d810"
)
CORE_SOURCE_IDENTITY = {
    "artifact": "xml",
    "document": CORE_DOCUMENT,
    "revision": CORE_REVISION,
    "sha256": CORE_XML_SHA256,
}

CORE_VECTOR_ID_RE = re.compile(r"^WEXP-CORE-00-V[0-9]{4,}$")
EXAMPLE_ID_RE = re.compile(r"^WEXP-EXAMPLE-V[0-9]{4,}$")
REQUIREMENT_ID_RE = re.compile(r"^WEXP-CORE-00-REQ-[0-9]{4,}$")
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains the same member name twice."""


class InvalidJSONConstantError(ValueError):
    """Raised for NaN and Infinity, which are not valid JSON values."""


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    vector_count: int = 0
    core_vector_count: int = 0
    candidate_count: int = 0
    released_count: int = 0
    schema_example_count: int = 0
    requirement_count: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def _reject_duplicate_keys(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON member {key!r}")
        result[key] = value
    return result


def _reject_invalid_constant(value: str) -> None:
    raise InvalidJSONConstantError(f"non-JSON numeric constant {value!r}")


def _load_json(path: Path, report: ValidationReport) -> Any | None:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_invalid_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        report.errors.append(f"{path}: invalid JSON: {exc}")
        return None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_location(parts: Iterable[Any]) -> str:
    location = "$"
    for part in parts:
        location += f"[{part}]" if isinstance(part, int) else f".{part}"
    return location


def _safe_manifest_path(value: Any) -> PurePosixPath | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    if path.as_posix() != value:
        return None
    return path


def _validate_exact_keys(
    value: dict[str, Any], expected: set[str], location: str, report: ValidationReport
) -> None:
    missing = sorted(expected - value.keys())
    unknown = sorted(set(value) - expected)
    if missing:
        report.errors.append(f"{location}: missing keys: {', '.join(missing)}")
    if unknown:
        report.errors.append(f"{location}: unknown keys: {', '.join(unknown)}")


def _load_schema(
    root: Path, relative_path: PurePosixPath, report: ValidationReport
) -> dict[str, Any] | None:
    schema_file = root / relative_path
    if schema_file.is_symlink():
        report.errors.append(f"schema must not be a symbolic link: {relative_path}")
        return None
    if not schema_file.is_file():
        report.errors.append(f"missing schema: {relative_path}")
        return None
    loaded = _load_json(schema_file, report)
    if not isinstance(loaded, dict):
        if loaded is not None:
            report.errors.append(f"{relative_path}: schema must be a JSON object")
        return None
    try:
        Draft202012Validator.check_schema(loaded)
    except SchemaError as exc:
        report.errors.append(f"{relative_path}: invalid JSON Schema: {exc.message}")
        return None
    return loaded


def _discover_vectors(root: Path, report: ValidationReport) -> list[Path]:
    files: list[Path] = []
    for relative_root in VECTOR_ROOTS:
        directory = root / relative_root
        if directory.is_symlink():
            report.errors.append(
                f"vector root must not be a symbolic link: {relative_root}"
            )
            continue
        if not directory.is_dir():
            continue
        for path in directory.rglob("*.json"):
            if path.is_symlink():
                report.errors.append(
                    f"vector must not be a symbolic link: {path.relative_to(root)}"
                )
            elif path.is_file():
                files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def _validate_requirements(
    root: Path, report: ValidationReport
) -> tuple[dict[str, Any] | None, set[str]]:
    registry_file = root / REQUIREMENTS_PATH
    if registry_file.is_symlink():
        report.errors.append(
            f"requirement registry must not be a symbolic link: {REQUIREMENTS_PATH}"
        )
        return None, set()
    if not registry_file.is_file():
        report.errors.append(f"missing requirement registry: {REQUIREMENTS_PATH}")
        return None, set()
    registry = _load_json(registry_file, report)
    if not isinstance(registry, dict):
        if registry is not None:
            report.errors.append(f"{REQUIREMENTS_PATH}: registry must be a JSON object")
        return None, set()

    _validate_exact_keys(
        registry,
        {"registry_version", "specification", "requirements"},
        str(REQUIREMENTS_PATH),
        report,
    )
    if registry.get("registry_version") != 1:
        report.errors.append(f"{REQUIREMENTS_PATH}: registry_version must be 1")
    if registry.get("specification") != CORE_SOURCE_IDENTITY:
        report.errors.append(f"{REQUIREMENTS_PATH}: Core source identity mismatch")

    entries = registry.get("requirements")
    if not isinstance(entries, list) or not entries:
        report.errors.append(f"{REQUIREMENTS_PATH}: requirements must be a non-empty array")
        return registry, set()

    required_entry_keys = {
        "dependencies",
        "id",
        "specification",
        "revision",
        "keyword",
        "normative_proposition",
        "review_status",
        "section",
        "source_locator",
        "vector_eligibility",
    }
    requirement_ids: set[str] = set()
    for index, entry in enumerate(entries):
        location = f"{REQUIREMENTS_PATH}: requirements[{index}]"
        if not isinstance(entry, dict):
            report.errors.append(f"{location} must be an object")
            continue
        _validate_exact_keys(entry, required_entry_keys, location, report)
        requirement_id = entry.get("id")
        if not isinstance(requirement_id, str) or not REQUIREMENT_ID_RE.fullmatch(
            requirement_id
        ):
            report.errors.append(
                f"{location}: invalid requirement ID {requirement_id!r}; expected "
                "WEXP-CORE-00-REQ-NNNN"
            )
        elif requirement_id in requirement_ids:
            report.errors.append(
                f"{location}: duplicate requirement ID {requirement_id!r}"
            )
        else:
            requirement_ids.add(requirement_id)

        if entry.get("specification") != CORE_DOCUMENT:
            report.errors.append(f"{location}: specification must be {CORE_DOCUMENT!r}")
        if entry.get("revision") != CORE_REVISION:
            report.errors.append(f"{location}: revision must be {CORE_REVISION!r}")
        if entry.get("review_status") != "ready-for-vector":
            report.errors.append(f"{location}: requirement is not ready for vectors")
        if entry.get("vector_eligibility") is not True:
            report.errors.append(f"{location}: requirement is not vector-eligible")

        for key in (
            "keyword",
            "normative_proposition",
            "section",
            "source_locator",
        ):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                report.errors.append(f"{location}: {key} must be a non-empty string")
        dependencies = entry.get("dependencies")
        if not isinstance(dependencies, list) or not dependencies:
            report.errors.append(f"{location}: dependencies must be a non-empty array")
        elif any(not isinstance(item, str) or not item.strip() for item in dependencies):
            report.errors.append(
                f"{location}: every dependency must be a non-empty string"
            )
        elif len(dependencies) != len(set(dependencies)):
            report.errors.append(f"{location}: dependencies must be unique")

    report.requirement_count = len(requirement_ids)
    return registry, requirement_ids


def _validate_core_vector(
    relative_path: PurePosixPath,
    document: dict[str, Any],
    harness_validator: Draft202012Validator | None,
    requirement_ids: set[str],
    used_requirements: set[str],
    report: ValidationReport,
) -> None:
    label = relative_path.as_posix()
    vector_id = document.get("vector_id")
    classification = document.get("classification")

    if classification == "non-normative-schema-example":
        report.schema_example_count += 1
        if relative_path != EXAMPLE_PATH:
            report.errors.append(
                f"{label}: the non-normative schema example must be stored at {EXAMPLE_PATH}"
            )
        if not isinstance(vector_id, str) or not EXAMPLE_ID_RE.fullmatch(vector_id):
            report.errors.append(f"{label}: invalid schema-example vector ID {vector_id!r}")
        return

    report.core_vector_count += 1
    if not isinstance(vector_id, str) or not CORE_VECTOR_ID_RE.fullmatch(vector_id):
        report.errors.append(
            f"{label}: invalid Core -00 vector ID {vector_id!r}; expected "
            "WEXP-CORE-00-VNNNN"
        )
    elif relative_path != PurePosixPath("vectors/core-00") / f"{vector_id}.json":
        report.errors.append(
            f"{label}: Core -00 vector path must match its revision-scoped vector ID"
        )

    if document.get("specification") != CORE_SOURCE_IDENTITY:
        report.errors.append(f"{label}: Core source identity mismatch")

    cited = document.get("requirement_ids")
    if isinstance(cited, list):
        seen: set[str] = set()
        for requirement_id in cited:
            if not isinstance(requirement_id, str) or not REQUIREMENT_ID_RE.fullmatch(
                requirement_id
            ):
                report.errors.append(
                    f"{label}: invalid requirement ID {requirement_id!r}; expected "
                    "WEXP-CORE-00-REQ-NNNN"
                )
            elif requirement_id in seen:
                report.errors.append(
                    f"{label}: duplicate requirement ID {requirement_id!r}"
                )
            elif requirement_id not in requirement_ids:
                report.errors.append(
                    f"{label}: unknown reviewed requirement {requirement_id!r}"
                )
            else:
                seen.add(requirement_id)
                used_requirements.add(requirement_id)

    if harness_validator is not None:
        harness_document = {
            "input": document.get("input"),
            "expected": document.get("expected"),
        }
        errors = sorted(
            harness_validator.iter_errors(harness_document),
            key=lambda error: tuple(str(item) for item in error.absolute_path),
        )
        for error in errors:
            report.errors.append(
                f"{label}: test-harness schema error at "
                f"{_json_location(error.absolute_path)}: {error.message}"
            )

    # The harness array represents entries from Core's extensions map. JSON
    # Schema uniqueItems rejects duplicate objects, but the same extension
    # name with different critical flags would still be two distinct objects.
    # Reject that contradictory post-structure fact explicitly.
    input_value = document.get("input")
    extensions = (
        input_value.get("unknown_extensions")
        if isinstance(input_value, dict)
        else None
    )
    if isinstance(extensions, list):
        seen_extension_names: set[str] = set()
        for index, extension in enumerate(extensions):
            name = extension.get("name") if isinstance(extension, dict) else None
            if not isinstance(name, str):
                continue
            if name in seen_extension_names:
                report.errors.append(
                    f"{label}: duplicate unknown extension name {name!r} at "
                    f"input.unknown_extensions[{index}]"
                )
            seen_extension_names.add(name)


def _validate_integrity_entry(
    root: Path,
    entry: Any,
    location: str,
    expected_path: PurePosixPath,
    report: ValidationReport,
) -> None:
    if not isinstance(entry, dict):
        report.errors.append(f"{location} must be an object")
        return
    _validate_exact_keys(entry, {"path", "sha256"}, location, report)
    relative_path = _safe_manifest_path(entry.get("path"))
    if relative_path != expected_path:
        report.errors.append(f"{location}: path must be {expected_path.as_posix()!r}")
        return
    declared_hash = entry.get("sha256")
    if not isinstance(declared_hash, str) or not SHA256_RE.fullmatch(declared_hash):
        report.errors.append(
            f"{location}: sha256 must be 64 lowercase hexadecimal characters"
        )
        return
    path = root / relative_path
    if path.is_symlink():
        report.errors.append(f"{location}: listed file must not be a symbolic link")
    elif not path.is_file():
        report.errors.append(f"{location}: listed file does not exist: {relative_path}")
    elif declared_hash != _sha256(path):
        report.errors.append(f"{location}: sha256 mismatch for {relative_path}")


def _validate_manifest(
    root: Path,
    version: str | None,
    vector_documents: dict[str, dict[str, Any]],
    vector_hashes: dict[str, str],
    report: ValidationReport,
) -> None:
    manifest_file = root / MANIFEST_PATH
    if manifest_file.is_symlink():
        report.errors.append(f"manifest must not be a symbolic link: {MANIFEST_PATH}")
        return
    if not manifest_file.is_file():
        report.errors.append(f"missing manifest: {MANIFEST_PATH}")
        return
    manifest = _load_json(manifest_file, report)
    if not isinstance(manifest, dict):
        if manifest is not None:
            report.errors.append(f"{MANIFEST_PATH}: manifest must be a JSON object")
        return

    required_keys = {
        "manifest_version",
        "manifest_kind",
        "repository_version",
        "release_status",
        "vector_category",
        "schemas",
        "requirements",
        "vectors",
    }
    _validate_exact_keys(manifest, required_keys, str(MANIFEST_PATH), report)
    if manifest.get("manifest_version") != 2:
        report.errors.append(f"{MANIFEST_PATH}: manifest_version must be 2")
    if manifest.get("manifest_kind") != "wexp-vector-integrity-index":
        report.errors.append(
            f"{MANIFEST_PATH}: manifest_kind must be 'wexp-vector-integrity-index'"
        )
    release_status = manifest.get("release_status")
    if release_status not in {"candidate", "released"}:
        report.errors.append(
            f"{MANIFEST_PATH}: release_status must be 'candidate' or 'released'"
        )
    if manifest.get("vector_category") != "specification-derived-test-vectors":
        report.errors.append(
            f"{MANIFEST_PATH}: vector_category must be "
            "'specification-derived-test-vectors'"
        )
    if version is not None and manifest.get("repository_version") != version:
        report.errors.append(
            f"{MANIFEST_PATH}: repository_version does not match VERSION ({version!r})"
        )

    schemas = manifest.get("schemas")
    if not isinstance(schemas, dict):
        report.errors.append(f"{MANIFEST_PATH}: schemas must be an object")
    else:
        _validate_exact_keys(
            schemas,
            {"vector_envelope", "core_00_test_harness"},
            f"{MANIFEST_PATH}: schemas",
            report,
        )
        _validate_integrity_entry(
            root,
            schemas.get("vector_envelope"),
            f"{MANIFEST_PATH}: schemas.vector_envelope",
            ENVELOPE_SCHEMA_PATH,
            report,
        )
        _validate_integrity_entry(
            root,
            schemas.get("core_00_test_harness"),
            f"{MANIFEST_PATH}: schemas.core_00_test_harness",
            HARNESS_SCHEMA_PATH,
            report,
        )

    _validate_integrity_entry(
        root,
        manifest.get("requirements"),
        f"{MANIFEST_PATH}: requirements",
        REQUIREMENTS_PATH,
        report,
    )

    entries = manifest.get("vectors")
    if not isinstance(entries, list):
        report.errors.append(f"{MANIFEST_PATH}: vectors must be an array")
        return

    manifest_paths: set[str] = set()
    manifest_ids: set[str] = set()
    for index, entry in enumerate(entries):
        location = f"{MANIFEST_PATH}: vectors[{index}]"
        if not isinstance(entry, dict):
            report.errors.append(f"{location} must be an object")
            continue
        expected_keys = {"path", "vector_id", "classification", "status", "sha256"}
        _validate_exact_keys(entry, expected_keys, location, report)

        relative_path = _safe_manifest_path(entry.get("path"))
        if relative_path is None:
            report.errors.append(f"{location}: unsafe or non-canonical path")
            continue
        path_string = relative_path.as_posix()
        if path_string in manifest_paths:
            report.errors.append(f"{location}: duplicate manifest path {path_string!r}")
        manifest_paths.add(path_string)

        vector_id = entry.get("vector_id")
        if not isinstance(vector_id, str) or not vector_id:
            report.errors.append(f"{location}: invalid vector_id")
        elif vector_id in manifest_ids:
            report.errors.append(f"{location}: duplicate manifest vector_id {vector_id!r}")
        else:
            manifest_ids.add(vector_id)

        declared_hash = entry.get("sha256")
        if not isinstance(declared_hash, str) or not SHA256_RE.fullmatch(declared_hash):
            report.errors.append(
                f"{location}: sha256 must be 64 lowercase hexadecimal characters"
            )
        elif path_string in vector_hashes and declared_hash != vector_hashes[path_string]:
            report.errors.append(f"{location}: sha256 mismatch for {path_string}")

        document = vector_documents.get(path_string)
        if document is None:
            continue
        if vector_id != document.get("vector_id"):
            report.errors.append(f"{location}: vector_id does not match the vector file")
        if entry.get("classification") != document.get("classification"):
            report.errors.append(
                f"{location}: classification does not match the vector file"
            )
        expected_status = (
            "non-normative-schema-example"
            if document.get("classification") == "non-normative-schema-example"
            else release_status
        )
        if entry.get("status") != expected_status:
            report.errors.append(
                f"{location}: status must be {expected_status!r} for this document"
            )
        if entry.get("status") == "candidate":
            report.candidate_count += 1
        elif entry.get("status") == "released":
            report.released_count += 1

    actual_paths = set(vector_hashes)
    for path in sorted(actual_paths - manifest_paths):
        report.errors.append(f"{MANIFEST_PATH}: unlisted vector file {path}")
    for path in sorted(manifest_paths - actual_paths):
        report.errors.append(
            f"{MANIFEST_PATH}: listed vector file does not exist: {path}"
        )


def validate_repository(root: Path) -> ValidationReport:
    """Validate one repository root and return all observed errors."""

    root = root.resolve()
    report = ValidationReport()

    version_file = root / "VERSION"
    version: str | None = None
    if version_file.is_symlink():
        report.errors.append("VERSION must not be a symbolic link")
    elif not version_file.is_file():
        report.errors.append("missing VERSION")
    else:
        try:
            version = version_file.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as exc:
            report.errors.append(f"VERSION: cannot read: {exc}")
        if version is not None and not SEMVER_RE.fullmatch(version):
            report.errors.append(f"VERSION: {version!r} is not valid SemVer")

    envelope_schema = _load_schema(root, ENVELOPE_SCHEMA_PATH, report)
    harness_schema = _load_schema(root, HARNESS_SCHEMA_PATH, report)
    envelope_validator = (
        Draft202012Validator(envelope_schema, format_checker=FormatChecker())
        if envelope_schema is not None
        else None
    )
    harness_validator = (
        Draft202012Validator(harness_schema, format_checker=FormatChecker())
        if harness_schema is not None
        else None
    )

    _, requirement_ids = _validate_requirements(root, report)
    vector_files = _discover_vectors(root, report)
    report.vector_count = len(vector_files)
    vector_documents: dict[str, dict[str, Any]] = {}
    vector_hashes: dict[str, str] = {}
    id_locations: dict[str, str] = {}
    digest_locations: dict[str, str] = {}
    used_requirements: set[str] = set()

    for path in vector_files:
        relative_path = PurePosixPath(path.relative_to(root).as_posix())
        label = relative_path.as_posix()
        digest = _sha256(path)
        vector_hashes[label] = digest
        prior_digest_path = digest_locations.get(digest)
        if prior_digest_path is not None:
            report.errors.append(
                f"{label}: duplicate vector document content also present at "
                f"{prior_digest_path}"
            )
        else:
            digest_locations[digest] = label

        loaded = _load_json(path, report)
        if not isinstance(loaded, dict):
            if loaded is not None:
                report.errors.append(f"{label}: vector must be a JSON object")
            continue
        vector_documents[label] = loaded

        if envelope_validator is not None:
            errors = sorted(
                envelope_validator.iter_errors(loaded),
                key=lambda error: tuple(str(item) for item in error.absolute_path),
            )
            for error in errors:
                report.errors.append(
                    f"{label}: envelope schema error at "
                    f"{_json_location(error.absolute_path)}: {error.message}"
                )

        vector_id = loaded.get("vector_id")
        if isinstance(vector_id, str):
            prior_id_path = id_locations.get(vector_id)
            if prior_id_path is not None:
                report.errors.append(
                    f"{label}: duplicate vector_id {vector_id!r}; first seen at "
                    f"{prior_id_path}"
                )
            else:
                id_locations[vector_id] = label

        _validate_core_vector(
            relative_path,
            loaded,
            harness_validator,
            requirement_ids,
            used_requirements,
            report,
        )

    unused_requirements = sorted(requirement_ids - used_requirements)
    if unused_requirements:
        report.errors.append(
            f"{REQUIREMENTS_PATH}: reviewed requirement IDs are not cited by any "
            f"Core -00 vector: {', '.join(unused_requirements)}"
        )

    _validate_manifest(root, version, vector_documents, vector_hashes, report)
    return report


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=_default_root(),
        help="repository root (default: parent of this script directory)",
    )
    args = parser.parse_args(argv)

    report = validate_repository(args.root)
    if not report.ok:
        print(f"FAIL: {len(report.errors)} validation error(s)", file=sys.stderr)
        for error in report.errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "PASS: valid schemas, reviewed requirement traceability, and integrity "
        f"manifest; {report.core_vector_count} Core -00 specification-derived "
        f"vector(s) ({report.candidate_count} candidate, "
        f"{report.released_count} released), {report.requirement_count} reviewed "
        f"requirement(s), {report.schema_example_count} non-normative schema "
        "example(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
