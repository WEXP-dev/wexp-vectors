# WEXP Core-01 vector index

Sixteen vectors, one per normative fixture C01-C16 of
[`draft-sergeev-wexp-core-01`](https://datatracker.ietf.org/doc/draft-sergeev-wexp-core/01/).
Expected outcomes are transcribed from the draft; an implementation's output
is never the source of one.

| Fixture | Vector | Classification | Expected code |
|---|---|---|---|
| C01 | [`WEXP-CORE-01-Q001-TV-0001`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0001.json) | `support-positive` | `—` |
| C02 | [`WEXP-CORE-01-Q001-TV-0002`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0002.json) | `support-above-claim-negative` | `E_MISSING_REQUIRED_EVIDENCE` |
| C03 | [`WEXP-CORE-01-Q001-TV-0003`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0003.json) | `qualifier-mismatch-negative` | `E_MISSING_REQUIRED_EVIDENCE` |
| C04 | [`WEXP-CORE-01-Q001-TV-0004`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0004.json) | `qualifier-mismatch-negative` | `E_MISSING_REQUIRED_EVIDENCE` |
| C05 | [`WEXP-CORE-01-Q001-TV-0005`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0005.json) | `qualifier-positive` | `—` |
| C06 | [`WEXP-CORE-01-Q001-TV-0006`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0006.json) | `support-below-claim-negative` | `E_MISSING_REQUIRED_EVIDENCE` |
| C07 | [`WEXP-CORE-01-Q001-TV-0007`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0007.json) | `boundary-negative` | `E_BASE_EXCEEDS_BOUNDARY` |
| C08 | [`WEXP-CORE-01-Q001-TV-0008`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0008.json) | `support-negative` | `E_MISSING_REQUIRED_EVIDENCE` |
| C09 | [`WEXP-CORE-01-Q001-TV-0009`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0009.json) | `claim-domain-fatal` | `—` |
| C10 | [`WEXP-CORE-01-Q001-TV-0010`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0010.json) | `counter-evidence-negative` | `E_COUNTER_EVIDENCE_UNRESOLVED` |
| C11 | [`WEXP-CORE-01-Q001-TV-0011`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0011.json) | `composition-positive` | `—` |
| C12 | [`WEXP-CORE-01-Q001-TV-0012`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0012.json) | `composition-limitation-positive` | `—` |
| C13 | [`WEXP-CORE-01-Q001-TV-0013`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0013.json) | `profile-gap-positive` | `E_IV_NOT_EVALUATED` |
| C14 | [`WEXP-CORE-01-Q001-TV-0014`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0014.json) | `counter-evidence-gap-negative` | `E_COUNTER_EVIDENCE_NOT_EVALUATED` |
| C15 | [`WEXP-CORE-01-Q001-TV-0015`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0015.json) | `counter-evidence-reason-negative` | `E_COUNTER_EVIDENCE_UNRESOLVED` |
| C16 | [`WEXP-CORE-01-Q001-TV-0016`](../vectors/WEXP-CORE-01-VECTORS-001/vectors/WEXP-CORE-01-Q001-TV-0016.json) | `profile-gap-unrelated-positive` | `—` |

## What each vector exercises

- **C01** — Exact intent support under an intent ceiling is accepted with relation equal.
- **C02** — Support above the asserted intent claim does not accept it; exact membership is required.
- **C03** — PROV support does not satisfy an asserted IV qualifier; the maximal alternative is incomparable.
- **C04** — IV support does not satisfy an asserted PROV qualifier; the maximal alternative is incomparable.
- **C05** — An exactly supported qualified invocation claim is accepted.
- **C06** — Without IV(execution), the asserted execution+IV claim is unsupported; both maximal alternatives sit structurally below it.
- **C07** — A supported execution finding above an accepted invocation ceiling yields E_BASE_EXCEEDS_BOUNDARY, not E_MISSING_REQUIRED_EVIDENCE.
- **C08** — With no base findings, the asserted observation claim is unsupported and downgraded.
- **C09** — An inadmissible intent+PROV claim is rejected via the fixed projection with E_CLAIM_OUT_OF_DOMAIN.
- **C10** — Unresolved-material counter-evidence affecting the exactly supported claim blocks acceptance without erasing support.
- **C11** — A composition-profile-emitted execution finding over chain T is accepted; the support entry basis is the premise union {bd,s1,s2,adj,w}.
- **C12** — L-boundary carries through to the support entry and inherited_limitations; the unexercised IV capability stays visible in evaluation_scope without creating a gap.
- **C13** — An affecting inherited profile gap is projected exactly and its limitation is inherited; it does not block acceptance.
- **C14** — A not-evaluated counter entry for the asserted claim blocks acceptance and yields the E_COUNTER_EVIDENCE_NOT_EVALUATED gap; the defeating entry for intent emits no reason for execution; both entries are preserved.
- **C15** — Applicable unresolved-material counter-evidence projects the Core status token plus its registered profile reason; the copied entry retains its scoped reason.
- **C16** — A profile gap affecting neither the asserted claim nor any SupportedClaims member is not projected, and its limitation is not inherited.
