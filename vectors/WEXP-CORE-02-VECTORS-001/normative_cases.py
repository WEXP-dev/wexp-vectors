#!/usr/bin/env python3
"""Source-authored complete C01..C16 expectations; no appraiser/oracle imports.

The row tables below implement Core-02 sections 8.4 and 13, adapted from
the pinned source-authored Core-01 builder. The new fixture context and
semantics identity are explicit. This is not independent external review.
"""
from copy import deepcopy

PROFILE='draft-sergeev-wexp-core-02/fixture-1'
CATALOG={PROFILE:{'tokens':{'P_COUNTER_FAIL':{'category':'substantive'}},
                  'relation_tokens':[], 'scope_names':[]}}
BASE={'O':'observation','I':'intent','N':'invocation','E':'execution'}
CAPS=('carrier-mapping','authenticity','target-binding','boundary-grounding',
      'observation-support','intent-support','invocation-support','execution-support',
      'provenance-support','independent-verification','composition','counter-evidence')

def claim(name):
    pieces=name.split('+')
    return {'base':BASE[pieces[0]],'qualifiers':[{'P':'PROV','V':'IV'}[q] for q in pieces[1:]]}

def atoms(*names):return [[PROFILE,name] for name in names]

def finding(base, qualifier=None):
    f={'target':'T','evaluation_context_ref':'C','target_binding':'supported',
       'semantic_validation':'supported','basis_refs':atoms(base if qualifier is None else qualifier+'('+base+')'),
       'reasons':[], 'limitations':[]}
    if qualifier is None:f['base']=BASE[base]
    else:f.update(qualifier={'P':'PROV','V':'IV'}[qualifier],qualified_base=BASE[base],
                  independence_validation='supported' if qualifier=='V' else 'not-applicable')
    return f

def counter(status, affected=(), reasons=(), basis=()):
    return {'status':status,'affected_claims':[claim(c) for c in affected],
            'basis_refs':atoms(*basis),'reasons':list(reasons),'limitations':[]}

def gap(token, affected, basis=(), limits=()):
    return {'token':token,'target':'T','evaluation_context_ref':'C',
            'affected_claims':[claim(c) for c in affected],
            'basis_refs':atoms(*basis),'limitations':atoms(*limits)}

def common(asserted, ceiling, bases=(), qualifiers=()):
    return {'semantics_version':'wexp-core-2','target':'T','asserted_claim':claim(asserted),
      'evaluation_context':{'id':'C','evaluated_at':'2026-10-12T00:00:00Z',
        'trust_configuration':'core02-fixture-trust-1','profile_identifiers':[PROFILE]},
      'boundary_finding':{'target':'T','evaluation_context_ref':'C','status':'supported',
        'target_binding':'supported','grounding':'attributed','ceiling_base':BASE[ceiling],
        'basis_refs':atoms('bd'),'reasons':[],'limitations':[]},
      'base_findings':[finding(b) for b in bases],
      'qualifier_findings':[finding(b,q) for b,q in qualifiers],
      'recorder_relations':[],'counter_evidence':[counter('not-supplied')],
      'evaluation_scope':[{'capability':c,'status':'evaluated'} for c in CAPS],
      'profile_evaluation_gaps':[],'inherited_limitations':[],'fatal_conditions':[]}

def rejected():
    return {'semantics_version':'wexp-core-2','verdict':'reject',
      'fatal_reasons':['E_CLAIM_OUT_OF_DOMAIN'],'target':None,'asserted_claim':None,
      'asserted_claim_supported':False,'support_entries':[],'supported_claims':[],
      'maximal_supported_claims':[],'support_relations':[],'boundary_ceiling':None,
      'boundary_grounding':None,'recorder_relations':None,'substantive_reasons':[],
      'evaluation_gaps':[],'evaluation_gap_entries':[],'counter_evidence':None,
      'inherited_limitations':None,'evaluation_context':None,'evaluation_scope':None}

