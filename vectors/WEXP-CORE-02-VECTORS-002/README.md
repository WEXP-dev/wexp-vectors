# WEXP-CORE-02-VECTORS-002

A source-encoded, specification-derived set of 35 cases for the published
`draft-sergeev-wexp-core-02`, semantics `wexp-core-2`, covering the section 7
Boundary Ceiling matrix `boundary_finding.status` x `boundary_finding.grounding` x
`boundary_finding.target_binding`. It extends `WEXP-CORE-02-VECTORS-001` revision 2
(lock commit `d6827a5e08fdf0aabecee5c025c369273c438db5`), which is unchanged. All 35
cases are non-normative derived cases (32 matrix cells, 2 section 12 scope controls,
1 acceptance probe); none restates a section 13 row.

This is not a conformance suite, certification, carrier test, mapping-profile test
or interoperability result. Passing it means agreement with the expectations frozen
here, nothing more.

## Why this set exists

Revision 2 of set 001 instantiates four of the 36 Core-observable matrix cells:
`supported x attributed x supported` (C01-C16 and most controls), `supported x
not-evaluated x supported` (R26), `unsupported x attributed x supported` (R32) and
`unsupported x asserted-only x supported` (P15). The boundary `target_binding` never
varies, `attested` never occurs, `status = not-evaluated` never occurs, and a supported
`asserted-only` boundary never occurs. The 32 empty cells, two section 12 scope
controls and one acceptance probe are the 35 cases here.
[`docs/BOUNDARY-MATRIX-001.md`](../../docs/BOUNDARY-MATRIX-001.md) is the matrix with
the section 7 sentence cited for every cell and the overlay of revision 2.

## How the expectations were produced

`inputs.py` builds the 35 inputs from the matrix. The expected results were derived
by a separate isolated session from the published text alone, without access to
any implementation or to the existing corpus expectations, and are stored verbatim
in `expectations/B01.json` .. `expectations/B35.json` together with that session's
derivation record ([`docs/core-02-boundary-matrix-002.md`](../../docs/core-02-boundary-matrix-002.md)).
They were frozen (hashed) before `wexp_ref.core02` was run against them. `corpus.py`
joins inputs and delivered expectations into `corpus.json`; it computes nothing.
Ambiguities found in the text are recorded in
[`docs/SPEC-ISSUES-core02-s7.md`](../../docs/SPEC-ISSUES-core02-s7.md); the text was not changed.

## Fixture

Every case is the section 13 common input with: asserted claim execution; one
execution base finding with supported target binding and semantic validation and
basis `E`; boundary ceiling execution, basis `bd`, limitation `L-boundary`. The boundary
status, grounding and target binding vary per cell. `evaluation_scope` is kept
consistent with the section 12 governed fields (`boundary-grounding` is not-evaluated
whenever boundary status, grounding or binding is not-evaluated; `target-binding` is
not-evaluated whenever the boundary binding is), except in the two controls B33 and
B34 that deliberately leave a scope value evaluated.

Two trust-configuration atoms occur. `core02-fixture-trust-1` is the section 13 atom,
"which accepts attributed boundary grounding". `core02-test-trust-asserted-only-1` is a
local test atom defined by this package only: an evaluation context whose minimum
acceptable boundary grounding is `asserted-only`. Core compares both as opaque atoms
(section 6.1); the second atom exists so that a supported asserted-only boundary can be
presented as a profile-conforming input. The acceptance axis is otherwise not
observable by Core, which is why it is an annotation in the matrix and not a cell.

Probe B35 is an input a conforming profile must not produce (section 7). Its frozen
`accept` is the Core-derived result under the reading that acceptance is a profile
obligation (issue A1). B35 is the one case expected to change if A1 is resolved toward
a Core-checked acceptance invariant; the other 34 cases do not depend on A1.

## Logical encoding, verification and limits

The JSON harness is identical to the one bound by set 001
(`WEXP-CORE-02-VECTORS-001/README.md`, "Logical encoding"): exact text atoms, ordered
scoped-atom pairs, arrays with set semantics, `null` for unavailable, Booleans never
equal to numbers. Run from the repository root with Python 3.12 or newer:

```sh
python vectors/WEXP-CORE-02-VECTORS-002/verify.py --rebuild
python vectors/WEXP-CORE-02-VECTORS-002/corpus.py --check --output build/core02-set002.json
```

The output path must not already exist. Default `verify.py` reads frozen data and
file hashes without importing the generator; `--rebuild` executes the hash-checked
`inputs.py` and `corpus.py` and compares the rebuilt bytes with `corpus.json`.
`--source-xml` checks the published XML bytes against the manifest digest. Neither
mode runs an appraiser or establishes that an expectation is correct. Where a case
and the published I-D disagree, the I-D wins and the case is a defect.
