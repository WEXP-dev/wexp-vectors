# Core-01 vector set 002 — expectation derivation record

Every expected appraisal below was derived from published text before either
public engine was run against it. The derivation is the primary artifact; the
vector files are its mechanical encoding. Where an engine and a derivation
disagree, this record is what gets re-examined first — but it is the engine, not
the expectation, that is presumed wrong until the derivation is shown to be.

## Freeze

    EXPECTATION-FREEZE ID       WEXP-CORE-01-V002-EXPECTATION-FREEZE-001
    derivation bundle sha256    18f6f8ebd0a58ea585e3bc407eb6d86a5f9e00fa50ef206d80fa5c6aaaccbf89
    vector set                  WEXP-CORE-01-VECTORS-002
    vector set sha256           aeaa790dfe37d47880b6d7c35863aedbaf9f3328f010b21db05373d8a1a9f21f
    descriptor sha256           194e19e91c15335e86cb91be959288d2281e1dc18dd16d47232b118b0c05813d
    profile sha256              1cb19dbe2f27ee95ba83aa37e82e8880eef43354c9c2f25c2b2857a38a4398f9
    manifest                    manifests/core-01-vectors-002.json

Derived only from:

- `draft-sergeev-wexp-core-01`, sha256 `84c0a164…`, the bytes bundled at
  `vectors/WEXP-CORE-01-VECTORS-002/spec/draft-sergeev-wexp-core-01.xml`
- `CORE-01-KNOWN-ISSUES-001` in `wexp-spec`
- `CORE-01-REPRESENTATION-CONTRACT-001` in `wexp-spec`

Not derived from `wexp-ref`, from any external implementation, or from any
private qualification candidate. The per-vector expectation digests below fix
that claim to specific bytes.

## Vectors

### WEXP-CORE-01-V002-TV-2001 — multi-qualifier-positive

    expectation sha256   0c2fab8e5d6aeb2c45c70c52d613c6b003362a32da395dcecf87c3617639aece
    verdict              accept
    asserted supported   true
    substantive          []
    gaps                 []
    fatal                []

**Input.** Asserted claim `{"base": "execution", "qualifiers": ["PROV", "IV"]}`, boundary
ceiling `execution`.

**Purpose.** Both PROV and IV are admitted on a supported execution base, so every subset of Q(execution) is supported, including the two-qualifier state.

**Derivation.** Section 8.1: A ranges over the subsets of the admitted qualifier set Q(b). Section 4.4 lists (execution,{PROV,IV}) as admissible because PROV is present only on execution. Section 8.2: the asserted claim is an exact member of SupportedClaims and counter-evidence does not block that exact claim, so the verdict is accept. Never derived from an engine.

### WEXP-CORE-01-V002-TV-2002 — unrelated-over-ceiling-positive

    expectation sha256   bdd6ab83fc952bf76b7ea26ff98db5200460e7993a27e7dafc58dad4f8489b12
    verdict              accept
    asserted supported   true
    substantive          []
    gaps                 []
    fatal                []

**Input.** Asserted claim `{"base": "intent", "qualifiers": []}`, boundary
ceiling `intent`.

**Purpose.** An execution finding sits above an intent ceiling while the asserted intent claim is supported. The unrelated finding is simply unsupported; it places no diagnostic on the asserted claim.

**Derivation.** Section 8.6: the boundary-exceeded row requires a usable boundary and a present asserted-base aggregate whose base is deeper than the ceiling. The asserted base is intent, which is not deeper than the intent ceiling, so the row does not apply to it. Section 8.2: accept is exact membership plus counter-evidence not blocking; the Section 8.4 algorithm tests exactly those two conditions, so a diagnostic set is not a third one. Never derived from an engine.

### WEXP-CORE-01-V002-TV-2003 — asserted-base-over-ceiling-negative

    expectation sha256   c2fac924da20623a71547802bdde1af42b43d68136cab43d00fba228931f0244
    verdict              downgrade
    asserted supported   false
    substantive          ["E_BASE_EXCEEDS_BOUNDARY"]
    gaps                 []
    fatal                []

**Input.** Asserted claim `{"base": "execution", "qualifiers": []}`, boundary
ceiling `intent`.

