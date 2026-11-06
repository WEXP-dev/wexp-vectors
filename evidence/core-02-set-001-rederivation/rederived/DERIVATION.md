# Independent derivation of the 89 Core-02 corpus expectations

Source of every expectation: `spec/draft-sergeev-wexp-core-02.txt` (draft-sergeev-wexp-core-02, 23 October 2026).
Nothing outside `handoff/` was read; no implementation was consulted or executed. The only expected
result consulted was `FORMAT-REFERENCE-C01.json` (format only). Python was used only to write the JSON
files from values stated in this document and to copy input members that the text says carry through.

Notation: `F1` = the fixture profile identity `draft-sergeev-wexp-core-02/fixture-1`; `X1` = the test
profile identity `wexp-core02-test-profile/extension-1` (present only in the 17 per-case catalogs).
`O I N E` = unqualified observation/intent/invocation/execution; `+P`/`+V` = PROV/IV. `S` =
supported_claims, `M` = maximal_supported_claims, `A` = asserted_claim_supported. A basis reference
`bd`, `E`, `V(E)` ... denotes the pair `[F1, "<local>"]`. `MALF` = E_MALFORMED_NORMALIZED_INPUT,
`PMI` = E_PROFILE_MAPPING_INVALID, `MISSING` = E_MISSING_REQUIRED_EVIDENCE.

## 0. Quote bank (verbatim sentences relied on; cited below as [Qn])

Section 4.4
- [Q1] "A typed claim is a pair (base, qualifiers), where base is a content base and qualifiers is a subset of {PROV, IV}. The claim is admissible only if PROV is absent or the base is execution."
- [Q2] "Well-formedness and admissibility are separate: (intent, {PROV}) uses a recognized base and qualifier set and is well-formed, but is inadmissible as an asserted claim and is rejected at step 6 when no earlier rejection applies in Section 6.2; an unknown base or qualifier, wrong logical type, or malformed qualifier set fails the structural check at step 3."
- [Q3] "An asserted claim outside this domain is rejected with E_CLAIM_OUT_OF_DOMAIN."

Section 4.5
- [Q4] "(b1, A1) <= (b2, A2)  iff  b1 <= b2 and A1 is a subset of A2" ... "For example, (execution, {PROV}) and (execution, {IV}) are incomparable, as are (invocation, {IV}) and (execution, {})."

Section 6 (normalized input)
- [Q5] "Every displayed top-level component is REQUIRED.  The only semantics version defined by this document is wexp-core-2.  Any other text-atom value is fatal and produces E_UNSUPPORTED_SEMANTICS_VERSION.  An absent or non-text value is malformed under Section 6.2."
- [Q6] "All findings are explicitly scoped.  The boundary finding, every base and qualifier aggregate, and every profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level evaluation-context identifier.  A foreign-scoped aggregate is not negative evidence for this appraisal; it violates the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID."
- [Q7] "A normalized input contains exactly one aggregated boundary finding, at most one aggregated base finding for each (target, base, evaluation_context) key, and at most one aggregated qualifier finding for each (target, qualifier, qualified_base, evaluation_context) key. ... Duplicate or conflicting aggregate findings are fatal and produce E_PROFILE_MAPPING_INVALID."
- [Q8] "A boundary finding with status = supported MUST contain ceiling_base.  Its absence is a profile-mapping failure and produces E_PROFILE_MAPPING_INVALID.  A supported boundary has a grounding value of asserted-only, attributed, or attested that the evaluation context accepts. grounding = not-evaluated is valid only with status = not-evaluated; either field paired differently produces E_PROFILE_MAPPING_INVALID.  When boundary status is unsupported or not-evaluated, a present ceiling_base is diagnostic carrier metadata only and is ignored by the Core algorithm."
- [Q9] "A PROV aggregate is valid only when qualified_base = execution and independence_validation = not-applicable.  An IV aggregate is valid only when qualified_base is one of the four content bases and independence_validation is supported, unsupported, or not-evaluated.  PROV on another base, IV with not-applicable, or another recognized but disallowed qualifier-field combination produces E_PROFILE_MAPPING_INVALID."
- [Q10] "A valid qualifier contributes support only when its exact qualified base is independently in B."
- [Q11] "counter_evidence is an entry set, not a single strongest status.  When no counter-evidence was supplied it contains exactly one not-supplied entry with empty affected claims, basis references, reasons, and limitations.  Otherwise not-supplied is absent and every entry names at least one admissible affected claim or all-admissible-claims."
- [Q12] "Every member of a counter entry's reasons set MUST be a token registered in the substantive category by a registry applicable to the mapping profile and MUST apply to that entry's affected claims. ... A non-Core token resolves uniquely, including category, through exactly one immutable registry revision identified by an applied profile_identifier; absence, ambiguity, or category disagreement produces E_PROFILE_MAPPING_INVALID.  Entry reasons are explanatory and do not change the entry status or block a claim by themselves."
- [Q13] "Likewise, every token in reasons[] on a boundary, base, or qualifier finding MUST be registered in the substantive category and apply to that finding."
- [Q14] "Every member of fatal_conditions MUST be a token registered in the fatal category by the Core registry or a registry applicable to the mapping profile. ... An absent, ambiguous, unregistered, or miscategorized member is a profile-mapping failure; the appraiser returns E_PROFILE_MAPPING_INVALID instead of treating that member as fatal."
- [Q15] "The optional current_scope_capability is present only when the entry represents the current appraiser's unperformed authenticity or composition assessment; it names exactly that initial capability.  The token registration also identifies that same capability: E_COMPOSITION_NOT_EVALUATED is initially registered for composition, while authenticity requires an exact profile token registered for authenticity assessment. ... A marker-token capability mismatch produces E_PROFILE_MAPPING_INVALID.  Absence of the marker means that the entry is inherited or otherwise diagnostic and does not determine a current capability status."
- [Q16] "A missing member, a wrong logical type, or a malformed atom or set member produces E_MALFORMED_NORMALIZED_INPUT at the structural check.  For a structurally valid entry, an empty affected-claim set, an absent, ambiguous, unregistered, or non-evaluation-gap token binding, an incorrect target or evaluation-context scope, a disallowed or mismatched current-scope marker, or an unbound profile-scoped atom produces E_PROFILE_MAPPING_INVALID at the cross-field check.  A valid entry is unrelated to this appraisal and is not projected only when its affected claims include none of the asserted claim, a member of SupportedClaims, or all-admissible-claims."

Section 6.1
- [Q17] "Content bases, qualifiers, statuses, grounding classes, verdicts, and the initial evaluation-scope names are closed enumerations whose members compare by the exact names defined in this document."
- [Q18] "Two aggregate entries with the same aggregate key are the duplicate condition in this section, even if every field is byte-identical."
- [Q19] "A recorder relation is the logical record shown in Section 6.  Its profile_identifier binds the immutable relation vocabulary; relation_token names one member of that vocabulary; subject_ref and object_ref are profile-scoped atoms ... Recorder relations are descriptive carried facts.  Their presence does not create a content-base or qualifier finding."

