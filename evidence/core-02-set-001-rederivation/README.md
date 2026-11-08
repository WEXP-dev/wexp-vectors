# Independent re-derivation of WEXP-CORE-02-VECTORS-001 (89 cases)

Purpose: the frozen Core-02 corpus (package revision 2, `corpus.json` SHA-256
`d5d2c9d54185f04ac59ac2b5642853a6ebd00c3d28a3239d62682186f5df323f`, lock commit
`d6827a5e08fdf0aabecee5c025c369273c438db5`) records `independent_external_review:
false` and an expectation origin of "same-agent source-authored". This record holds a
second, isolated derivation of all 89 expectations from the published text alone and
its component-wise comparison with the frozen expectations. Set 001 itself is not
changed by this record.

Result: **89 / 89 agree on all twenty components** under the harness set semantics. No
divergence to classify. The engine, run only after that comparison, also agrees 89 / 89.

## What the isolated session received

[`BRIEF-given-to-the-session.md`](BRIEF-given-to-the-session.md), the 89 inputs
(`input` member only, plus the per-case applied profile catalog for the 17 cases that
carry one), `profiles.json` (the fixture catalog), the published
`draft-sergeev-wexp-core-02` text from the IETF archive (XML SHA-256
`de983051a1c6ea51ea9b7f965fe9eabf2d97af92ab2f074781bd44e3f99c8782`; text rendering
SHA-256 `73f92a0d735acb4e77aa8ef907b2a695acf2b87073db0352459022398771da8b`), and the
section 13 fixture C01 with its expected result as a format reference. It did not receive
`corpus.json`, any `expected`, `derivation` or `source_anchors` member, any
implementation, the set 002 package, or any issue or review note. Its own list of every
file it opened is [`rederived/FILES-READ.txt`](rederived/FILES-READ.txt); the file it lists
as `BRIEF.md` is committed here unchanged as `BRIEF-given-to-the-session.md`.

Every handed-over file is digest-bound in [`HANDOFF-SHA256SUMS.txt`](HANDOFF-SHA256SUMS.txt).
[`check_handoff_inputs.py`](check_handoff_inputs.py) rebuilds the 89 input files, the profile
catalog and the C01 format reference from the frozen `corpus.json` and checks them against
that listing (92 files rebuilt and matching, plus the brief by digest); the published text
rendering is bound by its digest above.

The brief restates part of the harness contract and names, without saying which case is
which, the defect classes that occur among the inputs (missing members, wrong types, unknown
enum values, duplicate aggregates, foreign scope, unsupported semantics version, a lone
surrogate in a text atom) and the rule that input-derived members are carried through to an
accept or downgrade result. These are hints about the input material, not expectations; the
session still marked the lone-surrogate case (P08) as an open reading.

## What it delivered (stored verbatim)

- [`rederived/expected/`](rederived/expected/): 89 files `{"id", "expected"}`, twenty members each.
- [`rederived/DERIVATION.md`](rederived/DERIVATION.md): a quote bank of 63 verbatim sentences
  with section numbers and one entry per case (variation, quotes, derivation, ambiguity).
- [`rederived/AMBIGUITIES.json`](rederived/AMBIGUITIES.json): five entries, each with the full
  alternative expected result.
- [`rederived/_work/`](rederived/_work/): the session's own notation aid (a display dump of
  the inputs and the script it used to emit JSON from its hand-stated values). Kept as
  delivered so that the derivation is auditable; it is not an appraiser.

Freeze before any comparison: [`DELIVERED-SHA256SUMS.txt`](DELIVERED-SHA256SUMS.txt) lists
the SHA-256 of all 94 delivered files with paths relative to `rederived/` (the delivery
directory used the same names); its own SHA-256 is
`bb5b640213cec675654fa36a38714d1665ecd1d1d859083cc95290a6e1fe097e`.

## Comparison with the frozen expectations

[`compare_rederivation.py`](compare_rederivation.py) compares every case component by
component (`compare_rederivation.py <corpus.json> <rederived/expected> [<output>]`). Collections that the harness defines as sets are compared as sets; everything
else is compared exactly, with Booleans distinct from numbers and `null` distinct from an
absent member. It imports no implementation. Output: [`comparison.json`](comparison.json).

| | cases |
|---|---|
| compared | 89 |
| equal on all twenty components | 89 |
| differing in any component | 0 |
| missing or wrong shape | 0 |

