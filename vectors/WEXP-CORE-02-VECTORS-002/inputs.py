#!/usr/bin/env python3
"""Source-encoded inputs for WEXP-CORE-02-VECTORS-002 (section 7 boundary matrix).

Inputs only. Expected results live in expectations/*.json exactly as delivered by
the separate derivation session; this module never computes or imports an expectation,
and it imports no appraiser.
"""
from copy import deepcopy

PROFILE = 'draft-sergeev-wexp-core-02/fixture-1'
CATALOG = {PROFILE: {'tokens': {'P_COUNTER_FAIL': {'category': 'substantive'}},
                     'relation_tokens': [], 'scope_names': []}}
# Section 13 fixture atom: "accepts attributed boundary grounding".
TRUST_FIXTURE = 'core02-fixture-trust-1'
# Local test atom defined by this package: minimum acceptable boundary grounding is asserted-only.
TRUST_ASSERTED_ONLY = 'core02-test-trust-asserted-only-1'
CAPS = ('carrier-mapping', 'authenticity', 'target-binding', 'boundary-grounding',
        'observation-support', 'intent-support', 'invocation-support', 'execution-support',
        'provenance-support', 'independent-verification', 'composition', 'counter-evidence')
STATUS = ('supported', 'unsupported', 'not-evaluated')
GROUNDING = ('asserted-only', 'attributed', 'attested', 'not-evaluated')
BINDING = ('supported', 'unsupported', 'not-evaluated')
# Core-observable cells already instantiated by WEXP-CORE-02-VECTORS-001 revision 2.
COVERED = {('supported', 'attributed', 'supported'): 'C01-C16 and most R/P cases',
           ('supported', 'not-evaluated', 'supported'): 'R26',
           ('unsupported', 'asserted-only', 'supported'): 'P15',
           ('unsupported', 'attributed', 'supported'): 'R32'}

def atoms(*names):
    return [[PROFILE, name] for name in names]

def base_input(trust, status, grounding, binding):
    return {'semantics_version': 'wexp-core-2', 'target': 'T',
            'asserted_claim': {'base': 'execution', 'qualifiers': []},
            'evaluation_context': {'id': 'C', 'evaluated_at': '2026-10-12T00:00:00Z',
                                   'trust_configuration': trust, 'profile_identifiers': [PROFILE]},
            'boundary_finding': {'target': 'T', 'evaluation_context_ref': 'C', 'status': status,
                                 'target_binding': binding, 'grounding': grounding,
                                 'ceiling_base': 'execution', 'basis_refs': atoms('bd'),
                                 'reasons': [], 'limitations': atoms('L-boundary')},
            'base_findings': [{'target': 'T', 'evaluation_context_ref': 'C', 'base': 'execution',
                               'target_binding': 'supported', 'semantic_validation': 'supported',
                               'basis_refs': atoms('E'), 'reasons': [], 'limitations': []}],
            'qualifier_findings': [], 'recorder_relations': [],
            'counter_evidence': [{'status': 'not-supplied', 'affected_claims': [], 'basis_refs': [],
                                  'reasons': [], 'limitations': []}],
            'evaluation_scope': [{'capability': c, 'status': 'evaluated'} for c in CAPS],
            'profile_evaluation_gaps': [], 'inherited_limitations': [], 'fatal_conditions': []}

def set_scope(value, capability, status='not-evaluated'):
    next(x for x in value['evaluation_scope'] if x['capability'] == capability)['status'] = status

def cases():
    """Return the ordered list of {'id','kind','cell','derivation','input'} without expectations."""
    rows = []
    def add(kind, cell, why, value):
        rows.append({'id': f'B{len(rows) + 1:02}', 'kind': kind, 'cell': cell,
                     'source_anchors': ['boundary-ceiling', 'normalized-input', 'reasons', 'conformance'],
                     'derivation': why, 'input': deepcopy(value)})
    number = 0
    for status in STATUS:
        for grounding in GROUNDING:
            for binding in BINDING:
                number += 1
                if (status, grounding, binding) in COVERED:
                    continue
                trust = TRUST_ASSERTED_ONLY if (status, grounding) == ('supported', 'asserted-only') else TRUST_FIXTURE
                value = base_input(trust, status, grounding, binding)
                if 'not-evaluated' in (status, grounding, binding):
                    set_scope(value, 'boundary-grounding')
                if binding == 'not-evaluated':
                    set_scope(value, 'target-binding')
                add('matrix-cell', {'number': number, 'status': status, 'grounding': grounding,
                                    'target_binding': binding},
                    f'Section 7 matrix cell {number}: status={status}, grounding={grounding}, '
                    f'target_binding={binding}; evaluation_scope consistent with section 12 governed fields.',
                    value)
    value = base_input(TRUST_FIXTURE, 'not-evaluated', 'not-evaluated', 'supported')
    add('control', {'number': 0, 'status': 'not-evaluated', 'grounding': 'not-evaluated', 'target_binding': 'supported',
                    'variation': 'evaluation_scope[boundary-grounding] left evaluated'},
        'Section 12 control: boundary status and grounding are not-evaluated while evaluation_scope[boundary-grounding] '
        'stays evaluated; the cross-field check precedes section 7 precedence.', value)
    value = base_input(TRUST_FIXTURE, 'supported', 'attributed', 'not-evaluated')
    set_scope(value, 'target-binding')
    add('control', {'number': 0, 'status': 'supported', 'grounding': 'attributed', 'target_binding': 'not-evaluated',
                    'variation': 'evaluation_scope[target-binding] not-evaluated, [boundary-grounding] left evaluated'},
        'Section 12 control: boundary binding is a field governed by boundary-grounding; its not-evaluated status with an '
        'evaluated boundary-grounding scope is a cross-field violation.', value)
    value = base_input(TRUST_FIXTURE, 'supported', 'asserted-only', 'supported')
    add('probe', {'number': 0, 'status': 'supported', 'grounding': 'asserted-only', 'target_binding': 'supported',
                  'variation': 'trust_configuration core02-fixture-trust-1 (accepts attributed; asserted-only not accepted)'},
        'Acceptance probe: a supported asserted-only boundary under a context whose minimum is attributed. Section 7 forbids a '
        'profile from producing it; the probe records what Core, which sees an opaque trust atom, derives.', value)
    return rows

if __name__ == '__main__':
    import json
    print(json.dumps([{'id': r['id'], 'kind': r['kind'], 'cell': r['cell']} for r in cases()], indent=1))
