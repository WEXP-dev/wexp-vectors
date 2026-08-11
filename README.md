# WEXP implementation-independent test vectors

This repository is the public boundary for released,
implementation-independent WEXP test-vector artifacts. The WEXP specifications
are authoritative. Requirement traceability and expected results come from
specification text and reviewed requirement identifiers, never from observed
behavior of `wexp-ref` or another implementation.

The intended dependency direction is:

```text
WEXP specifications -> requirements -> vectors -> implementations
```

`wexp-ref` is an optional executable interpretation and test vehicle. This repository does not import, execute, or depend on it. An external developer should be able to implement and test WEXP using `wexp-spec` plus this repository.

## Released-vector status

Released normative protocol vectors are not yet available. Development and
review of unreleased vectors occur separately. The single file under `examples/`
is explicitly classified as `non-normative-schema-example`; it demonstrates the
repository envelope only and does not define WEXP input, output, wire format, or
semantics.

The schema and validator are test infrastructure. They are not part of the WEXP wire protocol and do not add normative meaning to a WEXP specification.

## Vector classes

| Semantic scope | Classification | What it tests |
| --- | --- | --- |
| Core semantics | `positive` | Specification-defined Core semantic behavior that is supported |
| Core semantics | `negative` | Specification-defined Core rejection or unsupported behavior |
| Representation validity | `valid` | Structural or representation validity |
| Representation invalidity | `invalid` | Structural or representation invalidity |
| Verification boundary | `boundary` | Unsupported or prohibited inference across verification boundaries |
| Interoperability | `interop` | Stable, mapped behavior involving an exactly identified external specification |
| Schema example | `non-normative-schema-example` | Repository schema examples only |

These classes preserve two important distinctions:

WEXP verification semantics are distinct from any particular record representation.

Structural validity of a record does not by itself establish semantic support
for the claim it carries.

## Vector envelope

Every vector is a JSON document validated by [`schema/vector.schema.json`](schema/vector.schema.json). Required fields are:

- `vector_id`
- `specification`
- `requirement_ids`
- `description`
- `classification`
- `input`
- `expected`

Each released protocol vector must cite at least one reviewed requirement ID. An `expected` value records specification-defined expected behavior; it must not be copied from implementation output.

Interop vectors additionally identify every external specification and its exact revision, and cite a stable `mapping_id`. Floating identities such as `HEAD`, `main`, or `latest` are rejected. All data needed to execute a released vector must be present in this public repository; validation must not require an implementation, any private repository, private services, or privileged credentials.

## Validate locally

Python 3.12 or newer is recommended.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-validator.txt
.venv/bin/python scripts/validate_vectors.py
.venv/bin/python -m unittest discover -s tests -v
```

The validator checks the JSON Schema itself, every vector against that schema,
duplicate JSON keys, duplicate vector and requirement IDs, ID formats,
classification/specification/ID agreement, interop revision and mapping rules,
and manifest paths, hashes, and metadata. Released protocol vectors, when
available, are stored under a generic `vectors/` root; no empty future class
hierarchy is committed in advance.

## Integrity manifest and version

[`manifests/vectors.json`](manifests/vectors.json) is an integrity index, not a conformance or publication attestation. It binds `VERSION`, the schema digest, and every vector JSON path, ID, classification, and digest. Adding or changing a vector requires updating the manifest in the same change.

Vector repository versions use SemVer independently from IETF document
revisions. IETF revision identifiers and vector release versions are different
namespaces.

## Licensing

Repository-authored vectors, schemas, validators, examples, and supporting
materials are licensed under the [Apache License 2.0](LICENSE) unless explicitly
stated otherwise. Expected behavior derives from published WEXP specifications,
not from `wexp-ref` behavior. This repository license does not relicense
underlying IETF specification text.

## Claims and non-claims

A passing repository check establishes only that the checked files satisfy this repository's structural and integrity rules. It does not establish complete protocol correctness, independent conformance, interoperability, IETF submission, IETF acceptance, or remote execution.
