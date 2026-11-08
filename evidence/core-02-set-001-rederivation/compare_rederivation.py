#!/usr/bin/env python3
"""Component-wise, set-aware comparison of a re-derived expectation directory with a frozen corpus.

usage: compare_rederivation.py <frozen corpus.json> <directory of re-derived <id>.json files> [<output comparison.json>]

Set semantics follow the harness description (corpus README, "Logical encoding"): the collections listed in
SET_FIELDS are compared as unordered sets; everything else exactly, with Booleans distinct from numbers and
null distinct from an absent member. No implementation is imported.
"""
import json, sys
from pathlib import Path
SET_FIELDS = {'qualifiers','profile_identifiers','basis_refs','reasons','limitations','base_findings','qualifier_findings',
              'recorder_relations','counter_evidence','evaluation_scope','profile_evaluation_gaps','inherited_limitations',
              'fatal_conditions','affected_claims','fatal_reasons','substantive_reasons','evaluation_gaps',
              'evaluation_gap_entries','supported_claims','maximal_supported_claims','support_entries','support_relations'}
def enc(v): return json.dumps(v, ensure_ascii=True, sort_keys=True, separators=(',',':'), allow_nan=False)
def logical(v, field=None):
    if type(v) is dict: return {k: logical(x, k) for k, x in v.items()}
    if type(v) is list:
        items = [logical(x) for x in v]
        return sorted(items, key=enc) if field in SET_FIELDS else items
    return v
def same(a, b): return enc(logical(a)) == enc(logical(b))
def main():
    corpus = json.loads(Path(sys.argv[1]).read_bytes())
    frozen = {c['id']: c['expected'] for c in corpus['cases']}
    newdir = Path(sys.argv[2])
    rows = []; agree = 0
    for cid, exp in frozen.items():
        p = newdir / f'{cid}.json'
        if not p.is_file():
            rows.append({'id': cid, 'status': 'MISSING'}); continue
        delivered = json.loads(p.read_bytes())
        if set(delivered) != {'id', 'expected'} or delivered['id'] != cid:
            rows.append({'id': cid, 'status': 'SHAPE', 'detail': 'file must hold exactly id and expected, with id equal to the file name'}); continue
        new = delivered['expected']
        if set(new) != set(exp):
            rows.append({'id': cid, 'status': 'SHAPE', 'missing': sorted(set(exp)-set(new)), 'extra': sorted(set(new)-set(exp))}); continue
        diffs = {k: {'frozen': exp[k], 'rederived': new[k]} for k in exp if not same({k: exp[k]}, {k: new[k]})}
        if diffs: rows.append({'id': cid, 'status': 'DIFF', 'components': diffs})
        else: rows.append({'id': cid, 'status': 'EQUAL'}); agree += 1
    extra = sorted(p.stem for p in newdir.glob('*.json') if p.stem not in frozen)
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_text(json.dumps({'equal': agree, 'compared': len(frozen), 'unexpected_files': extra, 'cases': rows}, indent=1, sort_keys=True) + '\n')
    print(f'EQUAL {agree}/{len(frozen)}' + (f'; unexpected files: {extra}' if extra else ''))
    for r in rows:
        if r['status'] != 'EQUAL':
            print(r['id'], r['status'], sorted(r['components']) if 'components' in r else {k: v for k, v in r.items() if k != 'id'})
    return 0 if agree == len(frozen) and not extra else 1
if __name__ == '__main__':
    raise SystemExit(main())
