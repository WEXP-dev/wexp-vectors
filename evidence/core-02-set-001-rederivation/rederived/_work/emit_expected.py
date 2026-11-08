# Notation aid only: every value below was derived by hand from
# spec/draft-sergeev-wexp-core-02.txt (see DERIVATION.md). This script merely
# writes the JSON files, copies input members that the text says carry through
# (target, asserted_claim, recorder_relations, counter_evidence,
# evaluation_context, evaluation_scope) and sorts set members.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INPUTS = os.path.join(ROOT, "inputs")
OUT = os.path.join(ROOT, "expected")
os.makedirs(OUT, exist_ok=True)

F1 = "draft-sergeev-wexp-core-02/fixture-1"
def r(local, prof=F1): return [prof, local]
bd = r("bd")

BASES = ["observation", "intent", "invocation", "execution"]
def claim(base, *quals): return {"base": base, "qualifiers": sorted(quals)}
O, I, N, E = claim("observation"), claim("intent"), claim("invocation"), claim("execution")
NV = claim("invocation", "IV")
EP, EV, EPV = claim("execution", "PROV"), claim("execution", "IV"), claim("execution", "PROV", "IV")

def ckey(c): return (BASES.index(c["base"]), tuple(sorted(c["qualifiers"])))
def sclaims(cs): return sorted(cs, key=ckey)
def srefs(xs):
    # set: keep the premise order bd, base, qualifier (Section 13 wording), drop equal duplicates
    out=[]
    for x in xs:
        if x not in out: out.append(x)
    return out

MEMBERS = ["semantics_version", "verdict", "fatal_reasons", "target", "asserted_claim",
           "asserted_claim_supported", "support_entries", "supported_claims",
           "maximal_supported_claims", "support_relations", "boundary_ceiling",
           "boundary_grounding", "recorder_relations", "substantive_reasons",
           "evaluation_gaps", "evaluation_gap_entries", "counter_evidence",
           "inherited_limitations", "evaluation_context", "evaluation_scope"]

def load(cid):
    with open(os.path.join(INPUTS, cid + ".json"), encoding="utf-8") as f:
        return json.load(f)["input"]

def reject(tokens):
    # Section 8.4 rejected_result: fixed projection.
    return {
        "semantics_version": "wexp-core-2", "verdict": "reject",
        "fatal_reasons": sorted(tokens), "target": None, "asserted_claim": None,
        "asserted_claim_supported": False, "support_entries": [], "supported_claims": [],
        "maximal_supported_claims": [], "support_relations": [], "boundary_ceiling": None,
        "boundary_grounding": None, "recorder_relations": None, "substantive_reasons": [],
        "evaluation_gaps": [], "evaluation_gap_entries": [], "counter_evidence": None,
        "inherited_limitations": None, "evaluation_context": None, "evaluation_scope": None,
    }

def core_gap(inp, token, affected, basis, lims):
    # Section 8.4: Core-derived gap entry = row token, input target and context id,
    # affected_claims={asserted claim} (finding rows) or the counter entry's exact
    # affected claims (counter rows), basis/limitations of the aggregate or entry.
    return {"token": token, "target": inp["target"],
            "evaluation_context_ref": inp["evaluation_context"]["id"],
            "affected_claims": sclaims(affected), "basis_refs": srefs(basis),
            "limitations": srefs(lims)}

def result(inp, verdict, supported, maximal, relations, entries, asserted_supported,
           reasons, gap_entries, ceiling, grounding, inherited):
    # entries: list of (claim, basis_refs, limitations); relations: list of (claim, relation)
    return {
        "semantics_version": "wexp-core-2", "verdict": verdict, "fatal_reasons": [],
        "target": inp["target"], "asserted_claim": inp["asserted_claim"],
        "asserted_claim_supported": asserted_supported,
        "support_entries": [{"claim": c, "basis_refs": srefs(b), "limitations": srefs(l)}
                            for c, b, l in sorted(entries, key=lambda t: ckey(t[0]))],
        "supported_claims": sclaims(supported),
        "maximal_supported_claims": sclaims(maximal),
        "support_relations": [{"supported_claim": c, "relation": rel}
                              for c, rel in sorted(relations, key=lambda t: ckey(t[0]))],
        "boundary_ceiling": ceiling, "boundary_grounding": grounding,
        "recorder_relations": inp["recorder_relations"],
        "substantive_reasons": sorted(reasons),
        "evaluation_gaps": sorted({g["token"] for g in gap_entries}),
        "evaluation_gap_entries": sorted(gap_entries, key=lambda g: json.dumps(g, sort_keys=True)),
        "counter_evidence": inp["counter_evidence"],
        "inherited_limitations": srefs(inherited),
        "evaluation_context": inp["evaluation_context"],
        "evaluation_scope": inp["evaluation_scope"],
    }

