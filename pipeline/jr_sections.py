                       

import re

                                                                          

_HEADNOTES = re.compile(r'(?m)^[ \t]*HEADNOTES[ \t]*$', re.IGNORECASE)
_CORE = re.compile(r'(?m)^[ \t]*CORE JUDGMENT[ \t]*$', re.IGNORECASE)
_FOOTNOTES = re.compile(r'(?m)^[ \t]*FOOTNOTES[ \t]*$', re.IGNORECASE)

                                                                              
                                                                                    
                                                
                                                                                         
_INGEST = re.compile(r'(?m)^[ \t]*INGEST[ \t]*-.*$')

                                        
_RULE = re.compile(r'(?m)^[ \t]*-{4,}[ \t]*$')

                                                                  
_ODD_SPACE = {
    '\xa0': ' ',                    
    ' ': ' ',        
    ' ': ' ',        
    ' ': ' ',          
    ' ': ' ',          
    ' ': ' ',                     
    '﻿': '',          
}



                                                                                           
                                                                                       
                                                                                            
                                                                                               
                                                                                             
                   
_CASE_HEADER = re.compile(r"^CASE:\s*(.+?)\s*$", re.M)
_TRAILING_CITE = re.compile(r"\s*\[\d{4}\]\s*[A-Za-z()]+\s*\d+\s*$")


def case_name(raw, path=""):
    
    import os
    m = _CASE_HEADER.search(str(raw or "")[:4000])
    name = m.group(1) if m else os.path.basename(str(path or ""))
    if name.lower().endswith(".txt"):
        name = name[:-4]
    return _TRAILING_CITE.sub("", name).strip()

def normalise(text):
    
    if not text:
        return ''
    for bad, good in _ODD_SPACE.items():
        text = text.replace(bad, good)
    return text.replace('\r\n', '\n').replace('\r', '\n')


def _clean(text):
    
    text = _INGEST.sub('', text)
    text = _RULE.sub('', text)
    return text.strip()


                                                                                           

                                                                    
_NUMPARA = re.compile(r'(?m)^[ \t]*(\d{1,4})\.[ \t]+(?=\S)')

                                                                                     
 
                                                                                             
                                                                                            
                                                                                           
                                                                                          
                                                                        
_BRACKETPARA = re.compile(r'(?m)^[ \t]*\[(\d{1,4})\][ \t]+(?=\S)')

                                                                                          
                                                                                           
                              
_YEARLIKE = 1500

                                                                                         
                                                                         
_ATTRIB = re.compile(r"(?m)^[ \t]*[A-Z][A-Z .,'‐-―&-]{2,80}?\b"
                     r"(?:C\.?J\.?|JJ\.?|J\.?A\.?|J\.?)[ \t]*\.?[ \t]*$")

                                                                                            
                                                                                               
MIN_RUN = 5


def _runs(text):
    
    hits = [(m.start(), int(m.group(1))) for m in _NUMPARA.finditer(text)]
    out, i = [], 0
    while i < len(hits):
        j = i
        while j + 1 < len(hits) and hits[j + 1][1] == hits[j][1] + 1:
            j += 1
        out.append((hits[i][0], hits[i][1], j - i + 1))
        i = j + 1
    return out


def bracket_body_start(text, min_run=6, min_prose=25, gap_tolerance=5):
    
    hits = []
    for m in _BRACKETPARA.finditer(text):
        n = int(m.group(1))
        if n >= _YEARLIKE:
            continue
        line_end = text.find('\n', m.end())
        line = text[m.end():line_end if line_end > 0 else len(text)]
        if len(line.strip()) < min_prose or not line.strip()[:1].isupper() \
                and not line.strip()[:1].isdigit() and line.strip()[:1] not in '"“‘':
            continue
        hits.append((m.start(), n))

    best = None
    for i, (pos, n) in enumerate(hits):
        if n != 1:
            continue
        want, run, gaps, j = 2, 1, 0, i + 1
        while j < len(hits):
            if hits[j][1] == want:
                run += 1
                want += 1
                gaps = 0
            else:
                gaps += 1
                if gaps > gap_tolerance:
                    break
            j += 1
                                                                                              
                                                                                         
                                                                                            
                                                                                            
                                                                               
         
                                                                                             
                                                                                    
                                                                                           
                     
        if run >= min_run:
            best = (pos, run)
            break
    return best[0] if best else None