Section 6.2 (ordered checks)
- [Q20] "1.  If the outer value is not an input record, or semantics_version is absent or is not a text atom, Core returns E_MALFORMED_NORMALIZED_INPUT."
- [Q21] "2.  If that readable value is not wexp-core-2, Core returns E_UNSUPPORTED_SEMANTICS_VERSION without applying the version-specific member rules below."
- [Q22] "3.  For wexp-core-2, a missing required member, unknown member, wrong logical type, unknown closed-enum value, or malformed set, entry, claim, token, or recorder relation returns E_MALFORMED_NORMALIZED_INPUT."
- [Q23] "4.  A well-typed wexp-core-2 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID.  Cross-field invariants include aggregate cardinality and keys, exact target and context scope, the counter-evidence sentinel, qualifier combinations, conditional ceiling_base, evaluation-scope consistency and extension-key binding, and profile or registry identity and token category."
- [Q24] "5.  If the structurally usable input has a non-empty valid fatal_conditions set, Core returns that complete set through the fixed rejection projection."
- [Q25] "6.  Otherwise an inadmissible asserted claim returns E_CLAIM_OUT_OF_DOMAIN."
- [Q26] "E_MALFORMED_NORMALIZED_INPUT, E_UNSUPPORTED_SEMANTICS_VERSION, E_PROFILE_MAPPING_INVALID, and E_CLAIM_OUT_OF_DOMAIN are derived only by the ordered Core checks and are invalid as supplied members of fatal_conditions.  The Core-defined supplied fatal members are E_UNKNOWN_CRITICAL_SEMANTIC, E_INTEGRITY_INVALID, E_BINDING_MISMATCH, and E_CHAIN_DESCRIPTION_INVALID. ... If any supplied member is appraiser-derived, unbound, ambiguous, or in the wrong category, the cross-field check returns only E_PROFILE_MAPPING_INVALID."
- [Q27] "Multiple valid supplied fatal members are returned together as a set.  No later check or diagnostic is added after any earlier rejection branch wins.  The fixed projection in Section 8.4 is the only Core result for every rejection branch."

Section 7
- [Q28] "An accept or downgrade result MUST preserve the boundary grounding status and its limitations."
- [Q29] "When status = not-evaluated, no base is added and the appraiser records E_BOUNDARY_NOT_EVALUATED.  When status = unsupported, no base is added and it records E_BOUNDARY_NOT_SUPPORTED.  Only status = supported with target_binding = supported and matching target and context makes ceiling_base usable."

Section 8.1
- [Q30] "A base b is in B if and only if all of the following hold: 1. the unique aggregate base finding for b has supported target binding and supported semantic validation; 2. the finding names the same target and evaluation context as the appraisal input; 3. the boundary finding is supported, target-bound, and scoped to that same target and context; and 4. the accepted Boundary Ceiling is at least b."
- [Q31] "PROV only when b is execution and a PROV finding for execution has target_binding = supported and semantic_validation = supported for the exact target and evaluation context; and IV only when an IV finding for b has target_binding = supported, semantic_validation = supported, and independence_validation = supported for the exact target and evaluation context."
- [Q32] "SupportedClaims = { (b, A) | b is in B, A is a subset of Q(b), and (PROV in A implies b == execution) }"
- [Q33] "MaximalSupportedClaims is the set of members of SupportedClaims that are not structurally dominated by another member under Section 4.5."
- [Q34] "For every member of SupportedClaims, the appraiser also produces a support entry containing the exact claim, the union of basis references used for its base, boundary, and qualifiers, and the limitations attached to those same premises.  Limitations from failed or unrelated findings are not attached to that support entry, but remain available as evaluation diagnostics where applicable."
- [Q35] "The result's inherited_limitations is the set union of the input's inherited limitations; limitations from each counter-evidence or profile-gap entry whose affected claims include the asserted claim, a member of SupportedClaims, or all-admissible-claims; boundary limitations; every support-entry limitation; and limitations attached to findings that determine a reason or gap for the asserted claim.  Limitations on unrelated failed findings are excluded."

Section 8.2
- [Q36] "accept  The asserted claim is an exact member of SupportedClaims and counter-evidence does not block that exact claim."  "downgrade  The input is safely interpretable and the asserted claim is admissible, but it is not exactly supported, or counter-evidence blocks acceptance."
- [Q37] "Counter-evidence blocks a claim when at least one entry has status not-evaluated, unresolved-material, or defeating and that entry's affected_claims contains the claim or all-admissible-claims. not-supplied and resolved-no-defeat entries do not block by themselves.  The reason token is derived from each applicable blocking entry; a defeating entry for one claim never changes the status of a separate not-evaluated entry for another claim."

Section 8.3
- [Q38] "For each maximal supported claim, the appraisal reports a pair {supported_claim, relation}, where relation is one of equal, support-below-claim, support-above-claim, or incomparable.  If no claim is supported, the relation array is empty."
- [Q39] "The separate Boolean asserted_claim_supported reports exact membership in SupportedClaims.  It remains true when the exact asserted claim is supported but a structurally deeper alternative causes the asserted claim not to appear in MaximalSupportedClaims."

Section 8.4
- [Q40] "for every boundary, base, or qualifier finding that is the asserted role or an exact premise of a SupportEntry: add its registered substantive reasons to reasons"
- [Q41] "for every profile gap entry whose affected claims include the asserted claim, a member of SupportedClaims, or all-admissible-claims: add that exact entry to GapEntries"
- [Q42] "for c in applicable_counter_entries(input.counter_evidence, input.asserted_claim): reasons = reasons union c.reasons; if c.status == not-evaluated: add gap_entry(E_COUNTER_EVIDENCE_NOT_EVALUATED, input.target, input.evaluation_context.id, c.affected_claims, c.basis_refs, c.limitations) to GapEntries; if c.status == unresolved-material: add E_COUNTER_EVIDENCE_UNRESOLVED to reasons; if c.status == defeating: add E_COUNTER_EVIDENCE_DEFEATING to reasons"
- [Q43] "rejected_result(fatal_tokens): return Appraisal with verdict = reject, semantics_version = "wexp-core-2", fatal_reasons = fatal_tokens, substantive_reasons = {}, evaluation_gaps = {}, evaluation_gap_entries = {}, supported_claims = {}, maximal_supported_claims = {}, support_entries = {}, support_relations = {}, asserted_claim_supported = false, boundary_ceiling = unavailable, boundary_grounding = unavailable, target = unavailable, asserted_claim = unavailable, recorder_relations = unavailable, counter_evidence = unavailable, inherited_limitations = unavailable, evaluation_context = unavailable, evaluation_scope = unavailable"
- [Q44] "applicable_counter_entries returns only entries whose affected claims include the asserted claim or all-admissible-claims and whose status blocks that claim under the same predicate; it preserves per-entry scope."
- [Q45] "Every Core-derived finding gap entry has the row's token, the input target and evaluation-context identifier, affected_claims={input.asserted_claim}, and the basis-reference and limitation sets of the aggregate that made the row true.  If the row concerns an absent aggregate, those two sets are empty.  A counter-derived gap entry instead retains that counter entry's exact affected claims, basis references, and limitations."

Section 8.5
- [Q46] "For an accept or downgrade result, boundary_ceiling is the accepted ceiling only when the boundary finding, its target binding, target, and context all pass; otherwise it is unavailable. boundary_grounding preserves the input grounding even when the boundary is unsupported."
- [Q47] "counter_evidence preserves every status, affected-claim set, basis-reference set, reason set, and limitation set from the normalized input without cross-claim status or reason collapse."

