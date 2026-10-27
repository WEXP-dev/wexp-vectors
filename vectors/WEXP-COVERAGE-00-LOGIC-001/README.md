# WEXP-COVERAGE-00-LOGIC-001

A bounded, source-derived logical test package for posted Coverage-00, rule set
`coverage/0.2.0`. This is **not a full Coverage evaluator**, not a conformance
suite, and not validation of the optional `pg-ledger/0.2.0` deployment profile.

## What the model means

`logic.py` evaluates the ten claim definitions in sections 4-5 on explicitly
supplied known finite worlds. A, C and R are test-oracle populations, not facts
that a deployed evaluator may infer from a signed bundle. A Boolean predicate
value in this model is not a CoverageResult outcome or a checked capture premise.
`null` represents an unavailable model component, not an empty population or a
standardized Coverage encoding. Relation edges stipulate the binding and payload
predicate; this code does not authenticate or establish those bindings.

The 12 frozen examples cover exact singleton, matching omissions, duplicate or
ambiguous creation, orphan receipts, extra recipient members, equal identifiers
with different content, empty scope, empty views with a real action, unavailable
views, and distinct occurrences with equal payload. Expectations are authored in
`cases.py` without importing the model; `cases.json` preserves their fixed bytes.

The checker also enumerates 31 relation graphs (93 predicate comparisons) and
64 delivery-population pairs (128 comparisons), using separate quantified
calculations. Five aggregation cases implement only section 7.3 step 5: their
inputs are **already admitted usable derivations**. Admission, transitive
assumptions, dependency ordering and contradiction checks are not implemented.
Five invalid-input controls retain those narrow interface boundaries.

## Reproduce

Use Python 3.12 or newer from the repository root:

```sh
python vectors/WEXP-COVERAGE-00-LOGIC-001/check.py --output build/coverage00-normal.json
python -O vectors/WEXP-COVERAGE-00-LOGIC-001/check.py --output build/coverage00-optimized.json
```

Output paths must be new and outside this frozen directory. Omitting `--output`
prints the summary without writing a report. All package file hashes are checked
before importing expectation or model code. The manifest is an integrity record,
not a signature; use an exact trusted Git commit as the external identity.

For an actual source-byte check, add `--source-xml path/to/draft-sergeev-wexp-coverage-00.xml`.
CI checks the exact XML in public `WEXP-dev/wexp-coverage-spec` at commit
`90e0faec458f63fe7f2faa8a100c805cca66ede0`, SHA-256
`a2bc01d01527e1ca9e867c11341ff259b0788a941b3d1aef979f8937b82cfe62`.
No private repository is required. A workflow is not evidence of execution until
its run completes; retain the exact commit, actual job results and run report.

## Boundaries and origin

This new public package retains the 12 example bytes and model from same-project
preparation. The publication wrapper adds pre-import integrity checks, exact
public source binding and external report paths. No historical private runtime
result is relabeled as a public execution. Expected predicate values are not
changed to match the checker.

This package does not implement all P1-P8/N1-N7 derivations, the complete result
contract, policy processing, PostgreSQL, action capture, AAC mapping or independent
interoperability. Historical `pg-ledger/0.1.0` trials and the separately named
Witnessability Coverage-002 research remain different evidence. Core-02 appraisals
are also a separate contract and are not inputs to this finite-model checker.

The posted specification remains authoritative if a case or model is wrong.
Repository-authored test code follows Apache-2.0; the referenced Internet-Draft
retains its own notices and is not relicensed by this package.
