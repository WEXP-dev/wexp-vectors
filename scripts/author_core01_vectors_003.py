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

V = []
def add(vid, fixture, classification, purpose, derivation, inp, exp, code=None):
    V.append({"vector_id": vid, "source_fixture": fixture, "classification": classification,
              "requirement_ids": [f"WEXP-CORE-01-V003-REQ-{fixture}"], "purpose": purpose,
              "derivation": derivation, "input": inp, "expected_code": code, "expected": exp})

EXEC = {"base": "execution", "qualifiers": []}
EXEC_IV = {"base": "execution", "qualifiers": ["IV"]}
INVOC = {"base": "invocation", "qualifiers": []}

SCOPE_RULE = (
    "Section 8.1: a base is in B only if, among the other conditions, \"the finding names the same "
    "target and evaluation context as the appraisal input\". Section 8.4 states the same requirement "
    "inside the admission predicate itself: f.target == input.target and f.evaluation_context_ref == "
    "input.evaluation_context.id. Section 6 adds that \"a foreign-scoped aggregate is not negative "
    "evidence for this appraisal\" -- it is not evidence here at all, so it neither supports a claim "
    "nor stands in for an aggregate that is genuinely absent. Section 8.6 then reports the asserted "
    "aggregate as absent, and Section 8.2 gives downgrade because the asserted claim is not an exact "
    "member of SupportedClaims."
)

# ---- control -------------------------------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution")])
add("WEXP-CORE-01-V003-TV-3001", "S3001", "scope-identity-control",
    "Every scope component matches, so the execution finding is admitted and supports the asserted claim. Without this control the rest of the set would show only that something is refused, not that the refusal is selective.",
    "Section 8.1: the finding names the same target and evaluation context as the input, target binding and semantic validation are supported, the boundary is supported and target-bound, and the accepted ceiling admits execution. Section 8.2: exact membership with non-blocking counter-evidence gives accept.",
    i, expected(i, verdict="accept", supported_claims=[EXEC],
                support_entries=[support_entry(EXEC, ["bd", "execution-T"])],
                asserted_supported=True, ceiling="execution"))

# ---- foreign target ------------------------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution", target=FOREIGN_TARGET)])
add("WEXP-CORE-01-V003-TV-3002", "S3002", "foreign-target-negative",
    "The only base finding names a different action target. It is the sole candidate support, so acceptance is reachable only if the target identity requirement is not enforced.",
    SCOPE_RULE + " Here the single execution finding names another target, so B is empty and no claim is supported.",
    i, expected(i, verdict="downgrade", supported_claims=[], support_entries=[],
                asserted_supported=False, ceiling="execution",
                substantive=["E_MISSING_REQUIRED_EVIDENCE"]),
    code="E_MISSING_REQUIRED_EVIDENCE")

# ---- foreign evaluation context -----------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution", ctx=FOREIGN_CONTEXT)])
add("WEXP-CORE-01-V003-TV-3003", "S3003", "foreign-context-negative",
    "The same shape through the other half of the scope: the finding names the right target under a different evaluation context. Paired with TV-3002 so neither half of the predicate can be dropped without a vector noticing.",
    SCOPE_RULE + " Here the target matches and the evaluation context does not, which fails the second conjunct of the Section 8.4 predicate.",
    i, expected(i, verdict="downgrade", supported_claims=[], support_entries=[],
                asserted_supported=False, ceiling="execution",
                substantive=["E_MISSING_REQUIRED_EVIDENCE"]),
    code="E_MISSING_REQUIRED_EVIDENCE")

# ---- both foreign --------------------------------------------------------
i = make_input(EXEC, "execution", [base_finding("execution", target=FOREIGN_TARGET, ctx=FOREIGN_CONTEXT)])
add("WEXP-CORE-01-V003-TV-3004", "S3004", "foreign-scope-negative",
    "Both scope components differ. An implementation that enforces neither, or only one, still admits nothing here.",
    SCOPE_RULE + " Both conjuncts fail; either alone would already exclude the finding.",
    i, expected(i, verdict="downgrade", supported_claims=[], support_entries=[],
                asserted_supported=False, ceiling="execution",
                substantive=["E_MISSING_REQUIRED_EVIDENCE"]),
    code="E_MISSING_REQUIRED_EVIDENCE")

# ---- strong qualifiers do not rescue foreign scope -----------------------
i = make_input(EXEC_IV, "execution",
               [base_finding("execution", target=FOREIGN_TARGET, ctx=FOREIGN_CONTEXT)],
               [qual_finding("execution", "IV", target=FOREIGN_TARGET, ctx=FOREIGN_CONTEXT)])
add("WEXP-CORE-01-V003-TV-3005", "S3005", "foreign-scope-strong-qualifier-negative",
    "Favourable target binding, semantic validation and independence on a foreign-scoped pair. Evidence quality is not a substitute for evidence identity.",
    SCOPE_RULE + " Section 8.1 admits IV into Q(b) only when the IV finding passes its assessments \"for the exact target and evaluation context\", so a qualifier cannot rescue a base that was never admitted, and cannot be admitted itself on a foreign scope.",
    i, expected(i, verdict="downgrade", supported_claims=[], support_entries=[],
                asserted_supported=False, ceiling="execution",
                substantive=["E_MISSING_REQUIRED_EVIDENCE"]),
    code="E_MISSING_REQUIRED_EVIDENCE")

# ---- mixed scope: no inflation ------------------------------------------
i = make_input(INVOC, "execution",
               [base_finding("invocation"), base_finding("execution", target=FOREIGN_TARGET)])
add("WEXP-CORE-01-V003-TV-3006", "S3006", "mixed-scope-no-inflation",
    "One in-scope invocation finding beside a stronger foreign-scoped execution finding. The in-scope claim must still be supported and the foreign one must add nothing beside it: exclusion is selective, not a blanket refusal of the whole input.",
    SCOPE_RULE + " The invocation finding satisfies every condition and enters B. The execution finding names another target and does not, so SupportedClaims contains the invocation claim alone, the asserted invocation claim is an exact member, and Section 8.2 gives accept. An implementation that admitted the foreign finding would report a deeper supported claim than the evidence for this target supports.",
    i, expected(i, verdict="accept", supported_claims=[INVOC],
                support_entries=[support_entry(INVOC, ["bd", "invocation-T"])],
                asserted_supported=True, ceiling="execution"))

V.sort(key=lambda x: x["vector_id"])

prof = copy.deepcopy(profile)
prof["profile_id"] = "wexp-core-01-vectors-003-profile"
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

def canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
freeze = {"expectation_freeze": "WEXP-CORE-01-V003-EXPECTATION-FREEZE-001",
          "derived_from": ["draft-sergeev-wexp-core-01 84c0a164"],
          "derived_from_engines": False,
          "vectors": [{"vector_id": v["vector_id"], "expected_code": v["expected_code"],
                       "expected_sha256": hashlib.sha256(canon(v["expected"])).hexdigest()} for v in V]}
freeze["derivation_bundle_sha256"] = hashlib.sha256(canon(freeze["vectors"])).hexdigest()
ensure(OUT / "freeze-003.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
print("EXPECTATION FREEZE:", freeze["expectation_freeze"])
print("derivation bundle :", freeze["derivation_bundle_sha256"])
for v in freeze["vectors"]:
    print(f"  {v['vector_id']}  {v['expected_sha256'][:32]}")