Section 8.6
- [Q48] "An absent aggregate triggers only its absence row; status rows require that aggregate to be present.  A present non-passing aggregate MUST NOT be reported as missing evidence merely because it contributes no supported claim. ... A boundary-exceeded row requires a usable boundary and a present asserted-base aggregate whose base is deeper than the ceiling.  Consequently a present supported base excluded by the ceiling produces E_BASE_EXCEEDS_BOUNDARY, not E_MISSING_REQUIRED_EVIDENCE."
- [Q49] matrix rows (verbatim): "E_BOUNDARY_NOT_SUPPORTED (substantive)  Boundary status = unsupported; source: boundary finding." / "E_BASE_EXCEEDS_BOUNDARY (substantive)  Usable boundary with asserted base deeper than its ceiling; sources: boundary and asserted-base findings." / "E_MISSING_REQUIRED_EVIDENCE (substantive)  Asserted-base aggregate absent; source: none." / "E_EXACT_CLAIM_NOT_SUPPORTED (substantive)  Asserted-base semantic_validation = unsupported; source: asserted-base finding." / "E_MISSING_REQUIRED_EVIDENCE (substantive)  Asserted PROV aggregate absent; source: none." / "E_PROV_NOT_EVALUATED (gap)  Asserted PROV target-binding or semantic assessment not-evaluated; source: PROV finding." / "E_MISSING_REQUIRED_EVIDENCE (substantive)  Asserted IV aggregate absent; source: none." / "E_IV_NOT_EVALUATED (gap)  Asserted IV target-binding, semantic, or independence assessment not-evaluated; source: IV finding." / "E_INDEPENDENCE_NOT_ESTABLISHED (substantive)  Asserted IV independence_validation = unsupported; source: IV finding." / "E_COUNTER_EVIDENCE_NOT_EVALUATED (gap)  Applicable counter entry status = not-evaluated; source: that counter entry." / "E_COUNTER_EVIDENCE_UNRESOLVED (substantive)  Applicable counter entry status = unresolved-material; source: that counter entry." / "E_COUNTER_EVIDENCE_DEFEATING (substantive)  Applicable counter entry status = defeating; source: that counter entry."
- [Q50] "For every blocking counter-evidence entry applicable to the asserted claim, the appraiser MUST add every token in that entry's reasons set to substantive_reasons, in addition to the Core token determined by the entry status.  Reasons on entries that do not affect the asserted claim do not enter that projection but remain preserved in the result entry."
- [Q51] "A finding reason is projected only from the boundary when it determines the asserted claim or a reported support entry, from an asserted-base or asserted-qualifier finding, or from a finding that is an exact premise of a reported support entry.  E_EVIDENCE_COVERAGE_MISMATCH, E_CHAIN_UNBOUND, E_COMPOSITION_WARRANT_MISSING, and E_SHARED_VERIFICATION_ROOT use this profile-reason path on a correctly scoped exact-role aggregate.  Profile-supplied gap entries, including E_COMPOSITION_NOT_EVALUATED, are included only when their affected claims contain the asserted claim, a member of SupportedClaims, or all-admissible-claims.  A supplied profile gap does not by itself block acceptance."

Section 12
- [Q52] "evaluation_scope is an unordered map from capability names to exactly one of evaluated or not-evaluated." ... "Every initial name MUST appear exactly once.  An extension key is the logical pair (profile_identifier, local_name) of two non-empty text atoms, where the immutable applied profile identifier occurs in evaluation_context.profile_identifiers and local_name names an extension in that revision.  The pair is its identity.  Core ignores an extension status for support and gap derivation but preserves the exact pair and status in the result.  A malformed pair or a missing, empty, or non-text atom produces E_MALFORMED_NORMALIZED_INPUT at the structural check in Section 6.2.  For a structurally valid key, an unbound or ambiguous profile or local-name binding, or a duplicate key in the scope map, produces E_PROFILE_MAPPING_INVALID at the following cross-field check."
- [Q53] "For counter-evidence, evaluated means the current capability-level procedure completed its assessment of the supplied entry set ... not-evaluated means that procedure was not completed. ... An evaluated capability can therefore contain a not-evaluated entry.  Core MUST NOT replace an entry status with the capability value.  The capability value alone MUST NOT create an ingress rejection, substantive finding, or evaluation gap for counter-evidence.  The entry's status and affected claims govern its effect under Section 8.6."
- [Q54] "For each base-support capability and for provenance-support, if the corresponding aggregate is present and the capability is not-evaluated, at least one governed status field in that aggregate MUST be not-evaluated, independently of whether the role is asserted.  A present wholly assessed single-role aggregate paired with not-evaluated violates the cross-field contract and produces E_PROFILE_MAPPING_INVALID.  An absent unasserted aggregate can represent an unexercised capability without creating a claim-specific gap."
- [Q55] "target-binding and independent-verification are shared across exact roles.  Their not-evaluated summary does not replace a passing assessment for a different exact role. ... A claim-required IV aggregate is present when the shared IV capability is not-evaluated, but its passing statuses need not be changed merely because another role was not assessed.  Claim-specific gaps are derived from the exact required aggregate, not from the shared summary alone."
- [Q56] "The external authenticity and composition capabilities use a fully syntactic rule: their scope value is not-evaluated if and only if at least one profile-gap entry names that capability in current_scope_capability, and is evaluated if and only if no entry names it."
- [Q57] "The governed status fields are: every finding's target_binding for target-binding; boundary status, binding, and grounding for boundary-grounding; the corresponding base aggregate's binding and semantic status for each base-support capability; PROV binding and semantic status for provenance-support; IV binding, semantic, and independence status for independent-verification. ... A scope value of evaluated with a governed not-evaluated status, a claim-required finding-backed not-evaluated capability without its aggregate, a current-scope marker whose capability is not not-evaluated, or an external capability value without the required marker presence or absence violates the cross-field contract and produces E_PROFILE_MAPPING_INVALID."
- [Q58] "A role-specific Core gap entry is emitted only by the claim-required matrix when its aggregate is required by the asserted claim.  A valid profile-gap entry is projected under its affected-claim rule.  Otherwise the scope map alone records the unexercised capability and does not become a reason, gap, or substantive finding."

Section 13
- [Q59] "Common input values are: semantics_version=wexp-core-2; target T; evaluation-context identifier C; evaluation time 2026-10-12T00:00:00Z; trust-configuration atom core02-fixture-trust-1, which accepts attributed boundary grounding; the singleton applied-profile set containing the immutable fixture identity defined below; a supported, target-bound, attributed boundary finding for T and C with basis bd and the stated ceiling; empty recorder relations, profile evaluation gaps, inherited limitations, and fatal conditions; counter-evidence consisting of one entry whose status is not-supplied and whose affected-claim, basis-reference, reason, and limitation sets are empty; and every initial evaluation-scope capability set to evaluated."
- [Q60] "For each member of S, support_entries contains exactly one entry whose basis-reference set is the union of bd, its base finding's basis references, and any qualifier findings' basis references; its limitations are the union of those premises.  support_relations contains the displayed relation for each member of M. gaps={} also means evaluation_gap_entries={}. For accept and downgrade rows, fields not varied by a row equal the common input values and carry through to the output.  A reject row instead uses the complete fixed projection in Section 8.4."
- [Q61] "P_COUNTER_FAIL is registered in the substantive category, is applicable to C15's counter entry ... The profile defines no recorder-relation tokens or scope-extension names.  Opaque fixture atoms compare by exact Unicode scalar text; a displayed basis reference or limitation denotes the ordered pair of this profile identity and its displayed local name.  No URI, case, or Unicode normalization is implicit."

Section 15
- [Q62] "A marker naming a different capability or a token without such a binding produces E_PROFILE_MAPPING_INVALID."
- [Q63] "In particular, a reason carried by a finding or a profile-supplied evaluation gap can coexist with accept; its presence does not negate a passing exact predicate."

## 0.1 Shared derivation blocks

- **[REJECT]** When an ordered check fails, the result is exactly [Q43]: verdict reject, semantics_version
  wexp-core-2, fatal_reasons = the token(s), the four derived sets and the entry/relation sets empty,
  asserted_claim_supported false, and the ten input-derived members `unavailable` (encoded `null`). [Q27]:
  nothing is added after the winning branch.
- **[CARRY]** For accept/downgrade, `target`, `asserted_claim`, `recorder_relations`, `counter_evidence`
  [Q47], `evaluation_context`, `evaluation_scope` [Q52 "preserves the exact pair and status"] are the input
  values; `boundary_ceiling`/`boundary_grounding` follow [Q46]; `semantics_version` = wexp-core-2.
- **[STD-E]** "standard execution accept": asserted E; execution finding supported/supported for T,C;
  boundary supported, target-bound, attributed, ceiling execution, basis bd. By [Q30] B={E}; no qualifier
  findings so Q(E)={} and by [Q32] S={E}; M={E} [Q33]; A=true [Q39]; relation E:equal [Q38]; support entry
  E with basis {bd,E}, limitations {} [Q34]; no matrix row true (asserted-base aggregate present and
  passing, boundary usable, ceiling not exceeded) so Core reasons/gaps are empty; counter entry
  not-supplied does not block [Q37]; verdict accept [Q36]; boundary_ceiling execution, grounding attributed [Q46].
