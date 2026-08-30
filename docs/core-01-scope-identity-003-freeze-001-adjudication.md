# Set 003 — FREEZE-001 adjudication

## Status

    expectation freeze   WEXP-CORE-01-V003-EXPECTATION-FREEZE-001
    vector-set digest    272cd71cf9d2fb049b1a00d626004342362f16aa67480ade5231919b0e7063ff
    candidate commit     cfdd855f8dbf4aa3904363f52f01bbae8f73ef12
    date of rejection    2026-08-30
    status               REJECTED_BEFORE_ACCEPTANCE

These identities were publicly disclosed on a pull-request branch. They were
never accepted into `main`, and they are not historical published vector
identities. They are preserved here so that the disclosure has a record, and the
commit that carried them is left in place rather than amended away.

## What was wrong

FREEZE-001 expected a foreign-scoped aggregate to produce a **downgrade** with an
empty supported set, on the reasoning that §8.1 and §8.4 exclude such a finding
from support construction.

That reasoning is true and incomplete. §6.2 terminates the appraisal before §8 is
reached:

> A well-typed wexp-core-1 input that violates a cross-field invariant returns
> E_PROFILE_MAPPING_INVALID. Cross-field invariants include aggregate cardinality
> and keys, **exact target and context scope**, …

Exact scope is a cross-field invariant at ingress position 4. An input containing a
foreign-scoped aggregate is contract-invalid as a whole, and the correct result is
`reject` with `fatal_reasons = {E_PROFILE_MAPPING_INVALID}`. No supported-claim
construction happens at all, so no downgrade, and no
`E_MISSING_REQUIRED_EVIDENCE`: the early fatal branch wins.

## The specific error

FREEZE-001 recorded that the fatal disposition "needs a registered
`E_PROFILE_MAPPING_INVALID` role that the applied profile does not have, so it is
not representable here". That treated a Core-derived rejection branch as though it
were an optional profile capability, and then derived the expectation from what
the inherited profile vocabulary happened to contain.

§6.2 says the opposite:

> E_MALFORMED_NORMALIZED_INPUT, E_UNSUPPORTED_SEMANTICS_VERSION,
> E_PROFILE_MAPPING_INVALID, and E_CLAIM_OUT_OF_DOMAIN are **derived only by the
> ordered Core checks and are invalid as supplied members of fatal_conditions**.

The token is Core-derived. It never appears as a supplied member of
`fatal_conditions`, and the profile's job is to name it, not to permit it. The
correct response to a missing role was to declare it — as set 002's profile
already declares `claim_out_of_domain`, another derived-only token — not to weaken
the expectation to fit the vocabulary that was inherited.

## What was not the cause

- **No implementation output was used as the replacement oracle.** The correction
  comes from the ordered procedure in §6.2, re-read directly. Neither the public
  engines nor the privately repaired engines were consulted in deriving FREEZE-002,
  and neither had been run against the corrected cases when it was frozen.
- **Not implementation divergence.** Both public engines agree with each other on
  these inputs and are wrong; that was the original finding and it is unchanged.
- **Sets 001 and 002 were unaffected.** Their bytes, digests and evidence bundles
  are untouched by this adjudication and by the correction that follows it.

## Relationship to FREEZE-002

`WEXP-CORE-01-V003-EXPECTATION-FREEZE-002` replaces this candidate. FREEZE-001 was
not superseded after publication; it was rejected during pre-acceptance review,
which is the difference between a corrected record and a retracted one.
