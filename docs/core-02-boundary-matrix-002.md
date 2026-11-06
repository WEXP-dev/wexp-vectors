# Core-02 set 002: section 7 boundary matrix. Derivation, freeze and first run

Set `WEXP-CORE-02-VECTORS-002`: 35 cases for the Boundary Ceiling matrix
`boundary_finding.status` x `boundary_finding.grounding` x `boundary_finding.target_binding`
of published `draft-sergeev-wexp-core-02`. It answers the coverage question left open by
the earlier Core-01 pairing-invariant proposal (wexp-vectors pull request 10): the frozen
Core-02 corpus never varied the boundary dimensions that section 7 orders.

## The published text this set rests on

Section 7 (verbatim, the precedence paragraph):

> The boundary status has deterministic precedence. When status = not-evaluated, no base
> is added and the appraiser records E_BOUNDARY_NOT_EVALUATED. When status =
> unsupported, no base is added and it records E_BOUNDARY_NOT_SUPPORTED. Only status =
> supported with target_binding = supported and matching target and context makes
> ceiling_base usable. A failed target binding prevents use of the ceiling and adds the
> Core substantive reason E_EVIDENCE_NOT_BOUND; an unevaluated target binding prevents
> use of the ceiling and adds the Core gap E_BOUNDARY_NOT_EVALUATED, as specified by
> Section 8.6.

and the preservation rule:

> An accept or downgrade result MUST preserve the boundary grounding status and its
> limitations. A reject result instead uses the fixed projection in Section 8.4.

