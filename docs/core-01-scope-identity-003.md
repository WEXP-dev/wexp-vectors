# Core-01 vector set 003 — scope identity

Seven vectors covering one requirement family: the normalized input's
cross-field contract that every aggregate names the same target and evaluation
context as the appraisal itself.

## The requirement, and where it takes effect

§6 binds the scope:

> The boundary finding, every base and qualifier aggregate, and every
> profile-gap entry have a target equal to the top-level target and an
> evaluation_context_ref equal to the top-level evaluation-context identifier.
> A foreign-scoped aggregate is not negative evidence for this appraisal; it
> violates the normalized-input cross-field contract and produces
> E_PROFILE_MAPPING_INVALID.

§6.2 places it among the ordered rejection checks, at position 4:

> A well-typed wexp-core-1 input that violates a cross-field invariant returns
> E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate
> cardinality and keys, **exact target and context scope**, …

So the check terminates the appraisal. §8 support construction never runs, and
no substantive reason or evaluation gap is produced: the early fatal branch
wins, and §8.4's fixed rejection projection is the result.

§8.1 and §8.4 separately refuse to admit such a finding — "the finding names
the same target and evaluation context as the appraisal input", and
`f.target == input.target and f.evaluation_context_ref ==
input.evaluation_context.id`. A complete appraisal never reaches that test,
which is why the vectors here test the ordered procedure and not the predicate.

`E_PROFILE_MAPPING_INVALID` is derived only by the ordered Core checks and is
invalid as a supplied member of `fatal_conditions`. The applied profile names
the token Core emits; it does not grant permission to reject.

## Why this set exists

No published vector exercised the contract. Across sets 001 and 002 all 58
scope-bearing records use the same target `T` and the same evaluation context
`C`. With the dimension constant, no input could tell an implementation that
enforces the contract apart from one that does not — and two implementations
that both skipped it agreed with each other on every published vector. A
differential harness detects divergent mistakes; a dimension that never varies
produces no divergence to detect.

## Freeze

    EXPECTATION-FREEZE ID       WEXP-CORE-01-V003-EXPECTATION-FREEZE-002
    derivation bundle sha256    742fcb8a14cd111151aa0b7b5e0c4f06459d4c3a141cd620c605f31aab298d4a
    vector set sha256           338b14cffdb846ca2aec4574ad9e52dd3615e15c8de7861d922e4323989440cd
    descriptor sha256           eac0db02ce6c5da0c2359fd21c618c123e3c4c3595526e6380f9a0b2d24459f0
    profile sha256              91c4dc6c2c8d866bbf32aa0f19b4fb85d59b1de4f2a85bdb89831f0d84155364
    specification sha256        84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d

Derived from published Core-01 only. Not from the public engines, not from any
privately repaired engine, and not from differential agreement. Frozen before
any implementation was run against these cases.

An earlier candidate, `WEXP-CORE-01-V003-EXPECTATION-FREEZE-001`, was rejected
during pre-acceptance review for expecting a downgrade where the ordered checks
require a fatal reject. It is recorded in
[`core-01-scope-identity-003-freeze-001-adjudication.md`](core-01-scope-identity-003-freeze-001-adjudication.md).

## Vectors

### WEXP-CORE-01-V003-TV-3001 — scope-identity-control

    expectation sha256   5b36dc9074a1e8cf46ccb5f3ca9d7fba3c3fcadd79976521fd037aea5ee58fde
    verdict              accept
    fatal reasons        []

**Purpose.** Every applicable scope matches, so the input satisfies the cross-field contract, reaches Section 8, and the execution finding supports the asserted claim. Without this control the set would show only that inputs are refused, not that refusal is selective.

**Derivation.** Section 6: every aggregate carries the top-level target and evaluation-context identifier, so the cross-field invariant holds and the ordered checks pass. Section 8.1: the finding names the same target and evaluation context as the input, binding and semantic validation are supported, the boundary is supported and target-bound, and the accepted ceiling admits execution. Section 8.2: exact membership with non-blocking counter-evidence gives accept.

### WEXP-CORE-01-V003-TV-3002 — base-foreign-target-fatal

    expectation sha256   0953c8327024eb71772e3adc7916f17b45ed6ff6f64eae81fff38e3c1bff5fbd
    verdict              reject
    fatal reasons        ["E_PROFILE_MAPPING_INVALID"]

**Purpose.** A base aggregate names a different action target. The input violates the cross-field contract and is rejected before any claim is appraised.