def body_start(text, require_anchor=True):
    
    runs = [r for r in _runs(text) if r[1] == 1 and r[2] >= MIN_RUN]
    if not runs:
        return None
    pos = max(runs, key=lambda r: r[2])[0]

                                                                                             
                                                        
    head = text.rfind('\n', 0, pos)
    for _ in range(4):
        if head <= 0:
            break
        prev = text.rfind('\n', 0, head)
        line = text[prev + 1:head]
        if _ATTRIB.match(line):
            return prev + 1
        if len(line.strip()) > 60:                                                         
            break
        head = prev
    return None if require_anchor else pos


                                                                                     
 
                                                                                              
                                                                  
 
                                                          
                                                                                              
                                                                                            
 
                                                                        
                                                                                              
                                                                                            
                                                                                           
                                                                                 
 
                                                                                          
                                           
                                                                                
                                                                                 
 
                                                                                          
_SHORT_FILE = 6000


def dominant_numbering(text):
    
                                                                                             
                                                                                              
                                                                                               
                                                                                        
                                  
    m_fn = _FOOTNOTES.search(text)
    body = text[:m_fn.start()] if m_fn else text
    dots = sum(1 for _ in _NUMPARA.finditer(body))
    brks = sum(1 for m in _BRACKETPARA.finditer(body) if int(m.group(1)) < _YEARLIKE)
    if dots == 0 and brks == 0:
        return None
    return 'bracket' if brks > dots else 'dot'


def _detect_body(text):
    
    bs = body_start(text)
    if bs is not None:
        return bs, 'dot'
    bs = bracket_body_start(text)
    if bs is not None:
        return bs, 'bracket'
                                                                                         
                                             
    if len(text) <= _SHORT_FILE:
        bs = bracket_body_start(text, min_run=3)
        if bs is not None:
            return bs, 'bracket-short'
    return None, None


                                                                              
 
                                                                                               
                                                                                              
                                                                                            
                                                                                          
                                                                               
 
                                                                                              
                                                                                                
                                                                                             
                                                     
 
                                                                                          
                                                                                             
                             
_FRONT_MATTER = (
    re.compile(r"(?m)^[ \t]*(?:BETWEEN|AND)[ \t]+[A-Z]"),                       
    re.compile(r"(?m)^[ \t]*Counsel\s*:", re.I),
    re.compile(r"(?m)^[ \t]*Solicitors?\s*:", re.I),
    re.compile(r"(?m)^[ \t]*(?:RESERVED\s+)?JUDGMENT\s+OF\s+[A-Z]"),
    re.compile(r"delivered by me", re.I),
    re.compile(r"(?m)^[ \t]*(?:CIV|CRI|FAM)-\d{4}-\d{3}-\d{4,6}"),
)


def has_front_matter(chunk):
    
    return any(p.search(chunk) for p in _FRONT_MATTER)


                                                                                            
 
                                                                                             
                                                                                                
                                                                                             
                                                                                    
 
                                                                                           
                                                              
                                      
 
                                          
 
                                                                                              
 
                                                                                          
                                                                                             
             
 
                                          
 
                                                                      
 
                                                                                              
                                                                                          
                                                                                             
                                                                                              
                                                  
 
                                                                                                
                                                     
 
                                                                                             
                                                                                         
                                                            
                                                                                            
                                                                                               
                                                                                              
                                                                                            
                                                                                            
                                                                                   
                                                                                         
                                                                                        
                                                                                               
                                                          
                                                                                           
                                                                                     
 
                                                                                              
                                                                                           
        

