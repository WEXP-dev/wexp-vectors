# WEXP Test Vectors

WEXP (Witnessed Execution Protocol) is an IETF-oriented specification effort
for evaluating support for claims about software and AI execution within
explicit evidence and observation boundaries.

This repository provides schemas and validation tools for
implementation-independent WEXP test vectors. The WEXP specifications are
authoritative. Expected behavior comes from published specification text.
Reviewed requirement IDs provide traceability to that text. Expected behavior
never comes from observed behavior of `wexp-ref` or another implementation.

**Released normative protocol vectors: none yet.**

The repository contains seven Core -00 specification-derived test vectors for
review. They remain candidates: they are neither released vectors nor a
conformance suite. The repository also contains reviewed requirement references,
two schemas, validation tooling and tests, an integrity manifest, and one
explicitly non-normative schema example.

The intended dependency direction is:

```text
WEXP specifications -> requirements -> vectors -> implementations
```

`wexp-ref` is an optional executable interpretation and test vehicle. This
repository does not import, execute, or depend on it.

## Vector status

The seven files under `vectors/core-00/` form the first Core -00 candidate
slice. Each expected result is traced through
[`requirements/core-00.json`](requirements/core-00.json) to exact published
Core -00 sections. The registry includes only requirements reviewed as ready
for vectors. The integrity manifest marks each specification-derived vector as
`candidate`.

The single file under `examples/` is classified as
`non-normative-schema-example`. It demonstrates only the vector envelope; it
does not define WEXP input, output, wire format, or semantics.

The Core -00 inputs use the abstract representation defined by
[`schema/core-00-test-harness.schema.json`](schema/core-00-test-harness.schema.json).
It is explicitly a non-normative test representation, not a WEXP record,
protocol wire format, or source of WEXP semantics. Both schemas and the
validator check repository files; they do not define normative protocol
behavior.

## WEXP repositories

- [Specifications — `wexp-spec`](https://github.com/WEXP-dev/wexp-spec) —
  published WEXP specifications and their provenance.
- [Test vectors — `wexp-vectors`](https://github.com/WEXP-dev/wexp-vectors) —
  schemas and validation tools for implementation-independent WEXP test vectors.
- [Reference implementation — `wexp-ref`](https://github.com/WEXP-dev/wexp-ref)
  — the reference implementation and generic execution tools.

## Vector classes

The current candidate package uses these classes:

| Semantic scope | Classification | What it tests |
| --- | --- | --- |
| Core semantics | `positive` | Specification-defined Core semantic behavior that is supported |
| Core semantics | `negative` | Specification-defined Core rejection or unsupported behavior |
| Verification ceiling | `boundary` | Behavior at an evidence, observation, or implementation-capability limit |
| Schema example | `non-normative-schema-example` | Repository schema examples only |

These classes preserve two important distinctions:

WEXP verification semantics are distinct from any particular record representation.

Structural validity of a record does not by itself establish semantic support
for the claim it carries.

## Vector envelope

Every document is validated by
[`schema/vector.schema.json`](schema/vector.schema.json). Core -00 vector files
use revision-scoped IDs and include:

- `vector_id`
- `specification`
- `requirement_ids`
- `purpose`
- `classification`
- `test_representation`
- `input`
- `expected`
- `derivation`

Each Core -00 candidate cites at least one reviewed
`WEXP-CORE-00-REQ-NNNN` requirement. An `expected` value records behavior
derived from the published specification and reviewed requirements; it must not
be copied from implementation output. The package is self-contained and does
not require `wexp-ref`, another implementation, a private repository, private
services, or privileged credentials.

## Validate locally

Python 3.12 or newer is recommended.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-validator.txt
.venv/bin/python scripts/validate_vectors.py
.venv/bin/python -m unittest discover -s tests -v
```

The validator checks both JSON Schemas, the non-normative harness inputs and
expected observations, duplicate JSON keys, duplicate revision-scoped IDs,
reviewed requirement status and use, Core -00 source identity, and every
manifest path, digest, classification, and candidate status.

## Integrity manifest and version

[`manifests/vectors.json`](manifests/vectors.json) is an integrity index, not a
conformance or publication attestation. It binds `VERSION`, both schema
digests, the reviewed requirement registry, and every vector JSON path, ID,
classification, status, and digest. Adding or changing a file covered by the
integrity index requires updating the manifest in the same change.

Vector repository versions use SemVer independently from IETF document
revisions. IETF revision identifiers and vector release versions are different
namespaces.

## Public genesis

The [public genesis manifest](provenance/PUBLIC-GENESIS.json) inventories the
files in this repository's first authorized public commit. It is not a vector
release, conformance result, interoperability result, or IETF acceptance
record.

## Licensing

Repository-authored vectors, schemas, validators, examples, and supporting
materials are licensed under the [Apache License 2.0](LICENSE) unless explicitly
stated otherwise. This repository license does not relicense underlying IETF
specification text.

## Claims and non-claims

A passing repository check establishes only that the checked files meet this
repository's structural and integrity rules. It does not establish complete
protocol correctness, independent conformance, interoperability, IETF
submission or acceptance, or remote execution.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution and traceability
requirements.

## WEXP Core-01 vector set

`vectors/WEXP-CORE-01-VECTORS-001/` is the specification-derived vector set for
[`draft-sergeev-wexp-core-01`](https://datatracker.ietf.org/doc/draft-sergeev-wexp-core/01/),
sixteen vectors covering the normative fixtures C01–C16.

    vector set      e315b6055148dbf05c6104c57feb991104b1ae6a47741a99cde5eb50d1900daf
    specification   84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d

### Normative status

The Internet-Draft is normative. This set is a reference test corpus derived from
it: every expected appraisal is transcribed from the draft's normative fixtures,
never produced by running an implementation. Where a vector and the draft
disagree, the draft wins and the vector is a defect.

Passing this set does not make an implementation certified, conformant, or
endorsed. It means the implementation agreed with sixteen transcribed
expectations.

### Contents

- `descriptor.json` — set identity, bound file digests, specification binding
- `profile.json` — token registry, orderings, scope keys, per-vector bindings
- `vectors/` — the sixteen vectors
- `spec/draft-sergeev-wexp-core-01.xml` — byte-identical copy of the published
  XML, so the binding is checkable offline. `wexp-spec` and the IETF remain
  authoritative; this copy exists to be verified, not to be cited.
- `SHA256SUMS`, and `manifests/core-01-vectors.json`

### Validating

    pip install -r requirements-validator.txt
    python3 scripts/validate_core01_vectors.py

Schemas are `schema/core-01-{descriptor,profile,vector}.schema.json`. They are
separate from the Core-00 envelope, which is closed and describes a different
vector shape.
