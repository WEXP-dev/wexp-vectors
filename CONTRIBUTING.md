# Contributing vectors

Contributions are welcome when each expected result can be traced to a
requirement in a published WEXP specification. Published WEXP specifications
are authoritative; `wexp-ref` does not define expected behavior.

## Contribution requirements

For each proposed protocol vector:

1. Identify the exact WEXP document and revision that defines the expected behavior.
2. Cite one or more existing reviewed requirement IDs accepted by the schema. Do not invent a requirement to make a vector pass validation.
3. Select the class that matches the property being tested. Keep record structure separate from semantic verification.
4. Choose a stable, unique vector ID in the namespace enforced by the schema.
5. Make the input and expected result self-contained and implementation-neutral.
6. Add the vector to `manifests/vectors.json` with its exact SHA-256 digest and matching metadata.
7. Run the validator and unit tests documented in `README.md`.

If the specification is ambiguous, stop and document the ambiguity through the
specification review process. Do not infer expected semantics from an
implementation and do not use a vector to silently create new normative
meaning.

Schema examples must live under `examples/`, use the `WEXP-EXAMPLE-` ID namespace, and be classified exactly as `non-normative-schema-example`. They cannot cite fictional requirement IDs or be presented as protocol tests.

## Interop contributions

Only stable interop cases intended for release belong here. Experimental cases
belong in the pre-publication workspace.

An interop vector must:

- identify each external specification and its exact document revision, immutable commit, tag, or digest;
- state the external relationship as `REFERENCE`, `MAPPING`, or `DEPENDENCY` without upgrading conceptual similarity into a dependency;
- cite a reviewed mapping with `mapping_id`;
- state its assumptions;
- derive expected behavior from the applicable specifications and mapping, not from `wexp-ref` output;
- include everything needed to run the case without a private repository.

Floating revisions (`HEAD`, branches, `latest`, and equivalents) are not accepted.

## What review establishes

A merged vector may demonstrate the expected behavior for the requirements it
cites. Passing it does not prove complete WEXP correctness or independent
conformance. GitHub Actions runs repeatable checks; it does not define WEXP.

Unless explicitly documented otherwise, contributions are submitted under the
repository's Apache License 2.0. No contributor license agreement, copyright
assignment, or sign-off requirement is introduced by this statement.
