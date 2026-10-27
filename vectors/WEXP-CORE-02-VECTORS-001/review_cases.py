#!/usr/bin/env python3
"""Author full expectations from the draft and explicit review cases.

No appraiser import or output is used. Review cases are non-normative.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from normative_cases import build, common, finding, claim, counter, gap, atoms, PROFILE, CATALOG

HERE = Path(__file__).resolve().parent
SOURCE_SHA256 = 'de983051a1c6ea51ea9b7f965fe9eabf2d97af92ab2f074781bd44e3f99c8782'

def scope(v, cap, status='not-evaluated'):
    next(x for x in v['evaluation_scope'] if x['capability']==cap)['status']=status

def reject(token):
    e=deepcopy(build()['cases'][8]['expected'])
    e['fatal_reasons']=token if isinstance(token,list) else [token]
    return e

def result(v, supported=(), maximal=(), relations=(), exact=False,
           verdict='downgrade', reasons=(), gaps=(), limitations=(), ceiling='copy',
           support_limits=None):
    # Support sets and relations are explicit case expectations, never inferred.
    entries=[]
    for c in supported:
        parts=c.split('+')
        entries.append({'claim':claim(c),
          'basis_refs':atoms('bd',parts[0],*(q+'('+parts[0]+')' for q in parts[1:])),
          'limitations':atoms(*(support_limits or {}).get(c,()))})
    return {'semantics_version':'wexp-core-2','verdict':verdict,'fatal_reasons':[],
      'target':v['target'],'asserted_claim':deepcopy(v['asserted_claim']),
      'asserted_claim_supported':exact,'support_entries':entries,
      'supported_claims':[claim(c) for c in supported],
      'maximal_supported_claims':[claim(c) for c in maximal],
      'support_relations':[{'supported_claim':claim(c),'relation':r} for c,r in zip(maximal,relations,strict=True)],
      'boundary_ceiling':v['boundary_finding'].get('ceiling_base') if ceiling=='copy' else ceiling,
      'boundary_grounding':v['boundary_finding']['grounding'],
      'recorder_relations':deepcopy(v['recorder_relations']),
      'substantive_reasons':list(reasons),'evaluation_gaps':sorted(set(g['token'] for g in gaps)),
      'evaluation_gap_entries':deepcopy(list(gaps)),'counter_evidence':deepcopy(v['counter_evidence']),
      'inherited_limitations':atoms(*limitations),'evaluation_context':deepcopy(v['evaluation_context']),
      'evaluation_scope':deepcopy(v['evaluation_scope'])}

def package():
    data=build()
    cases=data['cases']
    for c in cases:
        c.update(kind='normative-transcription',source_anchors=['vectors','algorithm'],
                 derivation='Core-02 C01-C16 table and its explicitly defined common fixture environment; all twenty result fields.')
    def add(cid,v,e,anchors,why,profiles=None):
        entry={'id':cid,'kind':'derived-review-case','source_anchors':anchors,
               'derivation':why,'input':deepcopy(v),'expected':deepcopy(e)}
        if profiles is not None:entry['profiles']=deepcopy(profiles)
        if len(e) != 20:
            raise ValueError('Expected exactly twenty result components')
        cases.append(entry)

    v=deepcopy(cases[13]['input']);scope(v,'counter-evidence')
    e=deepcopy(cases[13]['expected']);e['evaluation_scope']=deepcopy(v['evaluation_scope'])
    add('R01',v,e,['conformance','verdict','reasons'],'Changing only counter capability to not-evaluated preserves both entry statuses and the exact C14 support/gap outcome.')

    v=common('I','E',['I','E']);scope(v,'execution-support')
    add('R02',v,reject('E_PROFILE_MAPPING_INVALID'),['conformance','input-validity'],'Present wholly assessed unasserted execution conflicts with its single-role not-evaluated summary.')
    v=common('E','E',['E'],[('E','P')]);scope(v,'provenance-support')
    add('R03',v,reject('E_PROFILE_MAPPING_INVALID'),['conformance','input-validity'],'The same strict agreement applies to unasserted PROV.')
    v=common('I','E',['I','E']);scope(v,'execution-support');v['base_findings'][1]['semantic_validation']='not-evaluated'
    add('R04',v,result(v,['I'],['I'],['equal'],True,'accept'),['conformance','supported-claims','reasons'],'Unasserted unevaluated execution is valid and does not manufacture an intent gap.')
    v=common('N+V','E',['N'],[('N','V'),('E','V')]);scope(v,'independent-verification');v['qualifier_findings'][1]['semantic_validation']='not-evaluated'
    add('R05',v,result(v,['N','N+V'],['N+V'],['equal'],True,'accept'),['conformance','qualifiers','reasons'],'Shared IV preserves a passing exact invocation role despite an unperformed execution role.')
    v=common('N','E',['N','E']);v['base_findings'][1]['target_binding']='not-evaluated';scope(v,'target-binding');scope(v,'execution-support')
    add('R06',v,result(v,['N'],['N'],['equal'],True,'accept'),['conformance','supported-claims','reasons'],'Shared target binding does not erase passing invocation binding.')
    v=common('E+V','E',['E'],[('E','V')]);v['qualifier_findings'][0]['semantic_validation']='not-evaluated';scope(v,'independent-verification')
    add('R07',v,result(v,['E'],['E'],['support-below-claim'],False,'downgrade',gaps=[gap('E_IV_NOT_EVALUATED',['E+V'],['V(E)'])]),['reasons'],'Present IV with an evaluation gap is not missing evidence; no catch-all reason is added.')

    # Profile resolution controls retain the applied-identity boundary.
    v=deepcopy(cases[14]['input']);v['evaluation_context']['profile_identifiers']=[]
    for f in [v['boundary_finding']]+v['base_findings']+v['counter_evidence']:f['basis_refs']=[]
    add('R08',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input','vectors'],'An un-applied catalog entry cannot register C15 reason semantics; basis atoms are cleared to isolate token resolution.')
    v=deepcopy(cases[14]['input'])
    add('R09',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'An applied immutable fixture identity must resolve in the configured profile catalog.',{})
    p=deepcopy(CATALOG);p[PROFILE]['tokens']={}
    add('R10',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'Negative catalog-resolution control: the token registration is unavailable.',p)
    p=deepcopy(CATALOG);p[PROFILE]['tokens']['P_COUNTER_FAIL']['category']='evaluation-gap'
    add('R11',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'Negative catalog-resolution control: the returned category conflicts with the required substantive category.',p)
    p=deepcopy(CATALOG);other='core02-review-ambiguous-profile-1';p[other]=deepcopy(CATALOG[PROFILE]);v['evaluation_context']['profile_identifiers'].append(other)
    add('R12',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'Two applied profile registries resolve the same non-Core token ambiguously.',p)
    v=deepcopy(cases[14]['input']);e=deepcopy(cases[14]['expected'])
    add('R13',v,e,['normalized-input'],'The same second catalog entry is harmless when it is not applied.',p)

    for n,(field,key,value) in enumerate([
        ('boundary_finding','target','foreign'),('boundary_finding','evaluation_context_ref','foreign'),
        ('base_findings','target','foreign'),('base_findings','evaluation_context_ref','foreign'),
        ('qualifier_findings','target','foreign'),('qualifier_findings','evaluation_context_ref','foreign'),
        ('profile_evaluation_gaps','target','foreign'),('profile_evaluation_gaps','evaluation_context_ref','foreign')],14):
        v=common('E+V','E',['E'],[('E','V')]);v['profile_evaluation_gaps']=[gap('E_IV_NOT_EVALUATED',['E+V'])]
        f=v[field] if field=='boundary_finding' else v[field][0];f[key]=value
        add(f'R{n:02}',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input','input-validity'],'Foreign aggregate/gap '+field+'.'+key+' is an ingress mapping error; a good parallel finding cannot rescue it.')

    v=common('E','E',['E']);v['base_findings'].append(deepcopy(v['base_findings'][0]))
    add('R22',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'Duplicate aggregate keys are a cross-field error even for identical records.')
    v=common('E','E',['E']);v['boundary_finding'].pop('ceiling_base')
    add('R23',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'Supported boundary requires a ceiling.')
    v=common('E','E',['E']);v['counter_evidence']=[]
    add('R24',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'An empty entry set cannot replace the not-supplied sentinel.')
    v=common('E','E',['E'],[('E','V')]);v['qualifier_findings'][0]['independence_validation']='not-applicable'
    add('R25',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'Recognized but disallowed IV status is a mapping error.')
    v=common('E','E',['E']);v['boundary_finding']['grounding']='not-evaluated'
    add('R26',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input'],'Supported boundary with not-evaluated grounding violates conditional pairing.')

    v=common('E','E',['E']);v['semantics_version']='wexp-core-1';v['unknown_field']=True
    add('R27',v,reject('E_UNSUPPORTED_SEMANTICS_VERSION'),['input-validity','compatibility'],'Readable unsupported semantics wins before version-specific unknown-member validation.')
    v=common('E','E',['E']);v.pop('semantics_version');v['fatal_conditions']=['E_INTEGRITY_INVALID']
    add('R28',v,reject('E_MALFORMED_NORMALIZED_INPUT'),['input-validity'],'Missing semantics version wins before supplied fatal conditions.')
    v=common('I+P','E');v['fatal_conditions']=['E_INTEGRITY_INVALID','E_BINDING_MISMATCH']
    add('R29',v,reject(['E_INTEGRITY_INVALID','E_BINDING_MISMATCH']),['input-validity','algorithm'],'Both valid supplied fatal tokens precede asserted-domain rejection.')
    v=common('E','E',['E']);v['base_findings'][0]['target']='foreign';v['fatal_conditions']=['E_INTEGRITY_INVALID']
    add('R30',v,reject('E_PROFILE_MAPPING_INVALID'),['input-validity'],'Cross-field rejection precedes supplied fatal and all later diagnostics.')
    v=common('E','E',['E']);v['fatal_conditions']=['E_CLAIM_OUT_OF_DOMAIN']
    add('R31',v,reject('E_PROFILE_MAPPING_INVALID'),['input-validity'],'Appraiser-derived fatal tokens cannot be supplied.')

    v=common('E','E',['E']);v['boundary_finding']['status']='unsupported'
    add('R32',v,result(v,reasons=['E_BOUNDARY_NOT_SUPPORTED'],ceiling=None),['boundary-ceiling','reasons'],'Unsupported boundary makes a present diagnostic ceiling unusable but does not become ingress rejection.')
    v=common('E','E',['E']);v['base_findings'][0]['semantic_validation']='unsupported'
    add('R33',v,result(v,reasons=['E_EXACT_CLAIM_NOT_SUPPORTED']),['reasons'],'A present negative exact base has its own substantive reason, not missing evidence.')
    v=common('E+P','E',['E'],[('E','P')]);v['qualifier_findings'][0]['semantic_validation']='not-evaluated';scope(v,'provenance-support')
    add('R34',v,result(v,['E'],['E'],['support-below-claim'],gaps=[gap('E_PROV_NOT_EVALUATED',['E+P'],['P(E)'])]),['reasons'],'Present unevaluated PROV emits its exact gap and retains unqualified execution support.')
    v=common('E+V','E',['E'],[('E','V')]);v['qualifier_findings'][0]['independence_validation']='unsupported'
    add('R35',v,result(v,['E'],['E'],['support-below-claim'],reasons=['E_INDEPENDENCE_NOT_ESTABLISHED']),['reasons'],'A failed independence predicate does not create a missing-IV reason.')
    v=common('E','E',['E']);g=gap('E_COMPOSITION_NOT_EVALUATED',['E']);g['current_scope_capability']='composition';v['profile_evaluation_gaps']=[g]
    add('R36',v,reject('E_PROFILE_MAPPING_INVALID'),['normalized-input','conformance'],'Current composition marker requires matching not-evaluated capability.')
    scope(v,'composition')
    add('R37',v,result(v,['E'],['E'],['equal'],True,'accept',gaps=[g]),['reasons','conformance'],'A consistent supplied profile gap is preserved but alone does not block acceptance.')
    v=common('E','E',['E']);scope(v,'composition')
    add('R38',v,reject('E_PROFILE_MAPPING_INVALID'),['conformance'],'Not-evaluated external capability requires its current-scope marker.')
    v=common('E','E',['E']);v['evaluation_scope'].append({'capability':['unapplied-profile','x'],'status':'evaluated'})
    add('R39',v,reject('E_PROFILE_MAPPING_INVALID'),['conformance'],'Extension capability requires an applied immutable profile binding.')

    # Entry-scoped counter behavior covers both current capability values.
    for offset,status in enumerate(['resolved-no-defeat','not-evaluated','unresolved-material','defeating'],40):
        v=common('E','E',['E']);v['counter_evidence']=[counter(status,['E'],basis=['c'])];scope(v,'counter-evidence')
        kwargs={'exact':True,'verdict':'accept' if status=='resolved-no-defeat' else 'downgrade'}
        if status=='not-evaluated':kwargs['gaps']=[gap('E_COUNTER_EVIDENCE_NOT_EVALUATED',['E'],['c'])]
        elif status=='unresolved-material':kwargs['reasons']=['E_COUNTER_EVIDENCE_UNRESOLVED']
        elif status=='defeating':kwargs['reasons']=['E_COUNTER_EVIDENCE_DEFEATING']
        add(f'R{offset:02}',v,result(v,['E'],['E'],['equal'],**kwargs),['conformance','verdict','reasons'],'Each supplied entry keeps its status when current counter procedure is not completed: '+status+'.')
    v=common('E','E',['E']);v['counter_evidence']=[counter('defeating',['I'])]
    add('R44',v,result(v,['E'],['E'],['equal'],True,'accept'),['verdict','reasons'],'Defeat of intent is not defeat of execution.')

    # Finding reason projection is checked on boundary, asserted role,
    # unasserted exact support premise, and unrelated failed role.
    for cid,where,used in [('R45','boundary',True),('R46','asserted',True),('R47','support-premise',True),('R48','unrelated',False)]:
        v=common('E','E',['E','I'])
        if where=='boundary':f=v['boundary_finding']
        elif where=='asserted':f=v['base_findings'][0]
        else:f=v['base_findings'][1]
        f['reasons']=['E_EVIDENCE_COVERAGE_MISMATCH'];f['limitations']=atoms('L-scope')
        if where=='unrelated':f['semantic_validation']='unsupported'
        supported=['I','E'] if where!='unrelated' else ['E']
        limits={c:['L-scope'] for c in supported} if where=='boundary' else {'E':['L-scope']} if where=='asserted' else {'I':['L-scope']} if where=='support-premise' else {}
        add(cid,v,result(v,supported,['E'],['equal'],True,'accept',reasons=['E_EVIDENCE_COVERAGE_MISMATCH'] if used else [],limitations=['L-scope'] if used else [],support_limits=limits),['reasons','supported-claims'],'The profile reason projection route is '+where+'; a carried explanatory token does not independently change a status.')

    profile_bytes=(json.dumps(CATALOG,sort_keys=True,separators=(',',':'))+'\n').encode()
    return {'id':'WEXP-CORE-02-VECTORS-001','semantics_version':'wexp-core-2',
      'source_path':'drafts/core/02/draft-sergeev-wexp-core-02.xml',
      'source_sha256':SOURCE_SHA256,
      'expectation_origin':'Same-agent source-authored expectations; normative rows adapted from the pinned source-authored Core16 builder, review expectations specified above without invoking an appraiser.',
      'independent_external_review':False,'full_conformance_claim':False,
      'profile_registry_sha256':hashlib.sha256(profile_bytes).hexdigest(),
      'representation':'See REPRESENTATION.md; JSON is a local non-normative harness.',
      'profiles':CATALOG,'cases':cases}