- **[CROSS-FIELD-OK]** Unless stated, each accept/downgrade input was checked against [Q6]-[Q16], [Q52]-[Q57]
  (scope T/C everywhere, single aggregates per key, sentinel rule, qualifier combinations, conditional
  ceiling_base, 12 initial names once each, governed-field consistency, marker rules, token binding under
  the applied catalog) and none fails.

---

## C01-C16 (Section 13 normative rows, derived from Table 2 and [Q59]-[Q61])

### C01
(a) Assert I; intent finding supported; ceiling intent.
(b) Table 2 row C01: "S=M={I}; A=true; relations={I:equal}; accept; fatal/reasons/gaps={}." [Q30]-[Q34], [Q60].
(c) B={I} (intent finding supported/supported, boundary usable, intent <= intent). Q(I)={}. S=M={I}; A=true;
relation equal; support entry I basis {bd,I}, limitations {}; reasons/gaps {}; verdict accept; ceiling intent,
grounding attributed; inherited_limitations {} (nothing in the [Q35] union). [CARRY].
(d) none. (Matches FORMAT-REFERENCE-C01.json exactly.)

### C02
(a) Assert I; only execution finding supported; ceiling execution.
(b) Row C02: "S=M={E}; A=false; relations={E:support-above-claim}; downgrade; reasons={E_MISSING_REQUIRED_EVIDENCE}; fatal/gaps={}." [Q30], [Q49] "Asserted-base aggregate absent".
(c) B={E}; S=M={E}; A=false; E is structurally above I [Q4] so relation support-above-claim; support entry E
basis {bd,E}; the intent aggregate is absent so MISSING; downgrade [Q36]; ceiling execution.
(d) none.

### C03
(a) Assert E+V; execution and PROV(execution) supported; no IV finding; ceiling execution.
(b) Row C03: "S={E,E+P}; M={E+P}; A=false; relations={E+P:incomparable}; downgrade; reasons={E_MISSING_REQUIRED_EVIDENCE}". [Q31], [Q32], [Q4], [Q49] "Asserted IV aggregate absent".
(c) B={E}; Q(E)={PROV}; S={E, E+P}; M={E+P}; E+P and E+V incomparable [Q4]; entries E {bd,E}, E+P {bd,E,P(E)};
reasons MISSING (asserted IV aggregate absent); downgrade.
(d) none.

### C04
(a) Assert E+P; execution and IV(execution) supported; no PROV finding; ceiling execution.
(b) Row C04: "S={E,E+V}; M={E+V}; A=false; relations={E+V:incomparable}; downgrade; reasons={E_MISSING_REQUIRED_EVIDENCE}". [Q31], [Q49] "Asserted PROV aggregate absent".
(c) B={E}; Q(E)={IV}; S={E,E+V}; M={E+V}; entries E {bd,E}, E+V {bd,E,V(E)}; reasons MISSING; downgrade.
(d) none.

### C05
(a) Assert N+V; invocation and IV(invocation) supported; ceiling invocation.
(b) Row C05: "S={N,N+V}; M={N+V}; A=true; relations={N+V:equal}; accept; fatal/reasons/gaps={}." [Q31].
(c) B={N}; Q(N)={IV}; S={N,N+V}; M={N+V}; A=true; entries N {bd,N}, N+V {bd,N,V(N)}; accept; ceiling invocation.
(d) none.

### C06
(a) Assert E+V; invocation, IV(invocation), execution supported; no IV(execution); ceiling execution.
(b) Row C06: "S={N,N+V,E}; M={N+V,E}; A=false; relations={N+V:support-below-claim,E:support-below-claim}; downgrade; reasons={E_MISSING_REQUIRED_EVIDENCE}". [Q10] (IV(N) does not qualify E).
(c) B={N,E}; Q(N)={IV}; Q(E)={}; S={N,N+V,E}; M={N+V,E} (incomparable with each other [Q4]); both below E+V;
entries N {bd,N}, N+V {bd,N,V(N)}, E {bd,E}; reasons MISSING (asserted IV(execution) absent); downgrade.
(d) none.

### C07
(a) Assert E; execution supported; ceiling invocation.
(b) Row C07: "S=M={}; A=false; relations={}; downgrade; reasons={E_BASE_EXCEEDS_BOUNDARY}". [Q30] item 4; [Q48]; [Q49].
(c) execution > invocation so E not in B; S=M={}; relations {} [Q38]; boundary usable and asserted-base
aggregate present and deeper than ceiling -> E_BASE_EXCEEDS_BOUNDARY (not MISSING [Q48]); downgrade;
boundary_ceiling invocation [Q46]; grounding attributed; no limitations.
(d) none.

### C08
(a) Assert O; no base findings; ceiling observation.
(b) Row C08: "S=M={}; A=false; relations={}; downgrade; reasons={E_MISSING_REQUIRED_EVIDENCE}".
(c) B={}; MISSING (asserted-base aggregate absent); downgrade; ceiling observation; grounding attributed.
(d) none.

### C09
(a) Assert inadmissible (intent, {PROV}); no base findings; ceiling execution.
(b) Row C09 (reject, fixed projection). [Q1]-[Q3], [Q25], [Q43]; Section 13: "For C09, the otherwise unstated boundary ceiling is execution; the fixed rejection projection makes this input field unavailable in the result."
(c) Steps 1-5 pass (well-formed claim [Q2], no cross-field defect, empty fatal set); step 6 -> E_CLAIM_OUT_OF_DOMAIN. [REJECT].
(d) none.

### C10
(a) Assert I; intent supported; ceiling intent; one counter entry unresolved-material affecting I, empty reasons.
(b) Row C10: "S=M={I}; A=true; relations={I:equal}; downgrade; reasons={E_COUNTER_EVIDENCE_UNRESOLVED}; fatal/gaps={}." [Q36], [Q37], [Q42].
(c) Support as C01 (S=M={I}, A=true, entry I {bd,I}); the entry blocks I [Q37] -> downgrade; counter loop adds
E_COUNTER_EVIDENCE_UNRESOLVED; its reasons set is empty, so nothing else; gaps {}; counter_evidence carried
[Q47]; inherited_limitations {} (entry limitations empty).
(d) none.

### C11
(a) Chain target T; assert E; composition profile emitted execution finding with basis {s1,s2,adj,w}; ceiling execution.
(b) Row C11: "S=M={E}; A=true; relations={E:equal}; accept; fatal/reasons/gaps={}. The execution support entry basis is {bd,s1,s2,adj,w}." Section 9: "The C11 and C12 fixtures ... test Core support construction and limitation carry-through".
(c) [STD-E] with support-entry basis {bd,s1,s2,adj,w} [Q34].
(d) none.

### C12
(a) As C11; boundary and the execution finding carry L-boundary; independent-verification = not-evaluated; no warrant resolves either.
(b) Row C12: "S=M={E}; A=true; relations={E:equal}; accept; gaps={}; inherited_limitations={L-boundary}; fatal/reasons={}. The support entry also carries L-boundary.  The unexercised IV capability remains visible in evaluation_scope but creates no claim-unrelated gap token." [Q34], [Q35], [Q55], [Q57] (IV not claim-required, so "claim-required finding-backed not-evaluated capability without its aggregate" is not triggered), [Q58].
(c) [STD-E]; support entry E basis {bd,s1,s2,adj,w}, limitations {L-boundary} (boundary and base premises);
inherited_limitations {L-boundary}; evaluation_scope carried with independent-verification not-evaluated; no gap.
(d) none.

