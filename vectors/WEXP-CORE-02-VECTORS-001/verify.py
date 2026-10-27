#!/usr/bin/env python3
"""Read-only integrity checks; default mode reads data without importing generators."""
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
    if type(name) is not str or Path(name).name != name:
        raise ValueError('Unsafe manifest member')
    path = HERE / name
    if path.is_symlink() or not path.is_file():
        raise ValueError('Missing or linked manifest member: ' + name)
    return path.read_bytes()

def verify(source_xml=None, expected_manifest=None, rebuild=False):
    raw_manifest = member('manifest.json')
    if expected_manifest is not None and sha(raw_manifest) != expected_manifest:
        raise ValueError('Manifest differs from external pin')
    manifest = decode(raw_manifest)
    if manifest['semantics_version'] != 'wexp-core-2':
        raise ValueError('Wrong manifest semantics')
    allowed = {'copy', 'hashlib', 'json', 'pathlib', 'argparse', 'ast', 'corpus',
               'normative_cases', 'review_cases', 'final_contract_cases'}
    for name, digest in manifest['files'].items():
        if not name.endswith('.py'):
            raise ValueError('Code manifest member must be Python')
        raw = member(name)
        if sha(raw) != digest:
            raise ValueError('Source hash mismatch: ' + name)
        for node in ast.walk(ast.parse(raw)):
            imports = ([item.name.split('.')[0] for item in node.names]
                       if isinstance(node, ast.Import) else
                       [(node.module or '').split('.')[0]]
                       if isinstance(node, ast.ImportFrom) else [])
            if any(item not in allowed for item in imports):
                raise ValueError('Expectation dependency not allowed: ' + name)
    representation = manifest['harness_representation']
    if representation['path'] != 'README.md' or sha(member('README.md')) != representation['sha256']:
        raise ValueError('Frozen representation description mismatch')
    frozen = manifest['frozen_data']
    if frozen['path'] != 'corpus.json':
        raise ValueError('Unexpected frozen data path')
    expanded = member(frozen['path'])
    if (len(expanded) != frozen['bytes'] or len(expanded) != manifest['expanded_corpus_bytes']
            or sha(expanded) != frozen['sha256']
            or sha(expanded) != manifest['expanded_corpus_sha256']):
        raise ValueError('Frozen corpus bytes differ')
    package = decode(expanded)
    if package['semantics_version'] != 'wexp-core-2':
        raise ValueError('Wrong expanded semantics')
    ids = [case['id'] for case in package['cases']]
    expected_ids = ([f'C{n:02}' for n in range(1, 17)]
                    + [f'R{n:02}' for n in range(1, 49)]
                    + [f'P{n:02}' for n in range(1, 26)])
    if ids != expected_ids or len(ids) != manifest['case_count']:
        raise ValueError('Case inventory mismatch')
    for case in package['cases']:
        result = case['expected']
        if set(result) != FIELDS or type(result['asserted_claim_supported']) is not bool:
            raise ValueError('Incomplete or mistyped expected result: ' + case['id'])
    if package['source_sha256'] != manifest['specification']['sha256']:
        raise ValueError('Package/source identity mismatch')
    if source_xml is not None and sha(Path(source_xml).read_bytes()) != manifest['specification']['sha256']:
        raise ValueError('Published XML digest mismatch')
    # Executing known generator code is explicit, after all source hashes pass.
    if rebuild:
        import corpus
        if corpus.encoded() != expanded:
            raise ValueError('Rebuilt corpus differs from frozen data')
    return {'status': 'PASS_CORPUS_INTEGRITY', 'case_count': len(ids),
            'source_xml_bytes_checked': source_xml is not None,
            'generator_executed': rebuild, 'appraiser_executed': False,
            'manifest_sha256': sha(raw_manifest),
            'expanded_corpus_sha256': sha(expanded)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-xml', type=Path)
    parser.add_argument('--expected-manifest-sha256')
    parser.add_argument('--rebuild', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.source_xml, args.expected_manifest_sha256, args.rebuild), sort_keys=True))
