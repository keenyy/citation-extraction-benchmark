                       

import csv
import re
import unicodedata

                                                                                             

_DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−⁃﹘﹣－"), "-")
_NONASCII = re.compile(r"[^\x00-\x7f]")


def _fold_char(m):
    c = m.group(0)
    if c in "‘’‛ʼ´`":                                                                 
        return c
    d = unicodedata.normalize("NFD", c)
    return d[0] if d[0].isascii() and d[0].isalpha() and len(d) > 1 else c


def _cased(text):
    
    t = unicodedata.normalize("NFKC", text or "")
    if not t.isascii():
        t = _NONASCII.sub(_fold_char, t).translate(_DASHES)
    return t


def _lower(cased):
    low = cased.lower()
    if len(low) != len(cased):                                                                      
        low = "".join(c.lower() if len(c.lower()) == 1 else c for c in cased)
    low = low.translate({0x2018: "'", 0x2019: "'", 0x201b: "'", 0x02bc: "'", 0xb4: "'", 0x60: "'"})
    if "�" in low:
        low = _FFFD_LETTER.sub("e", low)
    return low


_FFFD_LETTER = re.compile(r"(?<=[a-z])�(?=[a-z])")
_TOK = re.compile(r"\w+")
_GAP_OK = re.compile(r"(?:[.,]?[\s\-]+|\.)\Z")


def normalise(text):
    
    return _lower(_cased(text))


                                                                                                             

_FN_REF = re.compile(r"(?<=[a-zA-Z.,;:)\]])\d{1,3}(?=\s|$)")
_NOT_A_WORD = re.compile(r"^[-_=*.–—]+$")


def count_words(text):
    if not text:
        return 0
    return sum(1 for t in _FN_REF.sub("", text).split() if not _NOT_A_WORD.match(t))


                                                                                         

class Lexicon:
    

    def __init__(self, name):
        self.name = name
        self.index = {}
        self.rows = {}                                             

    def add(self, canonical, phrase, row):
        toks = tuple(_TOK.findall(normalise(phrase)))
        if not toks:
            return
        self.rows.setdefault(canonical, row)
        lst = self.index.setdefault(toks[0], [])
        if not any(t == toks for t, _c, _r in lst):
            lst.append((toks, canonical, row))

    def finish(self):
        for lst in self.index.values():
            lst.sort(key=lambda x: (-len(x[0]), -sum(map(len, x[0]))))


_RES = {}
                                                                                                                             
                                                                                                                      
_SKIP_VARIANTS = {"pp", "said", "such", "same"}


def _flags(row):
    return sorted(k for k, v in row.items() if k.startswith("src_") and v == "1")