### C13
(a) Assert E; execution supported; ceiling execution; profile gap entry (T,C) token E_IV_NOT_EVALUATED, affects E, basis u1, limitation L-upstream, no marker.
(b) Row C13: "accept; gaps={E_IV_NOT_EVALUATED}; fatal/reasons={}; inherited_limitations={L-upstream}. evaluation_gap_entries contains exactly the supplied entry." [Q41], [Q51] "A supplied profile gap does not by itself block acceptance", [Q35].
(c) [STD-E]; the entry affects E (asserted) so it is copied exactly into evaluation_gap_entries and its token
projected; inherited_limitations {L-upstream}; verdict accept.
(d) none.

### C14
(a) Assert E; execution supported; counter entries: defeating for I; not-evaluated for E; both empty reasons.
(b) Row C14: "S=M={E}; A=true; relations={E:equal}; downgrade; reasons={}; gaps={E_COUNTER_EVIDENCE_NOT_EVALUATED}; fatal={}. The gap entry affects only E; both counter entries are preserved and no E_COUNTER_EVIDENCE_DEFEATING reason is emitted for E." [Q37], [Q42], [Q44], [Q45].
(c) Support as [STD-E]; the not-evaluated entry for E blocks -> downgrade; gap entry
{E_COUNTER_EVIDENCE_NOT_EVALUATED, T, C, affected [E], basis [], limitations []}; the defeating entry affects
only I, which is neither asserted nor in S, so it is not applicable; counter_evidence carried with both entries.
(d) none.

### C15
(a) Assert E; execution supported; counter entry unresolved-material affects E, reason P_COUNTER_FAIL, basis p1, no limitations.
(b) Row C15: "downgrade; reasons={E_COUNTER_EVIDENCE_UNRESOLVED, P_COUNTER_FAIL}; gaps={}; fatal={}. The copied counter entry retains its scoped reason." [Q12], [Q50], [Q61] (P_COUNTER_FAIL registered substantive under F1).
(c) Support as [STD-E]; blocking entry -> downgrade; reasons = Core token + entry reasons; counter_evidence carried.
(d) none.

### C16
(a) Assert E; execution supported; profile gap E_IV_NOT_EVALUATED affects only N+V, basis u2, limitation L-unrelated.
(b) Row C16: "accept; fatal/reasons/gaps={}; inherited_limitations={}. The unrelated profile gap and its limitation are not projected." [Q16] last sentence, [Q41], [Q35].
(c) [STD-E]; N+V is not asserted, not in S={E}, not all-admissible-claims -> entry not projected; no limitation inherited.
(d) none.

---

## R01-R48

### R01
(a) C14's two counter entries plus evaluation_scope counter-evidence = not-evaluated.
(b) [Q53] "The capability value alone MUST NOT create an ingress rejection, substantive finding, or evaluation gap for counter-evidence."; [Q37], [Q42], [Q45].
(c) [CROSS-FIELD-OK] (counter-entry statuses are excluded from the governed-field test [Q57]). Result as C14:
S=M={E}, A=true, downgrade, gaps {E_COUNTER_EVIDENCE_NOT_EVALUATED} with entry affecting [E], basis [], limitations [];
reasons {}; evaluation_scope carried with counter-evidence not-evaluated.
(d) none.

### R02
(a) Assert I; intent AND execution findings wholly supported; execution-support = not-evaluated.
(b) [Q54] "A present wholly assessed single-role aggregate paired with not-evaluated violates the cross-field contract and produces E_PROFILE_MAPPING_INVALID."; [Q23] step 4.
(c) Steps 1-3 pass; step 4 fails -> PMI. [REJECT].
(d) none.

### R03
(a) Assert E; PROV(execution) wholly supported; provenance-support = not-evaluated.
(b) [Q54] (rule applies "for provenance-support" too).
(c) PMI. [REJECT].
(d) none.

### R04
(a) Assert I; intent supported; execution finding semantic_validation = not-evaluated; execution-support = not-evaluated.
(b) [Q54] (execution aggregate has a governed not-evaluated field: consistent); [Q57] (no "evaluated" capability has a governed not-evaluated status); [Q30]; [Q58] "A role-specific Core gap entry is emitted only by the claim-required matrix when its aggregate is required by the asserted claim."
(c) [CROSS-FIELD-OK]. B={I} (execution fails item 1). S=M={I}; A=true; relation equal; entry I {bd,I}; the
execution aggregate is not claim-required so no E_BASE_NOT_EVALUATED; reasons/gaps {}; accept; ceiling
execution; scope carried.
(d) none.

### R05
(a) Assert N+V; invocation and IV(invocation) supported; extra IV(execution) with semantic not-evaluated; independent-verification = not-evaluated; ceiling execution.
(b) [Q55] shared-role rule ("A claim-required IV aggregate is present when the shared IV capability is not-evaluated, but its passing statuses need not be changed merely because another role was not assessed."); [Q10]; [Q31].
(c) [CROSS-FIELD-OK]: IV(execution) carries the governed not-evaluated status that justifies the summary; the
IV(invocation) aggregate keeps its passing statuses. B={N} (no execution base finding). Q(N)={IV} ->
S={N,N+V}; M={N+V}; A=true; relation equal; entries N {bd,N}, N+V {bd,N,V(N)}. IV(execution) contributes
nothing (E not in B [Q10]) and is not the asserted role, so no gap. accept; ceiling execution; scope carried.
(d) none.

### R06
(a) Assert N; invocation supported; execution finding target_binding = not-evaluated; target-binding and execution-support = not-evaluated.
(b) [Q54], [Q55] ("Their not-evaluated summary does not replace a passing assessment for a different exact role"), [Q57] (target_binding governs both target-binding and execution-support; both are not-evaluated), [Q30], [Q58].
(c) [CROSS-FIELD-OK]. B={N}; S=M={N}; A=true; relation equal; entry N {bd,N}; execution aggregate not claim-required -> no gap; accept; ceiling execution; scope carried.
(d) none.

### R07
(a) Assert E+V; execution supported; IV(execution) semantic_validation = not-evaluated (binding and independence supported); independent-verification = not-evaluated.
(b) [Q31] (IV requires semantic supported); [Q49] "E_IV_NOT_EVALUATED (gap)  Asserted IV target-binding, semantic, or independence assessment not-evaluated; source: IV finding."; [Q48] present non-passing aggregate is not "missing"; [Q45].
(c) [CROSS-FIELD-OK]. B={E}; Q(E)={}; S=M={E}; A=false; relation support-below-claim; entry E {bd,E};
gap entry {E_IV_NOT_EVALUATED, T, C, affected [E+V], basis [V(E)], limitations []}; reasons {}; downgrade.
(d) none.

### R08
(a) profile_identifiers = [] ; findings carry no basis refs; counter entry unresolved-material with reason P_COUNTER_FAIL.
(b) [Q12] "A non-Core token resolves uniquely, including category, through exactly one immutable registry revision identified by an applied profile_identifier; absence ... produces E_PROFILE_MAPPING_INVALID."
(c) An empty profile set is a well-typed set (no structural defect). No applied profile can resolve P_COUNTER_FAIL -> PMI. [REJECT].
(d) none.

### R09
(a) Per-case catalog is empty although F1 is listed in profile_identifiers; counter reason P_COUNTER_FAIL.
(b) [Q12]; BRIEF: a profile identity absent from the applied catalog cannot resolve anything.
(c) Token unresolvable -> PMI. [REJECT].
(d) none.

### R10
(a) Catalog F1 registers no tokens; counter reason P_COUNTER_FAIL.
(b) [Q12] "absence ... produces E_PROFILE_MAPPING_INVALID".
(c) PMI. [REJECT].
(d) none.

### R11
(a) Catalog F1 registers P_COUNTER_FAIL in category evaluation-gap; used as a counter reason.
(b) [Q12] "MUST be a token registered in the substantive category ... category disagreement produces E_PROFILE_MAPPING_INVALID."
(c) PMI. [REJECT].
(d) none.

