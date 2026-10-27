# Coverage-00 test entry point

[WEXP-COVERAGE-00-LOGIC-001](vectors/WEXP-COVERAGE-00-LOGIC-001/README.md)
is a bounded finite-model package tied to posted `draft-sergeev-wexp-coverage-00`
and rule set `coverage/0.2.0`. Its 12 fixed examples and additional enumerated
checks preserve the distinctions between complete, sound and exact claims.

It is separate from the Core-02 appraisal corpus. Known test-world populations
are inputs to this model, not observations established by a deployed collector.
The aggregation helper consumes already usable derivations; it is not the full
premise/rule evaluator and does not emit the complete CoverageResult contract.

No `pg-ledger/0.2.0` implementation conformance, PostgreSQL execution, capture
coverage, AAC mapping or new interop is established by these checks. Follow the
package's reproduction instructions and pinned-source workflow for its exact scope.
