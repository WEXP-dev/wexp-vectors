"""Source-derived controls for the posted Core-02, separate from C01-C16.

No implementation imports. Expectations are authored before qualification.
"""
from copy import deepcopy
from normative_cases import CATALOG, PROFILE, common, claim, atoms, gap
from review_cases import scope, reject, result

EXT = 'wexp-core02-test-profile/extension-1'
EXTENSION = {'tokens': {'P_AUTH_GAP': {'category': 'evaluation-gap',
                                     'current_scope_capability': 'authenticity'}},
             'relation_tokens': ['same-controller'], 'scope_names': ['audit-window']}

def cases():
    rows = []
    def add(name, value, expected, sections, why, profiles=None):
        item = {'id': name, 'kind': 'derived-posting-case',
                'source_sections': sections, 'derivation': why,
                'input': deepcopy(value), 'expected': deepcopy(expected)}
        if profiles is not None:
            item['profiles'] = deepcopy(profiles)
        if len(expected) != 20:
            raise ValueError('Expected exactly twenty result components')
        rows.append(item)

    # Section 12 explicitly fixes structural classification, including precedence.
    malformed = [[], [EXT], [EXT, 'audit-window', 'extra'],
                 [EXT, ''], ['', 'audit-window'], [EXT, 0],
                 [EXT, None], [EXT, '\ud800']]
    for number, key in enumerate(malformed, 1):
        value = common('E', 'E', ['E'])
        value['evaluation_scope'].append({'capability': key, 'status': 'evaluated'})
        add(f'P{number:02}', value, reject('E_MALFORMED_NORMALIZED_INPUT'),
            ['6.2', '12'], 'Malformed extension pair is structural, before binding checks.')
    value = common('E', 'E', ['E'])
    value['base_findings'][0]['target'] = 'foreign'
    value['evaluation_scope'].append({'capability': [], 'status': 'evaluated'})
    value['fatal_conditions'] = ['E_INTEGRITY_INVALID']
    add('P09', value, reject('E_MALFORMED_NORMALIZED_INPUT'), ['6.2', '12'],
        'Malformed pair precedes foreign scope and supplied fatal conditions.')
    value = common('E', 'E', ['E'])
    value['evaluation_scope'].append({'capability': [EXT, 'audit-window'], 'status': 'evaluated'})
    add('P10', value, reject('E_PROFILE_MAPPING_INVALID'), ['6.2', '12'],
        'A well-formed but unapplied extension pair is a mapping failure.')

    profiles = deepcopy(CATALOG)
    profiles[EXT] = deepcopy(EXTENSION)
    value['evaluation_context']['profile_identifiers'].append(EXT)
    add('P11', value, result(value, ['E'], ['E'], ['equal'], True, 'accept'),
        ['8.4', '12'], 'Bound extension status is preserved without changing exact support.', profiles)
    scope(value, [EXT, 'audit-window'])
    add('P12', value, result(value, ['E'], ['E'], ['equal'], True, 'accept'),
        ['8.4', '12'], 'Unperformed extension alone creates no Core gap or support ceiling.', profiles)
    value['evaluation_scope'].append(deepcopy(value['evaluation_scope'][-1]))
    add('P13', value, reject('E_PROFILE_MAPPING_INVALID'), ['6.2', '12'],
        'Duplicate bound extension key is a cross-field violation.', profiles)

    value = common('E+P+V', 'E', ['E'], [('E', 'P'), ('E', 'V')])
    add('P14', value, result(value, ['E', 'E+P', 'E+V', 'E+P+V'],
                            ['E+P+V'], ['equal'], True, 'accept'),
        ['4.4', '8.1'], 'Both qualifiers coexist and every subset is reported.')
    value = common('E', 'E', ['E'])
    value['boundary_finding']['status'] = 'unsupported'
    value['boundary_finding']['grounding'] = 'asserted-only'
    value['boundary_finding']['limitations'] = atoms('L-boundary')
    add('P15', value, result(value, reasons=['E_BOUNDARY_NOT_SUPPORTED'],
                            limitations=['L-boundary'], ceiling=None),
        ['7', '8.5'], 'Unsupported boundary retains its grounding and limitations.')

    value = common('E', 'E', ['E'])
    value['evaluation_context']['profile_identifiers'].append(EXT)
    scope(value, 'authenticity')
    entry = gap('P_AUTH_GAP', ['E'], ['auth-basis'], ['L-auth'])
    entry['current_scope_capability'] = 'authenticity'
    value['profile_evaluation_gaps'] = [entry]
    add('P16', value, result(value, ['E'], ['E'], ['equal'], True, 'accept',
                            gaps=[entry], limitations=['L-auth']),
        ['6', '8.4', '12'], 'A bound current authenticity gap is copied; it is not an independent veto.', profiles)
    broken = deepcopy(value)
    broken['profile_evaluation_gaps'][0]['current_scope_capability'] = 'composition'
    add('P17', broken, reject('E_PROFILE_MAPPING_INVALID'), ['6', '12'],
        'Well-typed token/capability mismatch is mapping failure.', profiles)
    broken = deepcopy(value)
    broken['profile_evaluation_gaps'][0]['current_scope_capability'] = 'execution-support'
    add('P18', broken, reject('E_PROFILE_MAPPING_INVALID'), ['6', '6.2'],
        'Recognized but disallowed initial capability is a mapping failure.', profiles)
    broken = deepcopy(value)
    broken['profile_evaluation_gaps'][0]['current_scope_capability'] = 'unknown-capability'
    add('P19', broken, reject('E_MALFORMED_NORMALIZED_INPUT'), ['6.2'],
        'Unknown closed capability name is structural.', profiles)
    broken = deepcopy(value)
    del broken['profile_evaluation_gaps'][0]['token']
    add('P20', broken, reject('E_MALFORMED_NORMALIZED_INPUT'), ['6', '6.2'],
        'Missing required gap member is structural.', profiles)
    broken = deepcopy(value)
    broken['profile_evaluation_gaps'][0]['affected_claims'] = []
    add('P21', broken, reject('E_PROFILE_MAPPING_INVALID'), ['6', '6.2'],
        'Well-typed empty affected-claim set is mapping failure.', profiles)
    broken = deepcopy(value)
    broken['profile_evaluation_gaps'][0]['token'] = 'E_INTEGRITY_INVALID'
    add('P22', broken, reject('E_PROFILE_MAPPING_INVALID'), ['6', '6.2'],
        'A valid token in the wrong category is mapping failure.', profiles)

    value = common('E', 'E', ['E'])
    value['evaluation_context']['profile_identifiers'].append(EXT)
    relation = {'profile_identifier': EXT, 'relation_token': 'same-controller',
                'subject_ref': [EXT, 'a'], 'object_ref': [EXT, 'b'],
                'basis_refs': [[EXT, 'binding']], 'limitations': []}
    value['recorder_relations'] = [relation]
    add('P23', value, result(value, ['E'], ['E'], ['equal'], True, 'accept'),
        ['6.1', '8.5'], 'Recorder relation is carried without manufacturing IV.', profiles)
    value['asserted_claim'] = claim('E+V')
    add('P24', value, result(value, ['E'], ['E'], ['support-below-claim'],
                            reasons=['E_MISSING_REQUIRED_EVIDENCE']),
        ['4.3', '6.1', '8.6'], 'Descriptive relation does not substitute for an IV finding.', profiles)
    value = common('E', 'E', ['E'])
    value['target'] = '\u00e9'
    value['boundary_finding']['target'] = '\u00e9'
    value['base_findings'][0]['target'] = 'e\u0301'
    add('P25', value, reject('E_PROFILE_MAPPING_INVALID'), ['6.1', '6.2'],
        'Target equality is exact; no implicit Unicode or URI normalization.')
    return rows