### R12
(a) profile_identifiers = [F1, core02-review-ambiguous-profile-1]; both applied catalogs register P_COUNTER_FAIL (substantive); counter entry as C15.
(b) [Q12] "resolves uniquely ... through exactly one immutable registry revision identified by an applied profile_identifier; absence, ambiguity, or category disagreement produces E_PROFILE_MAPPING_INVALID."
(c) Primary: two applied revisions register the token -> not "exactly one" -> ambiguity -> PMI. [REJECT].
(d) AMBIGUITY (recorded): if concordant registrations are read as unambiguous because the category agrees,
the input is valid and the result equals C15 (downgrade; reasons {E_COUNTER_EVIDENCE_UNRESOLVED, P_COUNTER_FAIL})
with evaluation_context carrying both identifiers. Primary chosen because the text makes "exactly one"
revision the resolution rule and lists "ambiguity" separately from "category disagreement".

### R13
(a) Catalog contains both profiles, but only F1 is applied; counter entry as C15.
(b) [Q12] (resolution is "through ... an applied profile_identifier"; the second catalog entry is not applied).
(c) Unique resolution via F1 -> valid. Result = C15: S=M={E}; A=true; downgrade; reasons {E_COUNTER_EVIDENCE_UNRESOLVED, P_COUNTER_FAIL}; gaps {}.
(d) none.

### R14
(a) Assert E+V with supported execution and IV findings and a valid profile gap; boundary_finding.target = "foreign".
(b) [Q6]; [Q23] "exact target and context scope".
(c) PMI. [REJECT].
(d) none.

### R15
(a) As R14 but boundary_finding.evaluation_context_ref = "foreign".  (b) [Q6]. (c) PMI. [REJECT]. (d) none.

### R16
(a) As R14 but execution base finding target = "foreign".  (b) [Q6]. (c) PMI. [REJECT]. (d) none.

### R17
(a) As R14 but execution base finding evaluation_context_ref = "foreign".  (b) [Q6]. (c) PMI. [REJECT]. (d) none.

### R18
(a) As R14 but IV(execution) target = "foreign".  (b) [Q6]. (c) PMI. [REJECT]. (d) none.

### R19
(a) As R14 but IV(execution) evaluation_context_ref = "foreign".  (b) [Q6]. (c) PMI. [REJECT]. (d) none.

### R20
(a) As R14 but the profile gap entry target = "foreign".
(b) [Q16] "an incorrect target or evaluation-context scope ... produces E_PROFILE_MAPPING_INVALID at the cross-field check"; [Q6].
(c) PMI. [REJECT]. (d) none.

### R21
(a) As R14 but the profile gap entry evaluation_context_ref = "foreign".  (b) [Q16], [Q6]. (c) PMI. [REJECT]. (d) none.

### R22
(a) Two byte-identical execution base aggregates.
(b) [Q18] "Two aggregate entries with the same aggregate key are the duplicate condition in this section, even if every field is byte-identical."; [Q7] "Duplicate or conflicting aggregate findings are fatal and produce E_PROFILE_MAPPING_INVALID."; [Q23] "aggregate cardinality and keys".
(c) PMI. [REJECT].
(d) Considered reading "malformed set" (step 3, MALF) for a repeated set member; rejected because the text
explicitly classifies the aggregate-key duplicate as the Section 6 duplicate condition with PMI.

### R23
(a) Boundary status supported with ceiling_base absent.
(b) [Q8] "A boundary finding with status = supported MUST contain ceiling_base.  Its absence is a profile-mapping failure and produces E_PROFILE_MAPPING_INVALID."; [Q23] "conditional ceiling_base".
(c) PMI (ceiling_base is marked optional in the schema, so its absence is not a missing required member). [REJECT].
(d) none.

### R24
(a) counter_evidence = [] (no sentinel).
(b) [Q11] "When no counter-evidence was supplied it contains exactly one not-supplied entry"; [Q23] "the counter-evidence sentinel".
(c) Empty set is well-typed; sentinel invariant fails -> PMI. [REJECT].
(d) none.

### R25
(a) IV(execution) with independence_validation = not-applicable.
(b) [Q9] "IV with not-applicable ... produces E_PROFILE_MAPPING_INVALID."
(c) PMI. [REJECT]. (d) none.

### R26
(a) Boundary status supported with grounding = not-evaluated.
(b) [Q8] "grounding = not-evaluated is valid only with status = not-evaluated; either field paired differently produces E_PROFILE_MAPPING_INVALID."
(c) PMI. [REJECT]. (d) none.

### R27
(a) semantics_version = "wexp-core-1" and an extra member unknown_field.
(b) [Q21] step 2 "without applying the version-specific member rules below"; [Q5].
(c) Step 1 passes (text atom present); step 2 -> E_UNSUPPORTED_SEMANTICS_VERSION; the unknown member is never examined. [REJECT].
(d) none.

### R28
(a) semantics_version absent; fatal_conditions = [E_INTEGRITY_INVALID].
(b) [Q20] step 1; [Q5] "An absent or non-text value is malformed under Section 6.2."
(c) MALF; the supplied fatal set is never reached [Q27]. [REJECT].
(d) none.

### R29
(a) fatal_conditions = [E_INTEGRITY_INVALID, E_BINDING_MISMATCH]; asserted (intent,{PROV}); no base findings.
(b) [Q24] step 5 "returns that complete set"; [Q26] (both are Core-defined supplied fatal members); [Q27] "Multiple valid supplied fatal members are returned together as a set."; [Q2] (inadmissible claim is rejected at step 6 only "when no earlier rejection applies").
(c) Steps 1-4 pass; step 5 -> fatal_reasons {E_INTEGRITY_INVALID, E_BINDING_MISMATCH}. [REJECT].
(d) none.

### R30
(a) fatal_conditions = [E_INTEGRITY_INVALID] and execution finding target = "foreign".
(b) [Q6]; [Q23] step 4 precedes [Q24] step 5; [Q27].
(c) PMI only. [REJECT]. (d) none.

### R31
(a) fatal_conditions = [E_CLAIM_OUT_OF_DOMAIN] (an appraiser-derived token) with an otherwise standard accept input.
(b) [Q26] "If any supplied member is appraiser-derived, unbound, ambiguous, or in the wrong category, the cross-field check returns only E_PROFILE_MAPPING_INVALID."
(c) PMI. [REJECT]. (d) none.

### R32
(a) Boundary status unsupported (grounding attributed, target-bound, ceiling_base present); execution supported.
(b) [Q8] (ceiling_base ignored when unsupported); [Q29]; [Q49] E_BOUNDARY_NOT_SUPPORTED; [Q46]; [Q48] (exceeded row needs a usable boundary); [Q30] item 3.
(c) B={} -> S=M={}, A=false, relations {}; reasons {E_BOUNDARY_NOT_SUPPORTED}; asserted-base aggregate present and passing so no MISSING/EXACT rows; downgrade; boundary_ceiling unavailable (null); boundary_grounding attributed; inherited_limitations {}.
(d) none.

### R33
(a) Execution semantic_validation = unsupported.
(b) [Q49] "E_EXACT_CLAIM_NOT_SUPPORTED (substantive)  Asserted-base semantic_validation = unsupported".
(c) B={}; S=M={}; reasons {E_EXACT_CLAIM_NOT_SUPPORTED}; downgrade; ceiling execution (boundary usable); grounding attributed.
(d) none.

### R34
(a) Assert E+P; execution supported; PROV(execution) semantic not-evaluated (binding supported); provenance-support = not-evaluated.
(b) [Q54] (consistent); [Q31]; [Q49] "E_PROV_NOT_EVALUATED (gap)  Asserted PROV target-binding or semantic assessment not-evaluated"; [Q45].
(c) B={E}; Q(E)={}; S=M={E}; A=false; relation support-below-claim; entry E {bd,E}; gap entry {E_PROV_NOT_EVALUATED, T, C, affected [E+P], basis [P(E)], limitations []}; reasons {}; downgrade; scope carried.
(d) none.