MALF = "E_MALFORMED_NORMALIZED_INPUT"
PMI = "E_PROFILE_MAPPING_INVALID"
MISSING = "E_MISSING_REQUIRED_EVIDENCE"

EXPECTED = {}
ALT = {}  # id -> (question, primary, alternative, alt_expected)

# ---------------- C01-C16 (Section 13 table) ----------------
inp = load("C01"); EXPECTED["C01"] = result(inp, "accept", [I], [I], [(I, "equal")], [(I, [bd, r("I")], [])], True, [], [], "intent", "attributed", [])
inp = load("C02"); EXPECTED["C02"] = result(inp, "downgrade", [E], [E], [(E, "support-above-claim")], [(E, [bd, r("E")], [])], False, [MISSING], [], "execution", "attributed", [])
inp = load("C03"); EXPECTED["C03"] = result(inp, "downgrade", [E, EP], [EP], [(EP, "incomparable")], [(E, [bd, r("E")], []), (EP, [bd, r("E"), r("P(E)")], [])], False, [MISSING], [], "execution", "attributed", [])
inp = load("C04"); EXPECTED["C04"] = result(inp, "downgrade", [E, EV], [EV], [(EV, "incomparable")], [(E, [bd, r("E")], []), (EV, [bd, r("E"), r("V(E)")], [])], False, [MISSING], [], "execution", "attributed", [])
inp = load("C05"); EXPECTED["C05"] = result(inp, "accept", [N, NV], [NV], [(NV, "equal")], [(N, [bd, r("N")], []), (NV, [bd, r("N"), r("V(N)")], [])], True, [], [], "invocation", "attributed", [])
inp = load("C06"); EXPECTED["C06"] = result(inp, "downgrade", [N, NV, E], [NV, E], [(NV, "support-below-claim"), (E, "support-below-claim")], [(N, [bd, r("N")], []), (NV, [bd, r("N"), r("V(N)")], []), (E, [bd, r("E")], [])], False, [MISSING], [], "execution", "attributed", [])
inp = load("C07"); EXPECTED["C07"] = result(inp, "downgrade", [], [], [], [], False, ["E_BASE_EXCEEDS_BOUNDARY"], [], "invocation", "attributed", [])
inp = load("C08"); EXPECTED["C08"] = result(inp, "downgrade", [], [], [], [], False, [MISSING], [], "observation", "attributed", [])
EXPECTED["C09"] = reject(["E_CLAIM_OUT_OF_DOMAIN"])
inp = load("C10"); EXPECTED["C10"] = result(inp, "downgrade", [I], [I], [(I, "equal")], [(I, [bd, r("I")], [])], True, ["E_COUNTER_EVIDENCE_UNRESOLVED"], [], "intent", "attributed", [])
comp = [bd, r("s1"), r("s2"), r("adj"), r("w")]
inp = load("C11"); EXPECTED["C11"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, comp, [])], True, [], [], "execution", "attributed", [])
inp = load("C12"); EXPECTED["C12"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, comp, [r("L-boundary")])], True, [], [], "execution", "attributed", [r("L-boundary")])
inp = load("C13"); EXPECTED["C13"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [inp["profile_evaluation_gaps"][0]], "execution", "attributed", [r("L-upstream")])
inp = load("C14"); EXPECTED["C14"] = result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [core_gap(inp, "E_COUNTER_EVIDENCE_NOT_EVALUATED", [E], [], [])], "execution", "attributed", [])
inp = load("C15"); EXPECTED["C15"] = result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, ["E_COUNTER_EVIDENCE_UNRESOLVED", "P_COUNTER_FAIL"], [], "execution", "attributed", [])
inp = load("C16"); EXPECTED["C16"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [])

