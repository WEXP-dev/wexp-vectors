#!/usr/bin/env python3
"""Expand WEXP-CORE-02-VECTORS-002: source-encoded inputs joined with verbatim frozen expectations.

Never invokes an appraiser. Expectations are read from expectations/*.json exactly as delivered by
the separate derivation session; this script does not compute, repair or reorder them.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_SHA256 = 'de983051a1c6ea51ea9b7f965fe9eabf2d97af92ab2f074781bd44e3f99c8782'

def strict_pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('Duplicate JSON member: ' + key)
        result[key] = value
    return result

def build():
    from inputs import cases, CATALOG
    rows = cases()
    for row in rows:
        path = HERE / 'expectations' / (row['id'] + '.json')
        if path.is_symlink() or not path.is_file():
            raise ValueError('Missing frozen expectation: ' + row['id'])
        delivered = json.loads(path.read_bytes(), object_pairs_hook=strict_pairs)
        if delivered.get('id') != row['id'] or set(delivered) != {'id', 'expected'}:
            raise ValueError('Expectation file shape: ' + row['id'])
        if len(delivered['expected']) != 20:
            raise ValueError('Expected exactly twenty result components: ' + row['id'])
        row['expected'] = delivered['expected']
    profile_bytes = (json.dumps(CATALOG, sort_keys=True, separators=(',', ':')) + '\n').encode()
    return {'id': 'WEXP-CORE-02-VECTORS-002', 'semantics_version': 'wexp-core-2',
            'source_path': 'drafts/core/02/draft-sergeev-wexp-core-02.xml',
            'source_sha256': SOURCE_SHA256,
            'predecessor': {'id': 'WEXP-CORE-02-VECTORS-001', 'package_revision': 2,
                            'expanded_corpus_sha256': 'd5d2c9d54185f04ac59ac2b5642853a6ebd00c3d28a3239d62682186f5df323f'},
            'expectation_origin': 'Inputs authored from the section 7 matrix; expectations derived by a separate '
                                  'isolated session from the published text alone and frozen before any appraiser run. '
                                  'Same-project work, not independent external review.',
            'independent_external_review': False, 'full_conformance_claim': False,
            'profile_registry_sha256': hashlib.sha256(profile_bytes).hexdigest(),
            'representation': 'See README.md; JSON is a local non-normative harness identical to WEXP-CORE-02-VECTORS-001.',
            'profiles': CATALOG, 'cases': rows}

def encoded():
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
            path = HERE / name
            if not path.resolve().is_relative_to(HERE) or path.is_symlink():
                raise SystemExit('Unsafe manifest path')
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise SystemExit('Frozen source mismatch: ' + name)
    raw = encoded()
    digest = hashlib.sha256(raw).hexdigest()
    if manifest is not None and manifest['expanded_corpus_sha256'] != digest:
        raise SystemExit('Frozen expanded corpus mismatch')
    if args.output:
        if args.output.resolve().is_relative_to(HERE):
            raise SystemExit('Refusing to write inside the frozen package')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as stream:
            stream.write(raw)
    print(json.dumps({'cases': len(build()['cases']), 'sha256': digest, 'appraiser_executed': False}))

if __name__ == '__main__':
    main()
