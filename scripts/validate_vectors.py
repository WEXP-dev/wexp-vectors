#!/usr/bin/env python3
"""Validate the self-contained WEXP vector repository.

This tool validates repository infrastructure. It does not implement WEXP and
does not determine protocol conformance independently of the specifications.
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
        "jsonschema is required; install requirements-validator.txt"
    ) from exc


SCHEMA_PATH = PurePosixPath("schema/vector.schema.json")
MANIFEST_PATH = PurePosixPath("manifests/vectors.json")
VECTOR_ROOTS = (
    PurePosixPath("vectors"),
    PurePosixPath("examples"),
)

REQUIREMENT_ID_RE = re.compile(r"^WEXP-(CORE|REPRESENTATION)-REQ-[0-9]{4,}$")
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
FULL_COMMIT_RE = re.compile(r"^(?:[a-fA-F0-9]{40}|[a-fA-F0-9]{64})$")
FULL_DIGEST_RE = re.compile(r"^(?:sha256:)?[a-fA-F0-9]{64}$")

CLASS_RULES = {
    "positive": ("core", "WEXP-CORE-"),
    "negative": ("core", "WEXP-CORE-"),
    "valid": ("representation", "WEXP-REPRESENTATION-"),
    "invalid": ("representation", "WEXP-REPRESENTATION-"),
    "boundary": ("boundary", "WEXP-BOUNDARY-"),
    "interop": ("interop", "WEXP-INTEROP-"),
    "non-normative-schema-example": ("schema-example", "WEXP-EXAMPLE-"),
}

FLOATING_REVISIONS = {
    "current",
    "develop",
    "development",
    "head",
    "latest",
    "main",
    "master",
    "tip",
    "trunk",
}


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains the same member name twice."""


class InvalidJSONConstantError(ValueError):
    """Raised for NaN and Infinity, which are not valid JSON values."""


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    vector_count: int = 0
    interop_count: int = 0
    schema_example_count: int = 0

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
        if isinstance(part, int):
            location += f"[{part}]"
        else:
            location += f".{part}"
    return location