# ---------------- P01-P25 ----------------
for cid in ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P09", "P20"]:
    EXPECTED[cid] = reject([MALF])
EXPECTED["P08"] = reject([MALF])
ALT["P08"] = ("Is a lone surrogate (U+D800) a 'text atom'? If the atom is not valid Unicode scalar text it is a malformed atom (structural check, step 3); if the harness treats any string value as a text atom, the pair is structurally valid and fails only the cross-field profile binding (profile not in profile_identifiers).",
              "E_MALFORMED_NORMALIZED_INPUT (lone surrogate is not Unicode scalar text; Section 12: 'A malformed pair or a missing, empty, or non-text atom produces E_MALFORMED_NORMALIZED_INPUT at the structural check')",
              "E_PROFILE_MAPPING_INVALID (structurally valid pair whose profile 'wexp-core02-test-profile/extension-1' is not an applied profile identifier)",
              reject([PMI]))
for cid in ["P10", "P13", "P17", "P21", "P22", "P25"]:
    EXPECTED[cid] = reject([PMI])
EXPECTED["P18"] = reject([PMI])
ALT["P18"] = ("current_scope_capability = 'execution-support' (a real initial capability name, but not authenticity/composition): is it a 'disallowed ... current-scope marker' (cross-field, step 4) or an 'unknown closed-enum value' of a field whose comment lists only 'authenticity | composition' (structural, step 3)?",
              "E_PROFILE_MAPPING_INVALID (Section 6: 'a disallowed or mismatched current-scope marker ... produces E_PROFILE_MAPPING_INVALID at the cross-field check'; Section 15: 'A marker naming a different capability ... produces E_PROFILE_MAPPING_INVALID')",
              "E_MALFORMED_NORMALIZED_INPUT (the marker's logical type is the closed set {authenticity, composition}; any other value is an unknown closed-enum value at step 3)",
              reject([MALF]))
EXPECTED["P19"] = reject([MALF])
ALT["P19"] = ("current_scope_capability = 'unknown-capability' (not any capability name): unknown closed-enum value (structural, step 3) or a 'disallowed' marker (cross-field, step 4)?",
              "E_MALFORMED_NORMALIZED_INPUT (Section 6.1: the initial evaluation-scope names are a closed enumeration; Section 6.2 step 3: 'unknown closed-enum value ... returns E_MALFORMED_NORMALIZED_INPUT')",
              "E_PROFILE_MAPPING_INVALID (reading every marker defect, including a value naming no capability, as 'a disallowed or mismatched current-scope marker' at the cross-field check)",
              reject([PMI]))
inp = load("P11"); EXPECTED["P11"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [])
inp = load("P12"); EXPECTED["P12"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [])
inp = load("P14"); EXPECTED["P14"] = result(inp, "accept", [E, EP, EV, EPV], [EPV], [(EPV, "equal")],
    [(E, [bd, r("E")], []), (EP, [bd, r("E"), r("P(E)")], []), (EV, [bd, r("E"), r("V(E)")], []), (EPV, [bd, r("E"), r("P(E)"), r("V(E)")], [])],
    True, [], [], "execution", "attributed", [])
inp = load("P15"); EXPECTED["P15"] = result(inp, "downgrade", [], [], [], [], False, ["E_BOUNDARY_NOT_SUPPORTED"], [], None, "asserted-only", [r("L-boundary")])
inp = load("P16"); EXPECTED["P16"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [inp["profile_evaluation_gaps"][0]], "execution", "attributed", [r("L-auth")])
inp = load("P23"); EXPECTED["P23"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [])
inp = load("P24"); EXPECTED["P24"] = result(inp, "downgrade", [E], [E], [(E, "support-below-claim")], [(E, [bd, r("E")], [])], False, [MISSING], [], "execution", "attributed", [])