**Purpose.** The asserted execution claim is itself deeper than the intent ceiling, so the boundary-exceeded row applies and the claim is not supported.

**Derivation.** Section 8.6: a present asserted-base aggregate whose base is deeper than the ceiling produces E_BASE_EXCEEDS_BOUNDARY, and consequently not E_MISSING_REQUIRED_EVIDENCE. Section 8.2: the asserted claim is admissible but not exactly supported, so the verdict is downgrade. Control for TV-2002: proves the row was narrowed, not disabled. Never derived from an engine.

### WEXP-CORE-01-V002-TV-2005 — counter-evidence-non-targeted-positive

    expectation sha256   84e0594430250690d3a9a76d9d0f612dbd8989a1dc013c0edc6f4d53a60406cc
    verdict              accept
    asserted supported   true
    substantive          []
    gaps                 []
    fatal                []

**Input.** Asserted claim `{"base": "invocation", "qualifiers": []}`, boundary
ceiling `invocation`.

**Purpose.** A not-evaluated counter-evidence entry targets an observation claim that is not the asserted claim, so it does not block acceptance of the asserted invocation claim.

**Derivation.** Section 8.2: counter-evidence blocks only for entries whose affected claims include the asserted claim or all-admissible-claims. The entry names observation, and the asserted claim is invocation, so the entry does not apply. Control pair against published fixture C14, whose entry does target the asserted claim. Never derived from an engine.

### WEXP-CORE-01-V002-TV-2006 — supplied-fatal-rejection

    expectation sha256   9a6b3ca0ff6aaf333855278bc496a3a9ca5dfeb77594a73ebfe43600070a05f1
    verdict              reject
    asserted supported   false
    substantive          []
    gaps                 []
    fatal                ["E_UNKNOWN_CRITICAL_SEMANTIC"]

**Input.** Asserted claim `{"base": "invocation", "qualifiers": []}`, boundary
ceiling `invocation`.

**Purpose.** A structurally usable input carries a valid supplied fatal condition, so Core returns that complete set through the fixed rejection projection without appraising the otherwise-supported claim.

**Derivation.** Section 6.2: if the structurally usable input has a non-empty valid fatal_conditions set, Core returns that complete set through the fixed rejection projection; this check precedes the inadmissible-claim check. E_UNKNOWN_CRITICAL_SEMANTIC is one of the Core-defined supplied fatal members and is registered by the applied profile. Section 8.4 gives the projection, whose input-derived components carry unavailable, represented as JSON null per R-001. Distinguishes ingress check 5 from check 6, which published fixture C09 covers. Never derived from an engine.

### WEXP-CORE-01-V002-TV-2007 — qualifier-domain-fatal

    expectation sha256   d1213fbb49683e4771952fe708cf745bee102304a81fc53f09867eeed3e33588
    verdict              reject
    asserted supported   false
    substantive          []
    gaps                 []
    fatal                ["E_CLAIM_OUT_OF_DOMAIN"]

**Input.** Asserted claim `{"base": "invocation", "qualifiers": ["PROV"]}`, boundary
ceiling `invocation`.

**Purpose.** PROV is admissible only on execution, so an asserted (invocation,{PROV}) claim is outside the admissible domain.

**Derivation.** Section 4.4: a claim is admissible only if PROV is absent or the base is execution; an asserted claim outside this domain is rejected with E_CLAIM_OUT_OF_DOMAIN, and an appraiser must not silently delete the invalid qualifier and reinterpret the assertion. Section 6.2 check 6 places this after the supplied-fatal check. Section 8.4 gives the fixed rejection projection, whose input-derived components carry the logical value unavailable, represented per R-001 as JSON null. Never derived from an engine.

### WEXP-CORE-01-V002-TV-2008 — gap-only-downgrade

    expectation sha256   8ef4e6d2c451eb5b10c383d3782edb5582a0eeca7327360efac3f8f33dead179
    verdict              downgrade
    asserted supported   false
    substantive          []
    gaps                 ["E_IV_NOT_EVALUATED"]
    fatal                []

**Input.** Asserted claim `{"base": "invocation", "qualifiers": ["IV"]}`, boundary
ceiling `invocation`.

**Purpose.** The asserted IV qualifier carries a not-evaluated independence assessment, so IV is not admitted, the asserted claim is not exactly supported, and the only diagnostic is a gap. The verdict must still be downgrade although the substantive set is empty.