Two cases (R29 `fatal_reasons`; P14 qualifier sets and the claim sets built from them)
differ only in the serialized order of set members. Section 6.1 defines these as unordered
sets and section 8.4 says set ordering is defined by the result carrier, so these are not
differences in the logical result. They are listed here so that a reader who diffs the JSON
files byte-wise is not misled.

Classification of divergences (error in the frozen expectation / error in the new
derivation / text ambiguity / engine defect): none, because there is no divergence.

## Readings the isolated session marked as open

Five cases carry a primary and an alternative reading. In every one, the frozen expectation
equals the primary reading and differs from the alternative, so these are not divergences;
they are places where two independent readers reached the same primary reading of text
that both consider open.

| case | question | primary (= frozen) | alternative |
|---|---|---|---|
| P08 | is a lone surrogate (U+D800) in an extension key a text atom? | malformed, `E_MALFORMED_NORMALIZED_INPUT` | structurally valid pair, unbound profile, `E_PROFILE_MAPPING_INVALID` |
| P18 | `current_scope_capability = execution-support` | disallowed marker at the cross-field check, `E_PROFILE_MAPPING_INVALID` | unknown closed-enum value of a two-valued field, malformed |
| P19 | `current_scope_capability = unknown-capability` | unknown closed-enum value, malformed | disallowed marker, `E_PROFILE_MAPPING_INVALID` |
| R12 | `P_COUNTER_FAIL` registered identically by two applied profile revisions | "exactly one immutable registry revision" fails, `E_PROFILE_MAPPING_INVALID` | concordant registrations resolve; downgrade as C15 |
| R47 | substantive reason on a supported, non-asserted finding that is a support premise | projected (section 8.4 premise loop) | excluded as not bearing on the asserted claim |

The session's derivation of R22 (duplicate aggregate) also weighs, in prose, a reading under
which repeated equal set members are a malformed set (`E_MALFORMED_NORMALIZED_INPUT`, section
6.1 "Equal members occur once") against the cross-field reading it chose
(`E_PROFILE_MAPPING_INVALID`, section 6 "Duplicate or conflicting aggregate findings are fatal
and produce E_PROFILE_MAPPING_INVALID"); it did not list R22 in `AMBIGUITIES.json`. The frozen
expectation is the cross-field reading. It is noted here as a sixth, derivation-only
alternative; the delivered files were not edited.

None of these coincides with issues A1-A6 recorded for the section 7 matrix (set 002);
they concern sections 6.2 and 12 (structural versus mapping classification of
current-scope markers and atoms), section 6 (registry uniqueness) and section 8.6 (reason
projection route). They are offered to the specification review process as wording
questions; the text was not changed and no case here is used to settle them.

## Engine run, after the comparison

`wexp_ref.core02` at `WEXP-dev/wexp-ref` commit `56289024c9ee748111f1f1d4f42728ffe04d8d69`,
appraiser SHA-256 `e0ea740ce09a65cc6a48495a39730483da1f00583e1e864e6269a2eab4187ddd`,
against the frozen `corpus.json`:

| interpreter | mode | status | equal full results | comparator negative controls |
|---|---|---|---|---|
| CPython 3.12.13 | normal | PASS_BOUNDED | 89 / 89 | 42 / 42 |
| CPython 3.12.13 | optimized (-O) | PASS_BOUNDED | 89 / 89 | 42 / 42 |

Reports in [`engine-run/`](engine-run/), with [`engine-run/RUN-RECORD.json`](engine-run/RUN-RECORD.json)
giving the runner commit (`git rev-parse HEAD` of a clean checkout), the appraiser digest
recomputed from that checkout, the interpreter, the optimize flag and the argv of each run.
The qualify report schema has no mode or timestamp member and the appraisal is deterministic,
so the two reports are byte-identical; mode and order are attested by the run record, not by
the report bytes. For the five open-reading cases the engine equals the primary reading and
differs from the alternative.

Order of evidence: the isolated session never had access to any engine output (its file list
contains none). The author of this record had seen a routine run of the same engine on the
same frozen corpus during earlier, unrelated work; that run is not part of this record. The
runs recorded here were made only after `comparison.json` had been produced. This ordering is
attested, not provable from the report bytes.

## What this does and does not establish

It establishes that a second derivation, made in isolation from the first and from every
implementation, reproduced all 89 frozen expectations of set 001 from the published text.
The corpus manifest's `independent_external_review: false` still stands as written: both
derivations are same-project work, and this record is not external review, certification,
conformance or interoperability evidence. Where a case and the published I-D disagree, the
I-D wins and the case is a defect; this record found no such case.
