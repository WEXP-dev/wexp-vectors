"""Finite-model checks of Coverage-00 sections 4, 5 and 7.3.

Test-harness truth is explicitly supplied. This is NOT a deployment evaluator,
proof of capture, evidence adapter, or producer of a normative CoverageResult.
"""
from collections import Counter

CLAIMS = ('delivery-complete', 'delivery-exact', 'supplied-correspondence',
          'source-complete', 'source-sound', 'source-exact',
          'creation-complete', 'creation-sound', 'creation-exact', 'empty-actions')

def _set(items, name):
    if items is None:
        return None
    if type(items) is not list:
        raise ValueError(name + ' must be a list or unavailable')
    values = [tuple(item) if type(item) is list else item for item in items]
    if any(type(value) not in (str, tuple) for value in values):
        raise ValueError('Invalid finite-model occurrence')
    if len(set(values)) != len(values):
        raise ValueError('Repeated occurrence; no implicit retry normalization')
    return set(values)

def relation_predicates(left, right, edges):
    if left is None or right is None:
        return None, None, None
    edge_set = set(edges)
    if len(edge_set) != len(edges) or any(x not in left or y not in right for x,y in edges):
        raise ValueError('Malformed finite relation')
    ld = Counter(x for x,y in edges)
    rd = Counter(y for x,y in edges)
    complete = all(rd[y] >= 1 for y in right)
    sound = all(ld[x] >= 1 for x in left)
    exact = all(ld[x] == 1 for x in left) and all(rd[y] == 1 for y in right)
    return complete, sound, exact

def evaluate_model(model):
    required = {'A','C','R','S','Rv','B','F','H'}
    if type(model) is not dict or set(model) != required:
        raise ValueError('This harness requires exactly the finite-model fields')
    populations = {name:_set(model[name], name) for name in ('A','C','R','S','Rv')}
    a,c,r,s,rv = [populations[name] for name in ('A','C','R','S','Rv')]
    def edges(name):
        return [(tuple(x) if type(x) is list else x,
                 tuple(y) if type(y) is list else y) for x,y in model[name]]
    cc,cs,ce = relation_predicates(c,a,edges('B'))
    sc,ss,se = relation_predicates(s,a,edges('F'))
    _,_,correspondence = relation_predicates(rv,s,edges('H'))
    return dict(zip(CLAIMS, (None if c is None or r is None else c<=r,
                            None if c is None or r is None else c==r,
                            correspondence,sc,ss,se,cc,cs,ce,
                            None if a is None else not a), strict=True))

def aggregate(evaluated, support_ids, refutation_ids):
    """Section 7.3(5), given already admitted usable derivation identifiers."""
    if type(evaluated) is not bool:
        raise ValueError('Evaluation flag must be Boolean')
    if not evaluated:
        if support_ids or refutation_ids:
            raise ValueError('Unevaluated test claim cannot carry evaluated derivations')
        return {'evaluation_status':'not-evaluated','outcome':None,
                'conflict':False,'support':[],'refutation':[]}
    support,refutation=sorted(set(support_ids)),sorted(set(refutation_ids))
    outcome = ('not-established' if bool(support)==bool(refutation) else
               'supported' if support else 'refuted')
    return {'evaluation_status':'evaluated','outcome':outcome,
            'conflict':bool(support and refutation),'support':support,'refutation':refutation}