Section 6 supplies the pairing invariant ("grounding = not-evaluated is valid only with
status = not-evaluated; either field paired differently produces
E_PROFILE_MAPPING_INVALID"), section 6.2 places it at ordered check 4, section 8.6 gives
the four boundary rows of the claim-required matrix, section 8.5 the ceiling/grounding
projection, section 8.1 the limitation union, and section 12 the governed fields of the
`boundary-grounding` and `target-binding` scope capabilities.

Published source: XML SHA-256 `de983051a1c6ea51ea9b7f965fe9eabf2d97af92ab2f074781bd44e3f99c8782`
(IETF archive bytes verified equal to the digest bound by set 001 revision 2).

## The matrix and what revision 2 covered

[`BOUNDARY-MATRIX-001.md`](BOUNDARY-MATRIX-001.md) enumerates the 36 Core-observable cells
(27 with grounding in {asserted-only, attributed, attested} plus 9 with grounding =
not-evaluated), cites the section 7 sentence for each, and overlays revision 2 (lock
commit `d6827a5e08fdf0aabecee5c025c369273c438db5`, `corpus.json`
`d5d2c9d54185f04ac59ac2b5642853a6ebd00c3d28a3239d62682186f5df323f`).

| | cells |
|---|---|
| Core-observable cells | 36 |
| reaching section 7 (accept/downgrade) | 21 |
| rejected at check 4 by the pairing invariant | 15 (9 under ambiguity A2) |
| covered by revision 2 | 4 (C01-C16 and controls; R26; R32; P15) |
| empty before this set | 32 |
| covered after this set | 36 |

The "context accepts the grounding class" axis requested for the matrix is shown as an
annotation: Core compares `trust_configuration` as an opaque atom and the input carries
no accepted-class field, so cells differing only in acceptance are Core-indistinguishable
(issue A1). One probe (B35) instantiates the accepts = no cell under the section 13 atom.

## How the expectations were produced and frozen

1. The matrix author wrote the 35 inputs (`inputs.py`) and a predicted outcome per cell
   in the matrix, from the text. No expectation file was written by the author.
2. A separate isolated session received only: the 35 inputs, the profile catalog, the
   published text (full `.txt` and section 7 verbatim), the encoding rules, and the
   section 13 fixture C01 as a format reference. It had no access to any implementation,
   to the existing corpus expectations, or to the author's matrix predictions, and it
   recorded every file it opened (`derivation/FILES-READ.txt`). It returned
   `expectations/B01.json` .. `B35.json`, `derivation/DERIVATION.md` (30 labelled
   verbatim quotes, 12 common derivation steps, per-vector derivation) and
   `derivation/AMBIGUITIES.json` (17 entries, 3 distinct questions, each with the full
   alternative result). All of these are stored verbatim; the only files the author
   wrote are `inputs.py`, `corpus.py`, `verify.py`, `manifest.json`, `README.md`.
3. The delivered files were hashed before any engine run:

       expectation freeze        WEXP-CORE-02-V002-EXPECTATION-FREEZE-001
       delivered-file digest list f4554e83aeb805f486a8c669ad9323a901bc697436e7d04386a33fccb60189a4
         (SHA-256 of derivation/DELIVERED-SHA256SUMS.txt, stored verbatim: the shasum -a 256
         listing of the 38 delivered files taken in the delivery directory, where the
         expectation files were under expected/ before being copied to expectations/)
       DERIVATION.md             24697882f95c84fa7b451dc34178209817256d436b09f0a70bce3cce17f1cd31
       AMBIGUITIES.json          16c26b572c7e42c65275a2cd54aebd37ae5538dfa59f12eb9dc199bba04ea3f9
       FILES-READ.txt            ee51a239d37a47ea5ce5be7297f784f581fa7d97b9ea3e7903eb6dca01810c8a
       expanded corpus.json      9e301333bfdaa4a96068fe44adc0cde3f8eb63bc08f77f164d1d568f609a8bc0 (118091 bytes)
       manifest.json             3961528fd349b584285d181ce466e0447d4e9f69a223ab33a4a70b1d6fdff8cb

   `corpus.py` joins inputs with the delivered expectations and computes nothing;
   `verify.py --rebuild` checks that the frozen `corpus.json` equals the rebuilt bytes and
   that every expanded expectation equals its delivered file.

## Frozen expectations (primary readings)

| case | status / grounding / binding | verdict | fatal | substantive reasons | gaps |
|---|---|---|---|---|---|
| B01 | supported / asserted-only / supported (test trust atom) | accept | | | |
| B02 | supported / asserted-only / unsupported | downgrade | | E_EVIDENCE_NOT_BOUND | |
| B03 | supported / asserted-only / not-evaluated | downgrade | | | E_BOUNDARY_NOT_EVALUATED |
| B04 | supported / attributed / unsupported | downgrade | | E_EVIDENCE_NOT_BOUND | |
| B05 | supported / attributed / not-evaluated | downgrade | | | E_BOUNDARY_NOT_EVALUATED |
| B06 | supported / attested / supported | accept | | | |
| B07 | supported / attested / unsupported | downgrade | | E_EVIDENCE_NOT_BOUND | |
| B08 | supported / attested / not-evaluated | downgrade | | | E_BOUNDARY_NOT_EVALUATED |
| B09 | supported / not-evaluated / unsupported | reject | E_PROFILE_MAPPING_INVALID | | |
| B10 | supported / not-evaluated / not-evaluated | reject | E_PROFILE_MAPPING_INVALID | | |
| B11 | unsupported / asserted-only / unsupported | downgrade | | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND | |
| B12 | unsupported / asserted-only / not-evaluated | downgrade | | E_BOUNDARY_NOT_SUPPORTED | E_BOUNDARY_NOT_EVALUATED |
| B13 | unsupported / attributed / unsupported | downgrade | | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND | |
| B14 | unsupported / attributed / not-evaluated | downgrade | | E_BOUNDARY_NOT_SUPPORTED | E_BOUNDARY_NOT_EVALUATED |
| B15 | unsupported / attested / supported | downgrade | | E_BOUNDARY_NOT_SUPPORTED | |
| B16 | unsupported / attested / unsupported | downgrade | | E_BOUNDARY_NOT_SUPPORTED, E_EVIDENCE_NOT_BOUND | |
| B17 | unsupported / attested / not-evaluated | downgrade | | E_BOUNDARY_NOT_SUPPORTED | E_BOUNDARY_NOT_EVALUATED |
| B18-B20 | unsupported / not-evaluated / any | reject | E_PROFILE_MAPPING_INVALID | | |
| B21-B29 | not-evaluated / {asserted-only, attributed, attested} / any | reject (A2) | E_PROFILE_MAPPING_INVALID | | |
| B30 | not-evaluated / not-evaluated / supported | downgrade | | | E_BOUNDARY_NOT_EVALUATED |
| B31 | not-evaluated / not-evaluated / unsupported | downgrade | | E_EVIDENCE_NOT_BOUND | E_BOUNDARY_NOT_EVALUATED |
| B32 | not-evaluated / not-evaluated / not-evaluated | downgrade | | | E_BOUNDARY_NOT_EVALUATED (one collapsed entry) |
| B33 | control: scope boundary-grounding left evaluated | reject | E_PROFILE_MAPPING_INVALID | | |
| B34 | control: binding not-evaluated, scope boundary-grounding evaluated | reject | E_PROFILE_MAPPING_INVALID | | |
| B35 | probe: supported / asserted-only under core02-fixture-trust-1 | accept (A1) | | | |

In every accept or downgrade: `boundary_grounding` equals the input grounding (including
`not-evaluated` for B30-B32); `boundary_ceiling` is `execution` for accept and
unavailable otherwise; `inherited_limitations` = {L-boundary}; the accept cases carry
S = M = {E}, relation equal, support entry basis {bd, E} with limitation L-boundary; every
gap entry is (E_BOUNDARY_NOT_EVALUATED, T, C, {execution}, {bd}, {L-boundary}). Rejects
use the complete section 8.4 fixed projection.

## First engine run (after the freeze)

`wexp_ref.core02` at `WEXP-dev/wexp-ref` commit `56289024c9ee748111f1f1d4f42728ffe04d8d69`,
appraiser SHA-256 `e0ea740ce09a65cc6a48495a39730483da1f00583e1e864e6269a2eab4187ddd`,
run with `python -m wexp_ref.core02.qualify --corpus corpus.json --expected-sha256 9e301333...`:

| interpreter | mode | status | equal full results | comparator negative controls |
|---|---|---|---|---|
| CPython 3.12.13 | normal | PASS_BOUNDED | 35 / 35 | 42 / 42 |
| CPython 3.12.13 | optimized (-O) | PASS_BOUNDED | 35 / 35 | 42 / 42 |
| CPython 3.14.6 | normal | PASS_BOUNDED | 35 / 35 | 42 / 42 |

Reports: [`evidence/core-02-set-002/`](../evidence/core-02-set-002/) (3.12 normal and
optimized reports are byte-identical, SHA-256
`9ed23413e9badcddea46c89887daa240bc1f476d12ececec79f82f530d2b5f59`). The comparison is
set-aware, as the harness requires: in 19 reports the engine's `observed` differs from the
frozen `expected` only in the member order of `evaluation_scope` (the engine emits it
sorted; the frozen files keep the section 12 listing order), which section 12 defines as an
unordered map. A plain JSON diff of the reports therefore shows differences that
`equal_full_result` correctly ignores. The engine also
differs from every one of the 17 recorded alternative readings, so it follows the
primary reading on A1, A2 and A6.

## Three-way comparison and classification

For each case three values were compared: the matrix author's predicted outcome
(verdict, fatal, reasons, gaps, ceiling, grounding), the frozen isolated-session
expectation (all twenty components), and the engine's observed result (all twenty
components). Result: 35 / 35 agree on all three. There is no divergence to classify as
vector error, expectation error, runner defect or specification ambiguity.

The agreement does not settle the three open readings; it records that two independent
readers and one implementation chose the same primary reading. Those readings are
recorded as A1, A2 and A6 in [`SPEC-ISSUES-core02-s7.md`](SPEC-ISSUES-core02-s7.md),
with the clarifications they would need. The text was not changed.

## Scope and non-claims

Thirty-five cases on one requirement family of one published revision. Set 001 revision
2 is unchanged and its lock in `wexp-ref` still points at it. This set is not a
conformance suite, not independent external review (same project, two sessions), not a
mapping-profile test, and not evidence about carrier authentication or real-world
boundary control. The published I-D remains authoritative; where a case and the text
disagree, the case is a defect.
