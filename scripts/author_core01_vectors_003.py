"""Author the WEXP-CORE-01-VECTORS-003 seed.

Every expected result is derived from published Core-01. No engine is consulted
here, and none was consulted before these expectations were frozen: the omission
these vectors distinguish was found by reading Section 8.1 and Section 8.4
against two implementations that both passed every previously published vector.
"""
import copy, hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build"
SET002 = ROOT / "vectors/WEXP-CORE-01-VECTORS-002"
profile = json.loads((SET002 / "profile.json").read_bytes())
sample = json.loads((SET002 / "vectors/WEXP-CORE-01-V002-TV-2001.json").read_bytes())
SCOPE = sample["input"]["evaluation_scope"]
REPR = sample["input"]["representation"]

TARGET, CONTEXT = "T", "C"
FOREIGN_TARGET, FOREIGN_CONTEXT = "T-other", "C-other"

def ensure(p):
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def base_finding(b, target=TARGET, ctx=CONTEXT):
    return {"base": b, "basis_refs": [f"{b}-{target}"], "evaluation_context_ref": ctx,
            "limitations": [], "reasons": [], "semantic_validation": "supported",
            "target": target, "target_binding": "supported"}

def qual_finding(b, q, target=TARGET, ctx=CONTEXT):
    return {"qualifier": q, "qualified_base": b, "basis_refs": [f"{q.lower()}-{target}"],
            "evaluation_context_ref": ctx,
            "independence_validation": "not-applicable" if q == "PROV" else "supported",
            "limitations": [], "reasons": [], "semantic_validation": "supported",
            "target": target, "target_binding": "supported"}

def make_input(asserted, ceiling, bases, quals=()):
    return {
        "asserted_claim": asserted, "base_findings": list(bases),
        "boundary_finding": {"basis_refs": ["bd"], "ceiling_base": ceiling,
            "evaluation_context_ref": CONTEXT, "grounding": "attributed", "limitations": [],
            "reasons": [], "status": "supported", "target": TARGET, "target_binding": "supported"},
        "counter_evidence": [{"affected_claims": [], "basis_refs": [], "limitations": [],
                              "reasons": [], "status": "not-supplied"}],
        "evaluation_context": {"id": CONTEXT}, "evaluation_scope": copy.deepcopy(SCOPE),
        "fatal_conditions": [], "inherited_limitations": [], "profile_evaluation_gaps": [],
        "qualifier_findings": list(quals), "recorder_relations": [], "representation": REPR,
        "semantics_version": "wexp-core-1", "target": TARGET,
    }

def support_entry(claim, refs):
    return {"claim": claim, "basis_refs": list(refs), "limitations": []}

def rel(asserted, claim):
    order = profile["orderings"]["base"]
    ai, bi = order.index(asserted["base"]), order.index(claim["base"])
    aq, bq = set(asserted["qualifiers"]), set(claim["qualifiers"])
    if ai == bi and aq == bq: return "equal"
    if bi >= ai and aq <= bq: return "support-above-claim"
    if ai >= bi and bq <= aq: return "support-below-claim"
    return "incomparable"

def expected(inp, *, verdict, supported_claims, support_entries, asserted_supported,
             ceiling, substantive=()):
    maximal = supported_claims
    return {
        "asserted_claim": inp["asserted_claim"], "asserted_claim_supported": asserted_supported,
        "boundary_ceiling": ceiling, "boundary_grounding": "attributed",
        "counter_evidence": inp["counter_evidence"], "evaluation_context": inp["evaluation_context"],
        "evaluation_gap_entries": [], "evaluation_gaps": [], "evaluation_scope": inp["evaluation_scope"],
        "fatal_reasons": [], "inherited_limitations": [], "maximal_supported_claims": maximal,
        "recorder_relations": inp["recorder_relations"], "semantics_version": "wexp-core-1",
        "substantive_reasons": list(substantive), "support_entries": support_entries,
        "support_relations": [{"relation": rel(inp["asserted_claim"], m), "supported_claim": m}
                              for m in maximal],
        "supported_claims": supported_claims, "target": inp["target"], "verdict": verdict,
    }