**Derivation.** Section 6.2 states the Core rejection checks as an ordered sequence, and exact target and context scope is one of the cross-field invariants at position 4: "A well-typed wexp-core-1 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate cardinality and keys, exact target and context scope, ..." Section 6 says why: "The boundary finding, every base and qualifier aggregate, and every profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level evaluation-context identifier. A foreign-scoped aggregate is not negative evidence for this appraisal; it violates the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID." The check terminates the appraisal, so Section 8 support construction never runs and no substantive reason or evaluation gap is produced. Section 8.4 gives the fixed rejection projection: every input-derived component is unavailable and every derived set is empty. E_PROFILE_MAPPING_INVALID is derived only by the ordered Core checks and is invalid as a supplied member of fatal_conditions, so the profile names it rather than permitting it. Here a base aggregate carries a target other than the top-level target.

### WEXP-CORE-01-V003-TV-3003 — base-foreign-context-fatal

    expectation sha256   0953c8327024eb71772e3adc7916f17b45ed6ff6f64eae81fff38e3c1bff5fbd
    verdict              reject
    fatal reasons        ["E_PROFILE_MAPPING_INVALID"]

**Purpose.** The same violation through the other half of the scope: the right target under a different evaluation context. Paired with TV-3002 so neither equality conjunct can be dropped without a vector noticing.

**Derivation.** Section 6.2 states the Core rejection checks as an ordered sequence, and exact target and context scope is one of the cross-field invariants at position 4: "A well-typed wexp-core-1 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate cardinality and keys, exact target and context scope, ..." Section 6 says why: "The boundary finding, every base and qualifier aggregate, and every profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level evaluation-context identifier. A foreign-scoped aggregate is not negative evidence for this appraisal; it violates the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID." The check terminates the appraisal, so Section 8 support construction never runs and no substantive reason or evaluation gap is produced. Section 8.4 gives the fixed rejection projection: every input-derived component is unavailable and every derived set is empty. E_PROFILE_MAPPING_INVALID is derived only by the ordered Core checks and is invalid as a supplied member of fatal_conditions, so the profile names it rather than permitting it. Here a base aggregate carries an evaluation_context_ref other than the top-level evaluation-context identifier.

### WEXP-CORE-01-V003-TV-3004 — qualifier-foreign-scope-fatal

    expectation sha256   0953c8327024eb71772e3adc7916f17b45ed6ff6f64eae81fff38e3c1bff5fbd
    verdict              reject
    fatal reasons        ["E_PROFILE_MAPPING_INVALID"]

**Purpose.** The base aggregate is in scope and only the qualifier aggregate is foreign. Section 6 names qualifier aggregates explicitly, so a favourable base does not rescue the input.

**Derivation.** Section 6.2 states the Core rejection checks as an ordered sequence, and exact target and context scope is one of the cross-field invariants at position 4: "A well-typed wexp-core-1 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate cardinality and keys, exact target and context scope, ..." Section 6 says why: "The boundary finding, every base and qualifier aggregate, and every profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level evaluation-context identifier. A foreign-scoped aggregate is not negative evidence for this appraisal; it violates the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID." The check terminates the appraisal, so Section 8 support construction never runs and no substantive reason or evaluation gap is produced. Section 8.4 gives the fixed rejection projection: every input-derived component is unavailable and every derived set is empty. E_PROFILE_MAPPING_INVALID is derived only by the ordered Core checks and is invalid as a supplied member of fatal_conditions, so the profile names it rather than permitting it. Section 6 binds "every base and qualifier aggregate" to the top-level scope, so a foreign-scoped qualifier aggregate violates the contract on its own. Section 8.1 would separately refuse to admit it into Q(b) "for the exact target and evaluation context", but the appraisal never reaches that test.

### WEXP-CORE-01-V003-TV-3005 — boundary-foreign-scope-fatal

    expectation sha256   0953c8327024eb71772e3adc7916f17b45ed6ff6f64eae81fff38e3c1bff5fbd
    verdict              reject
    fatal reasons        ["E_PROFILE_MAPPING_INVALID"]

**Purpose.** The boundary aggregate is foreign-scoped while every finding is in scope. Section 6 binds the boundary finding to the same contract as the aggregates.