_OWN_CITATION_LINE = re.compile(r"(?m)^CITATION:[ \t]*(.+?)[ \t]*$")
_NEUTRAL = re.compile(r"\[[ \t]*(\d{4})[ \t]*\][ \t]*"
                      r"([A-Za-z]+(?:\([A-Za-z]+\))?)[ \t]*(\d{1,5})")

                                                                                                
                                                                                           
                                                                                             
                    
_HDR_DATE = re.compile(r"[ \t]*\[[ \t]*(?:\d{1,2}[ \t]+[A-Za-z]+[ \t]+\d{4})?[ \t]*\]")

                                                                                            
                                                                                               
                                                                                              
                                                                  
_CASE_TRAIL = re.compile(r"[ \t]*\[[ \t]*\d{4}[ \t]*\][ \t]*[A-Za-z()]+[ \t]*\d+"
                         r"(?:[ \t]*\[[^\]]*\])?[ \t]*$")


                                                                                                
                                                                                                
                                             
 
                                                                            
 
            
 
                  
 
                     
 
                                                                                              
                                                                                            
                                                                                            
                                                                                            
                                                                                            
                                                                                          
                                                                                              
                                                     
 
                                                                                            
                                                                        
_NZ_COURT = re.compile(r"(?i)^NZ")


def _own_citation(text):
    
    m = _OWN_CITATION_LINE.search(text[:4000])
    n = _NEUTRAL.search(m.group(1)) if m else None
    if not n:
        m = _CASE_HEADER.search(text[:4000])
        n = _NEUTRAL.search(m.group(1)) if m else None
    if not n or not _NZ_COURT.match(n.group(2)):
        return None
    return re.compile(r"\[[ \t]*%s[ \t]*\][ \t]*%s[ \t]*%s(?![0-9])"
                      % (n.group(1), re.escape(n.group(2)), n.group(3)))


def _own_name(text):
    
    m = _CASE_HEADER.search(text[:4000])
    if not m:
        return None
    nm = _CASE_TRAIL.sub("", m.group(1)).strip()
    toks = [t for t in nm.split() if t]
    if len(toks) < 2 or len(nm) < 6:
        return None
    return re.compile(r"[ \t\n]+".join(re.escape(t) for t in toks), re.IGNORECASE)


def _mostly_caps(s, floor=0.6):
    
    up = sum(1 for c in s if c.isupper())
    lo = sum(1 for c in s if c.islower())
    return (up + lo) > 0 and up >= floor * (up + lo)


                                                                                            
                                                                                            
                                                                                                
                                                                                             
                                                                                             
                                                    
 
                                                                                          
                                                                                             
                                                                                                
                                                                                          
_CAPS_V = re.compile(r"(?:^|[ \t])[Vv]\.?(?:[ \t]|$)")
_HAS_YEAR = re.compile(r"\[[ \t]*\d{4}[ \t]*\]")


def _is_name_line(line):
    s = line.strip()
    return (5 < len(s) <= 200 and _mostly_caps(s) and bool(_CAPS_V.search(s))
            and not _HAS_YEAR.search(s) and s[-1] not in ".;,:")


def _is_name_tail(line):
    
    s = line.strip()
    return (0 < len(s) <= 60 and _mostly_caps(s) and not _CAPS_V.search(s)
            and not _HAS_YEAR.search(s) and s[-1] not in ".;,:")


def _absorb_caps_name(core, start):
    
    q = start
    while q > 0 and core[q - 1] in " \t\n":
        q -= 1
    if q == 0:
        return start
    ls1 = core.rfind("\n", 0, q) + 1
    if _is_name_line(core[ls1:q]):
        return ls1
    if _is_name_tail(core[ls1:q]) and ls1 > 0:
        ls0 = core.rfind("\n", 0, ls1 - 1) + 1
        if _is_name_line(core[ls0:ls1 - 1]):
            return ls0
    return start