def _is_floating_revision(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in FLOATING_REVISIONS:
        return True
    if normalized.startswith(("refs/heads/", "heads/")):
        return True
    return bool(
        re.search(
            r"(?:^|[/@])(?:current|develop|development|head|latest|main|master|tip|trunk)(?:$|[/])",
            normalized,
        )
    )


def _expected_location(relative_path: PurePosixPath) -> tuple[str, str] | None:
    parts = relative_path.parts
    if parts and parts[0] == "examples":
        return "schema-example", "non-normative-schema-example"
    return None


def _validate_vector_semantics(
    relative_path: PurePosixPath,
    document: dict[str, Any],
    report: ValidationReport,
) -> None:
    label = relative_path.as_posix()
    vector_id = document.get("vector_id")
    classification = document.get("classification")
    specification = document.get("specification")

    expected = _expected_location(relative_path)
    if expected is not None and (specification, classification) != expected:
        report.errors.append(
            f"{label}: location requires specification={expected[0]!r} and "
            f"classification={expected[1]!r}"
        )
    elif relative_path.parts[0] == "vectors" and classification == "non-normative-schema-example":
        report.errors.append(
            f"{label}: non-normative schema examples must be stored under examples/"
        )

    class_rule = CLASS_RULES.get(classification)
    if class_rule is not None:
        expected_specification, id_prefix = class_rule
        if specification != expected_specification:
            report.errors.append(
                f"{label}: classification {classification!r} requires "
                f"specification {expected_specification!r}"
            )
        if isinstance(vector_id, str) and not vector_id.startswith(id_prefix):
            report.errors.append(
                f"{label}: classification {classification!r} requires vector ID "
                f"prefix {id_prefix!r}"
            )

    requirement_ids = document.get("requirement_ids")
    if isinstance(requirement_ids, list):
        seen_requirements: set[str] = set()
        for requirement_id in requirement_ids:
            if not isinstance(requirement_id, str) or not REQUIREMENT_ID_RE.fullmatch(
                requirement_id
            ):
                report.errors.append(
                    f"{label}: invalid requirement ID {requirement_id!r}; expected "
                    "WEXP-CORE-REQ-NNNN or WEXP-REPRESENTATION-REQ-NNNN"
                )
            elif requirement_id in seen_requirements:
                report.errors.append(
                    f"{label}: duplicate requirement ID {requirement_id!r}"
                )
            else:
                seen_requirements.add(requirement_id)

    is_interop = classification == "interop"
    if not is_interop:
        return

    report.interop_count += 1
    mapping_id = document.get("mapping_id")
    if not isinstance(mapping_id, str) or not mapping_id.strip():
        report.errors.append(f"{label}: interop vector must declare mapping_id")

    external_specifications = document.get("external_specifications")
    if not isinstance(external_specifications, list) or not external_specifications:
        report.errors.append(
            f"{label}: interop vector must declare external_specifications"
        )
        return

    for index, external in enumerate(external_specifications):
        if not isinstance(external, dict):
            continue
        exact_revision = external.get("exact_revision")
        revision_kind = external.get("revision_kind")
        location = f"{label}: external_specifications[{index}]"
        if not isinstance(exact_revision, str) or not exact_revision.strip():
            report.errors.append(f"{location} must declare an exact_revision")
            continue
        if _is_floating_revision(exact_revision):
            report.errors.append(
                f"{location} uses floating revision {exact_revision!r}; pin an exact revision"
            )
        if revision_kind == "commit" and not FULL_COMMIT_RE.fullmatch(exact_revision):
            report.errors.append(
                f"{location} declares revision_kind='commit' but does not use a full commit ID"
            )
        if revision_kind == "digest" and not FULL_DIGEST_RE.fullmatch(exact_revision):
            report.errors.append(
                f"{location} declares revision_kind='digest' but does not use a full SHA-256 digest"
            )


def _discover_vectors(root: Path, report: ValidationReport) -> list[Path]:
    files: list[Path] = []
    for relative_root in VECTOR_ROOTS:
        directory = root / relative_root
        if not directory.is_dir():
            continue
        for path in directory.rglob("*.json"):
            if path.is_symlink():
                report.errors.append(f"vector must not be a symbolic link: {path.relative_to(root)}")
                continue
            if path.is_file():
                files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def _safe_manifest_path(value: Any) -> PurePosixPath | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    if path.as_posix() != value:
        return None
    return path


def _validate_manifest(
    root: Path,
    version: str | None,
    vector_documents: dict[str, dict[str, Any]],
    vector_hashes: dict[str, str],
    report: ValidationReport,
) -> None:
    manifest_file = root / MANIFEST_PATH
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
        "schema",
        "vectors",
    }
    missing_keys = sorted(required_keys - manifest.keys())
    if missing_keys:
        report.errors.append(
            f"{MANIFEST_PATH}: missing keys: {', '.join(missing_keys)}"
        )
    unknown_keys = sorted(set(manifest) - required_keys)
    if unknown_keys:
        report.errors.append(
            f"{MANIFEST_PATH}: unknown keys: {', '.join(unknown_keys)}"
        )

    if manifest.get("manifest_version") != 1:
        report.errors.append(f"{MANIFEST_PATH}: manifest_version must be 1")
    if manifest.get("manifest_kind") != "wexp-vector-integrity-index":
        report.errors.append(
            f"{MANIFEST_PATH}: manifest_kind must be 'wexp-vector-integrity-index'"
        )
    if manifest.get("release_status") not in {"public-infrastructure-only", "released"}:
        report.errors.append(
            f"{MANIFEST_PATH}: release_status must be 'public-infrastructure-only' or 'released'"
        )
    release_status = manifest.get("release_status")
    if version is not None and manifest.get("repository_version") != version:
        report.errors.append(
            f"{MANIFEST_PATH}: repository_version does not match VERSION ({version!r})"
        )

    schema_entry = manifest.get("schema")
    if not isinstance(schema_entry, dict):
        report.errors.append(f"{MANIFEST_PATH}: schema must be an object")
    else:
        if set(schema_entry) != {"path", "sha256"}:
            report.errors.append(
                f"{MANIFEST_PATH}: schema must contain exactly path and sha256"
            )
        schema_path = _safe_manifest_path(schema_entry.get("path"))
        if schema_path != SCHEMA_PATH:
            report.errors.append(
                f"{MANIFEST_PATH}: schema path must be {SCHEMA_PATH.as_posix()!r}"
            )
        else:
            schema_file = root / schema_path
            declared_hash = schema_entry.get("sha256")
            if not isinstance(declared_hash, str) or not SHA256_RE.fullmatch(
                declared_hash
            ):
                report.errors.append(
                    f"{MANIFEST_PATH}: schema sha256 must be 64 lowercase hexadecimal characters"
                )
            elif schema_file.is_file() and declared_hash != _sha256(schema_file):
                report.errors.append(f"{MANIFEST_PATH}: schema sha256 mismatch")

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
        if set(entry) != expected_keys:
            report.errors.append(
                f"{location} must contain exactly {', '.join(sorted(expected_keys))}"
            )

        relative_path = _safe_manifest_path(entry.get("path"))
        if relative_path is None:
            report.errors.append(f"{location} has an unsafe or non-canonical path")
            continue
        path_string = relative_path.as_posix()
        if path_string in manifest_paths:
            report.errors.append(f"{location} duplicates manifest path {path_string!r}")
        manifest_paths.add(path_string)

        vector_id = entry.get("vector_id")
        if not isinstance(vector_id, str) or not vector_id:
            report.errors.append(f"{location} has an invalid vector_id")
        elif vector_id in manifest_ids:
            report.errors.append(f"{location} duplicates manifest vector_id {vector_id!r}")
        else:
            manifest_ids.add(vector_id)

        if release_status == "public-infrastructure-only" and entry.get("status") == "released":
            report.errors.append(
                f"{location} cannot mark a vector released while the manifest is schema-only"
            )

        declared_hash = entry.get("sha256")
        if not isinstance(declared_hash, str) or not SHA256_RE.fullmatch(declared_hash):
            report.errors.append(
                f"{location} sha256 must be 64 lowercase hexadecimal characters"
            )
        elif path_string in vector_hashes and declared_hash != vector_hashes[path_string]:
            report.errors.append(f"{location} sha256 mismatch for {path_string}")

        document = vector_documents.get(path_string)
        if document is not None:
            if entry.get("vector_id") != document.get("vector_id"):
                report.errors.append(f"{location} vector_id does not match the vector file")
            if entry.get("classification") != document.get("classification"):
                report.errors.append(
                    f"{location} classification does not match the vector file"
                )
            expected_status = (
                "non-normative-schema-example"
                if document.get("classification") == "non-normative-schema-example"
                else "released"
            )
            if entry.get("status") != expected_status:
                report.errors.append(
                    f"{location} status must be {expected_status!r} for this vector"
                )

    actual_paths = set(vector_hashes)
    for path in sorted(actual_paths - manifest_paths):
        report.errors.append(f"{MANIFEST_PATH}: unlisted vector file {path}")
    for path in sorted(manifest_paths - actual_paths):
        report.errors.append(f"{MANIFEST_PATH}: listed vector file does not exist: {path}")


