                       

import argparse
import collections
import io
import json
import os
import re
import sqlite3
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import jr_citations as C                                                     
import jr_reporters as R                                                     
import jr_sections as S                                                      
import master5_sqlite as MS                                                  

LP = MS.LP

                                                                                               
                                  
SG = ("SGCA", "SGHC")
UK = ("UKHL", "UKSC")
NAME_SERIES = {
    "SLR": (SG, None), "SLRR": (SG, None),
    "CLR": (("HCA",), None), "ALJR": (("HCA",), None),
    "ALR": (("HCA",), r"\(\s*HCA\s*\)|High Court"),
    "SCR": (("SCC",), None),
    "HKCFAR": (("HKCFA",), None),
    "HKLRD": (("HKCFA",), r"\(\s*CFA\s*\)|Court of Final Appeal"),
    "AC": (UK, None), "APPCAS": (UK, None),
    "WLR": (UK, r"\(\s*(?:HL|UKHL|UKSC|SC\s*\(E\)|HL\s*\(E\))\s*\)|House of Lords|Supreme Court"),
    "ALLER": (UK, r"\(\s*(?:HL|UKHL|UKSC|SC\s*\(E\)|HL\s*\(E\))\s*\)|House of Lords|Supreme Court"),
    "NZLR": (("NZSC",), r"\(\s*SC\s*\)|\(\s*NZSC\s*\)|Supreme Court"),
}
PC_MARK = re.compile(r"^[\s,;]{0,3}\(\s*(?:PC|P\.C\.)\s*\)|^[^.;]{0,30}Privy Council")
                                                                  
OWN_SERIES = {"HCA": {"HCA", "CLR", "ALR", "ALJR"}, "SCC": {"SCC", "SCR"},
              "USSC": {"US", "SCT", "LED", "LED2D"}, "SGCA": {"SGCA", "SLR", "SLRR"},
              "SGHC": {"SGHC", "SLR", "SLRR"}, "UKHL": {"UKHL", "AC", "APPCAS", "WLR", "ALLER"},
              "UKSC": {"UKSC", "AC", "WLR", "ALLER"}, "NZSC": {"NZSC", "NZLR"},
              "HKCFA": {"HKCFA", "HKCFAR", "HKLRD"}}

GENERIC = set("""the a an of and or for in on at to by with re ex parte in the matter v vs versus
public prosecutor pp r rex regina king queen crown state states united people attorney general ag
attorneygeneral solicitor director commissioner commissioners comptroller minister secretary
registrar collector board council city county government federal commonwealth hksar hong kong
special administrative region republic singapore new zealand canada australia her his majesty
majestys hm ltd limited pte pty co company corp corporation inc plc llc llp sdn bhd bank holdings
holding group international another others anor ors anr and an other mr mrs ms dr sir lord lady
deceased estate trustees trustee executors executor administrator official assignee liquidator
liquidators receiver no appellant respondent applicant plaintiff defendant petitioner taxation
revenue inland customs excise police chief bhd nv bv ag sa gmbh""".split())


