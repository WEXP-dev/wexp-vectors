# Derivation of expected appraisals: WEXP-CORE-02-VECTORS-002, B01..B35

Derived solely from `spec/draft-sergeev-wexp-core-02.txt` (sections 4.2, 4.4, 4.5, 6, 6.1, 6.2, 7, 8.1-8.6, 12, 13)
and `spec/SECTION-7-verbatim.txt`. No implementation and no other corpus was consulted. `FORMAT-REFERENCE-C01.json`
was used for the shape of the twenty members only.

## 0. Shared input facts (verified by reading all 35 inputs)

Every input has: `semantics_version` = `wexp-core-2`; target `T`; context `C` (`evaluated_at` 2026-10-12T00:00:00Z,
profile set {`draft-sergeev-wexp-core-02/fixture-1`}); `asserted_claim` = (execution, {}); exactly one base finding
(execution, target T, context C, `target_binding` = supported, `semantic_validation` = supported, basis {E}, no reasons,
no limitations); no qualifier findings; `boundary_finding` with target T, context C, `ceiling_base` = execution,
basis {bd}, reasons {}, limitations {L-boundary}; one counter entry `not-supplied` with empty sets; empty
`recorder_relations`, `profile_evaluation_gaps`, `inherited_limitations`, `fatal_conditions`; a 12-key evaluation scope
with each initial name exactly once. The inputs differ ONLY in `boundary_finding.status`, `.grounding`,
`.target_binding`, `evaluation_context.trust_configuration`, and the `target-binding` / `boundary-grounding` scope
values (checked mechanically: every input stripped of those fields equals B01 stripped of them).

## 1. Verbatim sentences relied on (labels Q1..Q30 are referenced per vector below)

Section 4.2:
- Q1 "The bases have a structural content-depth order: observation < intent < invocation < execution"

Section 4.4:
- Q2 "The admissible claims are: (observation, {}) (observation, {IV}) (intent, {}) (intent, {IV}) (invocation, {})
  (invocation, {IV}) (execution, {}) (execution, {PROV}) (execution, {IV}) (execution, {PROV, IV})"

Section 4.5:
- Q3 "(b1, A1) <= (b2, A2) iff b1 <= b2 and A1 is a subset of A2"

Section 6:
- Q4 "All findings are explicitly scoped. The boundary finding, every base and qualifier aggregate, and every
  profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level
  evaluation-context identifier."
- Q5 "The boundary finding additionally requires supported target binding before its ceiling can be used."
- Q6 "A boundary finding with status = supported MUST contain ceiling_base. Its absence is a profile-mapping failure
  and produces E_PROFILE_MAPPING_INVALID. A supported boundary has a grounding value of asserted-only, attributed, or
  attested that the evaluation context accepts. grounding = not-evaluated is valid only with status = not-evaluated;
  either field paired differently produces E_PROFILE_MAPPING_INVALID. When boundary status is unsupported or
  not-evaluated, a present ceiling_base is diagnostic carrier metadata only and is ignored by the Core algorithm."
- Q7 "counter_evidence is an entry set, not a single strongest status. When no counter-evidence was supplied it
  contains exactly one not-supplied entry with empty affected claims, basis references, reasons, and limitations."

Section 6.1:
- Q8 "The target, evaluation-context identifier, evaluation time, and trust configuration are opaque logical atoms."
- Q9 "Core does not interpret an opaque atom; it only compares, copies, and set-unions it using that equality."

Section 6.2:
- Q10 "4. A well-typed wexp-core-2 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID.
  Cross-field invariants include aggregate cardinality and keys, exact target and context scope, the
  counter-evidence sentinel, qualifier combinations, conditional ceiling_base, evaluation-scope consistency and
  extension-key binding, and profile or registry identity and token category."
- Q11 "No later check or diagnostic is added after any earlier rejection branch wins. The fixed projection in
  Section 8.4 is the only Core result for every rejection branch."

Section 7:
- Q12 "For every supported claim (b, A), b MUST NOT exceed the accepted boundary_finding.ceiling_base."
- Q13 "An accept or downgrade result MUST preserve the boundary grounding status and its limitations. A reject
  result instead uses the fixed projection in Section 8.4."
- Q14 "boundary_finding.status = supported means that the boundary predicate required by the named evaluation
  context passed. The evaluation context MUST identify the minimum acceptable grounding."
- Q15 "An asserted-only or attributed finding can be supported only when the evaluation context explicitly accepts
  that grounding class; the result still reports the weaker grounding and its limitations."
- Q16 "The boundary status has deterministic precedence. When status = not-evaluated, no base is added and the
  appraiser records E_BOUNDARY_NOT_EVALUATED. When status = unsupported, no base is added and it records
  E_BOUNDARY_NOT_SUPPORTED. Only status = supported with target_binding = supported and matching target and
  context makes ceiling_base usable. A failed target binding prevents use of the ceiling and adds the Core
  substantive reason E_EVIDENCE_NOT_BOUND; an unevaluated target binding prevents use of the ceiling and adds the
  Core gap E_BOUNDARY_NOT_EVALUATED, as specified by Section 8.6."