**Derivation.** Section 8.1 admits IV only when independence_validation is supported, so IV is absent from Q(invocation) and (invocation,{IV}) is not in SupportedClaims. Section 8.6 gives exactly one row, the gap E_IV_NOT_EVALUATED for an asserted IV independence assessment that is not-evaluated; no substantive row applies because the aggregate is present, bound and semantically supported. Section 8.2 makes accept conditional on exact membership and non-blocking counter-evidence alone, so an empty substantive set does not make this accept. This separates the Core-derived gap path from published fixture C13, whose identical token is a profile-supplied gap on a claim that remains supported. Never derived from an engine.

## Derivation findings

Three expectations were wrong when first drafted and were corrected against the
published text before the freeze. They are recorded because a derivation record
that only shows the surviving answers hides how much of the work was correction.

**The verdict rule is Section 8.2, not Section 8.4.** Three derivations cited
Section 8.4 for the accept condition. Section 8.4 is the normative algorithm;
Section 8.2 is where `accept` is defined. The stated condition was right and the
citation was wrong, which is the more dangerous of the two failures: a reader
checking the citation would have found an algorithm rather than a rule.

**`E_INDEPENDENCE_NOT_ESTABLISHED` is not available under this profile.** The
independence vector was first drafted with `independence_validation` set to
`not-established` and an expected token of `E_MISSING_REQUIRED_EVIDENCE`. Both
were wrong. `not-established` is outside the profile's `independence` status
domain (`supported`, `unsupported`, `not-evaluated`, `not-applicable`), and the
matrix row for an absent aggregate does not apply to an aggregate that is
present. The profile registers seven roles and `E_INDEPENDENCE_NOT_ESTABLISHED`
is not one of them, so the `unsupported` reading was not reachable either. The
derivable case is a `not-evaluated` independence assessment, which is what
TV-2008 now carries.

**Support relations were being emitted as bare claims.** The authoring helper
silently ignored the computed relation set and wrote the supported-claim list
into `support_relations`. Section 8.5 requires each relation to be a
`{supported_claim, relation}` pair and Section 8.3 requires one per *maximal*
supported claim. Every accept and downgrade expectation was affected. Neither
engine had been run at the time, so nothing about this was discovered by
comparison — it was found by reading Section 8.5 against the emitted shape.

The last of these is the reason the freeze happens before any engine runs and
not after. Had the engines been consulted first, agreement between them on a
wrongly shaped projection would have looked like confirmation.

## What this set deliberately leaves out

`E_INDEPENDENCE_NOT_ESTABLISHED`, `E_IV_NOT_SUPPORTED`, `E_PROV_NOT_SUPPORTED`,
`E_PROV_NOT_EVALUATED`, `E_BASE_NOT_EVALUATED`, `E_EXACT_CLAIM_NOT_SUPPORTED`,
`E_EVIDENCE_NOT_BOUND`, `E_BOUNDARY_NOT_SUPPORTED`, `E_BOUNDARY_NOT_EVALUATED`
and `E_COUNTER_EVIDENCE_DEFEATING` are Core-defined matrix tokens with no role in
this profile's registry. A vector expecting one would be testing a profile that
does not exist rather than the specification. Extending the registry is a
separate decision with its own review; it is not smuggled in through a vector
set.

`E_EVIDENCE_COVERAGE_MISMATCH`, `E_CHAIN_UNBOUND`, `E_COMPOSITION_WARRANT_MISSING`
and `E_COMPOSITION_NOT_EVALUATED` are unregistered here too, but for a different
reason: Section 8.6 routes them through the profile-reason and profile-gap paths
rather than emitting them from a matrix row, so a vector for them would be
exercising a composition profile this set does not define.

The Section 6.2 ingress checks 1 to 4 — `E_MALFORMED_NORMALIZED_INPUT`,
`E_UNSUPPORTED_SEMANTICS_VERSION` and `E_PROFILE_MAPPING_INVALID` — are likewise
unregistered here. Their absence is a tooling-scope limit, not a gap in the
specification.

`KI-002` remains open and unadjudicated, so no vector in this set encodes an
expectation that depends on how it is resolved.