def validate_repository(root: Path) -> ValidationReport:
    """Validate one repository root and return all observed errors."""

    root = root.resolve()
    report = ValidationReport()

    version_file = root / "VERSION"
    version: str | None = None
    if not version_file.is_file():
        report.errors.append("missing VERSION")
    else:
        try:
            version = version_file.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as exc:
            report.errors.append(f"VERSION: cannot read: {exc}")
        if version is not None and not SEMVER_RE.fullmatch(version):
            report.errors.append(f"VERSION: {version!r} is not valid SemVer")

    schema_file = root / SCHEMA_PATH
    schema: dict[str, Any] | None = None
    if not schema_file.is_file():
        report.errors.append(f"missing schema: {SCHEMA_PATH}")
    else:
        loaded_schema = _load_json(schema_file, report)
        if isinstance(loaded_schema, dict):
            try:
                Draft202012Validator.check_schema(loaded_schema)
            except SchemaError as exc:
                report.errors.append(f"{SCHEMA_PATH}: invalid JSON Schema: {exc.message}")
            else:
                schema = loaded_schema
        elif loaded_schema is not None:
            report.errors.append(f"{SCHEMA_PATH}: schema must be a JSON object")

    schema_validator = (
        Draft202012Validator(schema, format_checker=FormatChecker())
        if schema is not None
        else None
    )

    vector_files = _discover_vectors(root, report)
    report.vector_count = len(vector_files)
    vector_documents: dict[str, dict[str, Any]] = {}
    vector_hashes: dict[str, str] = {}
    id_locations: dict[str, str] = {}
    digest_locations: dict[str, str] = {}

    for path in vector_files:
        relative_path = PurePosixPath(path.relative_to(root).as_posix())
        label = relative_path.as_posix()
        vector_hashes[label] = _sha256(path)
        prior_digest_path = digest_locations.get(vector_hashes[label])
        if prior_digest_path is not None:
            report.errors.append(
                f"{label}: duplicate vector document content also present at {prior_digest_path}"
            )
        else:
            digest_locations[vector_hashes[label]] = label

        loaded_document = _load_json(path, report)
        if not isinstance(loaded_document, dict):
            if loaded_document is not None:
                report.errors.append(f"{label}: vector must be a JSON object")
            continue
        vector_documents[label] = loaded_document

        if schema_validator is not None:
            schema_errors = sorted(
                schema_validator.iter_errors(loaded_document),
                key=lambda error: tuple(str(item) for item in error.absolute_path),
            )
            for error in schema_errors:
                report.errors.append(
                    f"{label}: schema error at {_json_location(error.absolute_path)}: "
                    f"{error.message}"
                )

        vector_id = loaded_document.get("vector_id")
        if isinstance(vector_id, str):
            prior_id_path = id_locations.get(vector_id)
            if prior_id_path is not None:
                report.errors.append(
                    f"{label}: duplicate vector_id {vector_id!r}; first seen at {prior_id_path}"
                )
            else:
                id_locations[vector_id] = label

        if loaded_document.get("classification") == "non-normative-schema-example":
            report.schema_example_count += 1
        _validate_vector_semantics(relative_path, loaded_document, report)

    _validate_manifest(
        root,
        version,
        vector_documents,
        vector_hashes,
        report,
    )
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
        "PASS: valid schema, manifest, and "
        f"{report.vector_count} vector document(s) "
        f"({report.schema_example_count} non-normative schema example(s), "
        f"{report.interop_count} interop vector(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