Section 8.1:
- Q17 "A base b is in B if and only if all of the following hold: 1. the unique aggregate base finding for b has
  supported target binding and supported semantic validation; 2. the finding names the same target and evaluation
  context as the appraisal input; 3. the boundary finding is supported, target-bound, and scoped to that same target
  and context; and 4. the accepted Boundary Ceiling is at least b."
- Q18 "For every member of SupportedClaims, the appraiser also produces a support entry containing the exact claim,
  the union of basis references used for its base, boundary, and qualifiers, and the limitations attached to those
  same premises."
- Q19 "The result's inherited_limitations is the set union of the input's inherited limitations; limitations from
  each counter-evidence or profile-gap entry whose affected claims include the asserted claim, a member of
  SupportedClaims, or all-admissible-claims; boundary limitations; every support-entry limitation; and limitations
  attached to findings that determine a reason or gap for the asserted claim. Limitations on unrelated failed
  findings are excluded."

Section 8.2:
- Q20 "accept The asserted claim is an exact member of SupportedClaims and counter-evidence does not block that
  exact claim." / "downgrade The input is safely interpretable and the asserted claim is admissible, but it is not
  exactly supported, or counter-evidence blocks acceptance."
- Q21 "not-supplied and resolved-no-defeat entries do not block by themselves."

Section 8.3:
- Q22 "For each maximal supported claim, the appraisal reports a pair {supported_claim, relation}, where relation
  is one of equal, support-below-claim, support-above-claim, or incomparable. If no claim is supported, the relation
  array is empty."

Section 8.4:
- Q23 (algorithm) "for every non-counter row of the claim-required diagnostic matrix: if that row's exact predicate
  is true: if the row is substantive: add its token to reasons else: add its exact Core gap entry to GapEntries"
- Q24 (rejected_result) "return Appraisal with verdict = reject, semantics_version = "wexp-core-2", fatal_reasons =
  fatal_tokens, substantive_reasons = {}, evaluation_gaps = {}, evaluation_gap_entries = {}, supported_claims = {},
  maximal_supported_claims = {}, support_entries = {}, support_relations = {}, asserted_claim_supported = false,
  boundary_ceiling = unavailable, boundary_grounding = unavailable, target = unavailable, asserted_claim =
  unavailable, recorder_relations = unavailable, counter_evidence = unavailable, inherited_limitations =
  unavailable, evaluation_context = unavailable, evaluation_scope = unavailable"
- Q25 "Every Core-derived finding gap entry has the row's token, the input target and evaluation-context
  identifier, affected_claims={input.asserted_claim}, and the basis-reference and limitation sets of the aggregate
  that made the row true." / "Two equal gap entries collapse under the logical equality in Section 6.1; entries
  that differ in any component remain separate. Substantive reason tokens are a set, so simultaneous causes of the
  same token produce one token without suppressing any distinct token."

Section 8.5:
- Q26 "For an accept or downgrade result, boundary_ceiling is the accepted ceiling only when the boundary finding,
  its target binding, target, and context all pass; otherwise it is unavailable. boundary_grounding preserves the
  input grounding even when the boundary is unsupported."

Section 8.6:
- Q27 "After the rejection checks, every applicable row is evaluated independently exactly once: finding and
  boundary rows use the first diagnostic loop" / "An absent aggregate triggers only its absence row; status rows
  require that aggregate to be present." / "A boundary-exceeded row requires a usable boundary and a present
  asserted-base aggregate whose base is deeper than the ceiling." / "All simultaneously applicable distinct tokens
  are emitted. No condition outside this matrix creates a Core-derived non-fatal token."
- Q28 matrix rows: "E_BOUNDARY_NOT_SUPPORTED (substantive) Boundary status = unsupported; source: boundary
  finding." / "E_BOUNDARY_NOT_EVALUATED (gap) Boundary status = not-evaluated; source: boundary finding." /
  "E_EVIDENCE_NOT_BOUND (substantive) Boundary target_binding = unsupported; source: boundary finding." /
  "E_BOUNDARY_NOT_EVALUATED (gap) Boundary target_binding = not-evaluated; source: boundary finding." /
  "E_BASE_EXCEEDS_BOUNDARY (substantive) Usable boundary with asserted base deeper than its ceiling" /
  "E_MISSING_REQUIRED_EVIDENCE (substantive) Asserted-base aggregate absent; source: none."

Section 12:
- Q29 "The governed status fields are: every finding's target_binding for target-binding; boundary status, binding,
  and grounding for boundary-grounding; ..." / "A scope value of evaluated with a governed not-evaluated status, a
  claim-required finding-backed not-evaluated capability without its aggregate, a current-scope marker whose
  capability is not not-evaluated, or an external capability value without the required marker presence or absence
  violates the cross-field contract and produces E_PROFILE_MAPPING_INVALID."
- Q30 "target-binding and independent-verification are shared across exact roles. Their not-evaluated summary does
  not replace a passing assessment for a different exact role." / "Core does not decide from profile-defined trust
  data whether an external assessment was required." / "Otherwise the scope map alone records the unexercised
  capability and does not become a reason, gap, or substantive finding."

