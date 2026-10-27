#!/usr/bin/env python3
"""Read-only corpus integrity checks. Never invokes an appraiser."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def verify(source_xml=None):
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    allowed = {'copy', 'hashlib', 'json', 'pathlib', 'argparse', 'ast', 'corpus',
               'normative_cases', 'review_cases', 'final_contract_cases'}
    for name, digest in manifest['files'].items():
        if Path(name).name != name or not name.endswith('.py'):
            raise ValueError('Unsafe manifest member')
        raw = (HERE / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('Source hash mismatch: ' + name)
        tree = ast.parse(raw)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports = [item.name.split('.')[0] for item in node.names]
            elif isinstance(node, ast.ImportFrom):
                imports = [(node.module or '').split('.')[0]]
            else:
                imports = []
            if any(item not in allowed for item in imports):
                raise ValueError('Expectation dependency not allowed: ' + name)
    representation = manifest['harness_representation']
    if representation['path'] != 'README.md' or hashlib.sha256((HERE / 'README.md').read_bytes()).hexdigest() != representation['sha256']:
        raise ValueError('Frozen representation description mismatch')
    # Only import expectation code after checking all source identities.
    import corpus
    expanded = corpus.encoded()
    if len(expanded) != manifest['expanded_corpus_bytes']:
        raise ValueError('Expanded corpus byte count mismatch')
    if hashlib.sha256(expanded).hexdigest() != manifest['expanded_corpus_sha256']:
        raise ValueError('Expanded corpus hash mismatch')
    package = json.loads(expanded)
    ids = [case['id'] for case in package['cases']]
    if len(ids) != manifest['case_count'] or len(set(ids)) != len(ids):
        raise ValueError('Case count or uniqueness mismatch')
    if ids[:16] != [f'C{n:02}' for n in range(1, 17)]:
        raise ValueError('Normative fixture inventory mismatch')
    for case in package['cases']:
        if len(case['expected']) != 20:
            raise ValueError('Incomplete expected result: ' + case['id'])
    if package['source_sha256'] != manifest['specification']['sha256']:
        raise ValueError('Package/source identity mismatch')
    if source_xml is not None:
        if hashlib.sha256(Path(source_xml).read_bytes()).hexdigest() != manifest['specification']['sha256']:
            raise ValueError('Published XML digest mismatch')
    return {'status': 'PASS_CORPUS_INTEGRITY', 'case_count': len(ids),
            'source_xml_bytes_checked': source_xml is not None,
            'appraiser_executed': False,
            'expanded_corpus_sha256': manifest['expanded_corpus_sha256']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-xml', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.source_xml), sort_keys=True))
