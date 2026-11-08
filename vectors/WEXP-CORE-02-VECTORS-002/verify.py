#!/usr/bin/env python3
"""Read-only integrity checks for WEXP-CORE-02-VECTORS-002; default mode imports no generator."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = {'semantics_version', 'verdict', 'fatal_reasons', 'target', 'asserted_claim',
          'asserted_claim_supported', 'support_entries', 'supported_claims',
          'maximal_supported_claims', 'support_relations', 'boundary_ceiling',
          'boundary_grounding', 'recorder_relations', 'substantive_reasons',
          'evaluation_gaps', 'evaluation_gap_entries', 'counter_evidence',
          'inherited_limitations', 'evaluation_context', 'evaluation_scope'}
ALLOWED_IMPORTS = {'copy', 'hashlib', 'json', 'pathlib', 'argparse', 'ast', 'inputs', 'corpus'}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def strict_pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('Duplicate JSON member: ' + key)
        result[key] = value
    return result

def decode(raw):
    return json.loads(raw, object_pairs_hook=strict_pairs)

def member(name):
    if type(name) is not str or '..' in Path(name).parts or Path(name).is_absolute():
        raise ValueError('Unsafe manifest member')
    path = HERE / name
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(HERE):
        raise ValueError('Missing or linked manifest member: ' + name)
    return path.read_bytes()

def verify(source_xml=None, expected_manifest=None, rebuild=False):
    raw_manifest = member('manifest.json')
    if expected_manifest is not None and sha(raw_manifest) != expected_manifest:
        raise ValueError('Manifest differs from external pin')
    manifest = decode(raw_manifest)
    if manifest['semantics_version'] != 'wexp-core-2' or manifest['corpus_id'] != 'WEXP-CORE-02-VECTORS-002':
        raise ValueError('Wrong manifest identity')
    for name, digest in manifest['files'].items():
        raw = member(name)
        if sha(raw) != digest:
            raise ValueError('Frozen file hash mismatch: ' + name)
        if name.endswith('.py'):
            for node in ast.walk(ast.parse(raw)):
                imports = ([item.name.split('.')[0] for item in node.names]
                           if isinstance(node, ast.Import) else
                           [(node.module or '').split('.')[0]]
                           if isinstance(node, ast.ImportFrom) else [])
                if any(item not in ALLOWED_IMPORTS for item in imports):
                    raise ValueError('Expectation dependency not allowed: ' + name)
    expected_files = {'inputs.py', 'corpus.py', 'verify.py', 'README.md',
                      'derivation/DERIVATION.md', 'derivation/AMBIGUITIES.json',
                      'derivation/FILES-READ.txt', 'derivation/DELIVERED-SHA256SUMS.txt'} | {
        f'expectations/B{n:02}.json' for n in range(1, manifest['case_count'] + 1)}
    if set(manifest['files']) != expected_files:
        raise ValueError('Manifest file inventory mismatch')
    frozen = manifest['frozen_data']
    if frozen['path'] != 'corpus.json':
        raise ValueError('Unexpected frozen data path')
    expanded = member(frozen['path'])
    if (len(expanded) != frozen['bytes'] or len(expanded) != manifest['expanded_corpus_bytes']
            or sha(expanded) != frozen['sha256']
            or sha(expanded) != manifest['expanded_corpus_sha256']):
        raise ValueError('Frozen corpus bytes differ')
    package = decode(expanded)
    if package['semantics_version'] != 'wexp-core-2' or package['id'] != 'WEXP-CORE-02-VECTORS-002':
        raise ValueError('Wrong expanded identity')
    ids = [case['id'] for case in package['cases']]
    if ids != [f'B{n:02}' for n in range(1, manifest['case_count'] + 1)]:
        raise ValueError('Case inventory mismatch')
    for case in package['cases']:
        delivered = decode(member('expectations/' + case['id'] + '.json'))
        if delivered['id'] != case['id'] or delivered['expected'] != case['expected']:
            raise ValueError('Expanded expectation differs from the frozen delivered file: ' + case['id'])
        result = case['expected']
        if set(result) != FIELDS or type(result['asserted_claim_supported']) is not bool:
            raise ValueError('Incomplete or mistyped expected result: ' + case['id'])
    if package['source_sha256'] != manifest['specification']['sha256']:
        raise ValueError('Package/source identity mismatch')
    pred = manifest['predecessor']
    if (package['predecessor']['expanded_corpus_sha256'] != pred['expanded_corpus_sha256']
            or pred['lock_commit'] != 'd6827a5e08fdf0aabecee5c025c369273c438db5'):
        raise ValueError('Predecessor pin mismatch')
    if source_xml is not None and sha(Path(source_xml).read_bytes()) != manifest['specification']['sha256']:
        raise ValueError('Published XML digest mismatch')
    if rebuild:
        import corpus
        if corpus.encoded() != expanded:
            raise ValueError('Rebuilt corpus differs from frozen data')
    return {'status': 'PASS_CORPUS_INTEGRITY', 'case_count': len(ids),
            'source_xml_bytes_checked': source_xml is not None,
            'generator_executed': rebuild, 'appraiser_executed': False,
            'manifest_sha256': sha(raw_manifest), 'expanded_corpus_sha256': sha(expanded)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-xml', type=Path)
    parser.add_argument('--expected-manifest-sha256')
    parser.add_argument('--rebuild', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.source_xml, args.expected_manifest_sha256, args.rebuild), sort_keys=True))
