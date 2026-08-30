# Core-01 vector set 003 — scope identity

Six vectors covering one requirement family: a finding contributes to
supported-claim construction only when it names the same target and evaluation
context as the appraisal input.

## Why this set exists

The requirement is stated three times in the specification, and no published
vector exercised it. Every finding in sets 001 and 002 — 58 scope-bearing
records across 25 vectors — uses the same target `T` and the same evaluation
context `C`. With the dimension constant, no input could tell an implementation
that checks scope apart from one that does not.

Two implementations did not check it, agreed with each other on every published
vector, and were compared differentially throughout. Their agreement was
accurate and uninformative: a differential harness detects divergent mistakes,
and a dimension that never varies produces no divergence.

The expectations below were derived from the specification and frozen before any
implementation was repaired against them.

## Freeze

    EXPECTATION-FREEZE ID       WEXP-CORE-01-V003-EXPECTATION-FREEZE-001
    derivation bundle sha256    03a5992df7f2be88ad17c5d4fb0acaac6da2853c27364b9b4a1b176361d6c783
    vector set sha256           272cd71cf9d2fb049b1a00d626004342362f16aa67480ade5231919b0e7063ff
    descriptor sha256           41f7ece37ba7fcae463b7cfd48ba8e1dcb902fab725884a34f9d3ee4a0c89bd1
    profile sha256              908a336ff0e49f8568801e304bdc1dc9e6130bdbd43999539d411e55fec5672c

Derived only from `draft-sergeev-wexp-core-01`, sha256 `84c0a164…`. Not derived
from any implementation, from differential agreement, or from repaired code.

## The requirement, as published

**§8.1**, on membership of the supported base set: a base is in B only if,
among the other conditions, "the finding names the same target and evaluation
context as the appraisal input".

**§8.4**, inside the admission predicate of the normative algorithm:

> for every base finding f, independently of the asserted claim: if f.target ==
> input.target and f.evaluation_context_ref == input.evaluation_context.id and
> f.target_binding == supported and …

**§8.1** again, for qualifiers: PROV and IV enter Q(b) only when the qualifier
finding passes its assessments "for the exact target and evaluation context".

**§6**, on what a foreign-scoped aggregate is: "A foreign-scoped aggregate is
not negative evidence for this appraisal." It is not evidence here at all, so it
neither supports a claim nor stands in for an aggregate that is genuinely absent.

## Vectors

### WEXP-CORE-01-V003-TV-3001 — scope-identity-control

    expectation sha256   5b36dc9074a1e8cf46ccb5f3ca9d7fba3c3fcadd79976521fd037aea5ee58fde
    verdict              accept
    asserted supported   true
    supported claims     [{"base": "execution", "qualifiers": []}]
    substantive          []

**Purpose.** Every scope component matches, so the execution finding is admitted and supports the asserted claim. Without this control the rest of the set would show only that something is refused, not that the refusal is selective.

**Derivation.** Section 8.1: the finding names the same target and evaluation context as the input, target binding and semantic validation are supported, the boundary is supported and target-bound, and the accepted ceiling admits execution. Section 8.2: exact membership with non-blocking counter-evidence gives accept.

### WEXP-CORE-01-V003-TV-3002 — foreign-target-negative

    expectation sha256   eccd7e9797765834ca499ad782e58ade0ff839df1dfb977919c4e40d988c870b
    verdict              downgrade
    asserted supported   false
    supported claims     []
    substantive          ["E_MISSING_REQUIRED_EVIDENCE"]

**Purpose.** The only base finding names a different action target. It is the sole candidate support, so acceptance is reachable only if the target identity requirement is not enforced.

**Derivation.** Section 8.1: a base is in B only if, among the other conditions, "the finding names the same target and evaluation context as the appraisal input". Section 8.4 states the same requirement inside the admission predicate itself: f.target == input.target and f.evaluation_context_ref == input.evaluation_context.id. Section 6 adds that "a foreign-scoped aggregate is not negative evidence for this appraisal" -- it is not evidence here at all, so it neither supports a claim nor stands in for an aggregate that is genuinely absent. Section 8.6 then reports the asserted aggregate as absent, and Section 8.2 gives downgrade because the asserted claim is not an exact member of SupportedClaims. Here the single execution finding names another target, so B is empty and no claim is supported.

### WEXP-CORE-01-V003-TV-3003 — foreign-context-negative

    expectation sha256   eccd7e9797765834ca499ad782e58ade0ff839df1dfb977919c4e40d988c870b
    verdict              downgrade
    asserted supported   false
    supported claims     []
    substantive          ["E_MISSING_REQUIRED_EVIDENCE"]

**Purpose.** The same shape through the other half of the scope: the finding names the right target under a different evaluation context. Paired with TV-3002 so neither half of the predicate can be dropped without a vector noticing.

**Derivation.** Section 8.1: a base is in B only if, among the other conditions, "the finding names the same target and evaluation context as the appraisal input". Section 8.4 states the same requirement inside the admission predicate itself: f.target == input.target and f.evaluation_context_ref == input.evaluation_context.id. Section 6 adds that "a foreign-scoped aggregate is not negative evidence for this appraisal" -- it is not evidence here at all, so it neither supports a claim nor stands in for an aggregate that is genuinely absent. Section 8.6 then reports the asserted aggregate as absent, and Section 8.2 gives downgrade because the asserted claim is not an exact member of SupportedClaims. Here the target matches and the evaluation context does not, which fails the second conjunct of the Section 8.4 predicate.