def fold(s):
    s = unicodedata.normalize("NFKD", str(s or "")).replace("’", "'")
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    s = re.sub(r"'s\b", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


_V = re.compile(r"\s(?:v|vs|versus)\.?\s", re.I)
_CITE_IN_NAME = re.compile(r"\[\d{4}\].*$|\(\d{3,4}\s*U\.?\s*S\.?.*$|\(\d+,\s*Orig.*$|\(\d+-\d+\).*$")


def sides(name):
    
    name = _CITE_IN_NAME.sub("", str(name or ""))
    name = re.sub(r"\([^()]*\)", " ", name)
    parts = _V.split(" " + name + " ", maxsplit=1)
    out = []
    for p in parts:
        w = [t for t in fold(p).split() if t not in GENERIC and not t.isdigit() and len(t) > 1]
        out.append(set(w))
    return out


def series_of(key):
    return " ".join(x for x in key.split() if not re.fullmatch(r"\d+(?:-\d+)?", x))


def years_of(key):
    m = re.match(r"(\d{4})(?:-(\d{2,4}))?\s", key)
    if not m:
        return None
    a = int(m.group(1))
    b = m.group(2)
    b = int(b if len(b) == 4 else str(a)[:2] + b) if b else a
    return set(range(a - 1, b + 1))


def is_sg_slr(key):
    m = re.match(r"(\d{4})(?:-\d+)? SLRR?(?: (\d+))? \d+$", key)
    if not m:
        return False
    return int(m.group(1)) >= 1965 and (m.group(2) is None or int(m.group(2)) <= 4)


def _toks(s):
    
    s = re.sub(r"\([^()]*\)|“[^”]*”", " ", s)
    out = []
    for w in re.findall(r"[^\W_]+(?:['’][^\W_]+)?", s):
        f = fold(w)
        for x in f.split():
            out.append((x, w[:1].islower()))
    return out


def _distinct(x):
    return x not in GENERIC and not x.isdigit() and len(x) > 1


def window_sides(text, start, floor):
    
    w = text[max(floor, start - 260):start]
                                                                                                   
    w = re.split(r"(?:(?<=[a-z]{4})\.\s+(?=[A-Z])|[;:]\s+|\n\s*\n|\b[Ss]ee\b|\bcf\b|\b[Ii]n\b(?=\s+[A-Z]))",
                 w)[-1] if w else ""
    w = re.sub(r"[\s,]*\(\d{4}\)\s*$|[\s,]*\[\d{4}\]\s*$", "", w)
    if len(w) > 200:
        w = w[-200:]
    ms = list(_V.finditer(" " + w + " "))
    if ms:
        m = ms[-1]
        left = (" " + w + " ")[:m.start()]
        right = (" " + w + " ")[m.end():]
        return ([_toks(left)[-8:], _toks(right)[:12]], w)
    mm = re.search(r"(?:\b(?:re|in re|ex parte)\s+)(.{2,80})$", w, re.I)
    if mm:
        return ([_toks(mm.group(1))], w)
    return (None, w)


def name_match(cited, corpus):
    
    if cited is None:
        return False
    if len(cited) == 1:
        c = {x for x, _ in cited[0] if _distinct(x)}
        allw = set().union(*corpus)
        return bool(c) and c <= allw and len(c) >= min(2, len(allw))
    if len(corpus) < 2:
        return False
    hits = 0
    left, right = cited
    kL, kR = corpus[0], corpus[1]
    run, stop = 0, None
    for x, low in reversed(left):
        if not _distinct(x):
            continue
        if x in kL:
            run += 1
            continue
        stop = (x, low)
        break
    if kL:
        if run < min(2, len(kL)) or (stop is not None and not stop[1]):
            return False
        hits += 1
    elif stop is not None and not stop[1]:
        return False                                                                            
    cR = {x for x, _ in right if _distinct(x)}
    if cR:
        if not kR or not cR <= kR or len(cR) < min(2, len(kR)):
            return False
        hits += 1
    return hits >= 1


                                                                                               
CA_CUE = re.compile(r"Court of Appeal|\bJJ?A\b|\(CA\)")
HC_CUE = re.compile(r"High Court|\bJC\b|\(HC\)")


def court_cue_contradicts(cue_text, court):
    
    if court == "SGHC":
        return bool(CA_CUE.search(cue_text)) and not HC_CUE.search(cue_text)
    if court == "SGCA":
        return bool(HC_CUE.search(cue_text)) and not CA_CUE.search(cue_text)
    return False


def own_keys(court, cit, fname, head):
    
    keys = set()
    norm = lambda s: re.sub(r"[\s.]+", "", s or "").lower()                      
    cit = (cit or "").strip()
                                                                                                      
                                                                                                              
                                                                                                                   
                                                                                                     
    if court == "MYFC":
        m = re.match(r"\[(\d{4})\]\s*MYFC\s+(.+)$", cit)
        return {"%s MYFC %s" % (m.group(1), re.sub(r"\s+", "", m.group(2)).upper())} if m else set()
    if cit and (norm(cit) in norm(fname) or norm(cit) in norm(head[:6000])):
        try:
            keys |= {x["key"] for x in C.items(cit, R, citing_court=court)}
        except Exception:                                                          
            pass
    allow = OWN_SERIES.get(court, set())
    lines = head.splitlines()[:80]
    for ln in lines:
        if not cit or norm(cit) not in norm(ln) and not re.match(r"\s*(?:Neutral citation|CITATION)\s*:", ln, re.I):
            continue
        if len(ln) > 320:
            i = ln.find(cit[:12]) if cit else -1
            ln = ln[max(0, i - 160):i + 160] if i >= 0 else ln[:320]
        try:
            for x in C.items(ln, R, citing_court=court):
                if series_of(x["key"]) in allow:
                    keys.add(x["key"])
        except Exception:                                                          
            pass
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    db = sqlite3.connect(a.db)
    J = {}
    for jid, court, sheet, cit, case, year, fn, tf in db.execute(
            'SELECT id,court,sheet,citation,"case",year,filename,text_found FROM judgment'):
        J[jid] = dict(court=court, sheet=sheet, cit=cit, case=case, year=year, fn=fn or "", tf=tf)
    dd = dict(db.execute("SELECT id,value FROM judgment_field WHERE column='Decision Date'").fetchall())
    for jid, j in J.items():
        y = str(dd.get(jid) or "")[:4]
        j["dyear"] = int(y) if y.isdigit() else (int(j["year"]) if str(j["year"] or "").isdigit() else None)
        j["sides"] = sides(j["case"])

                                          
    missing = []                                                                                 

    def _read(p):
        try:
            return io.open(LP + p, encoding="utf-8", errors="replace").read()
        except OSError:
            return None
    own = collections.defaultdict(set)
    texts = {}
    for n, (jid, j) in enumerate(J.items()):
        head = ""
        if j["tf"]:
            p, _ = MS.find_text(j["sheet"], j["fn"], j["cit"])
            raw = _read(p) if p else None
            if raw is not None:
                j["path"] = p
                head = re.split(r"(?m)^CORE JUDGMENT\s*$", raw, maxsplit=1)[0][:12000]
            elif p:
                missing.append(jid)
        for k in own_keys(j["court"], j["cit"], j["fn"], head):
            own[k].add(jid)
        if n % 5000 == 0:
            sys.stderr.write("own keys %d/%d\n" % (n, len(J)))
    OWN = {k: next(iter(v)) for k, v in own.items() if len(v) == 1}
    own_dup = {k: sorted(v) for k, v in own.items() if len(v) > 1}

                                                                                              
                               
    inv = collections.defaultdict(lambda: collections.defaultdict(set))
    for jid, j in J.items():
        if j["dyear"]:
            for side in j["sides"]:
                for t in side:
                    inv[(j["court"], j["dyear"])][t].add(jid)

                                        
    par = collections.defaultdict(lambda: collections.defaultdict(set))                           
    namev = collections.defaultdict(lambda: collections.defaultdict(set))
    name_amb = collections.Counter()
    veto = collections.Counter()
    cues = collections.defaultdict(collections.Counter)
    rowname = {}                                                                                   
    cur = db.execute("SELECT rowid,id,key,citation,aliases,start FROM citation ORDER BY id,start")
    last_id, text, prev_end = None, None, 0
    n = 0
    for rowid, cid, key, cit, aliases, start in cur:
        if cid != last_id:
            last_id, prev_end = cid, 0
            j = J.get(cid)
            text = None
            raw = _read(j["path"]) if j and j.get("path") else None
            if raw is not None:
                text = S.scope(S.split(raw), "core+fn")
            n += 1
            if n % 2000 == 0:
                sys.stderr.write("citing %d\n" % n)
        group = [key] + [x.strip() for x in (aliases or "").split(";") if x.strip()]
        owned = {OWN[k] for k in group if k in OWN}
        if len(owned) == 1:
            t = next(iter(owned))
            for k in group:
                if k not in OWN:
                    par[k][t].add(cid)
        cands_keys = [k for k in group if series_of(k) in NAME_SERIES or k in OWN]
        if text is None or start is None or not cands_keys:
            prev_end = (start or 0) + len(cit or "")
            continue
        ws, _w = window_sides(text, start, prev_end)
        after = text[start + len(cit or ""):start + len(cit or "") + 40]
        if series_of(key) in ("SLR", "SLRR"):
                                                                                                   
                                                           
            _ct = text[max(prev_end, start - 140):start] + " " + text[start + len(cit or ""):
                                                                       start + len(cit or "") + 90]
            ca, hc = bool(CA_CUE.search(_ct)), bool(HC_CUE.search(_ct))
            if ca != hc:
                cues[key]["CA" if ca else "HC"] += 1
        matched = set()
        if ws is not None:
            for k in cands_keys:
                sr = series_of(k)
                if sr in ("SLR", "SLRR") and not is_sg_slr(k):
                    continue
                if sr in NAME_SERIES:
                    courts, marker = NAME_SERIES[sr]
                    if PC_MARK.search(after):
                        continue
                    if marker and not re.search(marker, after):
                        continue
                    yrs = years_of(k)
                    if not yrs:
                        continue
                    words = {x for side in ws for x, _ in side if _distinct(x)}
                    pool = {jid for c_ in courts for y in yrs for t in words
                            for jid in inv.get((c_, y), {}).get(t, ())}
                    hits = [jid for jid in pool if jid != cid and name_match(ws, J[jid]["sides"])]
                    if len(hits) == 1:
                                                                                              
                                                                                                  
                                                                                
                        if court_cue_contradicts(_w + " " + after + text[start + len(cit or "") + 40:
                                                                         start + len(cit or "") + 90],
                                                 J[hits[0]]["court"]):
                            if k == key:
                                veto[k] += 1
                            continue
                        if k == key:
                            namev[k][hits[0]].add(cid)
                        matched.add(hits[0])
                    elif len(hits) > 1 and k == key:
                        name_amb[k] += 1
                elif k in OWN and name_match(ws, J[OWN[k]]["sides"]):
                    matched.add(OWN[k])
        rowname[rowid] = matched
        prev_end = start + len(cit or "")

                              
    MAP, why, conflicts = {}, {}, []
    for k, t in OWN.items():
        MAP[k], why[k] = t, ("own", 0)
    keys = set(par) | set(namev)
    for k in keys:
        if k in MAP:
            continue
        pv = {t: len(s) for t, s in par.get(k, {}).items()}
        nv = {t: len(s) for t, s in namev.get(k, {}).items()}
        pt = list(pv) if len(pv) == 1 and sum(pv.values()) >= 2 else None
        if len(pv) > 1:
            conflicts.append((k, "parallel", pv))
            continue
        if len(nv) > 1:
            conflicts.append((k, "name", nv))
            continue
        if name_amb.get(k) and nv:
            conflicts.append((k, "name ambiguous in %d rows" % name_amb[k], nv))
            continue
        tp = pt[0] if pt else None
        tn = next(iter(nv)) if nv else None
        if tp and tn and tp != tn:
            conflicts.append((k, "parallel vs name", {tp: pv[tp], tn: nv[tn]}))
            continue
        tgt = tp or tn
        if tgt and series_of(k) in ("SLR", "SLRR"):
                                                                                               
                                                                                                
                                                                                             
                                                                                                  
                                                                                                 
                                                 
            cq, tc = cues.get(k, {}), J[tgt]["court"]
            yrs = years_of(k) or set()
            ca_, hc_ = cq.get("CA", 0), cq.get("HC", 0)
            if (tc == "SGHC" and ca_ > hc_) or (tc == "SGCA" and hc_ > ca_):
                conflicts.append((k, "court named beside the citation is not the candidate's", dict(cq)))
                continue
            if tc == "SGHC" and yrs and J[tgt]["dyear"] is not None and J[tgt]["dyear"] < min(yrs) + 1 \
                    and not (hc_ > ca_):
                conflicts.append((k, "High Court decision the year before the report, High Court not named",
                                  {tgt: 1}))
                continue
        if tp and tn:
            MAP[k], why[k] = tp, ("parallel+name", pv[tp] + nv[tn])
        elif tp:
            MAP[k], why[k] = tp, ("parallel", pv[tp])
        elif tn and (series_of(k) not in ("SLR", "SLRR") or is_sg_slr(k)):
            MAP[k], why[k] = tn, ("name", nv[tn])

                     
    db.execute("DROP TABLE IF EXISTS citation_alias")
    db.execute("CREATE TABLE citation_alias (key TEXT PRIMARY KEY, judgment_id TEXT, how TEXT, votes INTEGER)")
    db.executemany("INSERT INTO citation_alias VALUES (?,?,?,?)",
                   [(k, t, why[k][0], why[k][1]) for k, t in MAP.items()])
    cols = [r[1] for r in db.execute("PRAGMA table_info(citation)")]
    if "cited_id" not in cols:
        db.execute("ALTER TABLE citation ADD COLUMN cited_id TEXT")
    db.execute("UPDATE citation SET cited_id = NULL")
    db.execute("UPDATE citation SET cited_id = (SELECT judgment_id FROM citation_alias a WHERE a.key = citation.key)")
                                                                                            
    upd = []
    for rowid, key, aliases in db.execute(
            "SELECT rowid,key,aliases FROM citation WHERE cited_id IS NULL AND aliases != ''").fetchall():
        ts = {MAP[x.strip()] for x in aliases.split(";") if x.strip() in MAP}
        if len(ts) == 1:
            t = next(iter(ts))
            if t in rowname.get(rowid, ()):
                upd.append((t, rowid))
    db.executemany("UPDATE citation SET cited_id = ? WHERE rowid = ?", upd)
                                     
    db.execute("UPDATE citation SET cited_id = NULL WHERE cited_id = id")
    db.execute("CREATE INDEX IF NOT EXISTS ix_cit_cited ON citation(cited_id)")
    db.execute("DROP VIEW IF EXISTS cited_count")
    db.execute("CREATE VIEW cited_count AS SELECT cited_id AS judgment_id, "
               "COUNT(DISTINCT id) AS n_citing_judgments, COUNT(*) AS n_citations "
               "FROM citation WHERE cited_id IS NOT NULL GROUP BY cited_id")
    db.execute("INSERT OR REPLACE INTO meta VALUES ('citeresolve', ?)",
               ("master5_citeresolve.py 17 Oct 2026: %d keys linked (%s); %d conflicting keys left unlinked; "
                "%d row-level alias links" % (len(MAP), dict(collections.Counter(w[0] for w in why.values())),
                                              len(conflicts), len(upd)),))
    db.commit()
    rep = {"keys_linked": len(MAP), "by_how": dict(collections.Counter(w[0] for w in why.values())),
           "own_key_claimed_twice": own_dup, "conflicts": [[k, w, {a: b for a, b in v.items()}] for k, w, v in conflicts],
           "row_alias_links": len(upd), "files_missing_now": missing}
    if a.report:
        json.dump(rep, io.open(a.report, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print({k: v for k, v in rep.items() if k not in ("own_key_claimed_twice", "conflicts", "files_missing_now")},
          "| files moved since the build:", len(missing),
          "| own keys claimed twice:", len(own_dup), "| conflicts:", len(conflicts))


if __name__ == "__main__":
    main()
