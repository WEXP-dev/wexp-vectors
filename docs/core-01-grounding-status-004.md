# Core-01 boundary status and grounding — vector set 004

Expectation authority: `WEXP-CORE-01-GROUNDING-STATUS-EXPECTATION-FREEZE-002`,
derivation bundle SHA-256
`646e0c6442890dffab44490d6c25cc51f0eb09ab106698629909e8022a7ec9f7`.

The expectations in this set were derived from the published specification bytes
alone, in an isolated context, and were committed and round-trip verified
**before** any implementation was inspected or executed. No implementation
output, and no agreement between implementations, contributed to any expected
result here.

Specification: `draft-sergeev-wexp-core-01`, XML SHA-256
`84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d`, 103095 bytes,
bundled with the set so the binding is checkable offline.

## The invariant

`boundary_finding` carries a `status` and a `grounding`. Section 6 constrains how
they may be paired:

> A supported boundary has a grounding value of `asserted-only`, `attributed`, or
> `attested` that the evaluation context accepts. `grounding = not-evaluated` is
> valid only with `status = not-evaluated`; either field paired differently
> produces `E_PROFILE_MAPPING_INVALID`.

A boundary that is **supported** while its grounding was **never evaluated** is
therefore not a weak input to be appraised cautiously. It is an input the
appraiser must refuse: Section 6.2 classifies a well-typed input that violates a
cross-field invariant at ordered position 4, which runs before a supplied fatal
set at position 5 and before an inadmissible asserted claim at position 6, and
Section 8.4 returns the fixed rejection projection for every rejection branch.

Section 7 and Section 14 give the reason the pairing matters rather than merely
the rule. A declared boundary can be false; the appraisal has to preserve whether
the boundary was asserted, attributed, attested, or not evaluated, and relying
parties must not erase that distinction. A boundary marked supported with its
grounding unevaluated erases it at the source.

## The three vectors

| Vector | Fixture | Boundary status | Boundary grounding | Expected |
|---|---|---|---|---|
| [`WEXP-CORE-01-V004-TV-4001`](../vectors/WEXP-CORE-01-VECTORS-004/vectors/WEXP-CORE-01-V004-TV-4001.json) | S4001 | `supported` | `attested` | `accept` |
| [`WEXP-CORE-01-V004-TV-4002`](../vectors/WEXP-CORE-01-VECTORS-004/vectors/WEXP-CORE-01-V004-TV-4002.json) | S4002 | `supported` | `not-evaluated` | `reject`, `E_PROFILE_MAPPING_INVALID` |
| [`WEXP-CORE-01-V004-TV-4003`](../vectors/WEXP-CORE-01-VECTORS-004/vectors/WEXP-CORE-01-V004-TV-4003.json) | S4003 | `supported` | `not-evaluated` | `reject`, `E_PROFILE_MAPPING_INVALID` |

Every vector is the Section 13 common input — target T, evaluation context C,
asserted claim execution, one supported execution base finding, ceiling
execution, one `not-supplied` counter entry — varied only in
`boundary_finding.grounding`, `evaluation_scope["boundary-grounding"]` and, for
S4003, `fatal_conditions`. Nothing else differs between them or from the
published control input used by set 003.

**S4001 — the control.** `attested` is admitted beside a supported status, and
the grounding class changes nothing downstream. Section 8.4's admission
predicate names no grounding value, and Section 8.6, which is exhaustive for
Core-derived non-fatal diagnostics, contains no grounding-keyed row. So this
input must produce the same appraisal as the same input grounded `attributed`,
differing only in the preserved `boundary_grounding`. Without it the set would
show only that inputs are refused, not that refusal is selective.

**S4002 — the invariant.** The pairing violation, isolated. The input is well
typed, every aggregate is correctly scoped, `ceiling_base` is present, and
`fatal_conditions` is empty, so position 4's pairing rule is the only thing it
fails.

**S4003 — the ordering consequence.** The same violation carrying a validly
supplied `E_UNKNOWN_CRITICAL_SEMANTIC`. Position 5 would fire on this input were
position 4 satisfied, so the expected result distinguishes an appraiser that
rejects for the right reason from one that rejects for a reason that happens to
be available. This is a consequence control for the invariant above; it is not a
second invariant.

## A note on `evaluation_scope`

S4002 and S4003 set `evaluation_scope["boundary-grounding"]` to `not-evaluated`,
not `evaluated`. Section 12 governs that capability by boundary status, binding
**and** grounding, and a scope value of `evaluated` beside a governed
`not-evaluated` status is itself a position-4 violation. Leaving the scope value
at `evaluated` would make the input fail two different invariants at once and
would not isolate the pairing rule. The set deliberately varies one thing.

## What this set exposes, and what it does not claim

At the time this set was authored, both engines in `wexp-ref` **accept** S4002:
an input the specification requires to fail closed at ingress is instead
appraised, and reports a supported execution claim resting on a boundary whose
grounding was never evaluated. Both engines return the same result, so comparing
them against each other does not surface it.

That is a statement about coverage, and it is the reason this set exists. The
published sets 001, 002 and 003 all hold `boundary_finding` at one supported,
attributed value; a dimension that never varies produces no divergence to detect,
and their expectations remain correct as written. Agreement between two
implementations written together from one reading of a specification is not
evidence that the reading was right.

This set does **not** claim that an independently derived implementation fails,
that Section 6.2 position 4 is completely covered, that the specification is
defective, or that any implementation is certified or conformant. Sets 001, 002
and 003 are unchanged and remain published.