def fixed_rejection(token):
    """Section 8.4 rejected_result: every input-derived appraisal component is
    unavailable, represented as JSON null by the harness, and every derived set
    is empty. No substantive reason and no evaluation gap is added, because the
    ordered checks terminated the appraisal before Section 8 ran."""
    return {
        "asserted_claim": None, "asserted_claim_supported": False,
        "boundary_ceiling": None, "boundary_grounding": None, "counter_evidence": None,
        "evaluation_context": None, "evaluation_gap_entries": [], "evaluation_gaps": [],
        "evaluation_scope": None, "fatal_reasons": [token], "inherited_limitations": None,
        "maximal_supported_claims": [], "recorder_relations": None,
        "semantics_version": "wexp-core-1", "substantive_reasons": [], "support_entries": [],
        "support_relations": [], "supported_claims": [], "target": None, "verdict": "reject",
    }

V = []
def add(vid, fixture, classification, purpose, derivation, inp, exp, code=None):
    V.append({"vector_id": vid, "source_fixture": fixture, "classification": classification,
              "requirement_ids": [f"WEXP-CORE-01-V003-REQ-{fixture}"], "purpose": purpose,
              "derivation": derivation, "input": inp, "expected_code": code, "expected": exp})

EXEC = {"base": "execution", "qualifiers": []}
EXEC_IV = {"base": "execution", "qualifiers": ["IV"]}
INVOC = {"base": "invocation", "qualifiers": []}

PRECEDENCE = (
    "Section 6.2 states the Core rejection checks as an ordered sequence, and exact target and "
    "context scope is one of the cross-field invariants at position 4: \"A well-typed wexp-core-1 "
    "input that violates a cross-field invariant returns E_PROFILE_MAPPING_INVALID. Cross-field "
    "invariants include aggregate cardinality and keys, exact target and context scope, ...\" "
    "Section 6 says why: \"The boundary finding, every base and qualifier aggregate, and every "
    "profile-gap entry have a target equal to the top-level target and an evaluation_context_ref "
    "equal to the top-level evaluation-context identifier. A foreign-scoped aggregate is not "
    "negative evidence for this appraisal; it violates the normalized-input cross-field contract "
    "and produces E_PROFILE_MAPPING_INVALID.\" The check terminates the appraisal, so Section 8 "
    "support construction never runs and no substantive reason or evaluation gap is produced. "
    "Section 8.4 gives the fixed rejection projection: every input-derived component is "
    "unavailable and every derived set is empty. E_PROFILE_MAPPING_INVALID is derived only by the "
    "ordered Core checks and is invalid as a supplied member of fatal_conditions, so the profile "
    "names it rather than permitting it."
)
FATAL = "E_PROFILE_MAPPING_INVALID"

# ---- control -------------------------------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution")])
add("WEXP-CORE-01-V003-TV-3001", "S3001", "scope-identity-control",
    "Every applicable scope matches, so the input satisfies the cross-field contract, reaches Section 8, and the execution finding supports the asserted claim. Without this control the set would show only that inputs are refused, not that refusal is selective.",
    "Section 6: every aggregate carries the top-level target and evaluation-context identifier, so the cross-field invariant holds and the ordered checks pass. Section 8.1: the finding names the same target and evaluation context as the input, binding and semantic validation are supported, the boundary is supported and target-bound, and the accepted ceiling admits execution. Section 8.2: exact membership with non-blocking counter-evidence gives accept.",
    i, expected(i, verdict="accept", supported_claims=[EXEC],
                support_entries=[support_entry(EXEC, ["bd", "execution-T"])],
                asserted_supported=True, ceiling="execution"))

# ---- base finding: foreign target ---------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution", target=FOREIGN_TARGET)])
add("WEXP-CORE-01-V003-TV-3002", "S3002", "base-foreign-target-fatal",
    "A base aggregate names a different action target. The input violates the cross-field contract and is rejected before any claim is appraised.",
    PRECEDENCE + " Here a base aggregate carries a target other than the top-level target.",
    i, fixed_rejection(FATAL), code=FATAL)

# ---- base finding: foreign evaluation context ---------------------------
i = make_input(EXEC, "execution", [base_finding("execution", ctx=FOREIGN_CONTEXT)])
add("WEXP-CORE-01-V003-TV-3003", "S3003", "base-foreign-context-fatal",
    "The same violation through the other half of the scope: the right target under a different evaluation context. Paired with TV-3002 so neither equality conjunct can be dropped without a vector noticing.",
    PRECEDENCE + " Here a base aggregate carries an evaluation_context_ref other than the top-level evaluation-context identifier.",
    i, fixed_rejection(FATAL), code=FATAL)

