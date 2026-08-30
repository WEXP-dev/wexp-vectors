# Implementing WEXP

A route for someone building their own WEXP implementation, from outside this
project.

There is no certification here, no badge, no endorsement, and no conformance
programme. There is a specification, a published set of expectations derived
from it, and a way to report what your implementation did.

## 1. Read the specification, not this repository

The current specification state is
[`draft-sergeev-wexp-core-01`](https://datatracker.ietf.org/doc/draft-sergeev-wexp-core/01/),
an Internet-Draft. It is not an Internet Standard, it has not been adopted by an
IETF working group, and being posted is neither of those things.

The authoritative artifact is the XML, published unchanged in
[`wexp-spec`](https://github.com/WEXP-dev/wexp-spec):

    draft-sergeev-wexp-core-01.xml
    sha256  84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d

Each Core-01 vector set binds that exact digest in its `descriptor.json`, so you
can check offline that the expectations you are running were derived from the
specification you are reading.

`wexp-spec` also carries a project-maintained known-issues record for `-01`. It
is not an RFC Editor erratum and changes no published byte, but an implementer
should read it before concluding that a disagreement is theirs.

## 2. Know which expectations are accepted

Accepted expectations are the vector sets on `main` in this repository. A set on
a branch or in an open pull request is not accepted, however complete it looks —
`WEXP-CORE-01-V003-EXPECTATION-FREEZE-001` was publicly visible on a branch and
was rejected in review before acceptance.

| Set | Vectors | Set digest |
| --- | --- | --- |
| `WEXP-CORE-01-VECTORS-001` | 16 | `e315b6055148dbf05c6104c57feb991104b1ae6a47741a99cde5eb50d1900daf` |
| `WEXP-CORE-01-VECTORS-002` | 9 | `8b2dfd5ac6f983201f8869c331b58936e3378f382a3a989b9a63c8d85791facf` |
| `WEXP-CORE-01-VECTORS-003` | 7 | `338b14cffdb846ca2aec4574ad9e52dd3615e15c8de7861d922e4323989440cd` |

The manifests under [`manifests/`](manifests/) are the identities to pin. Do not
pin a branch.

## 3. Understand how an expectation was determined

Every expected result is transcribed or derived from published specification
text, never from observed implementation behaviour. Set 001 transcribes fixtures
the draft states outright. Sets 002 and 003 derive expectations from normative
text that does not spell the case out, and the derivation is published in full,
per vector, with the section each expectation rests on.

Every expectation was frozen, with its digest, **before** any engine was run
against it. That ordering is the point: an expectation recorded first cannot
have been fitted to an implementation afterwards.

Where a vector and the specification disagree, the specification wins and the
vector is a defect. That has happened, and the record is public:

- [`docs/core-01-set-002-first-run.md`](docs/core-01-set-002-first-run.md) —
  on `WEXP-CORE-01-V002-TV-2008` two engines agreed with each other and both
  differed from the derivation. The expectation was left alone and the engines
  were corrected. Agreement between implementations did not establish
  correctness.
- [`docs/core-01-scope-identity-003-freeze-001-adjudication.md`](docs/core-01-scope-identity-003-freeze-001-adjudication.md)
  — a candidate expectation freeze was rejected during pre-acceptance review,
  and the corrected freeze was derived from the specification text before any
  implementation was repaired against it.

## 4. Make your run reproducible

Record enough that somebody else can repeat it without asking you anything:

- the exact `wexp-vectors` commit and the set digest you ran;
- the specification digest that set binds;
- your implementation's own exact identity;
- the environment, and the exact command;
- your result for every vector, including the ones you did not pass.

Compare against the expectation as published. A comparison that normalizes away
a difference is not a comparison.

The repository validates itself; the commands are in
[`README.md`](README.md#clone-and-validate-locally).

## 5. Publish the parts that let someone disagree with you

If you want a result to be usable by anyone else, publish:

- **what you implemented, and what you did not.** A declared partial surface
  with enumerated absences is a real, useful result. An unstated one is not.
- **your profile** — the tokens your implementation registers and the roles it
  gives them. Two implementations can differ on a diagnostic purely because
  their profiles register different tokens, and that difference is invisible
  unless both are stated.
- **your disagreements**, with your reasoning. A disagreement traced to
  specification text is the most useful thing you can publish.

## 6. Report it

- A vector you believe is wrong, or an expectation whose derivation you can
  refute from specification text: open an issue in this repository. Cite the
  section. A defect report that names the text beats one that names an
  implementation.
- A specification defect: `wexp-spec`.
- A question about how your system's evidence maps to a bounded WEXP claim:
  that is an interoperability question, and it goes to
  [`interop-test-lab`](https://github.com/WEXP-dev/interop-test-lab/blob/main/START-HERE.md).

## 7. What passing does not establish

Passing every vector in every accepted set does not establish:

- conformance, certification, or a pass mark of any kind;
- complete Core appraisal — the sets cover what they cover, and no set is a
  conformance suite;
- interoperability with any other implementation;
- IETF acceptance, adoption, or endorsement;
- that any particular execution claim is true.

It establishes that your implementation agreed with expectations this repository
derived from the specification, on the cases those expectations cover.

## 8. What "independently maintained" means here

The project reports independent implementation status honestly, so the term has
to mean something narrow.

An implementation this project would describe as **independently maintained** is
one that:

1. is maintained by someone other than this project and its authors;
2. derives its behaviour from the published specification rather than from
   `wexp-ref`'s source;
3. is publicly inspectable;
4. publishes its own results under its own identity.

`wexp-ref` contains two structurally separate engines and a comparator. They are
maintained within the same project. Their agreement is useful differential
evidence — and `TV-2008` is the case where it was not enough — but it is not
independent implementation validation, and this project does not report it as
one.

At the time of writing, no independently maintained implementation has been
published. If you publish one, say so in an issue here and the project's public
status will say so too.