def running_header_spans(core, text):
    
    if not core:
        return []
    crx = _own_citation(text)
    if crx is None:
        return []
    nrx = _own_name(text)
    body = bracket_body_start(core)
    out = []
    for m in crx.finditer(core):
        end = m.end()
        d = _HDR_DATE.match(core, end)
        if d:
            end = d.end()
        eol = core.find("\n", end)
        eol = len(core) if eol < 0 else eol
        if core[end:eol].strip():
                                                                                           
            continue
        start = m.start()

                                                                                              
        if nrx is not None:
            p = start
            while p > 0 and core[p - 1] in " \t\n":
                p -= 1
            for nm in nrx.finditer(core, max(0, p - 400), p):
                if nm.end() == p and _mostly_caps(core[nm.start():p]):
                    start = nm.start()
                    break
        if start == m.start():
            start = _absorb_caps_name(core, start)

        bol = core.rfind("\n", 0, start) + 1
        if not core[bol:start].strip():
            start = bol                                                                      
            end = min(len(core), eol + 1)
        else:
                                                                                             
                                                                                              
                                                     
            if start == m.start():
                continue
            end = eol

                                                                                              
                                                                                             
                                                                                            
                                                                                         
                  
        if body is None:
            ahead = core[start:start + 1200]
        elif start < body:
            ahead = core[start:body]
        else:
            ahead = ""
        if ahead and has_front_matter(ahead):
            continue
        out.append((start, end))
    return out


def strip_running_header(core, text):
    
    spans = running_header_spans(core, text)
    if not spans:
        return core
    for s, e in reversed(spans):
        core = core[:s] + core[e:]
    return core.strip()


def marker_check(text):
    
    text = normalise(text)
    m = _CORE.search(text)
    if not m:
        return None
    bs, conv = _detect_body(text)
    if bs is None:
        return None
    too_low = bs < m.start()
    too_high = (not too_low) and dominant_numbering(text) == 'bracket' \
        and has_front_matter(text[m.end():bs])
    return {
        'marker_at': m.start(),
        'body_at': bs,
        'convention': conv,
        'misplaced': too_low,                                                                   
        'front_matter_in_core': too_high,                                                       
        'chars_lost': max(0, m.start() - bs),
        'chars_contaminating': (bs - m.end()) if too_high else 0,
    }


def split(text, trust_marker=False):
    
    text = normalise(text)
    parts = _split_sections(text, trust_marker)
    parts["core"] = strip_running_header(parts["core"], text)
    return parts


def _split_sections(text, trust_marker=False):
    
    text = normalise(text)

    m_core = _CORE.search(text)
    if m_core and not trust_marker:
        bs, _conv = _detect_body(text)

                                                                                             
                                                                                             
                        
         
                                                                                              
                                                                                              
                                                                                             
                                                                                            
                                                                                            
                                                                                        
                                                                                             
                    
        if (bs is not None and dominant_numbering(text) == 'bracket'
                and bs > m_core.end() and has_front_matter(text[m_core.end():bs])):
            m_fn = _FOOTNOTES.search(text)
            m_hn = _HEADNOTES.search(text)
            hn = text[m_hn.end():bs] if m_hn else text[:bs]
            if m_fn and m_fn.start() > bs:
                return {'headnotes': _clean(hn),
                        'core': _clean(text[bs:m_fn.start()]),
                        'footnotes': _clean(text[m_fn.end():])}
            return {'headnotes': _clean(hn), 'core': _clean(text[bs:]), 'footnotes': ''}

        if bs is not None and bs < m_core.start():
            m_fn = _FOOTNOTES.search(text)
            m_hn = _HEADNOTES.search(text)
            hn = text[m_hn.end():bs] if m_hn else text[:bs]
            if m_fn and m_fn.start() > bs:
                return {'headnotes': _clean(hn),
                        'core': _clean(text[bs:m_fn.start()]),
                        'footnotes': _clean(text[m_fn.end():])}
            return {'headnotes': _clean(hn), 'core': _clean(text[bs:]), 'footnotes': ''}

    m_fn = _FOOTNOTES.search(text)
    m_hn = _HEADNOTES.search(text)

    if not m_core:
                                                                                         
        body = text[m_hn.end():] if m_hn else text
        hn = text[m_hn.end():m_hn.end()] if m_hn else ''
        if m_fn and m_fn.start() > (m_hn.end() if m_hn else 0):
            return {'headnotes': _clean(hn),
                    'core': _clean(body[:m_fn.start() - (m_hn.end() if m_hn else 0)]),
                    'footnotes': _clean(text[m_fn.end():])}
        return {'headnotes': _clean(hn), 'core': _clean(body), 'footnotes': ''}

    hn = text[m_hn.end():m_core.start()] if m_hn else text[:m_core.start()]

    if m_fn and m_fn.start() > m_core.end():
        core = text[m_core.end():m_fn.start()]
        fn = text[m_fn.end():]
    else:
        core = text[m_core.end():]
        fn = ''

    return {'headnotes': _clean(hn), 'core': _clean(core), 'footnotes': _clean(fn)}


                                                                         