# These data are the normative table's S, M, A, relation, verdict and reason
# columns, not calculated by an implementation of the appraisal procedure.
ROWS=[
 ('C01','I','I',['I'],[],['I'],['I'],True,['equal'],'accept',[]),
 ('C02','I','E',['E'],[],['E'],['E'],False,['support-above-claim'],'downgrade',['E_MISSING_REQUIRED_EVIDENCE']),
 ('C03','E+V','E',['E'],[('E','P')],['E','E+P'],['E+P'],False,['incomparable'],'downgrade',['E_MISSING_REQUIRED_EVIDENCE']),
 ('C04','E+P','E',['E'],[('E','V')],['E','E+V'],['E+V'],False,['incomparable'],'downgrade',['E_MISSING_REQUIRED_EVIDENCE']),
 ('C05','N+V','N',['N'],[('N','V')],['N','N+V'],['N+V'],True,['equal'],'accept',[]),
 ('C06','E+V','E',['N','E'],[('N','V')],['N','N+V','E'],['N+V','E'],False,['support-below-claim','support-below-claim'],'downgrade',['E_MISSING_REQUIRED_EVIDENCE']),
 ('C07','E','N',['E'],[],[],[],False,[],'downgrade',['E_BASE_EXCEEDS_BOUNDARY']),
 ('C08','O','O',[],[],[],[],False,[],'downgrade',['E_MISSING_REQUIRED_EVIDENCE']),
 ('C09','I+P','E',[],[],[],[],False,[],'reject',[]),
 ('C10','I','I',['I'],[],['I'],['I'],True,['equal'],'downgrade',['E_COUNTER_EVIDENCE_UNRESOLVED']),
 ('C11','E','E',['E'],[],['E'],['E'],True,['equal'],'accept',[]),
 ('C12','E','E',['E'],[],['E'],['E'],True,['equal'],'accept',[]),
 ('C13','E','E',['E'],[],['E'],['E'],True,['equal'],'accept',[]),
 ('C14','E','E',['E'],[],['E'],['E'],True,['equal'],'downgrade',[]),
 ('C15','E','E',['E'],[],['E'],['E'],True,['equal'],'downgrade',['E_COUNTER_EVIDENCE_UNRESOLVED','P_COUNTER_FAIL']),
 ('C16','E','E',['E'],[],['E'],['E'],True,['equal'],'accept',[]),
]

def build():
    cases=[]
    for cid, asserted, ceiling, bases, quals, supported, maximal, exact, relations, verdict, reasons in ROWS:
        v=common(asserted,ceiling,bases,quals)
        gs=[]; limits=[]
        if cid=='C10':v['counter_evidence']=[counter('unresolved-material',['I'])]
        if cid in ('C11','C12'):v['base_findings'][0]['basis_refs']=atoms('s1','s2','adj','w')
        if cid=='C12':
            v['boundary_finding']['limitations']=atoms('L-boundary')
            v['base_findings'][0]['limitations']=atoms('L-boundary')
            next(s for s in v['evaluation_scope'] if s['capability']=='independent-verification')['status']='not-evaluated'
            limits=atoms('L-boundary')
        if cid=='C13':
            gs=[gap('E_IV_NOT_EVALUATED',['E'],['u1'],['L-upstream'])]
            v['profile_evaluation_gaps']=deepcopy(gs);limits=atoms('L-upstream')
        if cid=='C14':
            v['counter_evidence']=[counter('defeating',['I']),counter('not-evaluated',['E'])]
            gs=[gap('E_COUNTER_EVIDENCE_NOT_EVALUATED',['E'])]
        if cid=='C15':v['counter_evidence']=[counter('unresolved-material',['E'],['P_COUNTER_FAIL'],['p1'])]
        if cid=='C16':v['profile_evaluation_gaps']=[gap('E_IV_NOT_EVALUATED',['N+V'],['u2'],['L-unrelated'])]
        if cid=='C09':expected=rejected()
        else:
            entries=[]
            for name in supported:
                parts=name.split('+')
                basis=['bd',parts[0]]+[q+'('+parts[0]+')' for q in parts[1:]]
                if cid in ('C11','C12'):basis=['bd','s1','s2','adj','w']
                entries.append({'claim':claim(name),'basis_refs':atoms(*basis),
                                'limitations':atoms('L-boundary') if cid=='C12' else []})
            expected={'semantics_version':'wexp-core-2','verdict':verdict,'fatal_reasons':[],
              'target':'T','asserted_claim':claim(asserted),'asserted_claim_supported':exact,
              'support_entries':entries,'supported_claims':[claim(c) for c in supported],
              'maximal_supported_claims':[claim(c) for c in maximal],
              'support_relations':[{'supported_claim':claim(c),'relation':rel} for c,rel in zip(maximal,relations,strict=True)],
              'boundary_ceiling':BASE[ceiling],'boundary_grounding':'attributed',
              'recorder_relations':[],'substantive_reasons':reasons,
              'evaluation_gaps':[g['token'] for g in gs],'evaluation_gap_entries':gs,
              'counter_evidence':deepcopy(v['counter_evidence']),
              'inherited_limitations':limits,'evaluation_context':deepcopy(v['evaluation_context']),
              'evaluation_scope':deepcopy(v['evaluation_scope'])}
        if len(expected) != 20:
            raise ValueError('Expected exactly twenty result components')
        cases.append({'id':cid,'input':v,'expected':expected})
    return {'profiles':CATALOG,'cases':cases}
