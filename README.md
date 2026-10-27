# WEXP Test Vectors and Bounded Logical Checks

Specification-derived expectations, revision-specific representations and
integrity tools. Published specifications are authoritative. Expected results
are authored from those specifications, not copied from an appraiser's output.
This repository does not import or depend on `wexp-ref`.

```text
specification -> reviewed requirements -> frozen expectations -> implementation results
```

## Select the contract before running a check

| Package | Exact contract | What is available |
|---|---|---|
| [WEXP-CORE-02-VECTORS-001](vectors/WEXP-CORE-02-VECTORS-001/README.md) | Core-02 / `wexp-core-2` | 89 complete logical inputs and twenty-component expectations (frozen `corpus.json`): 16 normative transcriptions, 73 derived controls |
| [WEXP-COVERAGE-00-LOGIC-001](vectors/WEXP-COVERAGE-00-LOGIC-001/README.md) | Coverage-00 / `coverage/0.2.0` | 12 known-finite-world examples plus bounded relation, delivery and aggregation checks; **not the full Coverage evaluator** |
| [Core-01 sets 001-003](CORE-CORPORA.md#core-01-vector-set) | Core-01 | Historical sets of 16, 9 and 7 cases, unchanged |
| [Core-00 slice](CORE-CORPORA.md#core-00-candidate-slice) | Core-00 | Seven historical candidate cases, unchanged |

**None is a conformance suite, certification or interoperability result.** A
passing integrity check is not an appraiser run. A successful bounded run is not
proof of complete implementation conformance or of real-world action capture.
Counts identify tested cases; they are not maturity scores.

## Core-02

```sh
python vectors/WEXP-CORE-02-VECTORS-001/verify.py
python vectors/WEXP-CORE-02-VECTORS-001/verify.py --rebuild
```

Python 3.12 or newer. By default `verify.py` checks the manifest and source hashes
and reads the frozen data-only `corpus.json` **without executing the expectation
generators**; consumers need only that file. `--rebuild` explicitly re-executes the
hash-checked generators and requires byte equality with `corpus.json`. Neither mode
invokes an appraiser. The manifest (package revision 2) binds exact source files,
representation, posted XML and the frozen corpus digest. `corpus.py --check --output
<new path>` still writes a separate expansion. Follow the corpus README for
full-result comparison and optional `--source-xml` verification. The
[dedicated workflow](.github/workflows/core02-corpus.yml) checks the pinned public
XML and normal/optimized rebuilds on Python 3.12 and 3.13. Exact identities are
recorded in [COMPATIBILITY.json](COMPATIBILITY.json).

## Coverage-00

```sh
python vectors/WEXP-COVERAGE-00-LOGIC-001/check.py --output build/coverage00-normal.json
python -O vectors/WEXP-COVERAGE-00-LOGIC-001/check.py --output build/coverage00-optimized.json
```

The [Coverage entry point](COVERAGE-00.md) explains the boundary: A, C and R are
known test-world populations, not established deployment facts. The aggregation
helper consumes already usable derivations. No complete P1-P8/N1-N7 evaluator,
full CoverageResult, policy/dependency engine, PostgreSQL or `pg-ledger/0.2.0`
conformance is supplied. See the [exact-source workflow](.github/workflows/coverage00-logic.yml).

## Historical Core corpora and installation guidance

The previous detailed README is preserved byte-for-byte in
[CORE-CORPORA.md](CORE-CORPORA.md), including original case derivations, freeze
records, schema descriptions, POSIX commands and Windows PowerShell 5.1 guidance.
[IMPLEMENTING.md](IMPLEMENTING.md) remains explicitly Core-01-scoped.

```sh
python -m pip install -r requirements-validator.txt
python scripts/validate_vectors.py
python scripts/validate_core01_vectors.py
python -m unittest discover -s tests -v
```

These commands validate the historical Core-00/Core-01 packages and repository
integrity. Run the separate new-contract commands above as well. Historical
manifests, expected results, specification snapshots and byte policies remain
unchanged. No result is relabeled merely because a newer contract is published.

All byte-bound files below `vectors/` have checkout text conversion disabled.
See [the canonical byte policy](docs/canonical-byte-policy.md). A validator still
fails on changed bytes; line-ending hints do not make different bytes equivalent.

## Public authorities and related work

- [Appraisal Core specifications](https://github.com/WEXP-dev/wexp-appraisal-core-spec): posted Core-02 and retained historical revisions.
- [Coverage specification](https://github.com/WEXP-dev/wexp-coverage-spec): separate Coverage-00 semantics and optional deployment profile.
- [Reference tooling](https://github.com/WEXP-dev/wexp-ref): an optional implementation consumer, never the source of expectations.
- [Interop records](https://github.com/WEXP-dev/wexp-interop): exact experimental packages and reproduction limits; historical results do not establish new-version compatibility.

## Licensing and contribution

Repository-authored vectors, models, schemas, tools and supporting material use
[Apache-2.0](LICENSE) unless otherwise stated. Underlying Internet-Draft text
retains its own notices. The [genesis inventory](provenance/PUBLIC-GENESIS.json)
is historical and is not amended by these additions.

Read [CONTRIBUTING.md](CONTRIBUTING.md). Preserve exact specification bindings,
freeze expectations before qualification, and report skipped or unavailable
checks as such. No check here establishes IETF acceptance, independent external
validation, physical execution truth or an application-policy decision.
