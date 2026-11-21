                                                                                                
                                                                                                                   
                                                                                                                
                                                                                                                  
                                                                                                 
                                                                                                                       
import os, io, re, json
H = os.path.dirname(os.path.abspath(__file__))
rl = json.load(io.open(os.path.join(H, 'read_list.json'), encoding='utf-8'))['judgments']
MONTHS = r'(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)'
CIT = [
    r'\[\d{4}\]\s+(?:\d+\s+)?[A-Z][A-Za-z]{1,8}(?:\s(?:Civ|Crim|Admin|Comm|Ch|QB|Fam|Pat|IPEC|TCC))?\s+\d{1,5}',                                      
    r'\(\d{4}\)\s+(?:\d+\s+)?[A-Z][A-Za-z\.&\' ]{0,20}?(?:\s?\(\d?(?:d|nd|rd|th|NS)\))?\s+\d{1,5}',                                          
    r'\b\d{4}\s+(?:SCC|ONCA|BCCA|QCCA|ABCA|NSCA|MBCA|SKCA|FCA|SGCA|SGHC|NZSC|NZCA|NZHC|HKCFA|HKCA|UKSC|UKHL|EWCA|EWHC)\s+\d{1,5}',
    r'\b\d{1,4}\s+(?!' + MONTHS + r'\b)(?:[A-Z][A-Za-z]{0,7}\.?\s?){1,4}(?:\((?:\d?d|2d|3d|4th|NS)\)\s?|(?:2d|3d|4th)\s)?\d{1,5}\b',                   
]
CIT_RE = re.compile('|'.join('(?:%s)' % p for p in CIT))
ACAD_RE = re.compile(r'(?:\(\d{4}\)|\[\d{4}\])\s+\d+\s+(?:[A-Z][A-Za-z\.&]*\s?){1,6}(?:L\.?\s?Rev\.?|L\.?\s?J\.?|L\.?\s?Q\.?|LQR|CLJ|MLR|Law\s+Review|Law\s+Journal|Law\s+Quarterly\s+Review|Rev\.?)\s+\d+'
                     r'|\b\d+\s+(?:[A-Z][A-Za-z\.&]*\s?){1,6}(?:L\.?\s?Rev\.?|L\.?\s?J\.?|Law\s+Review|Law\s+Journal)\s+\d+'
                     r'|[A-Z][A-Za-z\'\-]+(?:\s(?:&|and)\s[A-Z][A-Za-z\'\-]+)?(?:,|\s)\s?[^\n;:.]{3,80}?\(\d+(?:st|nd|rd|th)\s+ed')
def core(t):
    m = re.search(r'(?m)^CORE JUDGMENT\s*$', t)
    return t[m.end():] if m else t
def name_before(t, s):
    pre = t[max(0, s - 120):s]
    pre = re.split(r'[;\n]|(?<=[a-z])\.\s', pre)[-1].strip(' ,(')
    m = re.search(r"([A-Z][\w'&\.\- ]{0,60}?\sv\.?\s[\w'&\.\-\(\) ]{1,60}?)\s*,?$", pre)
    return (m.group(1) if m else pre[-60:]).strip(' ,(')
out = []
for j in rl:
    t = core(io.open(j['read_path'], encoding='utf-8', errors='replace').read())
    spans = sorted({(m.start(), m.end()) for m in CIT_RE.finditer(t)})
    keep = [s for s in spans if not any(o != s and o[0] <= s[0] and s[1] <= o[1] for o in spans)]
    items, cur = [], None
    for s, e in keep:
        c = re.sub(r'\s+', ' ', t[s:e]).strip()
        if cur and re.fullmatch(r'\s*[;,]\s*', t[cur['end']:s] or 'x'):
            cur['cites'].append(c); cur['end'] = e; continue
        cur = {'s': s, 'end': e, 'cites': [c]}; items.append(cur)
    seen, auth = set(), []
    for it in items:
        k = tuple(sorted(it['cites']))
        if k in seen: continue
        seen.add(k); auth.append({'name': name_before(t, it['s']), 'cites': it['cites'], 'court': '', 'note': '[CORE] regex'})
    acad = list(dict.fromkeys(re.sub(r'\s+', ' ', m.group(0)).strip() for m in ACAD_RE.finditer(t)))
    out.append({'idx': str(j['idx250']), 'citation': j['file'], 'court': j['court'], 'authorities': len(auth),
                'authority_list': auth, 'academic_works': acad, 'reports': [], 'own_history': [], 'uncodeable': [], 'note': 'regex baseline'})
json.dump(out, io.open(os.path.join(H, 'regex_reads.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('judgments', len(out), 'authorities', sum(o['authorities'] for o in out), 'academic', sum(len(o['academic_works']) for o in out))
