"""Author the 002 seed. Expectations derived from published Core-01 only.

No engine is run by this script. The projection *shape* follows the published
representation contract; every *value* is derived from the normative text cited
in the per-vector derivation record.
"""
import copy, hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build"

SET001 = ROOT / "vectors/WEXP-CORE-01-VECTORS-001"
profile = json.loads((SET001 / "profile.json").read_bytes())
sample = json.loads((SET001 / "vectors/WEXP-CORE-01-Q001-TV-0001.json").read_bytes())
SCOPE_ALL = sample["input"]["evaluation_scope"]
REPR = sample["input"]["representation"]

def ensure(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def base_finding(b, limitations=None):
    return {"base": b, "basis_refs": [b], "evaluation_context_ref": "C",
            "limitations": limitations or [], "reasons": [],
            "semantic_validation": "supported", "target": "T", "target_binding": "supported"}

def qual_finding(b, q, independence=None, semantic="supported"):
    if independence is None:
        independence = "not-applicable" if q == "PROV" else "supported"
    return {"qualifier": q, "qualified_base": b, "basis_refs": [f"{q.lower()}-{b}"],
            "evaluation_context_ref": "C", "independence_validation": independence,
            "limitations": [], "reasons": [], "semantic_validation": semantic,
            "target": "T", "target_binding": "supported"}

def make_input(asserted, ceiling, base_findings, qualifier_findings=(), counter=None,
               fatal=(), grounding="attributed", boundary_limitations=()):
    return {
        "asserted_claim": asserted,
        "base_findings": base_findings,
        "boundary_finding": {"basis_refs": ["bd"], "ceiling_base": ceiling,
            "evaluation_context_ref": "C", "grounding": grounding,
            "limitations": list(boundary_limitations), "reasons": [], "status": "supported",
            "target": "T", "target_binding": "supported"},
        "counter_evidence": counter if counter is not None else [
            {"affected_claims": [], "basis_refs": [], "limitations": [], "reasons": [],
             "status": "not-supplied"}],
        "evaluation_context": {"id": "C"},
        "evaluation_scope": copy.deepcopy(SCOPE_ALL),
        "fatal_conditions": list(fatal),
        "inherited_limitations": [],
        "profile_evaluation_gaps": [],
        "qualifier_findings": list(qualifier_findings),
        "recorder_relations": [],
        "representation": REPR,
        "semantics_version": "wexp-core-1",
        "target": "T",
    }

def support_entry(claim, basis_refs, limitations=()):
    return {"claim": claim, "basis_refs": list(basis_refs), "limitations": list(limitations)}

def expected(inp, *, verdict, supported_claims, support_entries, asserted_supported,
             ceiling, grounding, substantive=(), gaps=(), gap_entries=(), fatals=(),
             maximal=None, inherited=(), relations=None):
    """Assemble the projection from derived values plus the input-determined
    pass-through components the representation contract fixes."""
    return {
        "asserted_claim": inp["asserted_claim"],
        "asserted_claim_supported": asserted_supported,
        "boundary_ceiling": ceiling,
        "boundary_grounding": grounding,
        "counter_evidence": inp["counter_evidence"],
        "evaluation_context": inp["evaluation_context"],
        "evaluation_gap_entries": list(gap_entries),
        "evaluation_gaps": list(gaps),
        "evaluation_scope": inp["evaluation_scope"],
        "fatal_reasons": list(fatals),
        "inherited_limitations": list(inherited),
        "maximal_supported_claims": maximal if maximal is not None else supported_claims,
        "recorder_relations": inp["recorder_relations"],
        "semantics_version": "wexp-core-1",
        "substantive_reasons": list(substantive),
        "support_entries": support_entries,
        "support_relations": relations if relations is not None else [],
        "supported_claims": supported_claims,
        "target": inp["target"],
        "verdict": verdict,
    }

BD = ["bd"]
def rel(asserted, claim):
    """Section 4.5: (b1,A1) <= (b2,A2) iff b1<=b2 and A1 subset of A2."""
    order = profile["orderings"]["base"]
    a, b = asserted, claim
    ai, bi = order.index(a["base"]), order.index(b["base"])
    aq, bq = set(a["qualifiers"]), set(b["qualifiers"])
    if ai == bi and aq == bq: return "equal"
    if bi >= ai and aq <= bq: return "support-above-claim"
    if ai >= bi and bq <= aq: return "support-below-claim"
    return "incomparable"

def relations(asserted, maximal):
    return [{"relation": rel(asserted, m), "supported_claim": m} for m in maximal]

V = []
def add(vid, fixture, classification, purpose, derivation, inp, exp, code=None):
    V.append({"vector_id": vid, "source_fixture": fixture, "classification": classification,
              "requirement_ids": [f"WEXP-CORE-01-V002-REQ-{fixture}"], "purpose": purpose,
              "derivation": derivation, "input": inp, "expected_code": code, "expected": exp})

# ---- A: subsets of Q(b) -------------------------------------------------
i = make_input({"base":"execution","qualifiers":["PROV","IV"]}, "execution",
               [base_finding("execution")],
               [qual_finding("execution","PROV"), qual_finding("execution","IV")])
sc = [{"base":"execution","qualifiers":[]},{"base":"execution","qualifiers":["PROV"]},
      {"base":"execution","qualifiers":["IV"]},{"base":"execution","qualifiers":["PROV","IV"]}]
mx = [{"base":"execution","qualifiers":["PROV","IV"]}]
se = [support_entry(sc[0], ["bd","execution"]),
      support_entry(sc[1], ["bd","execution","prov-execution"]),
      support_entry(sc[2], ["bd","execution","iv-execution"]),
      support_entry(sc[3], ["bd","execution","prov-execution","iv-execution"])]
add("WEXP-CORE-01-V002-TV-2001","A2001","multi-qualifier-positive",
    "Both PROV and IV are admitted on a supported execution base, so every subset of Q(execution) is supported, including the two-qualifier state.",
    "Section 8.1: A ranges over the subsets of the admitted qualifier set Q(b). Section 4.4 lists (execution,{PROV,IV}) as admissible because PROV is present only on execution. Section 8.2: the asserted claim is an exact member of SupportedClaims and counter-evidence does not block that exact claim, so the verdict is accept. Never derived from an engine.",
    i, expected(i, verdict="accept", supported_claims=sc, support_entries=se,
                asserted_supported=True, ceiling="execution", grounding="attributed",
                maximal=mx, relations=relations(i["asserted_claim"], mx)))

# ---- B + D: unrelated over-ceiling finding, accept preserved ------------
i = make_input({"base":"intent","qualifiers":[]}, "intent",
               [base_finding("intent"), base_finding("execution")])
sc = [{"base":"intent","qualifiers":[]}]
se = [support_entry(sc[0], ["bd","intent"])]
add("WEXP-CORE-01-V002-TV-2002","B2002","unrelated-over-ceiling-positive",
    "An execution finding sits above an intent ceiling while the asserted intent claim is supported. The unrelated finding is simply unsupported; it places no diagnostic on the asserted claim.",
    "Section 8.6: the boundary-exceeded row requires a usable boundary and a present asserted-base aggregate whose base is deeper than the ceiling. The asserted base is intent, which is not deeper than the intent ceiling, so the row does not apply to it. Section 8.2: accept is exact membership plus counter-evidence not blocking; the Section 8.4 algorithm tests exactly those two conditions, so a diagnostic set is not a third one. Never derived from an engine.",
    i, expected(i, verdict="accept", supported_claims=sc, support_entries=se,
                asserted_supported=True, ceiling="intent", grounding="attributed",
                relations=relations(i["asserted_claim"], sc)))

# ---- C: control, asserted base itself over the ceiling ------------------
i = make_input({"base":"execution","qualifiers":[]}, "intent",
               [base_finding("intent"), base_finding("execution")])
sc = [{"base":"intent","qualifiers":[]}]
se = [support_entry(sc[0], ["bd","intent"])]
add("WEXP-CORE-01-V002-TV-2003","C2003","asserted-base-over-ceiling-negative",
    "The asserted execution claim is itself deeper than the intent ceiling, so the boundary-exceeded row applies and the claim is not supported.",
    "Section 8.6: a present asserted-base aggregate whose base is deeper than the ceiling produces E_BASE_EXCEEDS_BOUNDARY, and consequently not E_MISSING_REQUIRED_EVIDENCE. Section 8.2: the asserted claim is admissible but not exactly supported, so the verdict is downgrade. Control for TV-2002: proves the row was narrowed, not disabled. Never derived from an engine.",
    i, expected(i, verdict="downgrade", supported_claims=sc, support_entries=se,
                asserted_supported=False, ceiling="intent", grounding="attributed",
                substantive=["E_BASE_EXCEEDS_BOUNDARY"],
                relations=relations(i["asserted_claim"], sc)),
    code="E_BASE_EXCEEDS_BOUNDARY")

# ---- E: non-targeted counter-evidence -----------------------------------
counter = [{"affected_claims":[{"base":"observation","qualifiers":[]}],
            "basis_refs":["ce"], "limitations":[], "reasons":[], "status":"not-evaluated"}]
i = make_input({"base":"invocation","qualifiers":[]}, "invocation",
               [base_finding("invocation")], counter=counter)
sc = [{"base":"invocation","qualifiers":[]}]
se = [support_entry(sc[0], ["bd","invocation"])]
add("WEXP-CORE-01-V002-TV-2005","E2005","counter-evidence-non-targeted-positive",
    "A not-evaluated counter-evidence entry targets an observation claim that is not the asserted claim, so it does not block acceptance of the asserted invocation claim.",
    "Section 8.2: counter-evidence blocks only for entries whose affected claims include the asserted claim or all-admissible-claims. The entry names observation, and the asserted claim is invocation, so the entry does not apply. Control pair against published fixture C14, whose entry does target the asserted claim. Never derived from an engine.",
    i, expected(i, verdict="accept", supported_claims=sc, support_entries=se,
                asserted_supported=True, ceiling="invocation", grounding="attributed",
                relations=relations(i["asserted_claim"], sc)))

# ---- G: qualifier outside its admissible base ---------------------------
i = make_input({"base":"invocation","qualifiers":["PROV"]}, "invocation",
               [base_finding("invocation")])
add("WEXP-CORE-01-V002-TV-2007","G2007","qualifier-domain-fatal",
    "PROV is admissible only on execution, so an asserted (invocation,{PROV}) claim is outside the admissible domain.",
    "Section 4.4: a claim is admissible only if PROV is absent or the base is execution; an asserted claim outside this domain is rejected with E_CLAIM_OUT_OF_DOMAIN, and an appraiser must not silently delete the invalid qualifier and reinterpret the assertion. Section 6.2 check 6 places this after the supplied-fatal check. Section 8.4 gives the fixed rejection projection, whose input-derived components carry the logical value unavailable, represented per R-001 as JSON null. Never derived from an engine.",
    i, None, code="E_CLAIM_OUT_OF_DOMAIN")

# ---- H: asserted qualifier whose independence assessment did not run ----
iv = qual_finding("invocation", "IV", independence="not-evaluated")
iv["basis_refs"] = ["iv-invocation"]
iv["limitations"] = ["L-iv-scope"]
i = make_input({"base":"invocation","qualifiers":["IV"]}, "invocation",
               [base_finding("invocation")], [iv])
sc = [{"base":"invocation","qualifiers":[]}]
se = [support_entry(sc[0], ["bd","invocation"])]
ge = [{"affected_claims": [i["asserted_claim"]], "basis_refs": ["iv-invocation"],
       "evaluation_context_ref": "C", "limitations": ["L-iv-scope"], "target": "T",
       "token": "E_IV_NOT_EVALUATED"}]
add("WEXP-CORE-01-V002-TV-2008","H2008","gap-only-downgrade",
    "The asserted IV qualifier carries a not-evaluated independence assessment, so IV is not admitted, the asserted claim is not exactly supported, and the only diagnostic is a gap. The verdict must still be downgrade although the substantive set is empty.",
    "Section 8.1 admits IV only when independence_validation is supported, so IV is absent from Q(invocation) and (invocation,{IV}) is not in SupportedClaims. Section 8.6 gives exactly one row, the gap E_IV_NOT_EVALUATED for an asserted IV independence assessment that is not-evaluated; no substantive row applies because the aggregate is present, bound and semantically supported. Section 8.2 makes accept conditional on exact membership and non-blocking counter-evidence alone, so an empty substantive set does not make this accept. This separates the Core-derived gap path from published fixture C13, whose identical token is a profile-supplied gap on a claim that remains supported. Never derived from an engine.",
    i, expected(i, verdict="downgrade", supported_claims=sc, support_entries=se,
                asserted_supported=False, ceiling="invocation", grounding="attributed",
                gaps=["E_IV_NOT_EVALUATED"], gap_entries=ge, inherited=["L-iv-scope"],
                relations=relations(i["asserted_claim"], sc)),
    code="E_IV_NOT_EVALUATED")

print(f"  authored: {len(V)} vector(s)")
for v in V:
    print(f"    {v['vector_id']}  {v['classification']}  -> {v['expected_code'] or '(no token)'}")

def fixed_rejection(fatals):
    """Section 8.4: every input-derived component carries the logical value
    unavailable, represented as JSON null per representation contract R-001.
    Set-valued appraisal components are empty rather than unavailable."""
    return {
        "asserted_claim": None, "asserted_claim_supported": False,
        "boundary_ceiling": None, "boundary_grounding": None,
        "counter_evidence": None, "evaluation_context": None,
        "evaluation_gap_entries": [], "evaluation_gaps": [],
        "evaluation_scope": None, "fatal_reasons": list(fatals),
        "inherited_limitations": None, "maximal_supported_claims": [],
        "recorder_relations": None, "semantics_version": "wexp-core-1",
        "substantive_reasons": [], "support_entries": [], "support_relations": [],
        "supported_claims": [], "target": None, "verdict": "reject",
    }

for v in V:
    if v["vector_id"].endswith("TV-2007"):
        v["expected"] = fixed_rejection(["E_CLAIM_OUT_OF_DOMAIN"])

# ---- F: ingress check 5, a valid supplied fatal condition ---------------
i = make_input({"base":"invocation","qualifiers":[]}, "invocation",
               [base_finding("invocation")], fatal=["E_UNKNOWN_CRITICAL_SEMANTIC"])
add("WEXP-CORE-01-V002-TV-2006","F2006","supplied-fatal-rejection",
    "A structurally usable input carries a valid supplied fatal condition, so Core returns that complete set through the fixed rejection projection without appraising the otherwise-supported claim.",
    "Section 6.2: if the structurally usable input has a non-empty valid fatal_conditions set, Core returns that complete set through the fixed rejection projection; this check precedes the inadmissible-claim check. E_UNKNOWN_CRITICAL_SEMANTIC is one of the Core-defined supplied fatal members and is registered by the applied profile. Section 8.4 gives the projection, whose input-derived components carry unavailable, represented as JSON null per R-001. Distinguishes ingress check 5 from check 6, which published fixture C09 covers. Never derived from an engine.",
    i, fixed_rejection(["E_UNKNOWN_CRITICAL_SEMANTIC"]), code="E_UNKNOWN_CRITICAL_SEMANTIC")

V.sort(key=lambda x: x["vector_id"])
print(f"  total: {len(V)} vector(s)")
for v in V:
    assert v["expected"] is not None, v["vector_id"]
    print(f"    {v['vector_id']}  {v['expected']['verdict']:9} {v['expected_code'] or ''}")

prof = copy.deepcopy(profile)
prof["profile_id"] = "wexp-core-01-vectors-002-profile"
prof["harness"] = {"harness_schema_id": "urn:wexp:core-01:vectors-002:harness",
                   "label": "WEXP Core-01 vector harness 002",
                   "vector_schema_id": "urn:wexp:core-01:vectors-002:vector"}
prof["vector_bindings"] = {v["vector_id"]: {"requirement_ids": v["requirement_ids"],
                                            "source_fixture": v["source_fixture"],
                                            "classification": v["classification"]} for v in V}
seed = {
 "candidate_id": "WEXP-CORE-01-VECTORS-002",
 "authority": {"published_specification": True, "snapshot_id": "draft-sergeev-wexp-core-01",
               "snapshot_path": "spec/draft-sergeev-wexp-core-01.xml",
               "xml_bytes": 103095,
               "xml_sha256": "84c0a16467585c29925339a10dd287c2e67bfe21ed592826254bf424dc24f56d"},
 "profile": prof,
 "status": "WEXP-CORE-01-PUBLIC-VECTOR-SET",
 "release_status": "published-specification-derived",
 "non_claims": [
   "Extends the coverage of WEXP-CORE-01-VECTORS-001; does not replace the published Core-01 specification.",
   "Expected appraisals are derived from the published Internet-Draft, never from any implementation.",
   "Increased coverage does not make this a conformance suite.",
 ],
 "vectors": V,
}
ensure(OUT / "seed-002.json").write_text(json.dumps(seed, indent=2, sort_keys=True) + "\n")

def canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
freeze = {"expectation_freeze": "WEXP-CORE-01-V002-EXPECTATION-FREEZE-001",
          "derived_from": ["draft-sergeev-wexp-core-01 84c0a164…",
                           "CORE-01-KNOWN-ISSUES-001", "CORE-01-REPRESENTATION-CONTRACT-001"],
          "derived_from_engines": False,
          "vectors": [{"vector_id": v["vector_id"], "expected_code": v["expected_code"],
                       "expected_sha256": hashlib.sha256(canon(v["expected"])).hexdigest()} for v in V]}
freeze["derivation_bundle_sha256"] = hashlib.sha256(canon(freeze["vectors"])).hexdigest()
ensure(OUT / "freeze-002.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
print("  EXPECTATION FREEZE:", freeze["expectation_freeze"])
print("  derivation bundle :", freeze["derivation_bundle_sha256"])
for v in freeze["vectors"]:
    print(f"    {v['vector_id']}  {v['expected_sha256'][:32]}…")