**Derivation.** Section 6.2 states the Core rejection checks as an ordered sequence, and exact target and context scope is one of the cross-field invariants at position 4: "A well-typed wexp-core-1 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate cardinality and keys, exact target and context scope, ..." Section 6 says why: "The boundary finding, every base and qualifier aggregate, and every profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level evaluation-context identifier. A foreign-scoped aggregate is not negative evidence for this appraisal; it violates the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID." The check terminates the appraisal, so Section 8 support construction never runs and no substantive reason or evaluation gap is produced. Section 8.4 gives the fixed rejection projection: every input-derived component is unavailable and every derived set is empty. E_PROFILE_MAPPING_INVALID is derived only by the ordered Core checks and is invalid as a supplied member of fatal_conditions, so the profile names it rather than permitting it. Section 6 opens the sentence with "The boundary finding", so its scope is bound by the same cross-field invariant. Section 8.1 additionally requires the boundary to be "scoped to that same target and context" before its ceiling is usable, but that test is downstream of the rejection.

### WEXP-CORE-01-V003-TV-3006 — profile-gap-foreign-scope-fatal

    expectation sha256   0953c8327024eb71772e3adc7916f17b45ed6ff6f64eae81fff38e3c1bff5fbd
    verdict              reject
    fatal reasons        ["E_PROFILE_MAPPING_INVALID"]

**Purpose.** A profile-supplied gap entry is foreign-scoped. Section 6 binds profile-gap entries to the same contract as findings, and this category is otherwise untested anywhere in the corpus.

**Derivation.** Section 6.2 states the Core rejection checks as an ordered sequence, and exact target and context scope is one of the cross-field invariants at position 4: "A well-typed wexp-core-1 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate cardinality and keys, exact target and context scope, ..." Section 6 says why: "The boundary finding, every base and qualifier aggregate, and every profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level evaluation-context identifier. A foreign-scoped aggregate is not negative evidence for this appraisal; it violates the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID." The check terminates the appraisal, so Section 8 support construction never runs and no substantive reason or evaluation gap is produced. Section 8.4 gives the fixed rejection projection: every input-derived component is unavailable and every derived set is empty. E_PROFILE_MAPPING_INVALID is derived only by the ordered Core checks and is invalid as a supplied member of fatal_conditions, so the profile names it rather than permitting it. Section 6 names "every profile-gap entry" alongside the boundary finding and the aggregates, so a foreign-scoped gap entry violates the contract even though it carries a registered token and affects an admissible claim.

### WEXP-CORE-01-V003-TV-3007 — mixed-scope-fatal

    expectation sha256   0953c8327024eb71772e3adc7916f17b45ed6ff6f64eae81fff38e3c1bff5fbd
    verdict              reject
    fatal reasons        ["E_PROFILE_MAPPING_INVALID"]

**Purpose.** A fully valid in-scope invocation finding sits beside a foreign-scoped execution finding. One valid finding does not legalise an input that carries a foreign-scoped aggregate: the contract is a property of the input, not of the best aggregate in it.

**Derivation.** Section 6.2 states the Core rejection checks as an ordered sequence, and exact target and context scope is one of the cross-field invariants at position 4: "A well-typed wexp-core-1 input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate cardinality and keys, exact target and context scope, ..." Section 6 says why: "The boundary finding, every base and qualifier aggregate, and every profile-gap entry have a target equal to the top-level target and an evaluation_context_ref equal to the top-level evaluation-context identifier. A foreign-scoped aggregate is not negative evidence for this appraisal; it violates the normalized-input cross-field contract and produces E_PROFILE_MAPPING_INVALID." The check terminates the appraisal, so Section 8 support construction never runs and no substantive reason or evaluation gap is produced. Section 8.4 gives the fixed rejection projection: every input-derived component is unavailable and every derived set is empty. E_PROFILE_MAPPING_INVALID is derived only by the ordered Core checks and is invalid as a supplied member of fatal_conditions, so the profile names it rather than permitting it. The invocation aggregate satisfies every condition and would enter B on its own. It does not matter: the cross-field invariant is evaluated over the whole input at position 4, so the appraisal is rejected before B is constructed. An implementation that answered accept with the invocation claim here would be applying Section 8 to an input Section 6.2 had already refused.

## Scope of the set

Seven vectors covering one requirement family. Sets 001 and 002 are unchanged
and stand alongside this one. None of the three is a conformance suite, and
passing this one means agreement with the expectations it publishes — not that
the remaining §6.2 cross-field families, or the rest of the Core-01 surface, are
covered anywhere.