### WEXP-CORE-01-V003-TV-3004 — foreign-scope-negative

    expectation sha256   eccd7e9797765834ca499ad782e58ade0ff839df1dfb977919c4e40d988c870b
    verdict              downgrade
    asserted supported   false
    supported claims     []
    substantive          ["E_MISSING_REQUIRED_EVIDENCE"]

**Purpose.** Both scope components differ. An implementation that enforces neither, or only one, still admits nothing here.

**Derivation.** Section 8.1: a base is in B only if, among the other conditions, "the finding names the same target and evaluation context as the appraisal input". Section 8.4 states the same requirement inside the admission predicate itself: f.target == input.target and f.evaluation_context_ref == input.evaluation_context.id. Section 6 adds that "a foreign-scoped aggregate is not negative evidence for this appraisal" -- it is not evidence here at all, so it neither supports a claim nor stands in for an aggregate that is genuinely absent. Section 8.6 then reports the asserted aggregate as absent, and Section 8.2 gives downgrade because the asserted claim is not an exact member of SupportedClaims. Both conjuncts fail; either alone would already exclude the finding.

### WEXP-CORE-01-V003-TV-3005 — foreign-scope-strong-qualifier-negative

    expectation sha256   0d536dfd3fd25d9db7abe4f086a5e369dd023a5dc85d4ca557d00cbcf314e7e1
    verdict              downgrade
    asserted supported   false
    supported claims     []
    substantive          ["E_MISSING_REQUIRED_EVIDENCE"]

**Purpose.** Favourable target binding, semantic validation and independence on a foreign-scoped pair. Evidence quality is not a substitute for evidence identity.

**Derivation.** Section 8.1: a base is in B only if, among the other conditions, "the finding names the same target and evaluation context as the appraisal input". Section 8.4 states the same requirement inside the admission predicate itself: f.target == input.target and f.evaluation_context_ref == input.evaluation_context.id. Section 6 adds that "a foreign-scoped aggregate is not negative evidence for this appraisal" -- it is not evidence here at all, so it neither supports a claim nor stands in for an aggregate that is genuinely absent. Section 8.6 then reports the asserted aggregate as absent, and Section 8.2 gives downgrade because the asserted claim is not an exact member of SupportedClaims. Section 8.1 admits IV into Q(b) only when the IV finding passes its assessments "for the exact target and evaluation context", so a qualifier cannot rescue a base that was never admitted, and cannot be admitted itself on a foreign scope.

### WEXP-CORE-01-V003-TV-3006 — mixed-scope-no-inflation

    expectation sha256   bd41dfa481490dd808b7f3d9f80fc017c50a18a5420aec3ba82cfe361e70d76d
    verdict              accept
    asserted supported   true
    supported claims     [{"base": "invocation", "qualifiers": []}]
    substantive          []

**Purpose.** One in-scope invocation finding beside a stronger foreign-scoped execution finding. The in-scope claim must still be supported and the foreign one must add nothing beside it: exclusion is selective, not a blanket refusal of the whole input.

**Derivation.** Section 8.1: a base is in B only if, among the other conditions, "the finding names the same target and evaluation context as the appraisal input". Section 8.4 states the same requirement inside the admission predicate itself: f.target == input.target and f.evaluation_context_ref == input.evaluation_context.id. Section 6 adds that "a foreign-scoped aggregate is not negative evidence for this appraisal" -- it is not evidence here at all, so it neither supports a claim nor stands in for an aggregate that is genuinely absent. Section 8.6 then reports the asserted aggregate as absent, and Section 8.2 gives downgrade because the asserted claim is not an exact member of SupportedClaims. The invocation finding satisfies every condition and enters B. The execution finding names another target and does not, so SupportedClaims contains the invocation claim alone, the asserted invocation claim is an exact member, and Section 8.2 gives accept. An implementation that admitted the foreign finding would report a deeper supported claim than the evidence for this target supports.

## What this set does not cover

**The §6.2 ingress disposition.** §6 says a foreign-scoped aggregate "violates
the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID",
and §6.2 lists "exact target and context scope" among the cross-field invariants
of ingress position 4. That disposition is *fatal rejection of the whole input*,
which is stronger than the exclusion these vectors encode. It needs a registered
`E_PROFILE_MAPPING_INVALID` role that the applied profile does not have, so it is
not representable here and no vector asserts it. The two dispositions are
independent: §8.1 and §8.4 exclude the finding from support whether or not
ingress rejects the input, and that exclusion floor is what this set fixes.

**Boundary-finding scope.** §8.1 requires the boundary finding to be "scoped to
that same target and context" before its ceiling is usable. A distinguishing
vector for it is deliberately absent: an unusable boundary currently surfaces as
an implementation-level rejection rather than through the §8.6 boundary rows,
which is an already-declared known absence in the reference tooling. Encoding an
expectation for it here would test that separate absence rather than this one.

**Everything else.** Six vectors covering one requirement family. Sets 001 and
002 are unchanged and stand alongside this one; none of the three is a
conformance suite.
