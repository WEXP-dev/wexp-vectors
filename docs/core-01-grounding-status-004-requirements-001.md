# Core-01 set 004: reviewed requirements and bounded acceptance

Record: `S62-GSI-PR10-REVIEWED-REQUIREMENTS-001`.
Requirements review accepted: 2026-09-15. Documentary registration: 2026-09-18.
Status: `REVIEWED_FOR_PINNED_CORE01_VECTORS`; PR merge and release remain pending.

## Object and authority

This registry covers exactly three existing requirement IDs and the full expected
payloads of their existing vectors in [PR10](https://github.com/WEXP-dev/wexp-vectors/pull/10),
reviewed at `dc7a7ffc47556041e060c034bf8221ef5c654088`.
The later documentation commit has a different head and does not constitute
acceptance of that new head for merge.

Normative authority is the published
[Core-01 XML](https://github.com/WEXP-dev/wexp-spec/blob/b3465c4ec218389c9701e2fb225e8dc2f8aec234/drafts/core/01/draft-sergeev-wexp-core-01.xml),
103,095 bytes, SHA-256 `84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d`.
Section numbers below are paired with XML anchors. This registry records test
traceability; it does not create or amend specification requirements.

## Reviewed revision-specific entries

All three entries have status `REVIEWED_FOR_PINNED_CORE01_VECTORS`.
Existing identifiers retain their original spelling. Their names do not establish
that a registry review occurred before 2026-09-15.

| Existing requirement ID | Requirement exercised by the exact fixture | Normative anchors | Vector and complete expected result |
|---|---|---|---|
| `WEXP-CORE-01-V004-REQ-S4001` | For the normalized, consistent S4001 input, the supported, target-bound boundary with `grounding=attested` permits the stated execution claim. Appraisal preserves grounding; the grounding value introduces no additional §8 condition after successful ingress. This concerns the supplied fixture, not universal acceptance of every attestation in every context. | §6 `normalized-input`; §8.4 `algorithm`; §8.5 `appraisal-result`; §8.6 `reasons`; §13 common fixture. | `WEXP-CORE-01-V004-TV-4001`: full pinned `expected`; verdict `accept`, `boundary_grounding=attested`. |
| `WEXP-CORE-01-V004-REQ-S4002` | In S4002, `boundary_finding.status=supported` with `grounding=not-evaluated` violates pairing. With valid types and the other fixture conditions satisfied, Core rejects at ingress position 4. | §6 `normalized-input`, pairing paragraph; §6.2 `input-validity`, position 4; §8.4 `algorithm`, fixed rejection. | `WEXP-CORE-01-V004-TV-4002`: full fixed rejection projection; verdict `reject`, sole fatal `E_PROFILE_MAPPING_INVALID`. |
| `WEXP-CORE-01-V004-REQ-S4003` | In S4003, the same pairing violation precedes validly supplied `E_UNKNOWN_CRITICAL_SEMANTIC`. Rejection at position 4 prevents position 5 from adding a later reason. | §6 `normalized-input`; §6.2 `input-validity`, positions 4–5, supplied-fatal classification and prohibition on adding later-check results; §8.4 `algorithm`. | `WEXP-CORE-01-V004-TV-4003`: full fixed rejection projection; verdict `reject`, sole fatal `E_PROFILE_MAPPING_INVALID`; supplied token excluded from the result fatal set. |

For S4002/S4003, `evaluation_scope["boundary-grounding"]=not-evaluated` is
part of the fixture construction. Section 12 (`conformance`) governs grounding
under this capability. Setting its scope to `evaluated` would introduce another
position-4 violation and lose isolation of pairing. This is not a separate
negative scope-invariant test or a claim of full scope coverage.

The accepted object is each complete `expected` payload, not merely its verdict
or fatal-code summary. The carrier mapping of `unavailable` to JSON `null`
comes from the existing [Core-01 representation contract](https://github.com/WEXP-dev/wexp-spec/blob/b3465c4ec218389c9701e2fb225e8dc2f8aec234/representation/CORE-01-REPRESENTATION-CONTRACT-001.md).

## Exact identities

| Artifact | SHA-256 |
|---|---|
| Vector set 004 | `94cc33ac7758878924ffef451a41f92a71c15e5656df5b8f84dc4d40b655f848` |
| Descriptor | `7588c33304650f6839e0ac410bfe2a79126fa1ef4ff6928a9cf90b26a853c71a` |
| Profile | `64059dfa697a8ecc131195195a3735b571a6d7b5d806e4d63b4c8cbc3880b806` |
| [TV4001](../vectors/WEXP-CORE-01-VECTORS-004/vectors/WEXP-CORE-01-V004-TV-4001.json) | `3efef9dae5b2b023ed5669121ba15a8ff4be1f3446ecbbcd58f91e32a9851a60` |
| [TV4002](../vectors/WEXP-CORE-01-VECTORS-004/vectors/WEXP-CORE-01-V004-TV-4002.json) | `196275fd0392911cf82200bd7792e1242733b21b1727c31e658bf1180b424ce9` |
| [TV4003](../vectors/WEXP-CORE-01-VECTORS-004/vectors/WEXP-CORE-01-V004-TV-4003.json) | `aab0574708ac7f1164c5743d86a4b9d65a86f891daa5395380d4ef05cac210e5` |

The specification, descriptor, profile, vectors, SHA256SUMS and existing manifest
are unchanged by this registration. Sets 001–003 are unchanged.

## Decision provenance and limits

The Founder accepted `S62-GSI-PR10-ACCEPTANCE-CANDIDATE-001.md` on 2026-09-15,
SHA-256 `1da4bda204b4e8155861ead46589a62753fa7931f838838e16fb394b4f655c10`,
37,327 bytes. Its §7 accepts §3's mappings and complete pinned expectations
within §5's limits and authorizes this documentary registration. The acceptance
was recovered from conversation context; this record is not a digital signature
or exported transcript. The original candidate and decision provenance are
retained in the canonical private work repository at the pinned link recorded
below. Everything needed to interpret and execute these public vectors is
contained in this repository and the cited published specification.

- This is a new requirements review on 2026-09-15, not a reconstructed review on
  2026-08-30. It is separate from the earlier pre-reveal expectation freeze.
- The decision covers the supported-side fixture, positive control and fatal
  precedence control. `unsupported × not-evaluated` is absent. Complete pairing
  coverage and closure of S62-GSI are not established.
- The reverse implication `status=not-evaluated -> grounding=not-evaluated` and
  the three disputed cells are not decided by this review.
- Q8 `HOLD_FOUNDER_REQUIRED` remains. Bounded successor scope excludes every pair
  in which exactly one of status/grounding is `not-evaluated`, including these
  two negative fixtures. This published Core-01 review does not expand that scope.
- No merge, new vector-set release, engine change, or successor routing is
  authorized. SCR/MPC receives no normative authority from this review.
- No full Core-01 conformance or external independence of the two implementations
  is asserted. Historical reproduction is not new clean-room derivation.

The original [derivation record](core-01-grounding-status-004.md) is retained.
No engine was run for this documentation-only continuation.

Canonical decision provenance (private archive; not an execution dependency):
[S62-GSI-PR10-ACCEPTANCE-REGISTRATION-001](https://github.com/WEXP-dev/wexp-work/blob/17b531f56836bef2539e9b06b441ef346261ce24/design/s62-ear-001/pr10-acceptance-001/DECISION-001.md).
