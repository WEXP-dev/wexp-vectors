# Core-01 vector coverage plan 002

Frozen before any implementation was run. Every expected result below is derived
from published `draft-sergeev-wexp-core-01`, from
`CORE-01-KNOWN-ISSUES-001` where a known issue applies, and from
`CORE-01-REPRESENTATION-CONTRACT-001` where representation matters — never from
an engine.

`WEXP-CORE-01-VECTORS-002` **extends the coverage of**
`WEXP-CORE-01-VECTORS-001`. It does not replace the published Core-01
specification, and it does not modify the 001 set.

## Why these gaps exist

An independent implementation reached different verdicts from both public engines
on three constructions. None of the sixteen published vectors distinguished them:
no vector carried two qualifiers on one base, an unrelated over-ceiling finding,
or an accept with a non-empty diagnostic set. The two engines shared each defect,
so their agreement could not surface any of it. These vectors make each
distinction observable.

| # | Rule | Core section | 001 coverage | 002 vector | Expected class | Why needed |
|---|---|---|---|---|---|---|
| A | `A` ranges over the subsets of `Q(b)`; `(execution,{PROV,IV})` is admissible | §8.1 support construction; §4.4 admissible domain | none — no 001 vector carries two qualifiers on one base | `TV-2001` | accept, exact support of the two-qualifier state | distinguishes subset semantics from a singleton-only lift |
| B | boundary-exceeded row needs *a present asserted-base aggregate* deeper than the ceiling | §8.6 diagnostic matrix | none — 001 C07 exercises the asserted base itself | `TV-2002` | accept, empty diagnostic set | an unrelated deeper finding must not diagnose someone else's claim |
| C | control for B: the asserted base itself exceeds the ceiling | §8.6 | C07, but without a second unrelated finding present | `TV-2003` | downgrade + `E_BASE_EXCEEDS_BOUNDARY` | proves B narrowed the row rather than disabling it |
| D | accept = exact support **and** counter-evidence not blocking; nothing else | §8.4 / Verdict | none — no 001 vector pairs accept with a non-empty diagnostic set | `TV-2004` | accept with a non-empty diagnostic set | forbids re-adding a third accept condition |
| E | counter-evidence blocks only where its affected claims include the asserted claim or all-admissible-claims | §8.2 | C10, C14, C15 all target the asserted claim | `TV-2005` | accept — non-targeted entry does not propagate | control pair against C14 |
| F | a valid non-empty supplied `fatal_conditions` returns that set through the fixed rejection projection | §6.2 ingress check 5 | none — C09 exercises check 6 | `TV-2006` | reject, fixed rejection projection | ingress check 5 is distinct from check 6 |
| G | qualifier restricted to a base is inadmissible on another base | §4.4 admissible domain; profile `qualifier_admissibility` | none | `TV-2007` | reject + `E_CLAIM_OUT_OF_DOMAIN` | distinguishes domain rejection from missing evidence |
| H | a qualifier finding whose independence requirement is unmet does not lift a claim | §8.1; profile `qualifier_independence` | C03/C04 vary the claim, not the independence value | `TV-2008` | downgrade + `E_MISSING_REQUIRED_EVIDENCE` | the qualifier set must be built from *admitted* findings only |

## Not vectorized

| Rule | Reason |
|---|---|
| §6.2 ingress checks 1–4 — `E_MALFORMED_NORMALIZED_INPUT`, `E_UNSUPPORTED_SEMANTICS_VERSION`, `E_PROFILE_MAPPING_INVALID` | **NOT VECTORIZED — REQUIRES TOOLING SURFACE EXTENSION.** These tokens have no role in the public profile's registry and the reference tooling declares them outside its current surface. Authoring vectors for them would assert a surface the tooling does not claim. This is a tooling-scope decision, not a specification ambiguity. |
| KI-002 / C15 — non-Core token resolution without an applied profile identifier | **NOT VECTORIZED — REQUIRES ADJUDICATION.** KI-002 is OPEN. Vectorizing it would silently choose a `profile_identifiers` interpretation. |
| Remaining §8.6 rows beyond the profile's seven registered roles | **NOT VECTORIZED — REQUIRES TOOLING SURFACE EXTENSION.** Same reason as the ingress checks: the rule is determined, the public vocabulary is not. |

## Boundary

Coverage expands; this does not make 002 a conformance suite. §12's requirements
for that claim are assessed separately and are not satisfied by adding vectors.
