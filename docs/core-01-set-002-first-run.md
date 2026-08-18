# Core-01 set 002 — first engine run

The expectations in
[`core-01-vector-derivation-002.md`](core-01-vector-derivation-002.md) were
frozen in commit `bc1ad05f` with per-expectation digests. This is what happened
when the two `wexp-ref` engines were first run against them, afterwards.

    wexp-ref            5337fdc2c098bd82ca11168553190dd7204bec23 (public main)
    candidate           WEXP-CORE-01-VECTORS-002
    vector set sha256   aeaa790dfe37d47880b6d7c35863aedbaf9f3328f010b21db05373d8a1a9f21f
    environment         portable, Darwin/arm64

    vectors 7   engines agree 7   engines disagree 0   expectation mismatch 1

    QUALIFICATION FAIL

Six of the seven reproduce the frozen expectation byte for byte, from both
engines independently. The seventh is `WEXP-CORE-01-V002-TV-2008`, where the two
engines agree with each other and both differ from the derivation.

## The disagreement

    frozen expectation   8ef4e6d2c451eb5b10c383d3782edb5582a0eeca7327360efac3f8f33dead179
    both engines         55ee3c951eada1969e4060c1c38296c3795dd586637bdd765f92f81054a4105d

Sixteen of the twenty appraisal components agree, including every one that
carries the semantic outcome: `verdict` is `downgrade`, `asserted_claim_supported`
is false, and the supported, maximal and relation sets are identical. The engines
reach the right answer about the claim.

Four components differ, and all four follow from a single decision:

| component | derived from Section 8.6 | both engines |
|---|---|---|
| `substantive_reasons` | `[]` | `["E_MISSING_REQUIRED_EVIDENCE"]` |
| `evaluation_gaps` | `["E_IV_NOT_EVALUATED"]` | `[]` |
| `evaluation_gap_entries` | one entry, sourced from the IV finding | `[]` |
| `inherited_limitations` | `["L-iv-scope"]` | `[]` |

## Why the derivation is not the thing that is wrong

The input carries an IV aggregate for `invocation` with `target_binding` and
`semantic_validation` both `supported` and `independence_validation` set to
`not-evaluated`.

Section 6 states that an IV aggregate "is valid only when qualified_base is one
of the four content bases and independence_validation is supported, unsupported,
or not-evaluated". This aggregate is therefore present and valid, not absent.

Section 8.6 states that "an absent aggregate triggers only its absence row;
status rows require that aggregate to be present". `E_MISSING_REQUIRED_EVIDENCE`
appears in the matrix only on absence rows — "Asserted IV aggregate absent;
source: none". The row that does apply is the gap "Asserted IV target-binding,
semantic, or independence assessment not-evaluated; source: IV finding", which
yields `E_IV_NOT_EVALUATED`. That token is registered by this profile, under the
role `qualifier_not_evaluated`.

Section 8.6 closes the set: "The following claim-required matrix is exhaustive
for Core-derived non-fatal diagnostics ... No condition outside this matrix
creates a Core-derived non-fatal token."

Both engines instead reach `E_MISSING_REQUIRED_EVIDENCE` through a catch-all —
any asserted claim that is unsupported and not over-ceiling gets that token —
and neither engine ever emits `qualifier_not_evaluated` at all. In both, the
registered role is reachable only through a profile-supplied gap, never from a
qualifier finding.

The published fixtures do not support the broad reading either. All five C01-C16
fixtures that expect `E_MISSING_REQUIRED_EVIDENCE` have a genuinely absent
aggregate: C02 and C08 are missing the asserted-base aggregate, and C03, C04 and
C06 are each missing the asserted qualifier aggregate. None of them has a present
aggregate carrying a non-passing status.

## Why set 001 could not have found this

Fixture C13 carries `E_IV_NOT_EVALUATED`, but as a profile-supplied gap on a
claim that stays supported, so it exercises the profile path and leaves the
Core-derived path untested. No fixture in C01-C16 combines an unsupported
asserted claim with an empty substantive set, so nothing there distinguishes the
matrix from the catch-all. Both engines qualify green against all sixteen.

Re-running set 001 at this same `wexp-ref` commit still passes, 16 of 16, with
evidence bundle `d673a814ca406e28d61ab0bbfeb64005f1ecadbde5ba069751b95b5fd59df4bb`
— unchanged. Nothing here is a regression; it is previously unmeasured surface.

## Disposition

The expectation has not been altered, and the vector has not been softened to
make the run green. Two engines agreeing is not evidence that they are right when
both are built against the same reading, which is exactly the failure mode a
second independent engine is supposed to exclude and, here, does not.

Whether to correct the engines, to widen the profile registry so the neighbouring
matrix rows become reachable, or to record a declared deviation in the `wexp-ref`
PARTIAL inventory is not decided here. This branch changes no engine.
