                       
"""R108(b) (24 Nov 2026): A BARE CASE NAME COUNTS as an authority.

A bare case name is `X v Y`, `In re X`, `Re X` or `Ex parte X` printed in the judgment (core + footnotes) with no
citation beside it. Rule 1 still governs: a case is ONE authority, so a bare name of a case cited elsewhere in the
judgment adds nothing, and one bare name repeated is one authority.

Not counted: the judgment's own case name; a name with a citation, a footnote marker or a cross-reference
(supra, above, n 12) after it in the same sentence -- the citation engine reads those; generic labels (`Part v`,
`Plaintiff v Defendant`).

JURISDICTION: the name is matched against the case titles of the
corpus (Master 5.5 `Case` column). A match in one jurisdiction only gives that jurisdiction; no match, or matches in
several, gives `UNKNOWN` (Master column `Cites Unknown`), which still counts in the total.
"""
import re
import bisect

_TOK = (r"(?:[A-Z][\w'’`&.\-]*|\((?:[A-Z][\w.]*\s?){1,3}\)|of|and|&|the|de|la|du|des|for|in|on|ex|parte|von|van|der|"
        r"le|da|di|del|y|et|al|re|a|an|to|at|No\.?|\d{1,4})(?![\w'’`])")
_SIDE = r"[A-Z][\w'’`&.\-]*(?:[ \t]+" + _TOK + r"){0,8}"
_VS = re.compile(r"(?<![\w.])(" + _SIDE + r")[ \t]+v\.?[ \t]+(" + _SIDE + r")")
_RE = re.compile(r"(?<![\w])(In[ \t]+re|In[ \t]+the[ \t]+matter[ \t]+of|Re|Ex[ \t]+parte)[ \t]+(" + _SIDE + r")")
_LABEL = re.compile(r"(?i)^(?:chapter|part|schedule|article|section|volume|vol|book|title|appendix|division|annex|table|"
                    r"figure|clause|rule|order|plaintiff|defendant|claimant|applicant|appellant|respondent|"
                    r"petitioner|accused|the\s+plaintiff|the\s+defendant|[a-qs-z])$")
_TRAIL_DROP = re.compile(r"(?:\s+(?:of|and|&|the|de|la|du|des|for|in|on|ex|to|at|an|re|et|al|No\.?|\d{1,4}))+$", re.I)
_LEAD_DROP = re.compile(r"^(?:(?:See|see|In|Cf|cf|Also|also|And|Of|The|Per|per|From|from|Applying|applying|Following|"
                        r"following|Citing|citing|Approved|approving|But|Thus|So|As|Compare|Contra|E\.g\.|Vide|vide|Viz|See,|Except|Neither|"
                        r"Nor|Unlike|Like|Whereas|Although|While|Because|Since|Both|Either|Unless|Under|After|Before|"
                        r"Despite|On|By|Until|Where|When|If|Then|Here|There|Only|Even|Accordingly|However|Further|Indeed|"
                        r"Moreover|Similarly|Likewise|Again|Secondly|Thirdly|Finally|First|Second|Third)\s+)+")
_ABBR = re.compile(r"\b(?:Co|Ltd|Inc|Bros|St|Mr|Mrs|Dr|Corp|Pty|No|Ry|Rly|Assn|Dept|Govt|Bd|Comm|Comr|Commr|Ins|Mut|"
                   r"Nat|Int|Mfg|Mfrs|Ass|Soc|Univ|Est|Exors|Admrs|Ltee|Cie|Ste|Ave|[A-Z])\.$")
_STOP = {"the", "of", "and", "&", "for", "in", "on", "ex", "parte", "a", "an", "to", "at", "re", "pty", "ltd", "limited",
         "inc", "co", "corp", "corporation", "plc", "llc", "company", "anor", "another", "others", "ors", "no"}
_CROWN = re.compile(r"(?i)^(?:r|reg|regina|rex|the\s+queen|the\s+king|queen|king|people|state|united\s+states|"
                    r"public\s+prosecutor|pp|hma|her\s+majesty'?s?\s+advocate)$")
                                                                                                              
_CITE_AFTER = re.compile(
    r"^[\s,.;:]*(?:\[\d{1,3}\]|\(\d{1,3}\)(?!\s*\d)|\(?FN\s?\d{1,3}\)?|\d{1,3}\b|[¹²³⁰-⁹]+)"
    r"|[\[(]\s?(?:1[5-9]|20)\d{2}\s?[\])]"
    r"|\b\d{1,4}\s+[A-Z][A-Za-z.&()' ]{0,30}?\s+\d{1,5}\b"
    r"|\b(?:1[5-9]|20)\d{2}\s+(?:\(\d{1,2}\)\s+)?[A-Z][A-Za-z.()]{1,12}\s+\d"
    r"|^[\s,.;:]*(?:(?:Ltd|Co|Inc|Limited|Corp)\.?)?[\s,.]*[({]?[\w]{1,2}\)"
    r"|^[\s,]*at\s+(?:pp?\.?\s*)?\d"
    r"|\bAIR\s+\d{4}|\b(?i:supra|infra|ante|loc\.?\s*cit|op\.?\s*cit)\b|\b(?:post|above|below)\b|\bn\s?\d{1,3}\b"
    r"|\b(?:unreported|Nos?\.?\s?\d)")
