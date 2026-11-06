#!/usr/bin/env python3
"""Rebuild the input files handed to the isolated session from the frozen corpus.json and check them
against HANDOFF-SHA256SUMS.txt. usage: check_handoff_inputs.py <frozen corpus.json> <HANDOFF-SHA256SUMS.txt>
Only the 89 inputs/*.json and profiles.json are rebuilt here; the spec text, brief and format reference are
checked by digest when present in the same directory as this script's parent (BRIEF-given-to-the-session.md)."""
import hashlib, json, sys
from pathlib import Path
corpus = json.loads(Path(sys.argv[1]).read_bytes())
sums = dict(line.split('  ', 1)[::-1] for line in Path(sys.argv[2]).read_text().splitlines() if line.strip())
sums = {k.strip(): v for k, v in sums.items()}
def sha(b): return hashlib.sha256(b).hexdigest()
ok = bad = 0
for case in corpus['cases']:
    item = {'id': case['id'], 'input': case['input']}
    if 'profiles' in case: item['profiles'] = case['profiles']
    raw = (json.dumps(item, indent=1, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')
    if sums.get(f"inputs/{case['id']}.json") == sha(raw): ok += 1
    else: bad += 1; print('MISMATCH inputs/' + case['id'] + '.json')
raw = (json.dumps(corpus['profiles'], indent=1, sort_keys=True) + '\n').encode()
if sums.get('profiles.json') == sha(raw): ok += 1
else: bad += 1; print('MISMATCH profiles.json')
c01 = next(k for k in corpus['cases'] if k['id'] == 'C01')
raw = (json.dumps({'id': 'C01', 'note': 'section 13 normative fixture C01 transcribed; format reference for the twenty result components and the local JSON encoding only', 'input': c01['input'], 'expected': c01['expected']}, indent=1, sort_keys=True) + '\n').encode()
if sums.get('FORMAT-REFERENCE-C01.json') == sha(raw): ok += 1
else: bad += 1; print('MISMATCH FORMAT-REFERENCE-C01.json')
brief = Path(sys.argv[2]).with_name('BRIEF-given-to-the-session.md')
if brief.is_file():
    if sums.get('BRIEF.md') == sha(brief.read_bytes()): ok += 1
    else: bad += 1; print('MISMATCH BRIEF.md')
print(f'handoff files rebuilt and matching: {ok}; mismatching: {bad}; listed but not rebuilt here: {sorted(k for k in sums if k.startswith("spec/"))}')
sys.exit(1 if bad else 0)