def load_resources(path):
    
    import os
    A, W, B = Lexicon("A"), Lexicon("A_wiki"), Lexicon("B")
    with open(os.path.join(path, "latin_phrases.csv"), encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("count") != "1":
                continue
            row = {"term": r["term"], "list": "A", "ambiguous": r.get("ambiguous") == "1", "src": _flags(r),
                   "wiki": r.get("src_wiki") == "1"}
            forms = [r.get("normalised") or r["term"], r["term"]] + [
                v.strip() for v in (r.get("variants") or "").split("|") if v.strip() not in _SKIP_VARIANTS]
            canon = normalise(r.get("normalised") or r["term"])
            for f in forms:
                if not f:
                    continue
                A.add(canon, f, row)
                if row["wiki"]:
                    W.add(canon, f, row)
    with open(os.path.join(path, "archaic_legalese.csv"), encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            row = {"term": r["term"], "list": "B", "ambiguous": r.get("ambiguous") == "1", "src": _flags(r), "wiki": False}
            forms = [r.get("normalised") or r["term"], r["term"]] + [
                v.strip() for v in (r.get("variants") or "").split("|") if v.strip() not in _SKIP_VARIANTS]
            canon = normalise(r.get("normalised") or r["term"])
            for f in forms:
                if not f:
                    continue
                B.add(canon, f, row)
    for L in (A, W, B):
        L.finish()
    _RES.update(A=A, W=W, B=B)
    return _RES


                                                                                                  

_CAP_AFTER = re.compile(r"[\s]+[\[(\"'“‘A-Z0-9]")
_CAP_WORD_AFTER = re.compile(r"\.?[ \t]+[A-Z]")                                             
_LOWER_AFTER = re.compile(r"[ \t]+[a-z]")
_LINE_START = re.compile(r"(?:^|\n)[ \t>*#_|\[(-]*\Z")                                                                  
_CORAM_NAMES = re.compile(r"[ \t]+[A-Z]")
_NISI_PRE = {"decree", "order", "rule"}
_FIAT_BAD_NEXT = re.compile(r"\s+(money|currency|currencies|chrysler|spa|automobiles|500|panda|punto)\b", re.I)


def _ctx_ok(canon, cased, low, s, e, toks_before):
    if canon == "in re":                                                                        
        return False                                                                                                                          
    if canon == "ex parte":                                                                                           
        return not _CAP_WORD_AFTER.match(cased, e)
    if canon == "ex rel":
        return not _CAP_WORD_AFTER.match(cased, e)
    if canon == "procurator":                                                    
        return not re.match(r"[ \t\-]+fiscals?\b", low[e:e + 12])
    if canon == "coram":                                            
        if _LINE_START.search(cased[max(0, s - 40):s]) or cased[e:e + 1] == ":":
            return False
        if cased[s].isupper() and _CORAM_NAMES.match(cased, e):
            return False
        return True
    if canon == "nisi":
        return bool(toks_before) and toks_before[-1] in _NISI_PRE
    if canon == "fiat":
        if _FIAT_BAD_NEXT.match(low, e):
            return False
        if cased[s].isupper():                                                              
            k = s - 1
            while k >= 0 and cased[k] in " \t\"'“‘(":
                k -= 1
            return k < 0 or cased[k] in ".?!:\n"
        return True
    return True


                                                                                        

def _scan(low, cased, toks, lex):
    
    out = []
    n = len(toks)
    idx = lex.index
    i = 0
    while i < n:
        cand = idx.get(toks[i][0])
        hit = None
        if cand:
            for tt, canon, row in cand:
                k = len(tt)
                if i + k > n:
                    continue
                ok = True
                for j in range(1, k):
                    if toks[i + j][0] != tt[j] or not _GAP_OK.match(low[toks[i + j - 1][2]:toks[i + j][1]]):
                        ok = False
                        break
                if not ok:
                    continue
                s, e = toks[i][1], toks[i + k - 1][2]
                if canon in ("in re", "nisi", "fiat", "ex parte", "ex rel", "procurator", "coram"):
                    if not _ctx_ok(canon, cased, low, s, e, [t[0] for t in toks[max(0, i - 1):i]]):
                        continue
                hit = (s, e, k, canon, row)
                break
        if hit:
            out.append(hit)
            i += hit[2]
        else:
            i += 1
    return out


                                                                                                

_QTOK = re.compile(r"[“”\"]|(?<![\w])['‘](?=\S)|(?<=\S)['’](?![\w])|�|\n[ \t]*\n")
_BLOCK_LINE = re.compile(r"^(?: {4,}|\t|>)\S", re.M)


def _quote_spans(cased):
    
    spans = []
    dq = sq = None                                                        
    for m in _QTOK.finditer(cased):
        g = m.group(0)
        p = m.start()
        if g[0] == "\n":                                                                                        
            dq = sq = None
        elif g == "“":
            dq = p
        elif g == "”":
            if dq is not None:
                spans.append((dq, p)); dq = None
        elif g == '"':
            if dq is None:
                dq = p
            else:
                spans.append((dq, p)); dq = None
        elif g in ("‘",) or (g == "'" and cased[p + 1:p + 2] and (p == 0 or not cased[p - 1].isalnum())):
            if sq is None:
                sq = p
        elif g in ("’", "'"):
            if sq is not None:
                spans.append((sq, p)); sq = None
        elif g == "�":                                                                                    
            nxt = cased[p + 1:p + 2]
            if nxt.isdigit():
                continue
            prev = cased[p - 1:p] if p else " "
            if prev.isspace() or prev in "([":
                dq = p if dq is None else dq
            elif dq is not None:
                spans.append((dq, p)); dq = None
    for m in _BLOCK_LINE.finditer(cased):
        e = cased.find("\n", m.start())
        spans.append((m.start(), len(cased) if e < 0 else e))
    spans.sort()
    return spans


def _in_spans(spans, starts, s):
    import bisect
    k = bisect.bisect_right(starts, s) - 1
                                              
    while k >= 0 and k > bisect.bisect_right(starts, s) - 6:
        if spans[k][0] <= s < spans[k][1]:
            return True
        k -= 1
    return False


                                                                                       

def analyse(text, return_matches=False):
    if not _RES:
        raise RuntimeError("call load_resources(path) first")
    A, W, B = _RES["A"], _RES["W"], _RES["B"]
    cased = _cased(text)
    low = _lower(cased)
    words = count_words(text)
    toks = [(m.group(0), m.start(), m.end()) for m in _TOK.finditer(low)]

    ma = _scan(low, cased, toks, A)
    mb = _scan(low, cased, toks, B)
    mw = _scan(low, cased, toks, W)

    def per1000(x):
        return round(x / words * 1000, 4) if words else 0.0

                                   
    ev = sorted([(s, e, k, c, "A") for s, e, k, c, _r in ma] + [(s, e, k, c, "B") for s, e, k, c, _r in mb],
                key=lambda x: (x[0], -(x[1] - x[0])))
    clusters = []
    for s, e, k, c, lst in ev:
        if clusters and s < clusters[-1][1]:
            cl = clusters[-1]
            if e > cl[1]:
                cl[1] = e
            if (e - s) > cl[4]:
                cl[3], cl[4] = c, e - s
        else:
            clusters.append([s, e, 0, c, e - s])
    tok_starts = [t[1] for t in toks]
    import bisect
    spec_tokens = 0
    for cl in clusters:
        spec_tokens += bisect.bisect_left(tok_starts, cl[1]) - bisect.bisect_left(tok_starts, cl[0])

    shall = sum(1 for m in mb if m[3] == "shall")
    quoted_b = 0
    qspans = qstarts = None
    qflags = []
    if mb:
        qspans = _quote_spans(cased)
        qstarts = [q[0] for q in qspans]
        for m in mb:
            qf = _in_spans(qspans, qstarts, m[0])
            qflags.append(qf)
            quoted_b += qf
    quoted_b_excl = sum(1 for m, qf in zip(mb, qflags) if qf and m[3] != "shall")

    res = {
        "core_words": words,
        "latin_occurrences": len(ma),
        "latin_unique": len({m[3] for m in ma}),
        "latin_tokens": sum(m[2] for m in ma),
        "latin_per_1000": per1000(len(ma)),
        "legalese_occurrences": len(mb),
        "legalese_unique": len({m[3] for m in mb}),
        "legalese_tokens": sum(m[2] for m in mb),
        "legalese_per_1000": per1000(len(mb)),
        "shall_count": shall,
        "legalese_excl_shall_per_1000": per1000(len(mb) - shall),
        "legalese_quoted_occurrences": quoted_b,
        "legalese_quoted_share": round(quoted_b / len(mb), 4) if mb else 0.0,
        "shall_quoted": sum(1 for m, qf in zip(mb, qflags) if qf and m[3] == "shall"),
        "specialist_occurrences": len(clusters),
        "specialist_unique": len({cl[3] for cl in clusters}),
        "specialist_tokens": spec_tokens,
        "specialist_per_1000": per1000(len(clusters)),
        "lim_style_count": len(mw),
        "lim_style_per_1000": per1000(len(mw)),
    }
    if return_matches:
        wiki_spans = {(m[0], m[1]) for m in mw}
        out = []
        for s, e, k, c, row in ma:
            out.append({"term": cased[s:e], "canonical": c, "start": s, "end": e, "list": "A",
                        "src_wiki": row["wiki"], "lim_style": (s, e) in wiki_spans, "src": row["src"],
                        "ambiguous": row["ambiguous"], "quoted": None})
        for (s, e, k, c, row), qf in zip(mb, qflags):
            out.append({"term": cased[s:e], "canonical": c, "start": s, "end": e, "list": "B",
                        "src_wiki": False, "lim_style": False, "src": row["src"],
                        "ambiguous": row["ambiguous"], "quoted": qf})
        out.sort(key=lambda d: (d["start"], d["list"]))
        res["matches"] = out
        res["normalised_text"] = low
        res["cased_text"] = cased
    return res