_CONNECT = {"of", "and", "&", "the", "de", "la", "du", "des", "for", "von", "van", "der", "le", "da", "di", "del", "y", "et"}
_SENT_END = re.compile(r"(?<=[a-z)\]])\.\s+(?=[A-Z])|\n\s*\n")


def _to_sentence_end(t):
    """Cut at the first real sentence end: a full stop after an ordinary word of 5+ lower-case letters (or a
    closing bracket), then a capital. `App. D. C.`, `Ves.`, `Rep.` and initials are not sentence ends."""
    for m in re.finditer(r"\.\s+(?=[A-Z])", t):
        w = re.search(r"(\S+)$", t[:m.start()])
        w = w.group(1) if w else ""
                                                                                                                          
                                                                                                     
        if re.fullmatch(r"[a-z]{5,}|[A-Z][a-z]{4,}|.*[)\]”\"]", w):
            return t[:m.start()]
    return t


def _clean_side(s, left=False):
    s = re.split(r"\n", s)[0] if not left else re.split(r"\n", s)[-1]
    if not left:
        for m in re.finditer(r"\.\s+(?=[A-Z])", s):                                      
            if not _ABBR.search(s[:m.start() + 1]):
                s = s[:m.start()]
                break
        s = re.split(r"(?<=[A-Za-z])\d", s)[0]                                            
        s = re.split(r"\s+(?:AIR\b|\(?FN\s?\d|\d)", s)[0]                                                     
        s = re.split(r"\s+the\s+(?=[A-Z])", s)[0]                                                    
        s = re.split(r"\s+at\s+(?:pp?\.?\s*)?(?:\d|$)|\s+at\s+p\b", s)[0]                              
        s = re.split(r"\s+(?i:infra|supra|ante)\b", s)[0]                                            
    else:
        s = re.split(r"\.\s+(?=[A-Z])", s)[-1]
                                                                                                          
        toks, keep = s.split(), []
        for w in reversed(toks):
            if re.fullmatch(r"(?:J|JJ|LJ|LJJ|CJ|MR|LC|JA|JJA|P|SJ|JSC|LCJ|CJC|VC|Bt|J\.|L\.J\.|C\.J\.)[,.]?", w):
                break
            if w[:1].isupper() or w[:1] in "(&" or w.lower() in _CONNECT:
                keep.append(w)
                if w.endswith((",", ";", ":")):
                    keep.pop()
                    break
            else:
                break
        s = " ".join(reversed(keep))
        s = re.sub(r"^(?:(?:of|and|&|the|de|la|du|des|for|in|on|ex|to|at|a|an|re)\s+)+", "", s)
        s = _LEAD_DROP.sub("", s)
    s = _TRAIL_DROP.sub("", s.strip(" ,.;:"))
    return s.strip(" ,.;:")


def _words(s):
    s = s.lower().replace("’", "'")
    s = re.sub(r"\([^)]*\)", " ", s)
    return [w for w in re.findall(r"[a-z][a-z'\-]*", s) if w not in _STOP]


def side_key(s):
    s = s.strip()
    if _CROWN.match(s):
        return "r"
    w = _words(s)
    return " ".join(w[:2]) if w else ""


