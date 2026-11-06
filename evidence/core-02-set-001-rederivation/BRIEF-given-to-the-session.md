# Clean derivation brief: independent re-derivation of the 89 Core-02 corpus cases

You are an isolated derivation session. Your task is to derive the complete expected logical
appraisal for each of the 89 inputs in `inputs/` **from the published specification text alone**.
The inputs come from an existing published corpus whose expectations you must NOT see; the point
of this exercise is an independent second derivation that will later be compared with them.

## Hard rules

1. Read only files inside this directory (`handoff/`). Do not open any other directory, repository,
   package or module. Do not use the network. Do not import or run any WEXP implementation
   (nothing named `wexp_ref`, `wexp-ref`, appraiser, verifier). Do not look for or consult any
   test corpus, earlier expected results, issue lists or review notes. The only expected result you
   may look at is `FORMAT-REFERENCE-C01.json` (the published section 13 fixture C01, transcribed),
   given as a format reference.
2. Every expected value must be traceable to a sentence of the published text in `spec/`. Quote the
   sentences you rely on. If the text admits more than one reading for a case, say so, give both
   readings and the result under each, choose one as primary and explain why.
3. Do not infer a result from what an implementation "would probably do". If you cannot derive a
   component, say so instead of guessing.
4. Record in `FILES-READ.txt` every file you opened, one path per line.

## Specification

`spec/draft-sergeev-wexp-core-02.txt` is the published `draft-sergeev-wexp-core-02` (IETF archive).
You will need at least sections 4 (claim model, structural order), 5, 6 (normalized input and its
cross-field invariants), 6.1 (equality), 6.2 (ordered rejection checks), 7 (Boundary Ceiling),
8.1-8.6 (algorithm, result, diagnostic matrix), 9 (composition, as far as inputs touch it), 12
(evaluation scope, governed fields, extension keys, current-scope markers) and 13 (fixture
environment, fixture profile `draft-sergeev-wexp-core-02/fixture-1`, the C01-C16 table).

## Inputs

`inputs/C01.json` .. `C16.json`, `R01.json` .. `R48.json`, `P01.json` .. `P25.json`. Each file is
`{"id": ..., "input": <AppraisalInput>}` and, for 17 cases, additionally `"profiles": <catalog>`:
the applied profile catalog for THAT case, which replaces `profiles.json` for it. For the other
72 cases the catalog is `profiles.json`. A catalog maps an immutable profile identity to its
`tokens` (token -> {category, optional current_scope_capability}), `relation_tokens` and
`scope_names`. A profile identity that occurs in `evaluation_context.profile_identifiers` but is
absent from the applied catalog cannot resolve anything.

Some inputs are deliberately malformed or inconsistent (missing members, wrong types, unknown
enum values, duplicate aggregates, foreign scope, unsupported semantics version, lone surrogate
in a text atom, etc.). Derive the exact ordered-check outcome for them under section 6.2 and 12.
C01-C16 are the section 13 normative rows; derive them from the table and the common fixture
environment described there, not from memory of any corpus.

## Local JSON encoding of logical values (non-normative harness)

Opaque atoms are exact Unicode text. Profile-scoped atoms (basis references, limitations,
recorder subject/object refs) are ordered two-element arrays `[profile_identifier, local_name]`.
Extension scope keys are the same two-element array shape. Sets are JSON arrays with set
semantics; member order is not significant (prefer sorted order, any order is acceptable). A claim
is `{"base": ..., "qualifiers": [...]}`; `affected_claims` may instead be the text atom
`"all-admissible-claims"` where the text allows it. `evaluation_scope` is an array of
`{"capability": ..., "status": ...}`. `null` means the logical value *unavailable* (not an absent
member). Booleans must be JSON booleans. Every expected result has exactly these twenty members:

semantics_version, verdict, fatal_reasons, target, asserted_claim, asserted_claim_supported,
support_entries, supported_claims, maximal_supported_claims, support_relations, boundary_ceiling,
boundary_grounding, recorder_relations, substantive_reasons, evaluation_gaps, evaluation_gap_entries,
counter_evidence, inherited_limitations, evaluation_context, evaluation_scope.

A support entry is `{"claim", "basis_refs", "limitations"}`; a support relation is
`{"supported_claim", "relation"}`; a gap entry is `{"token", "target", "evaluation_context_ref",
"affected_claims", "basis_refs", "limitations"}` plus `current_scope_capability` only when the
input entry carried it. For an accept or downgrade, input-derived members (`target`,
`asserted_claim`, `recorder_relations`, `counter_evidence`, `evaluation_context`,
`evaluation_scope`) are the input values carried through. See `FORMAT-REFERENCE-C01.json`.

## Deliverables (write them into this directory)

1. `expected/<id>.json` for all 89 ids: `{"id": "<id>", "expected": { ...twenty members... }}`.
   Pure JSON, 1-space indent, sorted keys, ASCII-escaped, trailing newline.
2. `DERIVATION.md`: for every case, (a) the input variation in one line, (b) the verbatim sentences
   relied on with section numbers, (c) the derivation of verdict, fatal_reasons, substantive_reasons,
   evaluation_gaps / entries, boundary_ceiling, boundary_grounding, inherited_limitations,
   supported/maximal claims, support entries and relations, and (d) any ambiguity with both readings.
3. `AMBIGUITIES.json`: `[{"id": ..., "question": ..., "primary_reading": ..., "alternative_reading": ...,
   "alternative_expected": {...} }]` (empty array if none).
4. `FILES-READ.txt`.

Work through every case; do not stop early. Cases that share a derivation may share the reasoning
text, but each needs its own expected file and its own entry in `DERIVATION.md`. You may use
Python only as a notation aid to emit JSON you have derived yourself; never to compute an
expectation from an implementation.