Section 13 (fixture environment): "trust-configuration atom core02-fixture-trust-1, which accepts attributed
boundary grounding" and, for C12, "The support entry also carries L-boundary" with
"inherited_limitations={L-boundary}" when "boundary and a premise carry L-boundary".

## 2. Derivation steps common to every vector

S1 Rejection checks 1-3 (Q10 list, 8.4): outer record present, semantics_version is the text atom wexp-core-2,
   all members present and well-typed, all closed-enum values are defined members -> no E_MALFORMED_NORMALIZED_INPUT /
   E_UNSUPPORTED_SEMANTICS_VERSION in any vector.
S2 Cross-field check (Q10): aggregate cardinality (one boundary, one base finding) OK; scope of every finding is T/C
   (Q4) OK; counter sentinel is the single not-supplied entry with empty sets (Q7) OK; no qualifier aggregates;
   `ceiling_base` present when status = supported (Q6 first sentence) OK in every vector; evaluation scope has every
   initial name exactly once. The remaining cross-field tests that DO vary are:
   (i) Q6 pairing of grounding and status;
   (ii) Q29 scope consistency: boundary status/binding/grounding govern `boundary-grounding`; every finding's
        target_binding (including the boundary finding's) governs `target-binding`; "evaluated" with a governed
        not-evaluated field is E_PROFILE_MAPPING_INVALID.
   If (i) or (ii) fails -> reject with fatal {E_PROFILE_MAPPING_INVALID} and the fixed projection Q24 (Q11: nothing
   else is added). The trust-configuration atom is opaque (Q8, Q9); Core cannot test Q14/Q15 acceptance, see B35.
S3 `fatal_conditions` empty; asserted claim (execution, {}) is admissible (Q2) -> no E_CLAIM_OUT_OF_DOMAIN.
S4 B membership (Q17 / 8.4 loop): the execution finding satisfies conditions 1-2 in every vector. Condition 3 holds
   only when boundary status = supported AND target_binding = supported (target/context always T/C). Condition 4:
   execution <= execution (Q1, Q3) holds. So B = {execution} iff status = supported and target_binding = supported;
   otherwise B = {}.
S5 Q(b): no qualifier findings -> Q = {}; SupportedClaims = {(execution, {})} or {}; Maximal = same;
   asserted_claim_supported = membership.
S6 Diagnostic rows (Q23, Q27, Q28) with the boundary aggregate present and the asserted-base aggregate present and
   fully passing: only the four boundary status/binding rows can fire. E_BASE_EXCEEDS_BOUNDARY never fires (ceiling
   execution is not above execution and, when the boundary is unusable, the row requires a usable boundary).
   E_MISSING_REQUIRED_EVIDENCE never fires (asserted-base aggregate present). No PROV/IV rows (unqualified claim).
   Core gap entries use Q25: token, target T, context C, affected_claims {(execution, {})}, basis {bd}, limitations
   {L-boundary}; two rows yielding the same token with the same components collapse into one entry.
S7 Finding reasons: all findings have empty reasons -> nothing added. Profile gaps: none. Counter: the single
   not-supplied entry is not applicable/blocking (Q21) -> no counter tokens or gap entries.
S8 Verdict (Q20): accept iff asserted_claim_supported (counter never blocks here); else downgrade.
S9 boundary_ceiling (Q26): "execution" iff status, binding, target, context all pass; else unavailable (null).
   boundary_grounding (Q13, Q26, Q15): the input grounding, in every accept/downgrade result.
S10 inherited_limitations (Q19): the term "boundary limitations" is listed unconditionally, and in every
   non-reject vector the boundary finding is either a support premise or the finding that determines the reason/gap
   for the asserted claim -> {L-boundary}. Nothing else carries limitations.
S11 Support entry (Q18) for an accept: claim (execution, {}), basis = {bd} U {E}, limitations = {L-boundary} U {} =
   {L-boundary} (confirmed by the C12 row's "The support entry also carries L-boundary"). Relation (Q22): equal.
S12 Copied components: target, asserted_claim, recorder_relations ([]), counter_evidence (the input entry),
   evaluation_context, evaluation_scope (Section 12: "preserves the exact pair and status in the result").

## 3. Readings that the text leaves open (full detail in AMBIGUITIES.json)

R-A (Q6, affects B21-B29) "grounding = not-evaluated is valid only with status = not-evaluated; either field paired
   differently produces E_PROFILE_MAPPING_INVALID." Primary reading: the clause names the one valid pairing
   (status = not-evaluated, grounding = not-evaluated) and "either field paired differently" makes BOTH directions
   invalid, i.e. status = not-evaluated with grounding in {asserted-only, attributed, attested} is also
   E_PROFILE_MAPPING_INVALID. This is the natural meaning of "either field"; it is also consistent with Section 12's
   treatment of status and grounding as co-governed fields and with Section 7's statement that grounding classes
   are outcomes of an assessment ("a valid signature ... can make it attributed"). Alternative reading: only
   grounding = not-evaluated constrains status, so status = not-evaluated with a concrete grounding is valid and
   yields the Q16/Q28 gap E_BOUNDARY_NOT_EVALUATED (downgrade). Primary chosen: reject.
R-B (Q16 "deterministic precedence", affects B11-B14, B16, B17, B31) Primary reading: the 8.4 loop and Q27 ("every
   applicable row is evaluated independently exactly once", "All simultaneously applicable distinct tokens are
   emitted") govern diagnostics; precedence in Q16 concerns ceiling usability and base admission, not suppression
   of a row whose exact predicate is true. So a boundary with status = unsupported and target_binding = unsupported
   emits BOTH E_BOUNDARY_NOT_SUPPORTED and E_EVIDENCE_NOT_BOUND, etc. Alternative reading: "precedence" means the
   status row alone is emitted unless status = supported. Primary chosen: both rows (normative algorithm text).
R-C (Q14/Q15 vs Q8/Q9, affects B35) status = supported with grounding = asserted-only under core02-fixture-trust-1,
   described in Section 13 as the atom "which accepts attributed boundary grounding". Primary reading: Core treats
   the trust configuration as an opaque atom and cannot test acceptance; the acceptance obligation is on the profile
   (Q14: "MUST identify", "A profile MUST NOT mark a boundary supported merely because ..."), and Q6's only stated
   E_PROFILE_MAPPING_INVALID consequences are the missing ceiling_base and the not-evaluated pairing; Q10's list of
   Core cross-field invariants does not include grounding acceptance; Q30 "Core does not decide from profile-defined
   trust data". So Core returns accept and "the result still reports the weaker grounding" (Q15). Alternative
   reading: Q6 "A supported boundary has a grounding value ... that the evaluation context accepts" is itself a
   cross-field invariant and, taking the Section 13 description as the atom's minimum, asserted-only is not accepted
   -> reject {E_PROFILE_MAPPING_INVALID}. Primary chosen: accept.

## 4. Per-vector derivation

Notation: st = boundary status, gr = grounding, tb = boundary target_binding, trust = trust_configuration atom,
scope = evaluation-scope values that are not-evaluated (TB = target-binding, BG = boundary-grounding).
"Fixed projection" = Q24 with fatal_reasons = {E_PROFILE_MAPPING_INVALID} and all input-derived members null.
"Downgrade shell" = verdict downgrade; fatal {}; S=M={}; A=false; entries/relations {}; boundary_ceiling null;
boundary_grounding = gr; inherited_limitations {L-boundary}; copied components per S12.
"Gap entry G" = {token E_BOUNDARY_NOT_EVALUATED, target T, context C, affected_claims {(execution,{})},
basis {bd}, limitations {L-boundary}}.

### B01  st=supported gr=asserted-only tb=supported trust=core02-test-trust-asserted-only-1 scope={}
Quotes: Q6, Q12, Q15, Q16 ("Only status = supported with target_binding = supported ... makes ceiling_base usable"),
Q17, Q18, Q19, Q20, Q26, Q29.
S2: pairing valid (neither field not-evaluated); scope consistent (no governed field not-evaluated). Profile-side
premise consistent: the test atom's minimum is asserted-only, so Q15's acceptance condition is met (not a Core test).
S4: B = {execution}. S5: S = M = {(execution,{})}; A = true. S6/S7: no row predicate true; reasons {}, gaps {}.
S8: accept. S9: boundary_ceiling = execution; boundary_grounding = asserted-only ("the result still reports the
weaker grounding and its limitations", Q15). S10: inherited {L-boundary}. S11: support entry {claim E, basis {E,bd},
limitations {L-boundary}}; relation {E: equal}.
Result: accept; fatal {}; reasons {}; gaps {}.

### B02  st=supported gr=asserted-only tb=unsupported trust=core02-test-trust-asserted-only-1 scope={}
Quotes: Q5, Q16 ("A failed target binding prevents use of the ceiling and adds the Core substantive reason
E_EVIDENCE_NOT_BOUND"), Q17 cond. 3, Q28 row "E_EVIDENCE_NOT_BOUND (substantive) Boundary target_binding =
unsupported", Q26, Q19.
S2: valid; scope consistent (unsupported is not not-evaluated). S4: condition 3 fails -> B = {}. S6: row
E_EVIDENCE_NOT_BOUND true; no other row. S8: downgrade. S9: ceiling null; grounding asserted-only.
Result: downgrade shell; reasons {E_EVIDENCE_NOT_BOUND}; gaps {}.

### B03  st=supported gr=asserted-only tb=not-evaluated trust=core02-test-trust-asserted-only-1 scope={TB,BG}
Quotes: Q16 ("an unevaluated target binding prevents use of the ceiling and adds the Core gap
E_BOUNDARY_NOT_EVALUATED"), Q28 row "E_BOUNDARY_NOT_EVALUATED (gap) Boundary target_binding = not-evaluated",
Q25, Q29 (binding governs both target-binding and boundary-grounding; both scope values are not-evaluated, so the
"evaluated with a governed not-evaluated status" violation does not arise), Q30 (execution finding's supported
binding is unaffected by the shared not-evaluated summary).
S2: valid. S4: B = {}. S6: gap row true -> gap entry G; no substantive row. S8: downgrade. S9: ceiling null;
grounding asserted-only.
Result: downgrade shell; reasons {}; gaps {E_BOUNDARY_NOT_EVALUATED}; entries {G}.

### B04  st=supported gr=attributed tb=unsupported trust=core02-fixture-trust-1 scope={}
Same derivation as B02 (quotes Q5, Q16, Q17, Q28, Q26); grounding attributed is accepted by the fixture atom
(Section 13) and is in any case not a Core test.
Result: downgrade shell; reasons {E_EVIDENCE_NOT_BOUND}; gaps {}; boundary_grounding attributed.

### B05  st=supported gr=attributed tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Same derivation as B03 (quotes Q16, Q28, Q25, Q29).
Result: downgrade shell; reasons {}; gaps {E_BOUNDARY_NOT_EVALUATED}; entries {G}; boundary_grounding attributed.

### B06  st=supported gr=attested tb=supported trust=core02-fixture-trust-1 scope={}
Same derivation as B01 (quotes Q6, Q12, Q16, Q17, Q18, Q19, Q20, Q26). Section 7: "an applicable
boundary-grounding profile can make it attested"; attested is stronger than the fixture atom's attributed minimum.
Result: accept; fatal/reasons/gaps {}; boundary_ceiling execution; boundary_grounding attested; support entry
{E, basis {E,bd}, limitations {L-boundary}}; relation {E: equal}; inherited {L-boundary}.

### B07  st=supported gr=attested tb=unsupported trust=core02-fixture-trust-1 scope={}
Same as B02. Result: downgrade shell; reasons {E_EVIDENCE_NOT_BOUND}; gaps {}; boundary_grounding attested.

### B08  st=supported gr=attested tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Same as B03. Result: downgrade shell; reasons {}; gaps {E_BOUNDARY_NOT_EVALUATED}; entries {G};
boundary_grounding attested.

### B09  st=supported gr=not-evaluated tb=unsupported trust=core02-fixture-trust-1 scope={BG}
Quotes: Q6 "grounding = not-evaluated is valid only with status = not-evaluated; either field paired differently
produces E_PROFILE_MAPPING_INVALID."; Q10 step 4; Q11; Q24.
S2(i): grounding = not-evaluated paired with status = supported -> E_PROFILE_MAPPING_INVALID (this is the explicitly
stated direction of Q6; no reading issue). Q11: nothing further is derived.
Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B10  st=supported gr=not-evaluated tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Same as B09 (Q6 explicit direction). Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B11  st=unsupported gr=asserted-only tb=unsupported trust=core02-fixture-trust-1 scope={}
Quotes: Q6 (pairing valid: neither field is not-evaluated); Q16 "When status = unsupported, no base is added and it
records E_BOUNDARY_NOT_SUPPORTED." and "A failed target binding ... adds the Core substantive reason
E_EVIDENCE_NOT_BOUND"; Q27 "every applicable row is evaluated independently exactly once" / "All simultaneously
applicable distinct tokens are emitted"; Q28 rows E_BOUNDARY_NOT_SUPPORTED and E_EVIDENCE_NOT_BOUND; Q26
"boundary_grounding preserves the input grounding even when the boundary is unsupported"; Q19.
S2: valid; scope consistent. S4: B = {}. S6: both row predicates true -> both tokens (primary reading R-B).
Result: downgrade shell; reasons {E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND}; gaps {}; grounding asserted-only.
Ambiguity R-B: alternative reasons {E_BOUNDARY_NOT_SUPPORTED} only.

### B12  st=unsupported gr=asserted-only tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Quotes: Q6 (valid pairing); Q16; Q27; Q28 rows E_BOUNDARY_NOT_SUPPORTED (substantive) and "E_BOUNDARY_NOT_EVALUATED
(gap) Boundary target_binding = not-evaluated"; Q25; Q29 (binding not-evaluated; TB and BG scope both not-evaluated
-> consistent); Q26.
S4: B = {}. S6: substantive row E_BOUNDARY_NOT_SUPPORTED true; gap row (binding) true -> gap entry G.
Result: downgrade shell; reasons {E_BOUNDARY_NOT_SUPPORTED}; gaps {E_BOUNDARY_NOT_EVALUATED}; entries {G}.
Ambiguity R-B: alternative gaps {} (status row only).

### B13  st=unsupported gr=attributed tb=unsupported trust=core02-fixture-trust-1 scope={}
Same as B11. Result: downgrade shell; reasons {E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND}; gaps {};
grounding attributed. Ambiguity R-B as B11.

### B14  st=unsupported gr=attributed tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Same as B12. Result: downgrade shell; reasons {E_BOUNDARY_NOT_SUPPORTED}; gaps {E_BOUNDARY_NOT_EVALUATED};
entries {G}; grounding attributed. Ambiguity R-B as B12.

### B15  st=unsupported gr=attested tb=supported trust=core02-fixture-trust-1 scope={}
Quotes: Q6 (valid pairing); Q16 "When status = unsupported, no base is added and it records
E_BOUNDARY_NOT_SUPPORTED."; Q28 row E_BOUNDARY_NOT_SUPPORTED; Q17 cond. 3 ("the boundary finding is supported");
Q26; Q19.
S4: B = {}. S6: only the status row is true (binding supported). S8: downgrade.
Result: downgrade shell; reasons {E_BOUNDARY_NOT_SUPPORTED}; gaps {}; grounding attested. No ambiguity.

### B16  st=unsupported gr=attested tb=unsupported trust=core02-fixture-trust-1 scope={}
Same as B11. Result: downgrade shell; reasons {E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND}; gaps {};
grounding attested. Ambiguity R-B as B11.

### B17  st=unsupported gr=attested tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Same as B12. Result: downgrade shell; reasons {E_BOUNDARY_NOT_SUPPORTED}; gaps {E_BOUNDARY_NOT_EVALUATED};
entries {G}; grounding attested. Ambiguity R-B as B12.

### B18  st=unsupported gr=not-evaluated tb=supported trust=core02-fixture-trust-1 scope={BG}
Quotes: Q6 "grounding = not-evaluated is valid only with status = not-evaluated; either field paired differently
produces E_PROFILE_MAPPING_INVALID."; Q10; Q11; Q24.
S2(i): grounding = not-evaluated with status = unsupported (explicit direction of Q6) -> E_PROFILE_MAPPING_INVALID.
Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}. No ambiguity.

### B19  st=unsupported gr=not-evaluated tb=unsupported trust=core02-fixture-trust-1 scope={BG}
Same as B18. Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B20  st=unsupported gr=not-evaluated tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Same as B18. Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B21  st=not-evaluated gr=asserted-only tb=supported trust=core02-fixture-trust-1 scope={BG}
Quotes: Q6 "grounding = not-evaluated is valid only with status = not-evaluated; either field paired differently
produces E_PROFILE_MAPPING_INVALID."; Q10; Q11; Q24; (alternative) Q16 "When status = not-evaluated, no base is
added and the appraiser records E_BOUNDARY_NOT_EVALUATED.", Q28 row "E_BOUNDARY_NOT_EVALUATED (gap) Boundary
status = not-evaluated", Q25, Q26, Q19, Q29.
Primary (R-A bidirectional): status = not-evaluated is "paired differently" from grounding = not-evaluated ->
E_PROFILE_MAPPING_INVALID. Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.
Alternative (R-A unidirectional): input valid (BG scope not-evaluated matches governed status not-evaluated, Q29);
B = {} (Q17 cond. 3); gap row (status) true -> entry G; downgrade; ceiling null; grounding asserted-only;
inherited {L-boundary}; reasons {}; gaps {E_BOUNDARY_NOT_EVALUATED}.

### B22  st=not-evaluated gr=asserted-only tb=unsupported trust=core02-fixture-trust-1 scope={BG}
Primary as B21: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.
Alternative: downgrade shell; gaps {E_BOUNDARY_NOT_EVALUATED} (entry G) from the status row and reasons
{E_EVIDENCE_NOT_BOUND} from the binding row (Q28; under R-B primary both rows fire); grounding asserted-only.

### B23  st=not-evaluated gr=asserted-only tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Primary as B21: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.
Alternative: downgrade shell; both gap rows (status, binding) produce the same token and identical components ->
one entry G (Q25 "Two equal gap entries collapse"); gaps {E_BOUNDARY_NOT_EVALUATED}; reasons {}.

### B24  st=not-evaluated gr=attributed tb=supported trust=core02-fixture-trust-1 scope={BG}
As B21 (grounding attributed in the alternative). Primary: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B25  st=not-evaluated gr=attributed tb=unsupported trust=core02-fixture-trust-1 scope={BG}
As B22. Primary: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B26  st=not-evaluated gr=attributed tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
As B23. Primary: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B27  st=not-evaluated gr=attested tb=supported trust=core02-fixture-trust-1 scope={BG}
As B21 (grounding attested in the alternative). Primary: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B28  st=not-evaluated gr=attested tb=unsupported trust=core02-fixture-trust-1 scope={BG}
As B22. Primary: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B29  st=not-evaluated gr=attested tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
As B23. Primary: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}.

### B30  st=not-evaluated gr=not-evaluated tb=supported trust=core02-fixture-trust-1 scope={BG}
Quotes: Q6 (the one explicitly valid not-evaluated pairing); Q16 "When status = not-evaluated, no base is added and
the appraiser records E_BOUNDARY_NOT_EVALUATED."; Q28 row "E_BOUNDARY_NOT_EVALUATED (gap) Boundary status =
not-evaluated"; Q25; Q29 (status and grounding are governed by boundary-grounding, whose scope value is
not-evaluated -> consistent; target-binding evaluated with every finding's binding supported -> consistent); Q26
("otherwise it is unavailable"; grounding preserved); Q19; Q13.
S4: B = {}. S6: status gap row true -> entry G; binding row false. S8: downgrade. S9: ceiling null;
boundary_grounding = "not-evaluated" (the input grounding is preserved as a closed-enum value, not unavailable).
Result: downgrade shell; reasons {}; gaps {E_BOUNDARY_NOT_EVALUATED}; entries {G}; grounding not-evaluated.

### B31  st=not-evaluated gr=not-evaluated tb=unsupported trust=core02-fixture-trust-1 scope={BG}
Quotes as B30 plus Q16 "A failed target binding ... adds the Core substantive reason E_EVIDENCE_NOT_BOUND", Q27,
Q28 row E_EVIDENCE_NOT_BOUND. Scope: target-binding evaluated, boundary binding unsupported (not not-evaluated) ->
consistent.
S6: status gap row -> entry G; binding substantive row -> E_EVIDENCE_NOT_BOUND (R-B primary).
Result: downgrade shell; reasons {E_EVIDENCE_NOT_BOUND}; gaps {E_BOUNDARY_NOT_EVALUATED}; entries {G};
grounding not-evaluated. Ambiguity R-B: alternative reasons {}.

### B32  st=not-evaluated gr=not-evaluated tb=not-evaluated trust=core02-fixture-trust-1 scope={TB,BG}
Quotes as B30 plus Q28 row "E_BOUNDARY_NOT_EVALUATED (gap) Boundary target_binding = not-evaluated" and Q25 "Two
equal gap entries collapse under the logical equality in Section 6.1".
S2: all three governed fields not-evaluated; TB and BG scope both not-evaluated -> consistent.
S6: both gap rows true; entries identical in every component -> one entry G; token projection one token.
Result: downgrade shell; reasons {}; gaps {E_BOUNDARY_NOT_EVALUATED}; entries {G}; grounding not-evaluated.
(R-B does not change this result: either reading yields the same single token and entry.)

### B33  st=not-evaluated gr=not-evaluated tb=supported trust=core02-fixture-trust-1 scope={}  (boundary-grounding = evaluated)
Quotes: Q29 "The governed status fields are: ... boundary status, binding, and grounding for boundary-grounding" and
"A scope value of evaluated with a governed not-evaluated status ... violates the cross-field contract and produces
E_PROFILE_MAPPING_INVALID."; Q10 ("evaluation-scope consistency"); Q11; Q24.
S2(ii): boundary-grounding = evaluated while status and grounding are not-evaluated -> E_PROFILE_MAPPING_INVALID.
(Compare B30, identical except boundary-grounding = not-evaluated, which is valid.)
Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}. No ambiguity.

### B34  st=supported gr=attributed tb=not-evaluated trust=core02-fixture-trust-1 scope={TB}  (boundary-grounding = evaluated)
Quotes: Q29 (binding is a governed field of boundary-grounding: "boundary status, binding, and grounding for
boundary-grounding"; "A scope value of evaluated with a governed not-evaluated status ... produces
E_PROFILE_MAPPING_INVALID"); Q10; Q11; Q24.
S2(ii): boundary target_binding = not-evaluated while boundary-grounding = evaluated -> E_PROFILE_MAPPING_INVALID.
(target-binding = not-evaluated is itself consistent; compare B05, which has both scope values not-evaluated and
is valid.)
Result: fixed projection; fatal {E_PROFILE_MAPPING_INVALID}. No ambiguity.

### B35  st=supported gr=asserted-only tb=supported trust=core02-fixture-trust-1 scope={}
Quotes: Q8, Q9 (trust configuration is an opaque atom Core does not interpret); Q14, Q15 (profile-side acceptance
obligation; "the result still reports the weaker grounding and its limitations"); Q6 (Core-stated
E_PROFILE_MAPPING_INVALID consequences are the missing ceiling_base and the not-evaluated pairing only); Q10
(cross-field invariant list does not include grounding acceptance); Q30 "Core does not decide from profile-defined
trust data whether an external assessment was required"; Section 13 "core02-fixture-trust-1, which accepts
attributed boundary grounding"; then Q12, Q16, Q17, Q18, Q19, Q20, Q26 as for B01.
Primary (R-C): Core cannot and does not test whether the opaque atom accepts asserted-only; the input is
structurally and cross-field valid; derivation identical to B01 -> accept; boundary_ceiling execution;
boundary_grounding asserted-only; support entry {E, basis {E,bd}, limitations {L-boundary}}; relation {E: equal};
inherited {L-boundary}; fatal/reasons/gaps {}.
Alternative: treating Q6 "that the evaluation context accepts" as a Core cross-field invariant and the Section 13
description as fixing attributed as this atom's minimum, asserted-only is below the minimum -> fixed projection;
fatal {E_PROFILE_MAPPING_INVALID}. Recorded in AMBIGUITIES.json. Note that the profile-side premise is indeed
violated under the Section 13 description (the profile "MUST NOT" have marked it supported), but that violation is
not Core-observable from the normalized input.

## 5. Summary table

| ID  | status        | grounding     | tb            | trust   | scope n/e | verdict   | fatal                      | substantive_reasons                             | evaluation_gaps            |
|-----|---------------|---------------|---------------|---------|-----------|-----------|----------------------------|-------------------------------------------------|----------------------------|
| B01 | supported     | asserted-only | supported     | a-only  | -         | accept    | -                          | -                                               | -                          |
| B02 | supported     | asserted-only | unsupported   | a-only  | -         | downgrade | -                          | E_EVIDENCE_NOT_BOUND                            | -                          |
| B03 | supported     | asserted-only | not-evaluated | a-only  | TB,BG     | downgrade | -                          | -                                               | E_BOUNDARY_NOT_EVALUATED   |
| B04 | supported     | attributed    | unsupported   | fixture | -         | downgrade | -                          | E_EVIDENCE_NOT_BOUND                            | -                          |
| B05 | supported     | attributed    | not-evaluated | fixture | TB,BG     | downgrade | -                          | -                                               | E_BOUNDARY_NOT_EVALUATED   |
| B06 | supported     | attested      | supported     | fixture | -         | accept    | -                          | -                                               | -                          |
| B07 | supported     | attested      | unsupported   | fixture | -         | downgrade | -                          | E_EVIDENCE_NOT_BOUND                            | -                          |
| B08 | supported     | attested      | not-evaluated | fixture | TB,BG     | downgrade | -                          | -                                               | E_BOUNDARY_NOT_EVALUATED   |
| B09 | supported     | not-evaluated | unsupported   | fixture | BG        | reject    | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B10 | supported     | not-evaluated | not-evaluated | fixture | TB,BG     | reject    | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B11 | unsupported   | asserted-only | unsupported   | fixture | -         | downgrade | -                          | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND  | -                          |
| B12 | unsupported   | asserted-only | not-evaluated | fixture | TB,BG     | downgrade | -                          | E_BOUNDARY_NOT_SUPPORTED                        | E_BOUNDARY_NOT_EVALUATED   |
| B13 | unsupported   | attributed    | unsupported   | fixture | -         | downgrade | -                          | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND  | -                          |
| B14 | unsupported   | attributed    | not-evaluated | fixture | TB,BG     | downgrade | -                          | E_BOUNDARY_NOT_SUPPORTED                        | E_BOUNDARY_NOT_EVALUATED   |
| B15 | unsupported   | attested      | supported     | fixture | -         | downgrade | -                          | E_BOUNDARY_NOT_SUPPORTED                        | -                          |
| B16 | unsupported   | attested      | unsupported   | fixture | -         | downgrade | -                          | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND  | -                          |
| B17 | unsupported   | attested      | not-evaluated | fixture | TB,BG     | downgrade | -                          | E_BOUNDARY_NOT_SUPPORTED                        | E_BOUNDARY_NOT_EVALUATED   |
| B18 | unsupported   | not-evaluated | supported     | fixture | BG        | reject    | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B19 | unsupported   | not-evaluated | unsupported   | fixture | BG        | reject    | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B20 | unsupported   | not-evaluated | not-evaluated | fixture | TB,BG     | reject    | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B21 | not-evaluated | asserted-only | supported     | fixture | BG        | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B22 | not-evaluated | asserted-only | unsupported   | fixture | BG        | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B23 | not-evaluated | asserted-only | not-evaluated | fixture | TB,BG     | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B24 | not-evaluated | attributed    | supported     | fixture | BG        | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B25 | not-evaluated | attributed    | unsupported   | fixture | BG        | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B26 | not-evaluated | attributed    | not-evaluated | fixture | TB,BG     | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B27 | not-evaluated | attested      | supported     | fixture | BG        | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B28 | not-evaluated | attested      | unsupported   | fixture | BG        | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B29 | not-evaluated | attested      | not-evaluated | fixture | TB,BG     | reject*   | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B30 | not-evaluated | not-evaluated | supported     | fixture | BG        | downgrade | -                          | -                                               | E_BOUNDARY_NOT_EVALUATED   |
| B31 | not-evaluated | not-evaluated | unsupported   | fixture | BG        | downgrade | -                          | E_EVIDENCE_NOT_BOUND                            | E_BOUNDARY_NOT_EVALUATED   |
| B32 | not-evaluated | not-evaluated | not-evaluated | fixture | TB,BG     | downgrade | -                          | -                                               | E_BOUNDARY_NOT_EVALUATED   |
| B33 | not-evaluated | not-evaluated | supported     | fixture | -  (!)    | reject    | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B34 | supported     | attributed    | not-evaluated | fixture | TB (!)    | reject    | E_PROFILE_MAPPING_INVALID  | -                                               | -                          |
| B35 | supported     | asserted-only | supported     | fixture | -         | accept*   | -                          | -                                               | -                          |

`*` = primary reading; alternative recorded in AMBIGUITIES.json (R-A for B21-B29; R-C for B35; R-B alternatives for
B11-B14, B16, B17, B31 drop the second boundary row). `(!)` = scope inconsistent with a governed not-evaluated field.
In every non-reject row: boundary_grounding = input grounding; boundary_ceiling = execution for accept and null
otherwise; inherited_limitations = {L-boundary}; support entry present only for accept with basis {E, bd} and
limitations {L-boundary}; every gap entry is G (target T, context C, affected {(execution,{})}, basis {bd},
limitations {L-boundary}).