### R35
(a) Assert E+V; IV(execution) independence_validation = unsupported.
(b) [Q31]; [Q49] "E_INDEPENDENCE_NOT_ESTABLISHED (substantive)  Asserted IV independence_validation = unsupported".
(c) B={E}; Q(E)={}; S=M={E}; A=false; relation support-below-claim; reasons {E_INDEPENDENCE_NOT_ESTABLISHED}; gaps {}; downgrade.
(d) none.

### R36
(a) Profile gap E_COMPOSITION_NOT_EVALUATED with marker composition affecting E, while evaluation_scope composition = evaluated.
(b) [Q56]; [Q57] "a current-scope marker whose capability is not not-evaluated ... violates the cross-field contract and produces E_PROFILE_MAPPING_INVALID."
(c) PMI. [REJECT]. (d) none.

### R37
(a) As R36 with composition = not-evaluated.
(b) [Q56] (consistent); [Q15] (token registered for composition, marker composition: match); [Q41]; [Q51] "A supplied profile gap does not by itself block acceptance."
(c) [STD-E]; entry affects E -> copied exactly (including current_scope_capability composition), gaps {E_COMPOSITION_NOT_EVALUATED}; inherited_limitations {} (entry has none); accept; scope carried.
(d) none.

### R38
(a) composition = not-evaluated with no marked profile gap.
(b) [Q56]; [Q57] "an external capability value without the required marker presence or absence violates the cross-field contract".
(c) PMI. [REJECT]. (d) none.

### R39
(a) Extension scope key ["unapplied-profile","x"]; profile_identifiers = [F1].
(b) [Q52] "For a structurally valid key, an unbound or ambiguous profile or local-name binding ... produces E_PROFILE_MAPPING_INVALID".
(c) Pair of two non-empty text atoms -> structurally valid; profile not applied -> PMI. [REJECT]. (d) none.

### R40
(a) Counter entry resolved-no-defeat affecting E, basis c; counter-evidence = not-evaluated.
(b) [Q53]; [Q37] "not-supplied and resolved-no-defeat entries do not block by themselves."
(c) [STD-E]; not blocking -> accept; reasons/gaps {}; counter_evidence carried; inherited_limitations {} (entry limitations empty); scope carried.
(d) none.

### R41
(a) Counter entry not-evaluated affecting E, basis c; counter-evidence = not-evaluated.
(b) [Q37], [Q42], [Q45] "A counter-derived gap entry instead retains that counter entry's exact affected claims, basis references, and limitations."
(c) S=M={E}; A=true; blocked -> downgrade; gap entry {E_COUNTER_EVIDENCE_NOT_EVALUATED, T, C, affected [E], basis [c], limitations []}; reasons {}.
(d) none.

### R42
(a) Counter entry unresolved-material affecting E, basis c; counter-evidence = not-evaluated.
(b) [Q37], [Q42]. (c) downgrade; reasons {E_COUNTER_EVIDENCE_UNRESOLVED}; gaps {}; S=M={E}; A=true. (d) none.

### R43
(a) Counter entry defeating affecting E, basis c; counter-evidence = not-evaluated.
(b) [Q37], [Q42]. (c) downgrade; reasons {E_COUNTER_EVIDENCE_DEFEATING}; gaps {}; S=M={E}; A=true. (d) none.

### R44
(a) Assert E; single counter entry defeating for I only (no sentinel, correctly).
(b) [Q44] (applicable only if affected claims include the asserted claim or all-admissible-claims); [Q11] (one entry naming an admissible claim satisfies the sentinel rule); [Q50] second sentence.
(c) [STD-E]; entry not applicable -> accept; reasons/gaps {}; counter_evidence carried; inherited_limitations {}.
(d) none.

### R45
(a) Assert E; execution and intent supported; boundary (supported) carries reason E_EVIDENCE_COVERAGE_MISMATCH and limitation L-scope.
(b) [Q13] (E_EVIDENCE_COVERAGE_MISMATCH is a Core substantive token); [Q40] "for every boundary, base, or qualifier finding that is the asserted role or an exact premise of a SupportEntry: add its registered substantive reasons"; [Q51]; [Q63] "a reason carried by a finding ... can coexist with accept"; [Q34]; [Q35] "boundary limitations".
(c) B={I,E}; S={I,E}; M={E}; A=true; relation E:equal; entries I {bd,I} limitations {L-scope}, E {bd,E} limitations {L-scope} (the boundary is a premise of both); substantive_reasons {E_EVIDENCE_COVERAGE_MISMATCH}; verdict accept (exact membership and no counter block); inherited_limitations {L-scope}.
(d) none (both [Q40] and [Q51] name the boundary-as-premise path).

### R46
(a) Assert E; the asserted execution finding carries E_EVIDENCE_COVERAGE_MISMATCH and L-scope (semantic supported); intent supported.
(b) [Q40] ("the asserted role"), [Q51] ("from an asserted-base ... finding"), [Q63], [Q34], [Q35].
(c) S={I,E}; M={E}; A=true; accept; entries I {bd,I} {}, E {bd,E} {L-scope}; reasons {E_EVIDENCE_COVERAGE_MISMATCH}; inherited_limitations {L-scope}.
(d) none.

### R47
(a) Assert E; the non-asserted but supported intent finding carries E_EVIDENCE_COVERAGE_MISMATCH and L-scope.
(b) [Q40] "or an exact premise of a SupportEntry"; [Q51] "or from a finding that is an exact premise of a reported support entry"; [Q35] "every support-entry limitation".
(c) S={I,E}; M={E}; A=true; accept; entries I {bd,I} {L-scope}, E {bd,E} {}; the intent finding is an exact premise of the reported I entry -> reasons {E_EVIDENCE_COVERAGE_MISMATCH}; inherited_limitations {L-scope}.
(d) AMBIGUITY (recorded): Section 8.6 opens with "Substantive reasons describe why evidence does not support
the asserted claim", which could be read to exclude reasons on a non-asserted finding; but the two
operative sentences [Q40]/[Q51] explicitly include premises of any reported support entry. Alternative:
substantive_reasons {} (inherited_limitations unchanged).

### R48
(a) Assert E; intent finding semantic unsupported with E_EVIDENCE_COVERAGE_MISMATCH and L-scope.
(b) [Q35] "Limitations on unrelated failed findings are excluded."; [Q40]/[Q51] (intent is neither the asserted role nor a premise); [Q58].
(c) B={E}; S=M={E}; accept; reasons {}; gaps {}; inherited_limitations {}; entry E {bd,E} {}.
(d) none.

---

## P01-P25

### P01
(a) evaluation_scope has a 13th entry whose capability is `[]`.
(b) [Q52] "An extension key is the logical pair (profile_identifier, local_name) of two non-empty text atoms ... A malformed pair or a missing, empty, or non-text atom produces E_MALFORMED_NORMALIZED_INPUT at the structural check".
(c) Not a pair -> MALF at step 3. [REJECT]. (d) none.

### P02
(a) Extension key is a one-element array.  (b) [Q52]. (c) Malformed pair -> MALF. [REJECT]. (d) none.

### P03
(a) Extension key is a three-element array.  (b) [Q52]. (c) Malformed pair -> MALF. [REJECT]. (d) none.

### P04
(a) Extension key [X1, ""] (empty local name).  (b) [Q52] "missing, empty, or non-text atom". (c) MALF. [REJECT]. (d) none.

### P05
(a) Extension key ["", "audit-window"] (empty profile atom).  (b) [Q52]. (c) MALF. [REJECT]. (d) none.

### P06
(a) Extension key [X1, 0] (integer local name).  (b) [Q52] "non-text atom". (c) MALF. [REJECT]. (d) none.

### P07
(a) Extension key [X1, null].  (b) [Q52] "missing ... or non-text atom". (c) MALF. [REJECT]. (d) none.