# ---------------- R01-R48 ----------------
inp = load("R01"); EXPECTED["R01"] = result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [core_gap(inp, "E_COUNTER_EVIDENCE_NOT_EVALUATED", [E], [], [])], "execution", "attributed", [])
for cid in ["R02", "R03", "R08", "R09", "R10", "R11", "R14", "R15", "R16", "R17", "R18", "R19", "R20", "R21",
            "R22", "R23", "R24", "R25", "R26", "R30", "R31", "R36", "R38", "R39"]:
    EXPECTED[cid] = reject([PMI])
inp = load("R04"); EXPECTED["R04"] = result(inp, "accept", [I], [I], [(I, "equal")], [(I, [bd, r("I")], [])], True, [], [], "execution", "attributed", [])
inp = load("R05"); EXPECTED["R05"] = result(inp, "accept", [N, NV], [NV], [(NV, "equal")], [(N, [bd, r("N")], []), (NV, [bd, r("N"), r("V(N)")], [])], True, [], [], "execution", "attributed", [])
inp = load("R06"); EXPECTED["R06"] = result(inp, "accept", [N], [N], [(N, "equal")], [(N, [bd, r("N")], [])], True, [], [], "execution", "attributed", [])
inp = load("R07"); EXPECTED["R07"] = result(inp, "downgrade", [E], [E], [(E, "support-below-claim")], [(E, [bd, r("E")], [])], False, [], [core_gap(inp, "E_IV_NOT_EVALUATED", [EV], [r("V(E)")], [])], "execution", "attributed", [])
EXPECTED["R12"] = reject([PMI])
inp = load("R12")
ALT["R12"] = ("P_COUNTER_FAIL is registered (same category) by two applied profile revisions. Section 6 requires resolution 'through exactly one immutable registry revision identified by an applied profile_identifier; absence, ambiguity, or category disagreement produces E_PROFILE_MAPPING_INVALID'. Is two concordant registrations 'ambiguity' (reject) or does category agreement make the binding unambiguous (downgrade as in C15)?",
              "E_PROFILE_MAPPING_INVALID ('exactly one' registry revision; two applied revisions registering the token is ambiguity regardless of category agreement)",
              "downgrade exactly as C15 (reasons {E_COUNTER_EVIDENCE_UNRESOLVED, P_COUNTER_FAIL}) with evaluation_context carrying both profile identifiers",
              result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, ["E_COUNTER_EVIDENCE_UNRESOLVED", "P_COUNTER_FAIL"], [], "execution", "attributed", []))
