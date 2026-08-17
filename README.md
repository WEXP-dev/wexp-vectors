# WEXP Test Vectors

WEXP (Witnessed Execution Protocol) is an IETF-oriented specification effort for
evaluating support for claims about software and AI execution within explicit
evidence and observation boundaries.

This repository holds implementation-independent WEXP test vectors, their
schemas, and the tooling that validates them. The specifications are
authoritative: every expected outcome is transcribed from published
specification text, never from the observed behaviour of `wexp-ref` or any other
implementation. Where a vector and the specification disagree, the specification
wins and the vector is a defect.

```text
WEXP specifications -> requirements -> vectors -> implementations
```

`wexp-ref` is an optional executable interpretation and test vehicle. This
repository does not import, execute, or depend on it.

## What is here

| Set | Specification | Vectors | Status |
|---|---|---|---|
| [`vectors/WEXP-CORE-01-VECTORS-001/`](vectors/WEXP-CORE-01-VECTORS-001/) | `draft-sergeev-wexp-core-01` (posted) | 16 | specification-derived |
| [`vectors/core-00/`](vectors/core-00/) | `draft-sergeev-wexp-core-00` | 7 | candidate |
| [`examples/`](examples/) | none | 1 | non-normative schema example |

**No set here is a released conformance suite.** Passing them means an
implementation agreed with transcribed expectations; it is not certification,
conformance, interoperability, or IETF acceptance.

## Core-01 vector set

Sixteen vectors covering the normative fixtures C01–C16 of
[`draft-sergeev-wexp-core-01`](https://datatracker.ietf.org/doc/draft-sergeev-wexp-core/01/).

    vector set      e315b6055148dbf05c6104c57feb991104b1ae6a47741a99cde5eb50d1900daf
    specification   84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d

**[Vector index — all sixteen, by fixture](docs/core-01-vector-index.md)**

Contents of the set:

- [`descriptor.json`](vectors/WEXP-CORE-01-VECTORS-001/descriptor.json) — set
  identity, bound file digests, specification binding
- [`profile.json`](vectors/WEXP-CORE-01-VECTORS-001/profile.json) — token
  registry, orderings, scope keys, per-vector bindings
- [`vectors/`](vectors/WEXP-CORE-01-VECTORS-001/vectors/) — the sixteen vectors
- [`spec/draft-sergeev-wexp-core-01.xml`](vectors/WEXP-CORE-01-VECTORS-001/spec/draft-sergeev-wexp-core-01.xml)
  — byte-identical copy of the published XML, so the binding is checkable
  offline. `wexp-spec` and the IETF remain authoritative; this copy exists to be
  verified, not to be cited.
- [`SHA256SUMS`](vectors/WEXP-CORE-01-VECTORS-001/SHA256SUMS) and
  [`manifests/core-01-vectors.json`](manifests/core-01-vectors.json)

Schemas are
[`core-01-descriptor`](schema/core-01-descriptor.schema.json),
[`core-01-profile`](schema/core-01-profile.schema.json) and
[`core-01-vector`](schema/core-01-vector.schema.json). They are separate from the
Core-00 envelope, which is closed and describes a different vector shape.

## Core-00 candidate slice

The seven files under [`vectors/core-00/`](vectors/core-00/) form the first
Core-00 candidate slice. Each expected result is traced through
[`requirements/core-00.json`](requirements/core-00.json) to exact published
Core-00 sections; the registry includes only requirements reviewed as ready for
vectors, and the integrity manifest marks each as `candidate`.

Core-00 inputs use the abstract representation defined by
[`schema/core-00-test-harness.schema.json`](schema/core-00-test-harness.schema.json)
— explicitly a non-normative test representation, not a WEXP record, wire format,
or source of semantics. Every document is validated by
[`schema/vector.schema.json`](schema/vector.schema.json) and carries `vector_id`,
`specification`, `requirement_ids`, `purpose`, `classification`,
`test_representation`, `input`, `expected` and `derivation`, citing at least one
reviewed `WEXP-CORE-00-REQ-NNNN`.

The single file under [`examples/`](examples/) is classified
`non-normative-schema-example`. It demonstrates the vector envelope only; it
defines no WEXP input, output, wire format, or semantics.

### Vector classes

| Semantic scope | Classification | What it tests |
| --- | --- | --- |
| Core semantics | `positive` | Specification-defined Core semantic behavior that is supported |
| Core semantics | `negative` | Specification-defined Core rejection or unsupported behavior |
| Verification ceiling | `boundary` | Behavior at an evidence, observation, or implementation-capability limit |
| Schema example | `non-normative-schema-example` | Repository schema examples only |

These preserve two distinctions: WEXP verification semantics are distinct from
any particular record representation, and structural validity of a record does
not by itself establish semantic support for the claim it carries.

## Validate locally

Python 3.12 or newer is recommended.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-validator.txt
.venv/bin/python scripts/validate_vectors.py            # Core-00 slice and examples
.venv/bin/python scripts/validate_core01_vectors.py     # Core-01 set
.venv/bin/python -m unittest discover -s tests -v
```

[`scripts/validate_vectors.py`](scripts/validate_vectors.py) checks both Core-00
schemas, harness inputs and expected observations, duplicate JSON keys, duplicate
revision-scoped IDs, reviewed requirement status and use, Core-00 source
identity, and every manifest path, digest, classification and candidate status.

[`scripts/validate_core01_vectors.py`](scripts/validate_core01_vectors.py) checks
the Core-01 schemas, every bound-file digest and size, the profile digest, the
bundled specification copy against the digest the descriptor declares, and the
agreement between each vector, the descriptor and its profile binding.

## Integrity manifests and version

[`manifests/vectors.json`](manifests/vectors.json) is the Core-00 integrity index
and binds `VERSION`, both Core-00 schema digests, the reviewed requirement
registry, and every Core-00 vector path, ID, classification, status and digest.
[`manifests/core-01-vectors.json`](manifests/core-01-vectors.json) is the Core-01
index and binds the set identity, its schemas, and every artifact digest.

Neither is a conformance or publication attestation. Adding or changing a file
covered by an index requires updating that index in the same change.

Repository versions use SemVer independently from IETF document revisions; the
two are different namespaces.

## WEXP repositories

- [Specifications — `wexp-spec`](https://github.com/WEXP-dev/wexp-spec) —
  published WEXP specifications and their provenance. **Authoritative.**
- [Test vectors — `wexp-vectors`](https://github.com/WEXP-dev/wexp-vectors) —
  this repository: vectors derived from those specifications.
- [Reference implementation — `wexp-ref`](https://github.com/WEXP-dev/wexp-ref) —
  consumes this repository as an external corpus at a pinned commit. It never
  defines an expected outcome.

## Public genesis

The [public genesis manifest](provenance/PUBLIC-GENESIS.json) inventories the
files in this repository's first authorized public commit. It is not a vector
release, conformance result, interoperability result, or IETF acceptance record.

## Licensing

Repository-authored vectors, schemas, validators, examples, and supporting
materials are licensed under the [Apache License 2.0](LICENSE) unless explicitly
stated otherwise. This repository license does not relicense underlying IETF
specification text.

## Claims and non-claims

A passing repository check establishes only that the checked files meet this
repository's structural and integrity rules. It does not establish complete
protocol correctness, independent conformance, interoperability, IETF submission
or acceptance, or remote execution.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution and traceability
requirements.
