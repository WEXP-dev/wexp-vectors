# BOUNDARY-MATRIX-001: Core-02 section 7 status x grounding x target_binding coverage

Specification: published `draft-sergeev-wexp-core-02` (IETF archive / Datatracker), XML SHA-256
`de983051a1c6ea51ea9b7f965fe9eabf2d97af92ab2f074781bd44e3f99c8782` (equal to the digest bound by the frozen corpus manifest).
Frozen corpus overlaid: `WEXP-CORE-02-VECTORS-001` package revision 2, lock commit `d6827a5e08fdf0aabecee5c025c369273c438db5`,
`corpus.json` SHA-256 `d5d2c9d54185f04ac59ac2b5642853a6ebd00c3d28a3239d62682186f5df323f`, 89 cases.

Fixture for the verdict column: assert E (execution); one execution finding with supported target binding and
semantic validation; boundary ceiling execution; boundary basis `bd`; boundary limitation `L-boundary`; everything else
as the section 13 common input. The verdict, reasons and gaps columns are this author's section 7 derivation and are
**not** the frozen expectations; frozen expectations were derived by a separate clean session (see the derivation record).

## Section 7 sentences cited (verbatim)

- **Q1**: "Only status = supported with target_binding = supported and matching target and context makes ceiling_base usable."
- **Q2**: "When status = not-evaluated, no base is added and the appraiser records E_BOUNDARY_NOT_EVALUATED."
- **Q3**: "When status = unsupported, no base is added and it records E_BOUNDARY_NOT_SUPPORTED."
- **Q4**: "A failed target binding prevents use of the ceiling and adds the Core substantive reason E_EVIDENCE_NOT_BOUND;"
- **Q5**: "an unevaluated target binding prevents use of the ceiling and adds the Core gap E_BOUNDARY_NOT_EVALUATED, as specified by Section 8.6."
- **Q6**: "An asserted-only or attributed finding can be supported only when the evaluation context explicitly accepts that grounding class; the result still reports the weaker grounding and its limitations."
- **Q7**: "An accept or downgrade result MUST preserve the boundary grounding status and its limitations.  A reject result instead uses the fixed projection in Section 8.4."
- **Q8**: "The evaluation context MUST identify the minimum acceptable grounding."
- **Q9**: "A string or structural descriptor asserted by a producer is at most asserted-only; a valid signature associated with an accepted identity can make it attributed; and an applicable boundary-grounding profile can make it attested."
- **S6**: "[section 6] grounding = not-evaluated is valid only with status = not-evaluated; either field paired differently produces E_PROFILE_MAPPING_INVALID."
- **S6b**: "[section 6] A supported boundary has a grounding value of asserted-only, attributed, or attested that the evaluation context accepts."
- **S62**: "[section 6.2, check 4] A well-typed wexp-core-2 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID."
- **S12**: "[section 12] A scope value of evaluated with a governed not-evaluated status [...] violates the cross-field contract and produces E_PROFILE_MAPPING_INVALID."
- **S85**: "[section 8.5] boundary_ceiling is the accepted ceiling only when the boundary finding, its target binding, target, and context all pass; otherwise it is unavailable. boundary_grounding preserves the input grounding even when the boundary is unsupported."
- **S81**: "[section 8.1] The result's inherited_limitations is the set union of [...] boundary limitations; every support-entry limitation; and limitations attached to findings that determine a reason or gap for the asserted claim."

## Axis note: "context accepts grounding class"

Core receives `evaluation_context.trust_configuration` as an opaque atom (section 6.1) and the AppraisalInput has no field that
carries the accepted grounding set. Whether the context accepts a class is therefore a profile-side premise, visible to Core only
through the status the profile reports. Cells that differ only in this axis are Core-indistinguishable; the matrix shows the axis
as an annotation and counts coverage on the Core-observable cells (status x grounding x target_binding). See SPEC-ISSUES A1.

## Matrix (Core-observable cells)

