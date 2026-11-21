                       

import re

import nltk


LEADING_PARA_NUM = re.compile(r"(?m)^\s*\d{1,3}\.\s+")

_legal_tokenizer = None

                                                                        
                                                        


LEGAL_ABBREVIATIONS = {
                                                                              
    "v",                                                     
                                                                              
    "no", "nos",                                              
    "para", "paras",                                         
    "s", "ss",                                          
    "r", "rr",                                                         
    "art", "arts",                                       
    "ch",                                            
    "cl", "cls",                                       
    "sch",                                             
    "pt",                                          
    "reg", "regs",                                           
    "p", "pp",                                                    
    "fn",                                             
    "ed", "eds",                                                 
    "vol",                                           
    "app",                                             
                                                                              
    "eg", "ie",                                                             
    "cf",                                  
    "al",                                 
    "ibid", "id",                         
    "op", "cit", "loc",                                
    "et", "seq",                                   
    "supra", "infra",                                 
    "ante", "post",                          
    "viz", "etc",                                       
                                                                              
    "pte", "sdn", "bhd",                                         
    "pty",                                        
    "inc", "corp",                                   
    "ltd", "co",                              
    "plc", "llc", "llp",                            
                                                                              
    "dr", "mr", "mrs", "ms",                        
    "prof", "rev",                              
    "hon", "rt",                                   
    "jr", "sr",                              
    "gen", "col", "sgt",                              
                                                                              
    "j", "cj", "jj",                                                   
    "ja", "aj",                                                           
    "jca", "cja", "acj",                              
    "q", "qc", "kc",                                                       
    "sc", "sjc",                                                  
                                                                              
    "ors", "anor", "anr",                                
    "resp", "applt", "respt",                                           
                                                                              
    "ex", "re",                                     
    "vs",                                         
    "div",                                  
    "dept", "assn", "comm",                                              
    "dist", "crim",                                    
                                                                              
    "n", "c", "d", "f",                                               
    "fig", "govt", "min",                                         
    "approx", "est", "misc",                                                   
    "ref", "acc", "sect",                                                
}


def ensure_nltk():
    
    for pkg in ["punkt", "punkt_tab"]:
        try:
            nltk.data.find(f"tokenizers/{pkg}")
        except LookupError:
            nltk.download(pkg, quiet=True)


def get_legal_tokenizer():
    
    global _legal_tokenizer
    if _legal_tokenizer is not None:
        return _legal_tokenizer

    ensure_nltk()
    tokenizer = nltk.data.load("tokenizers/punkt_tab/english.pickle")
    tokenizer._params.abbrev_types.update(LEGAL_ABBREVIATIONS)
    _legal_tokenizer = tokenizer
    return _legal_tokenizer


                                                                      
                                                                         
_MULTI_PERIOD_ABBREVS = [
    (re.compile(r"\be\.g\.", re.IGNORECASE), "e\u00ADg\u00AD"),
    (re.compile(r"\bi\.e\.", re.IGNORECASE), "i\u00ADe\u00AD"),
    (re.compile(r"\bop\.\s*cit\.", re.IGNORECASE), "op\u00ADcit\u00AD"),
    (re.compile(r"\bloc\.\s*cit\.", re.IGNORECASE), "loc\u00ADcit\u00AD"),
    (re.compile(r"\bet\s+al\.", re.IGNORECASE), "et\u00ADal\u00AD"),
    (re.compile(r"\bet\s+seq\.", re.IGNORECASE), "et\u00ADseq\u00AD"),
]

_RESTORE_MAP = [
    ("e\u00ADg\u00AD", "e.g."),
    ("i\u00ADe\u00AD", "i.e."),
    ("op\u00ADcit\u00AD", "op. cit."),
    ("loc\u00ADcit\u00AD", "loc. cit."),
    ("et\u00ADal\u00AD", "et al."),
    ("et\u00ADseq\u00AD", "et seq."),
]


def legal_sent_tokenize(text: str) -> list:
    
    t = text
    for pattern, replacement in _MULTI_PERIOD_ABBREVS:
        t = pattern.sub(replacement, t)

    tokenizer = get_legal_tokenizer()
    sents = tokenizer.tokenize(t)

    restored = []
    for s in sents:
        for placeholder, original in _RESTORE_MAP:
            s = s.replace(placeholder, original)
        restored.append(s)
    return restored


                                                                                 
                                                                            
                                                                              
                                                       
 
                                                                          


_CITE_BRACKET_N = re.compile(
    r'(\[\s*\d{4}\s*\]\s+(?:\d+\s+)?[A-Z][A-Za-z\s\.\(\)]{1,30}\d+)\.'
)
_CITE_PAREN_N = re.compile(
    r'(\(\d{4}\)\s+\d+\s+[A-Z][A-Za-z\.]+\s+\d+)\.'
)
_CITE_VOL_N = re.compile(
    r'(\b\d{1,4}\s+(?:CLR|ALR|ALJR|FCR|NSWLR|VR|SASR|WAR|FLR|'
    r'AC|WLR|QB|KB|Ch|All\s+ER|SLR|MLJ|HKC|SCR|DLR|OR)\s+\d+)\.'
)
_CITE_PINPOINT_N = re.compile(
    r'(\[\s*\d+\s*\](?:\s*[-\u2013\u2014]\s*\[\s*\d+\s*\])?)\.'
)
_CITE_STAT_N = re.compile(
    r'\b((?:ss?|arts?|cls?|paras?)\s+\d+(?:[A-Z])?'
    r'(?:\s*[-\u2013\u2014]\s*\d+[A-Z]?)?)\.'
)


def prepare_for_punkt(text: str) -> str:
    
    t = LEADING_PARA_NUM.sub('', text)
    for pat, repl in _MULTI_PERIOD_ABBREVS:
        t = pat.sub(repl, t)
    t = _CITE_BRACKET_N.sub(r'\1 ', t)
    t = _CITE_PAREN_N.sub(r'\1 ', t)
    t = _CITE_VOL_N.sub(r'\1 ', t)
    t = _CITE_PINPOINT_N.sub(r'\1 ', t)
    t = _CITE_STAT_N.sub(r'\1 ', t)
    return t
