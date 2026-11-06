# SPEC-ISSUES-core02-s7: ambiguities met while deriving the section 7 boundary matrix

Published text: `draft-sergeev-wexp-core-02`, XML SHA-256
`de983051a1c6ea51ea9b7f965fe9eabf2d97af92ab2f074781bd44e3f99c8782`. These are
observations for the specification review process. The text was not changed and no
vector in `WEXP-CORE-02-VECTORS-002` is used to settle an ambiguity. Status of each
issue: open unless stated.

## A1. "that the evaluation context accepts" is not Core-checkable

Section 6: "A supported boundary has a grounding value of asserted-only, attributed,
or attested that the evaluation context accepts." Section 7: "An asserted-only or
attributed finding can be supported only when the evaluation context explicitly
accepts that grounding class" and "The evaluation context MUST identify the minimum
acceptable grounding."

The AppraisalInput carries `trust_configuration` as an opaque atom (section 6.1) and no
field that names the accepted grounding classes or the minimum. Core therefore cannot
test acceptance. Section 6.2 check 4 lists cross-field invariants with "include", an
open list, and the acceptance sentence sits in the same section 6 paragraph as the
pairing rule that does name `E_PROFILE_MAPPING_INVALID`. Two readings:

- (a) acceptance is a mapping-profile obligation only; Core appraises the input as
  given and reports the weaker grounding (section 7 "the result still reports the
  weaker grounding and its limitations"). Probe B35 records this outcome.
- (b) acceptance is a cross-field invariant; but Core has no data to evaluate it, so
  reading (b) is not implementable without a new input member.

Readings taken: the isolated derivation session chose (a) as primary for probe B35
(accept, grounding asserted-only preserved) and recorded (b) as the alternative;
`wexp_ref.core02` at commit `56289024c9ee748111f1f1d4f42728ffe04d8d69` produces (a).
The matrix author reached (a) independently. B35 is frozen under (a) and labelled a
probe; it is not a claim that the input is profile-conforming.

Suggested clarification: state explicitly that acceptance is evaluated by the mapping
profile before Core invocation and is not a section 6.2 cross-field check, or add the
accepted minimum to the normalized input.

## A2. Direction of the not-evaluated pairing rule

Section 6: "grounding = not-evaluated is valid only with status = not-evaluated; either
field paired differently produces E_PROFILE_MAPPING_INVALID."

Reading (two-way): `status = not-evaluated` also requires `grounding = not-evaluated`,
so `status = not-evaluated` with `grounding = attested` (or attributed, asserted-only)
is rejected at check 4. Reading (one-way): only `grounding = not-evaluated` is
constrained; a not-evaluated boundary may still carry an established grounding and the
result is downgrade with the gap `E_BOUNDARY_NOT_EVALUATED` and that grounding
preserved. "either field paired differently" supports the two-way reading; "is valid
only with" is written from the grounding side only. Cells 25-33 of the matrix (nine
cells, cases B21-B29) rest on this sentence.

Readings taken: the isolated session chose the two-way reading as primary (reject,
E_PROFILE_MAPPING_INVALID) and recorded the one-way reading with its full alternative
result; the matrix author reached the two-way reading independently; `wexp_ref.core02`
produces the two-way result on all nine cases. The nine cases are frozen under the
two-way reading and flagged by this issue.

Suggested clarification: "status = not-evaluated if and only if grounding =
not-evaluated; any other pairing produces E_PROFILE_MAPPING_INVALID", or the one-way
form if an unevaluated boundary with established grounding is meant to be expressible.

## A3. Section 7 "records" versus section 8.6 "claim-required" rows for the boundary

Section 7 says the appraiser "records E_BOUNDARY_NOT_EVALUATED" / "records
E_BOUNDARY_NOT_SUPPORTED" unconditionally for the respective status. Section 8.6
states that the matrix is "claim-required" and that "finding and boundary rows use the
first diagnostic loop"; the boundary rows have no asserted-base condition, so the two
sections agree for every admissible asserted claim. The word "claim-required" could be
read as making boundary rows conditional on the asserted claim. No vector depends on
this; noted for wording only.

## A4. Boundary target_binding = not-evaluated and the two gap rows with one token

Section 8.6 has two rows yielding `E_BOUNDARY_NOT_EVALUATED` (status = not-evaluated;
target_binding = not-evaluated). Section 8.4: "Every Core-derived finding gap entry has
the row's token, the input target and evaluation-context identifier,
affected_claims={input.asserted_claim}, and the basis-reference and limitation sets of
the aggregate that made the row true" and "Two equal gap entries collapse". When both
rows are true for the same boundary aggregate, the two entries are equal and collapse
to one. This follows from the text; it is listed because an implementation that keys
entries by row rather than by value would report two. Cell 36 (case B32) exercises it.

## A5. Scope value for boundary-grounding when nothing is not-evaluated

Section 12 states for base-support and provenance-support that a present wholly
assessed aggregate paired with a not-evaluated capability is a violation, and for the
shared capabilities that the summary "does not replace a passing assessment". For
`boundary-grounding`, which is neither, the text does not say whether
`boundary-grounding = not-evaluated` with a fully evaluated boundary aggregate is a
violation. Not exercised by this set.

## A6. "deterministic precedence" and the independent section 8.6 boundary rows

Section 7: "The boundary status has deterministic precedence. When status =
not-evaluated, no base is added and the appraiser records E_BOUNDARY_NOT_EVALUATED.
When status = unsupported, no base is added and it records E_BOUNDARY_NOT_SUPPORTED.
[...] A failed target binding prevents use of the ceiling and adds the Core
substantive reason E_EVIDENCE_NOT_BOUND; an unevaluated target binding prevents use of
the ceiling and adds the Core gap E_BOUNDARY_NOT_EVALUATED, as specified by Section 8.6."

Raised by the isolated session for cases B11-B14, B16, B17 and B31 (status
unsupported or not-evaluated combined with a failed or unevaluated binding). Reading
(a): "precedence" governs ceiling usability and base admission only; section 8.6
("every applicable row is evaluated independently exactly once"; "All simultaneously
applicable distinct tokens are emitted") makes both the status row and the binding row
fire, so the result carries both tokens. Reading (b): precedence suppresses the binding
row whenever the status row already fires, and only the status token appears.

Readings taken: the isolated session chose (a) as primary and recorded (b) with full
alternative results; the matrix author reached (a); `wexp_ref.core02` produces (a) on
all seven cases. Suggested clarification: state in section 7 that the precedence
sentence orders the ceiling decision only and does not suppress any section 8.6 row.