| # | status | grounding | target_binding | reachable via section 7 precedence | verdict | substantive reasons | gaps | ceiling usable | reported boundary_grounding | reported limitations | section 7 quotes | scope consistency (section 12) | covered by (rev 2) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | supported | asserted-only | supported (supported) | yes | accept | {} | {} | yes (boundary_ceiling = execution) | asserted-only | L-boundary in inherited_limitations and in the execution support entry | Q1, S6b, Q6, Q7, S85, S81 | - | **EMPTY** |
| 2 | supported | asserted-only | failed (unsupported) | yes | downgrade | E_EVIDENCE_NOT_BOUND | {} | no (boundary_ceiling = unavailable) | asserted-only | L-boundary in inherited_limitations | Q4, Q1, S6b, Q6, Q7, S85, S81 | - | **EMPTY** |
| 3 | supported | asserted-only | unevaluated (not-evaluated) | yes | downgrade | {} | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | asserted-only | L-boundary in inherited_limitations | Q5, Q1, S6b, Q6, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated; evaluation_scope[target-binding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 4 | supported | attributed | supported (supported) | yes | accept | {} | {} | yes (boundary_ceiling = execution) | attributed | L-boundary in inherited_limitations and in the execution support entry | Q1, S6b, Q6, Q7, S85, S81 | - | C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, C15, C16, R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R27, R28, R29, R30, R31, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25 |
| 5 | supported | attributed | failed (unsupported) | yes | downgrade | E_EVIDENCE_NOT_BOUND | {} | no (boundary_ceiling = unavailable) | attributed | L-boundary in inherited_limitations | Q4, Q1, S6b, Q6, Q7, S85, S81 | - | **EMPTY** |
| 6 | supported | attributed | unevaluated (not-evaluated) | yes | downgrade | {} | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | attributed | L-boundary in inherited_limitations | Q5, Q1, S6b, Q6, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated; evaluation_scope[target-binding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 7 | supported | attested | supported (supported) | yes | accept | {} | {} | yes (boundary_ceiling = execution) | attested | L-boundary in inherited_limitations and in the execution support entry | Q1, S6b, Q7, S85, S81 | - | **EMPTY** |
| 8 | supported | attested | failed (unsupported) | yes | downgrade | E_EVIDENCE_NOT_BOUND | {} | no (boundary_ceiling = unavailable) | attested | L-boundary in inherited_limitations | Q4, Q1, S6b, Q7, S85, S81 | - | **EMPTY** |
| 9 | supported | attested | unevaluated (not-evaluated) | yes | downgrade | {} | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | attested | L-boundary in inherited_limitations | Q5, Q1, S6b, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated; evaluation_scope[target-binding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 10 | supported | not-evaluated | supported (supported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | R26 |
| 11 | supported | not-evaluated | failed (unsupported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 12 | supported | not-evaluated | unevaluated (not-evaluated) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 13 | unsupported | asserted-only | supported (supported) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED | {} | no (boundary_ceiling = unavailable) | asserted-only | L-boundary in inherited_limitations | Q3, Q1, Q7, S85, S81 | - | P15 |
| 14 | unsupported | asserted-only | failed (unsupported) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND | {} | no (boundary_ceiling = unavailable) | asserted-only | L-boundary in inherited_limitations | Q3, Q4, Q1, Q7, S85, S81 | - | **EMPTY** |
| 15 | unsupported | asserted-only | unevaluated (not-evaluated) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | asserted-only | L-boundary in inherited_limitations | Q3, Q5, Q1, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated; evaluation_scope[target-binding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 16 | unsupported | attributed | supported (supported) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED | {} | no (boundary_ceiling = unavailable) | attributed | L-boundary in inherited_limitations | Q3, Q1, Q7, S85, S81 | - | R32 |
| 17 | unsupported | attributed | failed (unsupported) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND | {} | no (boundary_ceiling = unavailable) | attributed | L-boundary in inherited_limitations | Q3, Q4, Q1, Q7, S85, S81 | - | **EMPTY** |
| 18 | unsupported | attributed | unevaluated (not-evaluated) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | attributed | L-boundary in inherited_limitations | Q3, Q5, Q1, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated; evaluation_scope[target-binding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 19 | unsupported | attested | supported (supported) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED | {} | no (boundary_ceiling = unavailable) | attested | L-boundary in inherited_limitations | Q3, Q1, Q7, S85, S81 | - | **EMPTY** |
| 20 | unsupported | attested | failed (unsupported) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND | {} | no (boundary_ceiling = unavailable) | attested | L-boundary in inherited_limitations | Q3, Q4, Q1, Q7, S85, S81 | - | **EMPTY** |
| 21 | unsupported | attested | unevaluated (not-evaluated) | yes | downgrade | E_BOUNDARY_NOT_SUPPORTED | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | attested | L-boundary in inherited_limitations | Q3, Q5, Q1, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated; evaluation_scope[target-binding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 22 | unsupported | not-evaluated | supported (supported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 23 | unsupported | not-evaluated | failed (unsupported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 24 | unsupported | not-evaluated | unevaluated (not-evaluated) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 25 | not-evaluated | asserted-only | supported (supported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 26 | not-evaluated | asserted-only | failed (unsupported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 27 | not-evaluated | asserted-only | unevaluated (not-evaluated) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 28 | not-evaluated | attributed | supported (supported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 29 | not-evaluated | attributed | failed (unsupported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 30 | not-evaluated | attributed | unevaluated (not-evaluated) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 31 | not-evaluated | attested | supported (supported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 32 | not-evaluated | attested | failed (unsupported) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 33 | not-evaluated | attested | unevaluated (not-evaluated) | reject before section 7 (cross-field check 4 wins) | reject / fatal E_PROFILE_MAPPING_INVALID | n/a (fixed projection) | n/a (fixed projection) | no (no appraisal) | unavailable | unavailable | S6, S62, Q7 | - | **EMPTY** |
| 34 | not-evaluated | not-evaluated | supported (supported) | yes | downgrade | {} | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | not-evaluated | L-boundary in inherited_limitations | Q2, Q1, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 35 | not-evaluated | not-evaluated | failed (unsupported) | yes | downgrade | E_EVIDENCE_NOT_BOUND | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | not-evaluated | L-boundary in inherited_limitations | Q2, Q4, Q1, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |
| 36 | not-evaluated | not-evaluated | unevaluated (not-evaluated) | yes | downgrade | {} | E_BOUNDARY_NOT_EVALUATED | no (boundary_ceiling = unavailable) | not-evaluated | L-boundary in inherited_limitations | Q2, Q5, Q1, Q7, S85, S81, S12 | evaluation_scope[boundary-grounding] must be not-evaluated; evaluation_scope[target-binding] must be not-evaluated (section 12 governed fields), otherwise E_PROFILE_MAPPING_INVALID. | **EMPTY** |

## Acceptance annotation (status x grounding x accepts), 54-cell view

| status | grounding | accepts = yes | accepts = no |
|---|---|---|---|
| supported | asserted-only | reachable only with a context whose minimum is asserted-only (local test atom core02-test-trust-asserted-only-1); trust-1 accepts attributed (section 13) | NOT reachable from a conforming profile ("can be supported only when the evaluation context explicitly accepts", Q6); Core cannot detect it: trust_configuration is an opaque atom and no input field carries the accepted set (ambiguity A1) |
| supported | attributed | reachable with core02-fixture-trust-1 (section 13: accepts attributed boundary grounding) | NOT reachable from a conforming profile ("can be supported only when the evaluation context explicitly accepts", Q6); Core cannot detect it: trust_configuration is an opaque atom and no input field carries the accepted set (ambiguity A1) |
| supported | attested | reachable; attested is the strongest class (Q9) and section 7 names only asserted-only/attributed as needing explicit acceptance; any minimum (Q8) is met | not reachable: no minimum acceptable grounding (Q8) can exclude the strongest class |
| unsupported | asserted-only | reachable; Core-indistinguishable from accepts = no | reachable; a conforming profile reports unsupported or not-evaluated when the context does not accept the class (Q6); Core-indistinguishable from accepts = yes |
| unsupported | attributed | reachable; Core-indistinguishable from accepts = no | reachable; a conforming profile reports unsupported or not-evaluated when the context does not accept the class (Q6); Core-indistinguishable from accepts = yes |
| unsupported | attested | reachable; Core-indistinguishable from accepts = no | reachable; a conforming profile reports unsupported or not-evaluated when the context does not accept the class (Q6); Core-indistinguishable from accepts = yes |
| not-evaluated | asserted-only | reachable; Core-indistinguishable from accepts = no | reachable; a conforming profile reports unsupported or not-evaluated when the context does not accept the class (Q6); Core-indistinguishable from accepts = yes |
| not-evaluated | attributed | reachable; Core-indistinguishable from accepts = no | reachable; a conforming profile reports unsupported or not-evaluated when the context does not accept the class (Q6); Core-indistinguishable from accepts = yes |
| not-evaluated | attested | reachable; Core-indistinguishable from accepts = no | reachable; a conforming profile reports unsupported or not-evaluated when the context does not accept the class (Q6); Core-indistinguishable from accepts = yes |

Frozen cases instantiate the acceptance axis as follows: every case with `core02-fixture-trust-1` and grounding attributed is
accepts = yes; P15 (`core02-fixture-trust-1`, asserted-only, unsupported) is the conforming accepts = no report.

## Coverage summary (Core-observable cells)

- cells total: 36 (27 with grounding in the three classes + 9 with grounding = not-evaluated)
- cells that reach section 7 (accept/downgrade): 21
- cells rejected before section 7 by the section 6 pairing invariant: 15 (of which 9 rest on ambiguity A2)
- covered by revision 2 before this work: 4 -> #4 (C01, C02, C03...), #10 (R26), #13 (P15), #16 (R32)
- empty before this work: 32

## Empty cells and the vector written for each

- cell #1 (supported x asserted-only x supported) -> `B01`
- cell #2 (supported x asserted-only x unsupported) -> `B02`
- cell #3 (supported x asserted-only x not-evaluated) -> `B03`
- cell #5 (supported x attributed x unsupported) -> `B04`
- cell #6 (supported x attributed x not-evaluated) -> `B05`
- cell #7 (supported x attested x supported) -> `B06`
- cell #8 (supported x attested x unsupported) -> `B07`
- cell #9 (supported x attested x not-evaluated) -> `B08`
- cell #11 (supported x not-evaluated x unsupported) -> `B09`
- cell #12 (supported x not-evaluated x not-evaluated) -> `B10`
- cell #14 (unsupported x asserted-only x unsupported) -> `B11`
- cell #15 (unsupported x asserted-only x not-evaluated) -> `B12`
- cell #17 (unsupported x attributed x unsupported) -> `B13`
- cell #18 (unsupported x attributed x not-evaluated) -> `B14`
- cell #19 (unsupported x attested x supported) -> `B15`
- cell #20 (unsupported x attested x unsupported) -> `B16`
- cell #21 (unsupported x attested x not-evaluated) -> `B17`
- cell #22 (unsupported x not-evaluated x supported) -> `B18`
- cell #23 (unsupported x not-evaluated x unsupported) -> `B19`
- cell #24 (unsupported x not-evaluated x not-evaluated) -> `B20`
- cell #25 (not-evaluated x asserted-only x supported) -> `B21` [ambiguity: A2:]
- cell #26 (not-evaluated x asserted-only x unsupported) -> `B22` [ambiguity: A2:]
- cell #27 (not-evaluated x asserted-only x not-evaluated) -> `B23` [ambiguity: A2:]
- cell #28 (not-evaluated x attributed x supported) -> `B24` [ambiguity: A2:]
- cell #29 (not-evaluated x attributed x unsupported) -> `B25` [ambiguity: A2:]
- cell #30 (not-evaluated x attributed x not-evaluated) -> `B26` [ambiguity: A2:]
- cell #31 (not-evaluated x attested x supported) -> `B27` [ambiguity: A2:]
- cell #32 (not-evaluated x attested x unsupported) -> `B28` [ambiguity: A2:]
- cell #33 (not-evaluated x attested x not-evaluated) -> `B29` [ambiguity: A2:]
- cell #34 (not-evaluated x not-evaluated x supported) -> `B30`
- cell #35 (not-evaluated x not-evaluated x unsupported) -> `B31`
- cell #36 (not-evaluated x not-evaluated x not-evaluated) -> `B32`
- control `B33`: not-evaluated x not-evaluated x supported with evaluation_scope[boundary-grounding] = evaluated (section 12 inconsistency control)
- control `B34`: supported x attributed x not-evaluated with evaluation_scope[target-binding] = not-evaluated but [boundary-grounding] = evaluated (section 12 governed-field control)
- probe `B35`: supported x asserted-only x supported under `core02-fixture-trust-1` (acceptance axis = no; profile-obligation probe, ambiguity A1)

Total inputs handed to the clean session: 35 (32 matrix cells + 2 section 12 controls + 1 acceptance probe).
