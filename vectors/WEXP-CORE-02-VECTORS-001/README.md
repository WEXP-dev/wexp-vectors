# WEXP-CORE-02-VECTORS-001

A source-encoded, specification-derived executable corpus for the published
`draft-sergeev-wexp-core-02`, semantics `wexp-core-2`. It contains 16 normative
C01-C16 transcriptions, 48 derived review cases, and 25 additional posted-contract
controls. The latter 73 are non-normative tests, not new specification rules.

This is not a conformance suite, certification, carrier test, AAC mapping, Coverage
implementation or interoperability result. Core-01/Core-00 corpora retain their
identities. This package does not requalify their results.

## Frozen representation and expansion

`manifest.json` identifies the exact public specification, source files, profile
registry and expanded corpus digest. `normative_cases.py`, `review_cases.py` and
`final_contract_cases.py` encode expectations from the specification, without
importing or invoking an appraiser. `corpus.py` expands them to complete inputs
and all twenty expected logical result components. The source representation is
the committed corpus; the reproducible expanded JSON is not checked in a second
time. Changing either representation requires a new reviewed package identity.

Run from the repository root with Python 3.12 or newer:

```sh
python vectors/WEXP-CORE-02-VECTORS-001/verify.py
python vectors/WEXP-CORE-02-VECTORS-001/corpus.py --check --output build/core02-vectors.json
```

The output path must not already exist. Integrity verification does not run an
appraiser or establish correctness of expectations. To check source bytes, use:

```sh
python vectors/WEXP-CORE-02-VECTORS-001/verify.py --source-xml path/to/draft-sergeev-wexp-core-02.xml
```

The source XML is in public repository `WEXP-dev/wexp-appraisal-core-spec` at
commit `8e93013418ee578ac5e522ca7a8d86346b4e2a99`, path
`drafts/core/02/draft-sergeev-wexp-core-02.xml`, SHA-256
`de983051a1c6ea51ea9b7f965fe9eabf2d97af92ab2f074781bd44e3f99c8782`.
CI retrieves that exact public revision. No private repository is a dependency.

## Logical encoding

The local JSON harness is not a WEXP wire format. Opaque atoms use exact Unicode
scalar text. Scoped atoms and extension keys are ordered two-element arrays;
sets and the capability map are arrays with logical set/map semantics. Null
represents unavailable, not an absent component. Booleans must not compare equal
to numbers. Do not normalize Unicode, URLs, case, atom-pair order or remove
unexpected duplicate output members while comparing results.

Input collections declared as mathematical sets must not contain repeated equal
members in this representation. Duplicate aggregate keys and duplicate capability
keys are retained as explicit mapping-error controls, not silently deduplicated.
Malformed JSON, duplicate JSON object members and resource-limit failures occur
before this logical representation and must not manufacture a Core appraisal.

The fixture profile is `draft-sergeev-wexp-core-02/fixture-1`, exactly as defined
by section 13. Positive extension controls apply a separately identified local
`wexp-core02-test-profile/extension-1`; they do not redefine that normative profile.
Its catalog is carried in the cases. Negative catalog-resolution controls are
explicitly invalid resolutions, not alternative definitions of the fixture.

## Traceability and comparison

Every case has either source anchors (defined below) or exact source sections and
a derivation. The reviewed requirement groups are local traceability identifiers,
not a complete registry of every normative requirement:

| Identifier / source anchor | Published section | Requirement group |
|---|---|---|
| `vectors` | 13 | C01-C16, complete fixture environment and comparison |
| `algorithm` | 8.4-8.5 | Complete twenty-component output and rejection projection |
| `normalized-input` | 6-6.1 | Input fields, scope, aggregates, registry and equality |
| `input-validity` | 6.2 | Structural versus mapping classification and precedence |
| `conformance` | 12 | Capability/status consistency, extension shape and binding |
| `supported-claims` | 8.1 | Exact support, qualifiers, basis and limitations |
| `qualifiers` | 4.3-4.4 | Exact qualifier conditions and admissible claims |
| `verdict` | 8.2-8.3 | Exact support, blocking counters and structural explanation |
| `reasons` | 8.6 | Claim-required diagnostics and projection |
| `boundary-ceiling` | 7 | Exclusion without manufacturing support |
| `compatibility` | Appendix B | Explicit semantic-version selection; no relabeling |

For P01-P25, `source_sections` are the reviewed traceability identifiers. These
cases cover malformed extension pairs and precedence, valid extension preservation,
combined qualifiers, grounding preservation, profile gap classification, descriptive
recorder relations, and canonically equivalent but unequal Unicode target atoms.

A consumer must compare the complete decoded result, including unavailable values,
all diagnostics, context, scope, basis and limits. Verdict-only agreement is not
full-result agreement. Independent tools may expand the same frozen definitions;
this does not make the author-side expectations an independent external review.

## Origin and boundaries

The first 64 cases derive from same-project private preparation, reviewed against
the posted text for this new package. The preparation XML was not the final
published XML; historical test counts are not imported as evidence for this
package. P01-P25 were authored against the posted contract before the new appraiser
run. The public source and expanded digest are self-contained.

Known scope limits: finite cases, no raw carrier authentication, no composition
profile execution, no arbitrary profile-equality implementation, no Coverage-00
or PostgreSQL validation. The published I-D remains authoritative if a test is wrong.
Repository-authored code follows the repository's Apache-2.0 license; the referenced
Internet-Draft retains its own notices and is not relicensed by this corpus.