inp = load("R13"); EXPECTED["R13"] = result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, ["E_COUNTER_EVIDENCE_UNRESOLVED", "P_COUNTER_FAIL"], [], "execution", "attributed", [])
EXPECTED["R27"] = reject(["E_UNSUPPORTED_SEMANTICS_VERSION"])
EXPECTED["R28"] = reject([MALF])
EXPECTED["R29"] = reject(["E_INTEGRITY_INVALID", "E_BINDING_MISMATCH"])
inp = load("R32"); EXPECTED["R32"] = result(inp, "downgrade", [], [], [], [], False, ["E_BOUNDARY_NOT_SUPPORTED"], [], None, "attributed", [])
inp = load("R33"); EXPECTED["R33"] = result(inp, "downgrade", [], [], [], [], False, ["E_EXACT_CLAIM_NOT_SUPPORTED"], [], "execution", "attributed", [])
inp = load("R34"); EXPECTED["R34"] = result(inp, "downgrade", [E], [E], [(E, "support-below-claim")], [(E, [bd, r("E")], [])], False, [], [core_gap(inp, "E_PROV_NOT_EVALUATED", [EP], [r("P(E)")], [])], "execution", "attributed", [])
inp = load("R35"); EXPECTED["R35"] = result(inp, "downgrade", [E], [E], [(E, "support-below-claim")], [(E, [bd, r("E")], [])], False, ["E_INDEPENDENCE_NOT_ESTABLISHED"], [], "execution", "attributed", [])
inp = load("R37"); EXPECTED["R37"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [inp["profile_evaluation_gaps"][0]], "execution", "attributed", [])
inp = load("R40"); EXPECTED["R40"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [])
inp = load("R41"); EXPECTED["R41"] = result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [core_gap(inp, "E_COUNTER_EVIDENCE_NOT_EVALUATED", [E], [r("c")], [])], "execution", "attributed", [])
inp = load("R42"); EXPECTED["R42"] = result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, ["E_COUNTER_EVIDENCE_UNRESOLVED"], [], "execution", "attributed", [])
inp = load("R43"); EXPECTED["R43"] = result(inp, "downgrade", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, ["E_COUNTER_EVIDENCE_DEFEATING"], [], "execution", "attributed", [])
inp = load("R44"); EXPECTED["R44"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [])
CM = "E_EVIDENCE_COVERAGE_MISMATCH"
inp = load("R45"); EXPECTED["R45"] = result(inp, "accept", [I, E], [E], [(E, "equal")], [(I, [bd, r("I")], [r("L-scope")]), (E, [bd, r("E")], [r("L-scope")])], True, [CM], [], "execution", "attributed", [r("L-scope")])
inp = load("R46"); EXPECTED["R46"] = result(inp, "accept", [I, E], [E], [(E, "equal")], [(I, [bd, r("I")], []), (E, [bd, r("E")], [r("L-scope")])], True, [CM], [], "execution", "attributed", [r("L-scope")])
inp = load("R47"); EXPECTED["R47"] = result(inp, "accept", [I, E], [E], [(E, "equal")], [(I, [bd, r("I")], [r("L-scope")]), (E, [bd, r("E")], [])], True, [CM], [], "execution", "attributed", [r("L-scope")])
ALT["R47"] = ("A substantive reason carried by a supported but NON-asserted base finding (intent, while execution is asserted): is it projected into substantive_reasons because that finding is 'an exact premise of a SupportEntry' (intent is a member of SupportedClaims), or excluded because substantive reasons 'describe why evidence does not support the asserted claim'?",
              "projected: substantive_reasons={E_EVIDENCE_COVERAGE_MISMATCH} (Section 8.4: 'for every boundary, base, or qualifier finding that is the asserted role or an exact premise of a SupportEntry: add its registered substantive reasons to reasons'; Section 8.6: '... or from a finding that is an exact premise of a reported support entry')",
              "not projected: substantive_reasons={} (reading the projection as limited to findings bearing on the asserted claim); inherited_limitations still {L-scope} because 'every support-entry limitation' is in the union",
              result(inp, "accept", [I, E], [E], [(E, "equal")], [(I, [bd, r("I")], [r("L-scope")]), (E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [r("L-scope")]))
inp = load("R48"); EXPECTED["R48"] = result(inp, "accept", [E], [E], [(E, "equal")], [(E, [bd, r("E")], [])], True, [], [], "execution", "attributed", [])

# ---------------- write ----------------
ids = ["C%02d" % i for i in range(1, 17)] + ["R%02d" % i for i in range(1, 49)] + ["P%02d" % i for i in range(1, 26)]
assert sorted(ids) == sorted(EXPECTED), set(ids) ^ set(EXPECTED)
for cid in ids:
    exp = EXPECTED[cid]
    assert list(sorted(exp)) == sorted(MEMBERS) and len(exp) == 20, cid
    with open(os.path.join(OUT, cid + ".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"id": cid, "expected": exp}, indent=1, sort_keys=True, ensure_ascii=True) + "\n")
amb = [{"id": k, "question": q, "primary_reading": p, "alternative_reading": a, "alternative_expected": x}
       for k, (q, p, a, x) in sorted(ALT.items())]
with open(os.path.join(ROOT, "AMBIGUITIES.json"), "w", encoding="utf-8") as f:
    f.write(json.dumps(amb, indent=1, sort_keys=True, ensure_ascii=True) + "\n")
# summary table for the report
for cid in ids:
    e = EXPECTED[cid]
    print(cid, e["verdict"], "fatal=" + ",".join(e["fatal_reasons"]) or "-", "reasons=" + ",".join(e["substantive_reasons"]), "gaps=" + ",".join(e["evaluation_gaps"]))