# ---- qualifier finding foreign, base in scope ---------------------------
i = make_input(EXEC_IV, "execution", [base_finding("execution")],
               [qual_finding("execution", "IV", target=FOREIGN_TARGET)])
add("WEXP-CORE-01-V003-TV-3004", "S3004", "qualifier-foreign-scope-fatal",
    "The base aggregate is in scope and only the qualifier aggregate is foreign. Section 6 names qualifier aggregates explicitly, so a favourable base does not rescue the input.",
    PRECEDENCE + " Section 6 binds \"every base and qualifier aggregate\" to the top-level scope, so a foreign-scoped qualifier aggregate violates the contract on its own. Section 8.1 would separately refuse to admit it into Q(b) \"for the exact target and evaluation context\", but the appraisal never reaches that test.",
    i, fixed_rejection(FATAL), code=FATAL)

# ---- boundary finding foreign scope -------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution")])
i["boundary_finding"]["target"] = FOREIGN_TARGET
add("WEXP-CORE-01-V003-TV-3005", "S3005", "boundary-foreign-scope-fatal",
    "The boundary aggregate is foreign-scoped while every finding is in scope. Section 6 binds the boundary finding to the same contract as the aggregates.",
    PRECEDENCE + " Section 6 opens the sentence with \"The boundary finding\", so its scope is bound by the same cross-field invariant. Section 8.1 additionally requires the boundary to be \"scoped to that same target and context\" before its ceiling is usable, but that test is downstream of the rejection.",
    i, fixed_rejection(FATAL), code=FATAL)

# ---- profile gap entry foreign scope ------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution")])
i["profile_evaluation_gaps"] = [{
    "token": "E_IV_NOT_EVALUATED", "target": FOREIGN_TARGET, "evaluation_context_ref": CONTEXT,
    "affected_claims": [EXEC], "basis_refs": ["pg-1"], "limitations": []}]
add("WEXP-CORE-01-V003-TV-3006", "S3006", "profile-gap-foreign-scope-fatal",
    "A profile-supplied gap entry is foreign-scoped. Section 6 binds profile-gap entries to the same contract as findings, and this category is otherwise untested anywhere in the corpus.",
    PRECEDENCE + " Section 6 names \"every profile-gap entry\" alongside the boundary finding and the aggregates, so a foreign-scoped gap entry violates the contract even though it carries a registered token and affects an admissible claim.",
    i, fixed_rejection(FATAL), code=FATAL)

# ---- mixed: one valid finding does not legalise the input ---------------
i = make_input(INVOC, "execution",
               [base_finding("invocation"), base_finding("execution", target=FOREIGN_TARGET)])
add("WEXP-CORE-01-V003-TV-3007", "S3007", "mixed-scope-fatal",
    "A fully valid in-scope invocation finding sits beside a foreign-scoped execution finding. One valid finding does not legalise an input that carries a foreign-scoped aggregate: the contract is a property of the input, not of the best aggregate in it.",
    PRECEDENCE + " The invocation aggregate satisfies every condition and would enter B on its own. It does not matter: the cross-field invariant is evaluated over the whole input at position 4, so the appraisal is rejected before B is constructed. An implementation that answered accept with the invocation claim here would be applying Section 8 to an input Section 6.2 had already refused.",
    i, fixed_rejection(FATAL), code=FATAL)

V.sort(key=lambda x: x["vector_id"])


prof = copy.deepcopy(profile)
prof["profile_id"] = "wexp-core-01-vectors-003-profile"

# Section 6.2 derives E_MALFORMED_NORMALIZED_INPUT, E_UNSUPPORTED_SEMANTICS_VERSION,
# E_PROFILE_MAPPING_INVALID and E_CLAIM_OUT_OF_DOMAIN "only by the ordered Core
# checks", and they "are invalid as supplied members of fatal_conditions". The
# profile names the token Core emits at each position; it does not grant Core
# permission to reject. Set 002 already names claim_out_of_domain on the same
# basis. The delta from set 002 is declared here rather than inherited silently.
DERIVED_ONLY = ("E_MALFORMED_NORMALIZED_INPUT", "E_UNSUPPORTED_SEMANTICS_VERSION",
                "E_PROFILE_MAPPING_INVALID", "E_CLAIM_OUT_OF_DOMAIN")