### P08
(a) Extension key [X1, "\ud800"] (lone surrogate); profile_identifiers = [F1]; default catalog.
(b) [Q52]; [Q61] "Opaque fixture atoms compare by exact Unicode scalar text"; [Q16] "a malformed atom ... produces E_MALFORMED_NORMALIZED_INPUT at the structural check".
(c) Primary: a lone surrogate is not Unicode scalar text, so the local name is not a (well-formed) text atom -> malformed atom -> MALF at step 3. [REJECT].
(d) AMBIGUITY (recorded): if the harness treats any decoded string as a text atom, the pair is structurally
valid and the first failing check is the extension-key binding (X1 not applied) -> PMI.

### P09
(a) Three defects at once: scope entry with capability `[]` (structural), execution finding target "foreign" (cross-field), fatal_conditions [E_INTEGRITY_INVALID] (step 5).
(b) [Q22] step 3 precedes steps 4-5; [Q27] "No later check or diagnostic is added after any earlier rejection branch wins."
(c) MALF only. [REJECT]. (d) none.

### P10
(a) Extension key [X1,"audit-window"], well-formed; profile_identifiers = [F1]; default catalog has no X1.
(b) [Q52] "For a structurally valid key, an unbound ... profile ... binding ... produces E_PROFILE_MAPPING_INVALID at the following cross-field check."
(c) PMI. [REJECT]. (d) none.

### P11
(a) Extension key [X1,"audit-window"] = evaluated; profile_identifiers = [F1, X1]; per-case catalog binds X1 with scope_names ["audit-window"].
(b) [Q52] "Core ignores an extension status for support and gap derivation but preserves the exact pair and status in the result."
(c) [CROSS-FIELD-OK] (key bound). [STD-E]; evaluation_scope (13 entries) and evaluation_context (two identifiers) carried.
(d) none.

### P12
(a) As P11 with the extension status not-evaluated.
(b) [Q52] (extension status ignored for derivation, preserved in result); the governed-field rules [Q57] concern initial capabilities only.
(c) [STD-E]; scope carried with the extension pair = not-evaluated. accept.
(d) none.

### P13
(a) The extension key [X1,"audit-window"] appears twice (both not-evaluated).
(b) [Q52] "... or a duplicate key in the scope map, produces E_PROFILE_MAPPING_INVALID at the following cross-field check."
(c) PMI. [REJECT]. (d) none (text explicit).

### P14
(a) Assert E+P+V; execution, PROV(execution) and IV(execution) all supported; ceiling execution.
(b) [Q31], [Q32], [Q33], [Q4], [Q39], [Q60].
(c) B={E}; Q(E)={PROV,IV}; S={E, E+P, E+V, E+P+V}; M={E+P+V}; A=true; relation E+P+V:equal; entries E {bd,E},
E+P {bd,E,P(E)}, E+V {bd,E,V(E)}, E+P+V {bd,E,P(E),V(E)}; reasons/gaps {}; accept.
(d) none.

### P15
(a) Boundary status unsupported, grounding asserted-only, limitation L-boundary, target_binding supported, ceiling_base present (ignored).
(b) [Q8] (only the not-evaluated pairing is constrained; ceiling_base ignored when unsupported); [Q29]; [Q49]; [Q46] "boundary_grounding preserves the input grounding even when the boundary is unsupported"; [Q28]; [Q35] "boundary limitations".
(c) B={}; S=M={}; A=false; relations {}; reasons {E_BOUNDARY_NOT_SUPPORTED}; gaps {}; downgrade;
boundary_ceiling unavailable (null); boundary_grounding asserted-only; inherited_limitations {L-boundary}.
(d) none.

### P16
(a) profile_identifiers [F1,X1]; authenticity = not-evaluated; profile gap P_AUTH_GAP (X1 registers it as evaluation-gap for authenticity) with marker authenticity, affects E, basis [F1,"auth-basis"], limitation [F1,"L-auth"].
(b) [Q15] (marker/token capability match); [Q56] (authenticity not-evaluated iff an entry names it: consistent); [Q41]; [Q51]; [Q35].
(c) [CROSS-FIELD-OK]. [STD-E]; the entry affects E -> copied exactly (with current_scope_capability authenticity), gaps {P_AUTH_GAP}; inherited_limitations {L-auth}; accept; scope and context carried.
(d) none.

### P17
(a) As P16 but the marker says composition on P_AUTH_GAP (registered for authenticity); authenticity remains not-evaluated, composition evaluated.
(b) [Q15] "A marker-token capability mismatch produces E_PROFILE_MAPPING_INVALID."; [Q56]/[Q57] (both external capability values now contradict the marker set).
(c) PMI. [REJECT]. (d) none.

### P18
(a) As P16 but marker = "execution-support" (a valid initial capability name, not authenticity/composition).
(b) [Q16] "a disallowed or mismatched current-scope marker ... produces E_PROFILE_MAPPING_INVALID at the cross-field check"; [Q62] "A marker naming a different capability ... produces E_PROFILE_MAPPING_INVALID."; [Q15].
(c) Primary: the value is a well-typed capability name; it is disallowed/mismatched -> PMI at step 4. [REJECT].
(d) AMBIGUITY (recorded): the schema comment restricts the field to "authenticity | composition"; reading the
field as that two-member closed enumeration makes "execution-support" an unknown closed-enum value -> MALF at step 3.

### P19
(a) As P16 but marker = "unknown-capability".
(b) [Q17] (initial evaluation-scope names are a closed enumeration); [Q22] "unknown closed-enum value ... returns E_MALFORMED_NORMALIZED_INPUT".
(c) Primary: not a capability name at all -> unknown closed-enum value -> MALF at step 3. [REJECT].
(d) AMBIGUITY (recorded): if every marker defect is a "disallowed ... current-scope marker" [Q16] at the cross-field check, the result is PMI.

### P20
(a) Profile gap entry lacks the token member.
(b) [Q16] "A missing member ... produces E_MALFORMED_NORMALIZED_INPUT at the structural check."
(c) MALF. [REJECT]. (d) none.

### P21
(a) Profile gap entry with affected_claims = [].
(b) [Q16] "For a structurally valid entry, an empty affected-claim set ... produces E_PROFILE_MAPPING_INVALID".
(c) PMI. [REJECT]. (d) none.

### P22
(a) Profile gap entry token = E_INTEGRITY_INVALID (fatal category) with marker authenticity.
(b) [Q16] "non-evaluation-gap token binding ... produces E_PROFILE_MAPPING_INVALID"; Section 6: "Fatal tokens belong in fatal_conditions, and evaluation-gap tokens belong in profile_evaluation_gaps."
(c) PMI. [REJECT]. (d) none.

### P23
(a) profile_identifiers [F1,X1]; one recorder relation under X1 with relation_token same-controller (in X1's relation_tokens), X1-scoped subject/object/basis refs; assert E.
(b) [Q19] ("Recorder relations are descriptive carried facts.  Their presence does not create a content-base or qualifier finding."); [CARRY].
(c) [CROSS-FIELD-OK] (token in the applied vocabulary, atoms bound to an applied profile). [STD-E]; recorder_relations carried unchanged; accept.
(d) none.

### P24
(a) As P23 but assert E+V; no IV finding.
(b) [Q49] "Asserted IV aggregate absent"; [Q4]; [Q19].
(c) B={E}; Q(E)={}; S=M={E}; A=false; relation support-below-claim; entry E {bd,E}; reasons {MISSING}; gaps {}; downgrade; recorder_relations carried.
(d) none.

### P25
(a) Top-level target and boundary target are U+00E9 ("é"); the execution finding target is "e" + U+0301 (NFD).
(b) [Q61] "Opaque fixture atoms compare by exact Unicode scalar text ... No URI, case, or Unicode normalization is implicit."; [Q6] "A foreign-scoped aggregate ... produces E_PROFILE_MAPPING_INVALID."
(c) The scalar sequences differ, so the base finding is foreign-scoped -> PMI. [REJECT].
(d) none (Section 4.1 lets a mapping profile define equality, but the fixture profile fixes exact-scalar comparison, so no normalization reading is available under F1).
