"""Bounded finite-world checks, not a Coverage deployment evaluator."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
MEMBERS = {'logic.py', 'cases.py', 'cases.json', 'check.py', 'README.md'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--source-xml', type=Path)
    args = parser.parse_args()
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    if set(manifest['files']) != MEMBERS:
        raise ValueError('Incomplete or unexpected file inventory')
    for name, expected in manifest['files'].items():
        path = HERE / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen file mismatch: ' + name)
    if args.source_xml is not None and hashlib.sha256(args.source_xml.read_bytes()).hexdigest() != manifest['specification']['xml_sha256']:
        raise ValueError('Published Coverage XML digest mismatch')
    # Source identities are checked before any model or expectation import.
    from logic import CLAIMS, evaluate_model, relation_predicates, aggregate
    from cases import cases
    raw = (HERE / 'cases.json').read_bytes()
    expanded = (json.dumps(cases(), sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')
    if raw != expanded:
        raise ValueError('Frozen example bytes do not match source-authored expansion')
    rows=[]
    for case in json.loads(raw):
        actual=evaluate_model(case['model'])
        expected=dict(zip(CLAIMS,case['expected_values'],strict=True))
        if actual!=expected:
            raise SystemExit('Frozen case mismatch: '+case['id']+' '+repr((actual,expected)))
        rows.append({'id':case['id'],'passed':True,'predicate_values':actual})
    graphs=0
    for nx,ny in itertools.product(range(3),repeat=2):
        left,right=set(range(nx)),set(range(ny))
        possible=list(itertools.product(left,right))
        for mask in range(1<<len(possible)):
            edges=[edge for i,edge in enumerate(possible) if mask&(1<<i)]
            # Explicit quantified formula, no Counter or evaluator helpers.
            expected=(all(any(x==a and y==b for x,y in edges for a in left) for b in right),
                      all(any(x==a and y==b for x,y in edges for b in right) for a in left),
                      all(sum(1 for x,y in edges if x==a)==1 for a in left) and
                      all(sum(1 for x,y in edges if y==b)==1 for b in right))
            if relation_predicates(left,right,edges)!=expected:
                raise SystemExit('Relation mismatch')
            graphs+=1
    receipts=[('r1','h1'),('r1','h2'),('r2','h1')]
    delivery=0
    for cm,rm in itertools.product(range(8),repeat=2):
        c=[list(x) for i,x in enumerate(receipts) if cm&(1<<i)]
        r=[list(x) for i,x in enumerate(receipts) if rm&(1<<i)]
        m={'A':[],'C':c,'R':r,'S':[],'Rv':r,'B':[],'F':[],'H':[]}
        actual=evaluate_model(m)
        expected=all(any(x[0]==y[0] and x[1]==y[1] for y in r) for x in c)
        reverse=all(any(x[0]==y[0] and x[1]==y[1] for y in c) for x in r)
        if actual['delivery-complete']!=expected or actual['delivery-exact']!=(expected and reverse):
            raise SystemExit('Delivery identity/content mismatch')
        delivery+=1
    aggregation=[(True,[],[],'not-established',False),
                 (True,['p'],[],'supported',False),
                 (True,[],['n'],'refuted',False),
                 (True,['p'],['n'],'not-established',True),
                 (False,[],[],None,False)]
    for evaluated,pos,neg,outcome,conflict in aggregation:
        actual=aggregate(evaluated,pos,neg)
        if actual['outcome']!=outcome or actual['conflict']!=conflict or actual['support']!=pos or actual['refutation']!=neg:
            raise SystemExit('Aggregation mismatch')
    invalid_checks=0
    for fn in [lambda:aggregate(False,['p'],[]),lambda:aggregate(1,[],[]),
               lambda:evaluate_model({'A':[]}),
               lambda:relation_predicates({1},{2},[(1,3)]),
               lambda:evaluate_model({'A':['a','a'],'C':[],'R':[],'S':[],'Rv':[],'B':[],'F':[],'H':[]})]:
        try:fn()
        except ValueError:invalid_checks+=1
        else:raise SystemExit('Invalid input accepted')
    report={'status':'PASS_BOUNDED_LOGICAL_CHECKS','python':platform.python_version(),
            'optimized':not __debug__,'frozen_cases':rows,'finite_relation_graphs':graphs,
            'relation_predicate_comparisons':3*graphs,'delivery_population_pairs':delivery,
            'delivery_predicate_comparisons':2*delivery,'aggregation_cases':len(aggregation),
            'invalid_controls':invalid_checks,'full_rule_evaluator':False,
            'pg02_runtime_validation':False,'external_independent_review':False}
    report['specification'] = manifest['specification']['document']
    report['rule_set'] = manifest['rule_set']
    report['source_xml_bytes_checked'] = args.source_xml is not None
    report['cases_sha256'] = hashlib.sha256(raw).hexdigest()
    report['model_sha256'] = manifest['files']['logic.py']
    if args.output is not None:
        if args.output.resolve().is_relative_to(HERE):
            raise ValueError('Run evidence must stay outside the frozen package')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k!='frozen_cases'}, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