ADDED_ROLES = {"profile_mapping_invalid": "E_PROFILE_MAPPING_INVALID",
               "malformed_normalized_input": "E_MALFORMED_NORMALIZED_INPUT",
               "unsupported_semantics_version": "E_UNSUPPORTED_SEMANTICS_VERSION"}
registry = prof["token_registry"]
registry["roles"] = dict(registry["roles"], **ADDED_ROLES)
registry["classes"] = copy.deepcopy(registry["classes"])
for token in ADDED_ROLES.values():
    if token not in registry["classes"]["fatal"]:
        registry["classes"]["fatal"].append(token)
registry["classes"]["fatal"].sort()
registry["derived_only"] = list(DERIVED_ONLY)
# Supplied fatal members are exactly the Core-defined ones this profile admits;
# nothing derived may be supplied.
registry["supplied_fatal"] = ["E_UNKNOWN_CRITICAL_SEMANTIC"]
prof["harness"] = {"harness_schema_id": "urn:wexp:core-01:vectors-003:harness",
                   "label": "WEXP Core-01 vector harness 003",
                   "vector_schema_id": "urn:wexp:core-01:vectors-003:vector"}
prof["vector_bindings"] = {v["vector_id"]: {"requirement_ids": v["requirement_ids"],
                                            "source_fixture": v["source_fixture"],
                                            "classification": v["classification"]} for v in V}
seed = {
    "candidate_id": "WEXP-CORE-01-VECTORS-003",
    "authority": {"published_specification": True, "snapshot_id": "draft-sergeev-wexp-core-01",
                  "snapshot_path": "spec/draft-sergeev-wexp-core-01.xml", "xml_bytes": 103095,
                  "xml_sha256": "84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d"},
    "profile": prof, "status": "WEXP-CORE-01-PUBLIC-VECTOR-SET",
    "release_status": "published-specification-derived",
    "non_claims": [
        "Expected results are derived from the published Internet-Draft, never from any implementation.",
        "This set covers one requirement family; it is not a conformance suite and passing it is not certification.",
        "It does not establish that the rest of the Core-01 surface is covered.",
    ],
    "vectors": V,
}
ensure(OUT / "seed-003.json").write_text(json.dumps(seed, indent=2, sort_keys=True) + "\n")

# The authoring script asserts representability rather than assuming it: every
# fatal token an expectation uses must be named by a role in this profile, and
# must not be listed as suppliable.
_registry = prof["token_registry"]
_named = set(_registry["roles"].values())
for _v in V:
    for _t in _v["expected"].get("fatal_reasons") or []:
        assert _t in _named, f"{_v['vector_id']}: {_t} has no role in this profile"
        assert _t in _registry["classes"]["fatal"], f"{_t} not in the fatal class"
        assert _t not in (_registry.get("supplied_fatal") or ()), f"{_t} must not be suppliable"
        assert _t in _registry["derived_only"], f"{_t} must be declared Core-derived"
print(f"representability asserted for {len(_named & set(_registry['classes']['fatal']))} fatal role(s)")

def canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
freeze = {"expectation_freeze": "WEXP-CORE-01-V003-EXPECTATION-FREEZE-002",
          "derived_from": ["draft-sergeev-wexp-core-01 84c0a164"],
          "derived_from_engines": False,
          "derived_from_public_engines": False,
          "derived_from_private_repaired_engines": False,
          "derived_from_differential_agreement": False,
          "supersedes": {"id": "WEXP-CORE-01-V003-EXPECTATION-FREEZE-001",
                         "status": "REJECTED_BEFORE_ACCEPTANCE",
                         "record": "docs/core-01-scope-identity-003-freeze-001-adjudication.md"},
          "vectors": [{"vector_id": v["vector_id"], "expected_code": v["expected_code"],
                       "expected_sha256": hashlib.sha256(canon(v["expected"])).hexdigest()} for v in V]}
freeze["derivation_bundle_sha256"] = hashlib.sha256(canon(freeze["vectors"])).hexdigest()
ensure(OUT / "freeze-003.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
print("EXPECTATION FREEZE:", freeze["expectation_freeze"])
print("derivation bundle :", freeze["derivation_bundle_sha256"])
for v in freeze["vectors"]:
    print(f"  {v['vector_id']}  {v['expected_sha256'][:32]}")
