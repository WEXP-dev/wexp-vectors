#!/usr/bin/env python3
"""Expand a frozen source-encoded corpus. Never invokes an appraiser."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def build():
    from review_cases import package
    from final_contract_cases import cases as posting_cases
    data = package()
    data['cases'].extend(posting_cases())
    return data

def encoded():
    # Escaping includes an intentional isolated-surrogate negative test.
    return (json.dumps(build(), sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    manifest = None
    if args.check:
        manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
        for name, expected in manifest['files'].items():
            if Path(name).name != name:
                raise SystemExit('Unsafe manifest path')
            actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            if actual != expected:
                raise SystemExit('Frozen source mismatch: ' + name)
    raw = encoded()
    digest = hashlib.sha256(raw).hexdigest()
    if manifest is not None and manifest['expanded_corpus_sha256'] != digest:
        raise SystemExit('Frozen expanded corpus mismatch')
    if args.output:
        if args.output.resolve() in {p.resolve() for p in HERE.iterdir() if p.is_file()}:
            raise SystemExit('Refusing to overwrite source or manifest')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # Never overwrite an earlier generated artifact silently.
        with args.output.open('xb') as stream:
            stream.write(raw)
    print(json.dumps({'cases': len(build()['cases']), 'sha256': digest,
                      'appraiser_executed': False}))

if __name__ == '__main__':
    main()