def find_names(text):
    """Yield (start, end, display, key) for each case name in the text."""
                                                                                                
    out = []
    pos = 0
    while True:
                                                                                                                        
                                                                                
        m = _VS.search(text, pos)
        if not m:
            break
        a, b = _clean_side(m.group(1), left=True), _clean_side(m.group(2))
        pos = max(m.start(2) + 1, m.start(2) + len(b)) if b else m.end()
        if not a or not b or _LABEL.match(a) or _LABEL.match(b) or b[:1].isdigit():
            continue
                                                                                               
        if re.match(r"[ \t]+v\.?[ \t]", text[m.start(2) + len(b):m.start(2) + len(b) + 5]) and re.search(r"\s(?:and|or|&)\s", b):
            b = re.split(r"\s(?:and|or|&)\s(?!.*\s(?:and|or|&)\s)", b)[0].strip()
            pos = m.start(2) + len(b)                                            
        ka, kb = side_key(a), side_key(b)
        if ka and kb:
            out.append((m.start(1) + max(0, m.group(1).rfind(a.split()[0])), m.start(2) + len(b),
                        a + " v " + b, ka + "|" + kb))
    for m in _RE.finditer(text):
        x = _clean_side(m.group(2))
        if x and not _LABEL.match(x):
            k = side_key(x)
            ex = m.group(1).lower().startswith("ex")
            if k:
                out.append((m.start(), m.start(2) + len(x), ("Ex parte " if ex else "Re ") + x, ("ex|" if ex else "re|") + k))
    out.sort()
                                                                                        
    vs = [(s, e) for s, e, _d, k in out if not k.startswith(("re|", "ex|"))]
    out = [o for o in out if not (o[3].startswith(("re|", "ex|")) and any(s <= o[0] < e or o[0] <= s < o[1] for s, e in vs))]
                                                                                                         
                                                                                                                      
                                                                                                                   
                                                                            
    i = 0
    while i < len(out):
        s, e, d, k = out[i]
        while i + 1 < len(out) and re.fullmatch(r"\s*[,;:]\s*(?:In\s+re\s+|Re\s+|Ex\s+parte\s+)?", text[e:out[i + 1][0]] or "x") and (
                out[i + 1][3].startswith("ex|")
                or (k.startswith("re|") and not out[i + 1][3].startswith(("re|", "ex|")))
                or (k.startswith("ex|") and out[i + 1][3].startswith("re|"))):
            _s2, e, d2, _k2 = out[i + 1]
            d = d + "; " + d2
            i += 1
        yield s, e, d, k
        i += 1


def own_keys(own_name):
    return {k for _s, _e, _d, k in find_names(str(own_name or ""))}


def _first(k, i):
    return k.split("|")[i].split(" ")[:1]


def _same_case(k, c):
    """Two keys for one case: the same first words on both sides, or the same first party (not the Crown) with
    the other side abbreviated (`Woolmington v DPP` / `Woolmington v Director of Public Prosecutions`)."""
    if k == c:
        return True
    if _first(c, 0) == _first(k, 0) and _first(c, 1) == _first(k, 1):
        return True
    a1, a2 = k.split("|"); b1, b2 = c.split("|")
    if a1 == b1 and a1 not in ("r", "re"):
        x, y = sorted((a2, b2), key=len)
        ini = "".join(w[0] for w in y.split())
        if len(x.split()) == 1 and len(x) <= 5 and len(ini) >= 2 and x.startswith(ini):
            return True
    return False


def bare_names(text, cited_spans=(), own_name=None, gap=140):
    """Distinct bare case names: [(display, key, start)]."""
    starts = sorted(s for s, _e in cited_spans)
    own = own_keys(own_name)
    cited_keys, bare = set(), []
    names = list(find_names(text))
    for n_, (s, e, disp, k) in enumerate(names):
        nxt = names[n_ + 1][0] if n_ + 1 < len(names) and names[n_ + 1][0] > e else e + 200                          
        i = bisect.bisect_left(starts, e)
        near = i < len(starts) and starts[i] - e <= gap and not re.search(r"[.;]\s+[A-Z]", text[e:starts[i]])
        if not near:
            near = bool(_CITE_AFTER.search(_to_sentence_end(" ".join(text[e:min(e + 200, nxt)].split()))))
        if not near:
            near = bool(re.search(r"(?i)sub\s+nom\.?\s*$|\bsupra\W{0,3}$", text[max(0, s - 24):s]))
        if near:
            cited_keys.add(k)
        else:
            bare.append((s, e, disp, k))
    out, seen = [], set()
    for s, e, disp, k in bare:
        if any(_same_case(k, c) for c in cited_keys | own | seen):
            continue
        seen.add(k)
        out.append((disp, k, s))
    return out


class TitleIndex:
    """Case-title key -> jurisdiction, from the corpus. Looked up with the same test as the dedupe (`_same_case`), so
    `Paris v Stepney Borough Council` finds the corpus title `Paris v Stepney BC` and `Woolmington v Director of
    Public Prosecutions` finds `Woolmington v DPP`."""
    def __init__(self, pairs):
        """pairs: (title, jurisdiction, decision year or None)."""
        self.m = {}
        for p in pairs:
            title, jur = p[0], p[1]
            yr = p[2] if len(p) > 2 else None
            for _s, _e, _d, k in find_names(re.sub(r"[\[(]\d{4}[\])].*$", "", str(title))):
                self.m.setdefault(k.split("|")[0], []).append((k, jur, yr))
                break

    def jurisdiction(self, key, citing_year=None):
        """Only a corpus case decided no later than the citing judgment can be the case named. The Crown and `Re`
        first parties are too common to place a case on the other party's first word alone: those need the key."""
        side1 = key.split("|")[0]
        c = [(j, y) for k, j, y in self.m.get(side1, [])
             if (k == key if side1 in ("r", "re", "ex") else _same_case(key, k))]
        if citing_year:
            c = [(j, y) for j, y in c if not y or y <= citing_year]
        js = {j for j, _y in c}
        return next(iter(js)) if len(js) == 1 else "UNKNOWN"