SCOPES = {
    'core': ('core',),
    'core+fn': ('core', 'footnotes'),
    'all': ('headnotes', 'core', 'footnotes'),
}


def scope(parts, name):
    
    try:
        keys = SCOPES[name]
    except KeyError:
        raise ValueError(f"unknown scope {name!r}; expected one of {sorted(SCOPES)}")
    return '\n'.join(parts[k] for k in keys if parts.get(k))


                                                                         

def audit(text):
    
    parts = split(text)
    both = parts['core']
    mk = marker_check(text)
    return {
        'marker_misplaced': bool(mk and mk['misplaced']),
        'marker_chars_recovered': mk['chars_lost'] if mk else 0,
        'has_headnotes': bool(_HEADNOTES.search(text)),
        'has_core': bool(_CORE.search(text)),
        'has_footnotes': bool(_FOOTNOTES.search(text)),
        'core_empty': not both.strip(),
        'contaminated_ingest': bool(_INGEST.search(both)),
        'contaminated_rule': bool(_RULE.search(both)),
        'headnotes_hold_speech': bool(
            re.search(r'(?m)^\s*(LORD|LADY|BARONESS)\b|\.—', parts['headnotes'])),
    }


def citation_scope(parts, citing_court=None):
    
    body = scope(parts, "core+fn")
    return body                                                                                       
    lines = parts.get("headnotes", "").splitlines()
    selected = []
    continuing = False
    start = re.compile(r"(?:^[ \t]*\(?|\b)(?:ON[ \t]+(?:APPLICATION[ \t]+FOR[ \t]+LEAVE[ \t]+TO[ \t]+)?APPEAL[ \t]+FROM\b:?"
                       r"|(?<![^ \t(])FROM[ \t]+(?=[A-Z]{2,5}[ \t]*(?:NO|\d)))", re.I)
    for k, line in enumerate(lines):
        m = start.search(line)
        if m and (m.group(0).strip(" \t(").upper().startswith("ON") or m.start() == len(line) - len(line.lstrip(" \t("))):
            seg = re.split(r"\bJUDGMENT\b", line[m.start():], maxsplit=1)[0]
                                                                                                   
                                                                                                   
                                          
            if seg.lstrip().startswith("(") or line[:m.start()].rstrip().endswith("("):
                depth = 1 if not seg.lstrip().startswith("(") else 0
                for i, ch in enumerate(seg):
                    depth += (ch == "(") - (ch == ")")
                    if depth == 0 and ch == ")":
                        seg = seg[:i + 1]
                        break
            seg = seg[:300]
                                                                                             
            if re.fullmatch(r"(?i)[ \t(]*on[ \t]+appeal[ \t]+from:?[ \t]*", seg):
                nxt = next((x for x in lines[k + 1:k + 3] if x.strip()), "")
                seg += "\n" + re.split(r"\bJUDGMENT\b", nxt, maxsplit=1)[0]
            selected.append(seg)
            continuing = seg.count("(") > seg.count(")")
        elif continuing and line.strip():
            selected.append(line)
            if ")" in line: continuing = False
    return "\n\n".join(selected + [body])
