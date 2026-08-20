# Canonical byte policy

Git repository blobs are the authority bytes for WEXP vector artifacts. A
consumer verifies SHA-256 over the bytes in the working tree, so a supported
checkout must reproduce those blobs byte for byte. Line-ending conversion is
not part of vector generation and is not accepted as an equivalent encoding.

This inventory distinguishes files by function. It is intentionally based on
the actual binding graph rather than on filename extensions.

## Byte-bound / must preserve

| Paths | Binding or control |
| --- | --- |
| `vectors/WEXP-CORE-01-VECTORS-*/vectors/*.json` | Each raw file digest and byte count is declared by its set descriptor; the set identity is derived from the raw vector digests. |
| `vectors/WEXP-CORE-01-VECTORS-*/profile.json` | Its raw digest is declared by the set descriptor and the public set manifest. |
| `vectors/WEXP-CORE-01-VECTORS-*/descriptor.json` | Its raw digest is declared by the public set manifest. |
| `vectors/WEXP-CORE-01-VECTORS-*/spec/*.xml` | Its raw digest and byte count are declared by the descriptor and public set manifest. |
| `schema/core-01-*.schema.json` | Raw digests are declared by both Core-01 set manifests. |
| `vectors/core-00/*.json`, `examples/non-normative-schema-example.json` | Raw digests are declared by `manifests/vectors.json`. |
| `schema/vector.schema.json`, `schema/core-00-test-harness.schema.json`, `requirements/core-00.json` | Raw digests are declared by `manifests/vectors.json`. |
| `manifests/*.json`, `vectors/**/SHA256SUMS` | Integrity controls. Set 002's `SHA256SUMS` is itself manifest-bound; all of these controls must be delivered without checkout rewriting. |
| `evidence/core-01-set-002/*.json`, `provenance/PUBLIC-GENESIS.json` | Scoped published evidence and provenance controls. They retain repository bytes during checkout. |

The `.gitattributes` rules use `-text` for these paths. That tells Git not to
perform end-of-line conversion even when `core.autocrlf=true`. It does not
change any existing blob, digest, expected result, or verifier rule.

## Textual / normalization allowed

Source, automation, and metadata files that are not inputs to a published raw
byte digest may use the platform's normal textual checkout behavior:
`scripts/**`, `tests/**`, `.github/workflows/**`, `.gitattributes`, `.gitignore`,
`VERSION`, `requirements-validator.txt`, and `LICENSE`. Their parsers or
runtimes define their behavior; no vector identity is computed from their
checked-out bytes. `VERSION` is compared semantically with the repository
version in `manifests/vectors.json`; its raw bytes are not hashed there.

## Generated / derived

- `vectors/**/SHA256SUMS` is generated from the canonical artifact bytes and is
  then distributed as an integrity control. It is not regenerated after clone.
- A Core-01 vector-set identity is generated from the ordered vector IDs and
  raw vector SHA-256 values. The validator recomputes those raw digests from the
  checkout; it does not normalize file contents first.
- Set 002's expectation-freeze digest is generated from canonical JSON values,
  not from the Markdown record's line endings.
- `evidence/core-01-set-002/*.json` is derived from an engine run. Once
  published, it is an evidence record and its bytes are preserved.

All generated digest values are established from canonical source artifacts
before publication. Checkout is distribution, not a generation step.

## Non-bound documentation

`README.md`, `CONTRIBUTING.md`, and every file under `docs/**` do not
participate as raw files in a current vector or manifest digest. This includes
`docs/core-01-vector-derivation-002.md`: the freeze value shown there and in the
Set 002 manifest is derived from canonical JSON expectation values, not from
the Markdown bytes. Git may treat these documents as ordinary text.

Historical digests inside `provenance/PUBLIC-GENESIS.json` describe the
original public genesis snapshot; they do not make every later revision of
those paths a current byte-bound artifact.
