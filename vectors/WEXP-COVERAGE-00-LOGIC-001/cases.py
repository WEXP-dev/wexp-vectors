"""Source-authored finite-model expectations; no evaluator imports."""
from copy import deepcopy

BASE = {'A':['a1'],'C':[['r1','h1']],'R':[['r1','h1']], 'S':['s1'],
        'Rv':[['r1','h1']], 'B':[[['r1','h1'],'a1']], 'F':[['s1','a1']],
        'H':[[['r1','h1'],'s1']]}
# Column order is the ten claim identifiers of Coverage-00 section 5.
EXPECTED = {
 'exact-singleton':[True,True,True,True,True,True,True,True,True,False],
 'matching-omission':[True,True,True,False,True,False,False,True,False,False],
 'duplicate-creation':[True,True,False,True,True,True,True,True,False,False],
 'ambiguous-creation':[True,True,False,True,True,True,True,True,False,False],
 'orphan-receipt':[True,True,False,True,True,True,True,False,False,False],
 'extra-recipient':[True,False,False,True,True,True,True,True,True,False],
 'same-id-different-content':[False,False,False,True,True,True,True,True,True,False],
 'empty-scope':[True,True,True,True,True,True,True,True,True,True],
 'empty-views-not-empty-actions':[True,True,True,False,True,False,False,True,False,False],
 'source-unavailable':[True,True,None,None,None,None,True,True,True,False],
 'recipient-view-unavailable':[True,True,None,True,True,True,True,True,True,False],
 'equal-payload-distinct-actions':[True,True,True,True,True,True,True,True,True,False],
}

def cases():
    rows=[]
    def add(name,model,section):
        rows.append({'id':name,'source_sections':section,'model':deepcopy(model),
                     'expected_values':EXPECTED[name]})
    add('exact-singleton',BASE,['4','5'])
    m=deepcopy(BASE);m['A'].append('a2');add('matching-omission',m,['4','5','6.2'])
    m=deepcopy(BASE)
    for k in ('C','R','Rv'):m[k].append(['r2','h2'])
    m['B'].append([['r2','h2'],'a1']);m['H'].append([['r2','h2'],'s1'])
    add('duplicate-creation',m,['4','5','7.2:N4a'])
    m=deepcopy(BASE);m['A'].append('a2');m['S'].append('s2');m['B'].append([['r1','h1'],'a2'])
    m['F'].append(['s2','a2']);m['H'].append([['r1','h1'],'s2'])
    add('ambiguous-creation',m,['4','5','7.2:N4a'])
    m=deepcopy(BASE)
    for k in ('C','R','Rv'):m[k].append(['r2','h2'])
    add('orphan-receipt',m,['4','5','7.2:N4b'])
    m=deepcopy(BASE)
    for k in ('R','Rv'):m[k].append(['r2','h2'])
    add('extra-recipient',m,['4','5','7.2:N2b'])
    m=deepcopy(BASE);m['R']=[['r1','changed']];m['Rv']=deepcopy(m['R']);m['H']=[]
    add('same-id-different-content',m,['4','5','7.2:N2a'])
    m={k:[] for k in BASE};add('empty-scope',m,['5','7.1:P8'])
    m['A']=['a1'];add('empty-views-not-empty-actions',m,['5','6.2','7.1:P6'])
    m=deepcopy(BASE);m['S']=None;m['F']=[];m['H']=[]
    add('source-unavailable',m,['6.2','7.3'])
    m=deepcopy(BASE);m['Rv']=None;m['H']=[]
    add('recipient-view-unavailable',m,['6.2','7.3'])
    m=deepcopy(BASE);m['A'].append('a2');m['S'].append('s2')
    for k in ('C','R','Rv'):m[k].append(['r2','h1'])
    m['B'].append([['r2','h1'],'a2']);m['F'].append(['s2','a2']);m['H'].append([['r2','h1'],'s2'])
    add('equal-payload-distinct-actions',m,['4','5'])
    return rows
