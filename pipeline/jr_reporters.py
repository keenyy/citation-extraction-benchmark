                       

import re

from jr_reporter_data import (JURI_MAP, JOURNAL_REPORTERS, FALSE_REPORTERS, FORM_RULES)

                                                                         

                                                                     
_ORIGIN = [
                                                                                                 
    (re.compile(r'Case\s+[CT][-‑]\d+/\d+|EU:[CT]:\d{4}:\d+|\bECR\s+I?[-‑]?\s?\d+'
                r'|European\s+Court\s+of\s+Justice|\bECJ\b|Court\s+of\s+Justice', re.I), 'EU'),
                                                                                          
                                                                                               
                                                                                              
                                                                                         
                                 
    (re.compile(r'European\s+Court\s+of\s+Human\s+Rights|European\s+Commission\s+of\s+Human'
                r'\s+Rights|\bECtHR\b|\bEHRR\b|\bStrasbourg\b', re.I), 'ECHR'),
]

                                                                                              
                                                            
_ORIGIN_WINDOW = 90


def _origin(context, at):
    if not context:
        return None
    lo = max(0, at - _ORIGIN_WINDOW)
    hi = min(len(context), at + _ORIGIN_WINDOW)
    near = context[lo:hi]
    for pat, juri in _ORIGIN:
        if pat.search(near):
            return juri
    return None


                                                                         

                                                                                            
                                                               
_JOURNAL_CONTEXT = re.compile(
    r"(?:[A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)?\s*,\s*['\"‘’“”])"
                                                                                      
                                                                                     
                                                                                            
                                                                                            
                                                                                        
                                                                                           
                                                         
    r"|(?:(?<!\bThe )(?<!\bthe )['\"‘’“”][^'\"‘’“”]{8,90}['\"‘’“”]\s*,?\s*$)"
    r"|(?:\b(?:article|note|comment|casenote|editorial)\b\s*,?\s*$)",
    re.I)

                                                                             
                                                                                     
                                                     
                                                              
                                                                
                                                            
                                                                                        
                                                                                       
                                                                                        
                                                                              
                                                                                            
                                                                                          
                                                                                         
                                                                                    
_JOURNAL_HOMONYMS = {'CLJ', 'SLR', 'MLR', 'CRLJ'}
_ALWAYS_JOURNAL = {'LQR', 'CLP', 'JBL'}


def _looks_like_journal(rep_norm, context, at):
    if rep_norm not in _JOURNAL_HOMONYMS or not context:
        return False
    before = context[max(0, at - 120):at]
    return bool(_JOURNAL_CONTEXT.search(before))


                                                                         

                                                          
                                                                                              
                                                                                                 
                                    
_CONTEXT_HOMONYMS = {
    'MLJ':  {'citing_in': ({'SGCA', 'SGHC'}, 'SG'), 'default': 'MY'},
    'MLJU': {'citing_in': ({'SGCA', 'SGHC'}, 'SG'), 'default': 'MY'},
                                                                                    
                                                                                           
                                                                                           
                                                                                          
                                                                              
                                                                                          
                                                                                          
    'OR':   {'citing_in': ({'USSC'}, 'USA'), 'default': 'CAN'},
}


                                                                             
 
                                                                                      
                                                                                                 

                                                                                              
                                                                                             
                                                        
CORRECTIONS = {
                                                                                          
                                                                                       
                                                                                         
                                                                       
    'DR': 'ECHR', 'DANDR': 'ECHR', 'CD': 'ECHR',

                                                                                            
                                                                                            
                                                                                           
                                                                                        
    'R': 'UK',

                                                                                     
                                                       

                                                                  
    'VENTRIS': 'UK', 'VENT': 'UK',

                                                                                 
                                                                                          
                                                                                        
                                                                                       
                                                         
    'INDAPP': 'UK', 'INDIANAPP': 'UK', 'MOOINDAPP': 'UK',

                                                                                       
                                                                                         
                                                                                          
                                                                                        
                
    'FMCA': 'AU', 'FCCA': 'AU', 'FEDCFAMC1A': 'AU', 'FEDCFAMC2G': 'AU',

                                                                                          
                                                                                      
                                                                                           
                                      
    'WN(NSW)': 'AU',

                                                                                            
                                                                                             
                                                                                           
                                                                                    
    'CM': 'CAN',

                                                                                         
                                                                                           
                                                                                             
                                                                                             
                                                                        
    'WL': 'USA',

                                                                                              
                                                                                      
    'VLR': 'AU',

                                                                                           
                                                                                            
                                                                                            
                                                                                               
    'ALT': 'AU',

                                                                                             
                                                                      
    'HLSC': 'UK', 'HLSCOTCH': 'UK',

                                                                                          
                                                                       
    'ER': 'UK', 'ENGREP': 'UK',

                                                                                       
                                                                       
    'DOD': 'UK', 'STR': 'UK', 'TR': 'UK', 'KN': 'UK',

                                                                                             
                                                                                               
                                                                                            
                                                                                           
                                                                                           
    'SHAWSREPORTS': 'UK', 'DUNLOPSREPORTS': 'UK', 'PATON': 'UK', 'RETTIE': 'UK',
    'E&IAPP': 'UK', 'LEACC': 'UK', 'LRIR': 'UK',
                                                                                           
                                                
    'RR': 'UK', 'WMSAUND': 'UK', 'RUSS': 'UK', 'BUTT': 'UK',

                                                                                             
                                                                                           
                                                                                             
                                                                                             
                                                                       
    'EHRR': 'ECHR',                                       
    'EHRRSE': 'ECHR',                          
    'ECHR': 'ECHR',                                                         
    'EUROCTHR': 'ECHR', 'ECTHR': 'ECHR', 'CEDH': 'ECHR',
    'EHRRCD': 'ECHR',                            

                                                                                             
                                                                                             
                                    
    'ICJREPORTS': 'OTHER', 'ICJREP': 'OTHER', 'ICJ': 'OTHER',
                                                                                            
                                                                                           
                                                          
    'IEHC': 'OTHER', 'IECA': 'OTHER', 'IESC': 'OTHER', 'IEHCCOMM': 'OTHER',
}

SUPPLEMENT = {
                                                                                            
                                                                                         
                                                                                        
                                                                                    
                                                                                         
                 
    "JAC&W": "UK",                                             
    "CAR&P": "UK",                                                   
    "JURNS": "UK",                                           
    "ENGR": "UK",                                                              
                                                                             
                                                                                     
                                                                                          
                                                     
    "UKLAWRPCH": "UK", "UKLAWRPKQB": "UK", "UKLAWRPAC": "UK", "UKLAWRPHL": "UK",
    "UKLAWRPCP": "UK", "UKLAWRPEQ": "UK", "UKLAWRPEXCH": "UK", "UKLAWRPPC": "UK",
    "UKLAWRPPRO": "UK", "UKLAWRPADE": "UK", "UKLAWRPCCR": "UK",

                                                                                        
                                                                                               
                                                                           
    'APR': 'CAN', 'NFLDPEIR': 'CAN', 'NSR': 'CAN', 'NBR': 'CAN', 'NFLDR': 'CAN',
    'SASKR': 'CAN', 'ALTALR': 'CAN', 'BCLR': 'CAN', 'CPR': 'CAN', 'RFL': 'CAN',

                                                 
                                                                                             
                                                                                               
                                               
                                                                                      
                                                                   
                                                  
                                                                      
    'ALA': 'USA', 'ALASKA': 'USA', 'ARIZ': 'USA', 'ARK': 'USA', 'CAL': 'USA',
    'CALAPP': 'USA', 'CALRPTR': 'USA', 'COLO': 'USA', 'CONN': 'USA', 'DEL': 'USA',
    'FLA': 'USA', 'GA': 'USA', 'GAAPP': 'USA', 'HAW': 'USA', 'IDAHO': 'USA',
    'ILL': 'USA', 'ILLAPP': 'USA', 'IOWA': 'USA', 'KAN': 'USA', 'KY': 'USA',
    'LA': 'USA', 'ME': 'USA', 'MD': 'USA', 'MASS': 'USA', 'MICH': 'USA',
    'MINN': 'USA', 'MISS': 'USA', 'MO': 'USA', 'MOAPP': 'USA', 'MONT': 'USA',
    'NEB': 'USA', 'NEV': 'USA', 'NH': 'USA', 'NJ': 'USA', 'NJL': 'USA', 'NJEQ': 'USA',
    'NM': 'USA', 'NY': 'USA', 'NYS': 'USA', 'NYSUPP': 'USA', 'NYS2D': 'USA',
    'NC': 'USA', 'ND': 'USA', 'OHIOST': 'USA', 'OHIOAPP': 'USA', 'OHIOABS': 'USA',
    'OKLA': 'USA', 'ORE': 'USA', 'PA': 'USA', 'PASUPER': 'USA', 'RI': 'USA',
    'SD': 'USA', 'TENN': 'USA', 'TEX': 'USA', 'UTAH': 'USA', 'VT': 'USA',
    'VA': 'USA', 'WASH': 'USA', 'WVA': 'USA', 'WIS': 'USA', 'WYO': 'USA',
    'APPDIV': 'USA', 'MISC': 'USA', 'NJSUPER': 'USA', 'PASUPERCT': 'USA',
    'CALAPP2D': 'USA', 'ILLAPP2D': 'USA', 'OHIOST2D': 'USA', 'NYSUPP2D': 'USA',
                                                                                           
                                                                                        
                                                                                             
    'LD': 'USA',
                        
    'NW': 'USA', 'NW2D': 'USA', 'NE': 'USA', 'NE2D': 'USA', 'SW': 'USA', 'SW2D': 'USA',
    'SE': 'USA', 'SE2D': 'USA', 'SO': 'USA', 'SO2D': 'USA', 'ATL': 'USA',
                                                                                         
    'FSUPP': 'USA', 'FRD': 'USA', 'PET': 'USA', 'WHEAT': 'USA', 'CRANCH': 'USA',
    'DALL': 'USA', 'HOW': 'USA', 'BLACK': 'USA', 'WALL': 'USA', 'OTTO': 'USA',

                                                                                    
    'NZEMPC': 'NZ', 'NZACC': 'NZ', 'NZBLC': 'NZ', 'NZTC': 'NZ', 'NZRMA': 'NZ',

                                                                  
    'LGERA': 'AU', 'ALJR': 'AU', 'FLR': 'AU', 'ATPR': 'AU', 'ACLC': 'AU',

                                                                                     
                                               
    'SMCDT': 'SG', 'SGDT': 'SG', 'SGDC': 'SG', 'SGMC': 'SG', 'SGIPOS': 'SG', 'SGPDPC': 'SG',

                                                     
    'NIQB': 'UK', 'NICA': 'UK', 'NICH': 'UK', 'NIFAM': 'UK', 'NIMASTER': 'UK',

                                                                        
    'APPCAS': 'UK', 'LJKB': 'UK', 'LJQB': 'UK', 'LJCH': 'UK', 'LJEX': 'UK',
    'COREP': 'UK', 'CHD': 'UK', 'EX': 'UK', 'EXCH': 'UK', 'BING': 'UK', 'BINGNC': 'UK',
    'ESP': 'UK', 'STARK': 'UK', 'CPD': 'UK', 'MOORENS': 'UK', 'HLC': 'UK', 'BEAV': 'UK',
    'COWP': 'UK', 'VESJUN': 'UK', 'EDEN': 'UK', 'ATK': 'UK', 'CHCAS': 'UK', 'TLR': 'UK',

                                                                                            
                                                     
    'AR': 'CAN', 'CCC': 'CAN', 'OAC': 'CAN', 'MANR': 'CAN', 'BCAC': 'CAN', 'APR': 'CAN',
    'OR': 'CAN', 'ORD': 'CAN', 'NR': 'CAN', 'WWR': 'CAN', 'RJQ': 'CAN', 'QAC': 'CAN',
    'SASKR': 'CAN', 'NFLDPEIR': 'CAN', 'NSR': 'CAN', 'NBR': 'CAN',

                                                 
    'NYS': 'USA', 'NYS2D': 'USA', 'NE': 'USA', 'NE2D': 'USA', 'SW': 'USA', 'SW2D': 'USA',
    'SO': 'USA', 'SO2D': 'USA', 'P2D': 'USA', 'P3D': 'USA', 'CALRPTR': 'USA',

                                                          
    'ACRIMR': 'AU', 'ALD': 'AU', 'BPR': 'AU', 'ATR': 'AU', 'IPR': 'AU', 'ACSR': 'AU',
    'NZAR': 'NZ', 'NZFLR': 'NZ', 'PRNZ': 'NZ', 'CRNZ': 'NZ', 'NZELR': 'NZ',

                                                                                       
                                                                                      
                                                                                   
                                                                                       
     
                                                                                        
                                                          
                                                                     
                                                                
                                                                                       
                                                                                      
                                                                                   
                                                                             
                                                                              
                                                                         
    'AJNO': 'CAN', 'BCJNO': 'CAN', 'MJNO': 'CAN', 'NBJNO': 'CAN', 'NSJNO': 'CAN',
    'NFLDJNO': 'CAN', 'OJNO': 'CAN', 'PEIJNO': 'CAN', 'QJNO': 'CAN', 'JQNO': 'CAN',
    'SJNO': 'CAN', 'YJNO': 'CAN', 'NWTJNO': 'CAN', 'NUJNO': 'CAN', 'FCJNO': 'CAN',
    'IADDNO': 'CAN', 'TCJNO': 'CAN', 'CHRDNO': 'CAN', 'ACWSNO': 'CAN', 'WCBNO': 'CAN',

                                                                                     
                                                                                       
                                                                                        
                                                                                         
                                                                     
                                                                                          
                                                                                         
                                                                                    
                                                                                         
                                                                        
    'MVR': 'CAN', 'CPC': 'CAN', 'NFLD&PEIR': 'CAN', 'CBR': 'CAN', 'CRR': 'CAN',

                                                                                         
                                                                      
    'QCCA': 'CAN', 'QCCS': 'CAN', 'QCCQ': 'CAN', 'QCTDP': 'CAN',
    'NSCA': 'CAN', 'NSSC': 'CAN', 'NSPC': 'CAN',
    'NBCA': 'CAN', 'NBKB': 'CAN', 'NBQB': 'CAN', 'NBPC': 'CAN',
    'ABKB': 'CAN', 'ABPC': 'CAN', 'ABCJ': 'CAN',
    'SKKB': 'CAN', 'SKPC': 'CAN', 'MBKB': 'CAN', 'MBPC': 'CAN',
    'PESCAD': 'CAN', 'PESCTD': 'CAN', 'PESC': 'CAN', 'PECA': 'CAN',
    'NLCA': 'CAN', 'NLSC': 'CAN', 'NLTD': 'CAN',
    'NUCA': 'CAN', 'NUCJ': 'CAN', 'NWTCA': 'CAN', 'NWTSC': 'CAN',
    'YKCA': 'CAN', 'YKSC': 'CAN', 'YKTC': 'CAN',
    'ONSCDC': 'CAN', 'ONCJ': 'CAN', 'ONWSIAT': 'CAN',
    'HRTO': 'CAN', 'CHRT': 'CAN', 'CMAC': 'CAN', 'TCC': 'CAN',

                                                                                                
                                                                                                 
                                                                                          
                                                                                           
                                                                                            
                                                                        
                                                                                  
    'FEDAPPX': 'USA', 'FAPPX': 'USA', 'NLRB': 'USA', 'MJ': 'USA', 'JOHNSCAS': 'USA',
    'ILR': 'OTHER',
                                                                                              
                                                                                            
                                                                                            
                                                                                        
                                                                                              
                                                                                                  
                                                                                   
                                                                                     
    'S&D': 'UK', 'WS': 'UK', 'W&S': 'UK', 'BELLSAP': 'UK', 'BELLSAPC': 'UK', 'BELLAPP': 'UK',
    'BELLSAPP': 'UK', 'MACQAPP': 'UK', 'MACQAPPC': 'UK', 'MACQAP': 'UK', 'MACQREP': 'UK',
    'ROBAP': 'UK', 'ROBAPP': 'UK', 'SHAWSAPPCAS': 'UK', 'SHAWAPP': 'UK', 'PATONAPPCA': 'UK',
    'PATONAPP': 'UK', 'SH&ML': 'UK', 'MYL&CR': 'UK', 'AD&ELL': 'UK', 'ADOLPH&ELLIS': 'UK',
    'ROLLREP': 'UK', 'PWMS': 'UK', 'H&M': 'UK', 'QUEENSBENCHREPORTS': 'UK', 'QUEENSBENCH': 'UK',
    'COMMONBENCH': 'UK', 'EXCHEQUER': 'UK', 'TERMREPORTS': 'UK', 'VERNON': 'UK', 'SALKELD': 'UK',
    'MADDOCKS': 'UK', 'DEGEX&SM': 'UK', 'SOLJ': 'UK', 'WR': 'UK',
                                                                                   
    'OHIO': 'USA',
                                                    
    'FCAS': 'USA',
                                                                                             
    'HL': 'UK',
                                                                                                
                                                                                 
    'SHAWANDDUNLOP': 'UK', 'SHAWANDBALLANTINE': 'UK', 'SHAWANDMACLEAN': 'UK',
    'WILSONANDSHAW': 'UK', 'DOWANDCLARK': 'UK', 'ELLISANDBLACKBURN': 'UK', 'ELLISANDELLIS': 'UK',
    'ADOLPHUSANDELLIS': 'UK', 'BARNWALLANDADOLPHUS': 'UK', 'BARNEWALLANDADOLPHUS': 'UK',
    'BARNWALLANDALDERSON': 'UK', 'BARNEWALLANDALDERSON': 'UK', 'BARNWALLANDCRESSWELL': 'UK',
    'BARNEWALLANDCRESSWELL': 'UK', 'VESANDB': 'UK', 'VESANDBEA': 'UK', 'MEESONANDWELSBY': 'UK',
    'CLARKANDFINNELLY': 'UK', 'MYLNEANDCRAIG': 'UK', 'MYLNEANDKEEN': 'UK', 'MAULEANDSELWYN': 'UK',
    'CARRINGTONANDPAYNE': 'UK', 'BESTANDSMITH': 'UK', 'HURLSTONEANDNORMAN': 'UK',
    'HURLSTONEANDCOLTMAN': 'UK', 'RUSSELLANDMYLNE': 'UK', 'DEGEXANDSMALE': 'UK',
    'MANNINGANDGRANGER': 'UK', 'SCHOALESANDLEFROY': 'UK', 'BALLANDBEATTY': 'UK',
                                                                                                    
                                                                                                  
                                                                                                    
                                                                                                 
                                                                                      
                                                                                                   
                                                                                              
                                                                                          
                                                                                                       
    'APPCA': 'UK', 'BELLSAPPC': 'UK', 'BELLSAPPCA': 'UK', 'BINGHAMSNEWCASES': 'UK', 'CHANDIV': 'UK',
    'F(HL)': 'UK', 'MACQUEEN': 'UK', 'MER': 'UK', 'MURR': 'UK', 'PRICE': 'UK', 'RAILCAS': 'UK',
    'RAILWAYCA': 'UK', 'RAILWAYCAS': 'UK', 'RIDGPC': 'UK', 'ROBAPPC': 'UK', 'ROSSLC': 'UK',
    'SCH&LEF': 'UK', 'SCHLEF': 'UK', 'SHAPPCA': 'UK', 'VESJUNR': 'UK', 'VESSENR': 'UK', 'VESEY': 'UK',
                                                                                                            
                                                                                                      
                                                                                                       
                                                                                                              
                                                                                                                
                                                                
    'CLA&FINN': 'UK', 'CLAR&FINN': 'UK', 'CLA&FIN': 'UK', 'CL&FINN': 'UK', 'CLAANDFIN': 'UK', 'CLAANDFINN': 'UK',
    'ADANDEL': 'UK', 'ADANDELL': 'UK', 'CARANDP': 'UK', 'CARANDKIR': 'UK', 'MYLANDK': 'UK', 'MYLANDCR': 'UK',
    'MYL&CRAIG': 'UK', 'MANN&GR': 'UK', 'MAC&GORD': 'UK', 'KAY&JOHNSON': 'UK', 'RAILCA': 'UK', 'ROLL': 'UK',
    'CAMPREP': 'UK', 'MADDOX': 'UK', 'QBREP': 'UK', 'WBL': 'UK', 'CHANAPP': 'UK', 'PATONAP': 'UK',
    'NEWSER': 'UK',
}


def _prefix_rule(rep_norm):
    for prefix in ('EWCA', 'EWHC', 'UKFTT', 'UKUT', 'UKIAT', 'UKAIACT', 'NICA', 'NIQB', 'NICH'):
        if rep_norm.startswith(prefix):
            return 'UK'
    if rep_norm.startswith('OJ'):
        return 'CAN'
                                                                                     
                                                                                     
                                                                                         
                                                                                          
    if rep_norm.startswith('CARSWELL'):
        return 'CAN'
    return None


                                                                              

_external = None


def set_external_resolver(fn):
    
    global _external
    _external = fn


                                                                                            
                                                                                             
                                                                                           
_SERIES = re.compile(r'\s*\(\s*\d+\s*[a-z]{1,2}\s*\)\s*$', re.I)

                                                                                          
                                                                                              
                                                                            
                                                  
                                                                   
                                                                                            
                                           
_PERIODICAL = re.compile(
    r'(?:'
    r'(?:L|LAW|POLSCI|SCI|SOC|ECON|PHIL|CRIM|BUS|TAX|INTL|COMP|MED|ENV)?'
    r'(?:REV|REVIEW|JRNL|JOURNAL|QUARTERLY|YEARBOOK|YB|LAWYER|PSYCH|EDUCATION)$'
                                                                                          
                                                                                         
                                                          
    r'|^.{2,}LJ$'
                                                                         
    r'|^J[A-Z&]{3,}'
                                                                                            
                                                                                          
                                                                                           
                                                                                          
                                                                                  
    r'|(?:LAWRW|LAWRV|LAWREV|LAWJL|LREV)$'
    r')')


                                                                                        
                                                                                         
                                                                                   
_SERIES_SUFFIX = re.compile(r'\s*\([A-Za-z][A-Za-z. ]{0,8}\)\s*$')


def _norm(rep):
    r = str(rep or '').replace('\xa0', ' ').upper().strip()
    r = re.sub(r'\s+', ' ', r)
    r = re.sub(r'\.\s*\d+\s*$', '', r).strip()                                
    r = _SERIES.sub('', r).strip()                                               
                                                                                        
                                                                                             
                                                        
    return r, r.replace('.', '').replace(' ', '').replace("'", '').replace('’', '').replace('`', '')


                                                                          
 
                                                             
                                                                     
                                                                      
                                                                                
                                                                                      
                                        
_COURT_WORD = re.compile(r"(?i)\b(?:court|tribunal|commission)\b")

_COURT_PLACE = [
    ("AU", r"australia|australian|new\s+south\s+wales|queensland|victoria|"
           r"south\s+australia|western\s+australia|tasmania|northern\s+territory|"
           r"australian\s+capital\s+territory|\bNSW\b|\bQld\b|\bVic\b|\bWA\b|\bSA\b|\bTas\b|\bNT\b|\bACT\b"),
    ("NZ", r"new\s+zealand"),
    ("SG", r"singapore"),
    ("MY", r"malaysia|malaya"),
    ("HK", r"hong\s+kong"),
    ("IND", r"\bindia\b"),
    ("CAN", r"canada|ontario|quebec|british\s+columbia|alberta|manitoba|saskatchewan|"
            r"nova\s+scotia|new\s+brunswick|newfoundland|prince\s+edward"),
    ("USA", r"united\s+states|\bU\.?S\.?\b|supreme\s+court\s+of\s+the\s+united\s+states"),
    ("UK", r"england|wales|scotland|northern\s+ireland|united\s+kingdom|house\s+of\s+lords|"
           r"privy\s+council|\bEWCA\b|\bEWHC\b"),
]
_COURT_PLACE_RE = [(j, re.compile(p, re.I)) for j, p in _COURT_PLACE]


                                                                                              
_CD_ON = __import__("os").environ.get("JR_CIT_DATE", "1") != "0"
_CD_COURT_RE = (
    ("ECHR", re.compile(r"European[ ]Court[ ]of[ ]Human[ ]Rights|Eur\.?[ ]?Court[ ]?H\.?[ ]?R|ECtHR")),
    ("UK", re.compile(r"\bCourt[ ]of[ ]Session\b|\bHigh[ ]Court[ ]of[ ]Justiciary\b|\bEWCA\b|\bEWHC\b")),
)


def _court_name_jurisdiction(name):
    
    s = " ".join(str(name or "").split())
    if not s:
        return None
    for juri, rx in _COURT_PLACE_RE:
        if rx.search(s):
            return juri
    return None


                                                                                
                                                                               
                                                                              
                                                                       
                                                                                   
                                                                             
                                                
                                                                                    
                                                                                     
                                                                        
_NOT_LAW_REPORTS = frozenset({
    'UNTS', 'SH', 'SI',
                                                                            
                                                                                   
                                                                                
                                                                         
    'ATS', 'AIRACTS', 'AIR(ACTS)', 'AIR (ACTS)', 'USC', 'OJ', 'CFR', 'STAT',
    'HCATRANS',
    'FAMLAW', 'ALJ', 'PUBLICLAW', 'CURRENTLEGALPROBLEMS', 'CONV', 'CONVEYANCER',
    'LAWTEACHER', 'RESJUDICATAE', 'CLJ', 'INTJREFUGEELAW',
    'ACWSJ', 'NSWLEXIS', 'WLUK', 'LEXISCITATION',
                                                                                          
                                                                                    
                                                                                    
                                                
                                                                              
                                                                    
                                                                                         
                                                                                         
                                                                                      
                                                                                      
                                    
    'COLITT',
})


                                                                                         
                                                                                             
                                                                                           
                                                                                             
                               
 
                                                                                             
                                                                                       
                                                                                        
                                                    
                                                                                      
                                                                            
 
                                                                                          
                                                                                         
                                                                                         
                                                                                        
                                                                                       
                                                  
 
                                                                                       
                                                                                          
                                                                                          
                                                                                      
                           
 
                                                
                                                                     
                                                                    
                                                                                         
                                                                                      
                                                                                      
_DATABASE_TAG = frozenset({
                                                                                        
                                                                                       
                                                                                           
                                                                                
                                                                                           
                                                                                           
                                                                                              
                                                                                          
                                                                                               
                                                                            
                                                                                   
                                                                              
                       
                                                                                          
                                                                                           
                                                                                  
})


def is_database_tag(rep):
    
                                                                                          
                                                                                        
                                                
    return _norm(rep)[0] in _DATABASE_TAG



                                                                                    
_CITING_COURT_JURI = {
    'UK': 'UK', 'UKSC': 'UK', 'HL': 'UK', 'UK_HL_1996-2009': 'UK', 'HL_1709-2009': 'UK',
    'UKHL': 'UK',                                                                                      
    'SGHCF': 'SG', 'SGHCR': 'SG', 'SGHC(A)': 'SG', 'SGHC(I)': 'SG', 'SGCA(I)': 'SG',
    'HCA': 'AU', 'AU': 'AU',
    'SGCA': 'SG', 'SGHC': 'SG', 'SG': 'SG',
    'NZSC': 'NZ', 'NZCA': 'NZ', 'NZHC': 'NZ', 'NZ': 'NZ',
                                                                                                  
                                                                                             
                                                                                                
    'HKCFA': 'HK',
                                                                                                      
                                                                                                
    'MYFC': 'MY',
    'SCC': 'CAN', 'CA': 'CAN', 'CAN': 'CAN',
    'USSC': 'USA', 'USA': 'USA', 'US': 'USA',
}


                                                                                  
                                                                                     
                                                                                      
                                      
_SELF_IDENTIFYING = frozenset({
    'UKHL', 'UKSC', 'UKPC', 'EWCA', 'EWHC', 'EWCACIV', 'EWCACRIM', 'CSIH', 'CSOH',
    'HCA', 'FCA', 'FCAFC', 'FCCA', 'FMCA', 'NSWCA', 'NSWSC', 'VSCA', 'VSC', 'QCA',
    'QSC', 'WASCA', 'WASC', 'SASC', 'TASSC', 'NTSC', 'ACTSC',
    'SGCA', 'SGHC', 'SGDC', 'SGMC', 'SGHCF', 'SGHCR',
    'NZSC', 'NZCA', 'NZHC', 'NZDC', 'NZEMPC',
    'SCC', 'CANLII', 'ONCA', 'ONSC', 'BCCA', 'BCSC', 'ABCA', 'QCCA',
})


                                                                                         
                                                                                            
                                                     
_ACAD_CACHE = None


def _is_academic_abbrev(rn):
    
    global _ACAD_CACHE
    if _ACAD_CACHE is None:
        try:
            import re as _re
            import jr_academic as _A
            _ACAD_CACHE = {_re.sub(r"[^A-Z0-9]", "", str(k).upper())
                           for k in _A.CARDIFF_ACAD_ABBREVS}
        except Exception:                                     
            _ACAD_CACHE = set()
    return rn in _ACAD_CACHE


                                                                                          
                                                                                                   
                                                                                                  
                                        

                                                                                                    
                                                                                                   
                                                                                                  
                                                                                                
                                                                                                   
                                                                         
                                                                                                
                                                                                            
                                                                                                    
                                                                                                    
                                                                         
                                                                                                
                                                                                               
                                                                                              
                   
_CASE_NAME_REPORTS = {'CRIMLR': 'UK', 'ALJ': 'AU', 'CLJ': 'MY', 'RLR': 'UK', 'ILM': 'OTHER'}
_CASE_NAME_BEFORE = re.compile(
    r"(?:\b[A-Z][\w'’.&-]*(?:[ \t]+[\w'’.&()-]+){0,7}[ \t]+v\.?[ \t]+[A-Z(][^\"“”‘;:\n]{0,90}"
    r"|\b(?:Re|In[ \t]+re|Ex[ \t]+parte)[ \t]+[A-Z][^\"“”‘;:\n]{0,60})$")


def _case_name_before(context, at):
    
    before = context[max(0, at - 170):at]
    before = re.sub(r"[\s,(\[]+$", "", before)
    before = re.sub(r"[ \t]*\(?\d{1,3}\)?$", "", before) if re.search(r"[A-Za-z.]\(?\d{1,3}\)?$", before) else before
    return bool(_CASE_NAME_BEFORE.search(before))


                                                                                            
                                                                                              
                                                                                                  
                                                                                                 
                                                                                       
                                                                                         
_JOURNALS_20261013 = frozenset({
    'NJCL', 'CFLQ', 'RJT', 'RJTUM', 'RGD', 'ADVQ', 'CJCCJ', 'LEGALTHEORY', 'NZULR', 'NZJPIL',
    'TRUSTS&TRUSTEES', 'CJLS', 'CLQ', 'LAW&CONTEMPPROB', 'CPDUN', 'REVTRIMDRH', 'CJWL',
    'RDUB', 'CLELJ', 'SCIENCE',
})

                                                                                                
                                                                                                  
                                                                                               
                                                                                               
_NOT_CASES_20261013 = frozenset({
    'GO', 'GOII', 'OGII', 'GOI', 'OGI', 'CMND', 'CMD', 'LNTSER', 'LNTS', 'EWLC',
                                                                             
    'NZSCTRANS',
})
                                                                                                    
                                                                                               
                                              
_STATUTE_SERIES = frozenset({'SO', 'SC', 'SA', 'SBC', 'SM', 'SNB', 'SNS', 'SQ', 'SS', 'SNL', 'SPEI',
                             'RSO', 'RSC', 'RSA', 'RSBC', 'RSQ', 'LQ', 'LRQ'})
_YEAR_SERIES_YEAR = re.compile(r"(\d{4}),?[ \t]+[A-Z][A-Z.() ]{0,12}?,?[ \t]+(\d{4})\b")

_UK_COURTS = frozenset({'UK', 'UKHL', 'UKSC', 'HL', 'UK_HL_1996-2009', 'HL_1709-2009', 'UKPC'})
_SG_MY_COURTS = frozenset({'SGCA', 'SGHC', 'SG', 'MY'})


def _is_uk_court(citing_court):
    c = str(citing_court or '').upper()
    return c in _UK_COURTS or c.startswith(('UK', 'HL'))


def _rules_20261013(rep, rn, form, context, at, citing_court):
    
    cc = str(citing_court or '').upper()
    if rn in _CASE_NAME_REPORTS:
        if context is not None and at is not None and _case_name_before(context, at):
            return True, _CASE_NAME_REPORTS[rn]
        return True, None
    if rn in _JOURNALS_20261013 or rn in _NOT_CASES_20261013:
        return True, None
                                                                                               
                                                                                               
                                                                                                    
    if rn == 'SCLR' and (cc in ('SCC', 'CAN', 'CA') or re.search(r"\(\s*\d\s*[a-z]{1,2}\s*\)", str(rep))):
        return True, None
                                                                                            
    if rn == 'MLR' and cc not in _SG_MY_COURTS:
        return True, None
                                                                                          
                                                                                               
    if rn == 'APR' and str(rep).strip() in ('Apr', 'Apr.'):
        return True, None
                                                                                                  
                                                                                     
    if rn == 'APP' and cc in ('USSC', 'USA', 'US'):
        return True, None
                                                                                              
                                                                                              
    if rn == 'NLRB' and context is not None and at is not None and re.match(
            r"\d{1,3}[ \t]+N\.[ \t]?L\.[ \t]?R\.[ \t]?B\.[ \t]+\d{1,4}[-–]\d", context[at:at + 40]):
        return True, None
    if form == 'bare_rep' and rn in _STATUTE_SERIES and context is not None and at is not None:
        m = _YEAR_SERIES_YEAR.match(context[at:at + 40])
        if m and m.group(1) == m.group(2):
            return True, None
                                                                                                
                                                                                               
                                                                         
    if form == 'nominate' and rn in ('S', 'D', 'M') and _is_uk_court(citing_court):
        return True, 'UK'
    return False, None


                                                                                          
                                                                                                
                                                                                                
                                                                                   

                                                                         
                                                                                             
                                                                                                  
                                                                                                  
                                                                                                
                                                                                                    
_NOT_CASES_20261014 = frozenset({
    'EST&TRQ', 'WOMENSRTSLREP', 'MEDSCI&L', 'TRADEMARKREP', 'TAXNOTES', 'LABLAW', 'LAW&HUMBEHAV',
    'RDUS', 'BYIL', 'CLF', 'FEDSENTENCINGREP', 'CANADAGAZETTE', 'DCREG', 'OJL', 'OJC', 'CM',
    'COINST', 'STAIR', 'HUME',
                                                                              
    'IS',
                                                                                                        
                                  
    'UNGARES', 'GARES', 'UNSCRES', 'SCRES', 'UNGAOR', 'GAOR',
})
                                                                                           
                                                                               
                                                                                                         
                                                                               
                                                                                 
                                                                                 
_NAME_GATED_20261014 = frozenset({'AMSTREP', 'AMLR', 'ALRFED', 'ILJ', 'CRLR'})
_MONTHS_14 = (r"(?:January|February|March|April|May|June|July|August|September|October|November|"
              r"December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)\.?")
                                                                                             
                                                                                                    
_DATE_BEFORE_YEAR = re.compile(
    r"(?:\b\d{1,2}(?:st|nd|rd|th)?[ ]" + _MONTHS_14 + r"|\b" + _MONTHS_14 + r"[ ]\d{1,2},)[ ]$")
                                                                                       
                                                                                                 
                                                                                                  
_PRACTICE_BEFORE = re.compile(
                                                                                                
                                                                                                 
                                                                                             
                                                                                                        
    r"(?:\bPractice[ ](?:Statement|Direction|Note)s?\b(?:[ ]No\.?[ ]\d{1,3})?"
                                                                                                         
                                                                                                  
    r"(?:[ ]?[–—-][ ]?(?:[A-Z][A-Za-z’']*[ ]?){1,6})?"
    r"|\bCircular[ ]No\.?[ ]\d{1,3}[ ]of[ ]\d{4})"
                                                                                         
                                                                                                            
                                                                                                             
    r"[ ]?,?[ ]?(?:\((?:[^()]|\([^()]{0,20}\)){0,110}\))?[ ]?,?[ ]?(?:reported[ ]in[ ])?\(?[ ]?(?:[\[(](?:1[5-9]|20)\d{2}[\])][ ]?)?$")
                                                                                                         
                                                                                                              
_PRACTICE_REPORTS = re.compile(r"\[2007\][ ]3[ ]NZLR[ ]297\b")
_ANNOTATION_BEFORE = re.compile(r"\b[Aa]nnotation\b(?:(?![ ]v\.?[ ])[^.;]){0,60}$")
                                                                                              
                                                                                               
                                                                                                          
_PRACTICE_WORDS_BEFORE = re.compile(
    r"(?:\bPractice[ ](?:Statement|Direction|Note)s?|\bGuidelines[ ]issued[ ]by[ ]the[ ]Attorney[- ]General)"
    r"(?:[ ](?!(?:in|see|re|ex|cf|v)\b)(?:[a-z]+|\d+|Judicial|Precedent|House|Lords|Court|Appeal|Lord|Chief"
    r"|Justice|January|February|March|April|May|June|July|August|September|October|November|December),?){0,12}"
    r"(?:[ ]in[ ](?:January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{4})?"
    r"[ ]\(?[ ]?(?:[\[(](?:1[5-9]|20)\d{2}[\])][ ]?)?$")
                                                                                                
                                                           
_OSC_INSTRUMENT_BEFORE = re.compile(
    r"\b(?:National[ ](?:Instrument|Policy)|(?:CSA[ ]|OSC[ ])?(?:Staff[ ])?Notice|Multilateral[ ]Instrument"
    r"|Companion[ ]Policy|OSC[ ]Rule)[ ]\d{2}[-‐‑–]\d{3}(?:(?![ ]v\.?[ ])[^;]){0,170}$")
_US_STATES_14 = frozenset(
    "Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware Florida Georgia Hawaii "
    "Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan "
    "Minnesota Mississippi Missouri Montana Nebraska Nevada Ohio Oklahoma Oregon Pennsylvania "
    "Tennessee Texas Utah Vermont Virginia Washington Wisconsin Wyoming".split())


def _rules_20261014(rep, rn, form, context, at, citing_court):
    
    cc = str(citing_court or '').upper()
    raw = str(rep or '').strip()
    if rn in _NOT_CASES_20261014:
        return True, None
                                                                                                 
                                                                                                  
                                                                                                    
                                             
    if re.search(r"[A-Z][a-z]+\.?,?\sv\.?\s[A-Z][a-z]", raw) or re.search(r"\spp?\.?$", raw):
        return True, None
                                                                                                
                                                         
    if rn == 'ALL' and form == 'nominate':
        return True, None
                                                                                      
                                                                                                          
    if rn.endswith('ACT') and (len(rn) > 3 or form == 'nominate'):
        return True, None
                                                                                                 
                                                                                               
    if raw in ('Tr.', 'Tr', 'Cf.', 'Cf', 'Sec.', 'Sec'):
        return True, None
                                                                                                 
                                                                             
    if rn == 'OS' and (cc.startswith('SG') or cc in ('USSC', 'USA', 'US')):
        return True, None
                                                                                          
    if form == 'round' and raw in _US_STATES_14 and context is not None and at is not None and re.match(
            r"\((?:19|20)\d{2}\)\s+[A-Z][a-z]+\s+(?:19|20)\d{2}\b", context[at:at + 40]):
        return True, None
                                                                                                  
                                                                
    if rn == 'BPR' and cc in ('USSC', 'USA', 'US'):
        return True, None
    if context is None or at is None:
        return False, None
    before = " ".join(context[max(0, at - 200):at].split()) + " "
    after = " ".join(context[at:at + 60].split())
    if rn in _NAME_GATED_20261014 and not _case_name_before(context, at):
        return True, None
                                                                                                   
                                                                                                    
    if rn == 'PRICE' and form == 'nominate' and not _case_name_before(context, at):
        return True, None
    if _PRACTICE_BEFORE.search(before) or _ANNOTATION_BEFORE.search(before) \
            or _PRACTICE_WORDS_BEFORE.search(before) \
            or (rn == 'NZLR' and _PRACTICE_REPORTS.search(" ".join(context[max(0, at - 7):at + 20].split()))):
        return True, None
                                                                                                
                                     
    if rn == 'HOWSTTR' and re.search(r"\bRemarks[ ]upon\b[^;]{0,50}$", before):
        return True, None
                                                                                                    
                                                                                        
    if rn == 'BELL' and form == 'nominate' and not _case_name_before(context, at):
        return True, None
                                                               
                                                                      
                                                                          
                                                                                                  
    if re.match(r"\d{1,3}[ ]A\.[ ]\d[ ]R\.[ ]\d{1,2}[ ]P\.", after) \
            or re.search(r"\bTable[ ]$", before) \
            or re.search(r"\b\d{1,2}[ ](?:Car|Hen|Geo|Eliz|Jac|Will|Vict|Edw|Ric|Rich|Anne)[.:]?[ ]$", before):
        return True, None
    if rn == 'OSCB' and _OSC_INSTRUMENT_BEFORE.search(before):
        return True, None
                                                                                       
                                                                                            
                                           
                                                                                           
                                                                                                
    if rn.startswith('ICC') and re.search(
            r"(?:\bIn[ ]re[ ](?:[Tt]he[ ])?(?:(?![ ]v\.?[ ])[^,;.]){0,60}\b(?:Amendment|Act|Regulations?|Rules?)"
            r"|\b[A-Z][a-z]+[ ]of[ ](?:(?![ ]v\.?[ ])[^,;.]){0,60}\b(?:Regulations|Rules)),[ ]$", before):
        return True, None
                                                                                                 
                                                                                         
    if form == 'bare_rep' and rn in ('SCR', 'OS', 'PC') and _DATE_BEFORE_YEAR.search(before):
        return True, None
                                                                          
    if re.match(r"\d{1,2}[ ][A-Z][a-z]{2,5}\.[ ]\d[ ]?,?[ ]?c\.[ ]?\d", after):
        return True, None
                                                                                             
                                                                                                          
                                                                                                 
                                                                                            
    if rn == 'WL':
        num = re.match(r"(?:19|20)\d{2}[ ]WL[ ]\d{4,9}", after)
        n_ = re.escape(num.group(0)).replace(r"\ ", r"\s+") if num else None
        if re.search(r"Opp?\.[ ]?Att'?y\.?[ ]?Gen\.[^;]{0,40}$", before) \
                or re.match(r"[^()\n]{0,40}\(OLC\b", after) \
                or (n_ and re.search(r"Opp?\.\s?Att'?y\.?\s?Gen\.[^;\n]{0,40}" + n_ + "|" + n_ + r"[^()\n]{0,40}\(OLC\b", context)):
            return True, None
    return False, None


                                                                                              
                                                                                            
                                                                                             
                                                                                              
                                                                                              
                                                                                              
                                             
                                                                                              
                                                                                              
                                       
                                                                        
                                                                                              
                                                                                                           
                                                                                                       
                                                             
                                                                                                   
                                                                                                 
                                                          
                                                                                                 
                                         
                                                                                                 
                                                            
                                                                                                     
                                                                                       
                                                           
                                                                           
                                                                                      
                                            
_CITREP_20261014 = {
    'SALK': 'UK', 'HARE': 'UK', 'HA': 'UK', 'FREEM': 'UK', 'HBL': 'UK', 'ESPNPR': 'UK',
    'ESPREP': 'UK', 'ROABR': 'UK', 'S&ST': 'UK',
    'VCS': 'UK', 'CC': 'UK', 'CP': 'UK', 'ENGAP': 'UK', 'APPC': 'UK', 'LRHL': 'UK',
    'APPEALCAES': 'UK', 'LTREP': 'UK', 'MOOPCCNS': 'UK', 'MOORESPRCR': 'UK', 'PLOWDEN': 'UK',
    'CROELIZ': 'UK', 'COKESREPORTS': 'UK', 'LLOYDSREPORTS': 'UK', 'LLOYDSPRIZECASES': 'UK',

    'SECSER': 'UK', 'SCOTLAWREP': 'UK', 'SH&MAC': 'UK', 'SH&MLE': 'UK', 'BELLSAPPEALS': 'UK',
    'RHL': 'UK',
    'BALL&B': 'OTHER', 'DR&WAR': 'OTHER', 'IRJUR': 'OTHER', 'IRISHLR': 'OTHER',
    'IA': 'UK', 'LAH': 'IND',
    'JOHNS': 'USA', 'GRATT': 'USA', 'MCMULLAN': 'USA', 'METCALF': 'USA', 'RCHARLTON': 'USA',
    'FEDCAS': 'USA', 'MEDLRPTR': 'USA', 'UCCREP': 'USA', 'NER': 'USA', 'NAVR': 'USA',
    'WCB2D': 'CAN', 'WCB': 'CAN', 'MBHR': 'CAN', 'NWTTC': 'CAN', 'BCWLDNO': 'CAN', 'OLRDNO': 'CAN',
    'SCJNO': 'CAN',
    'NZCONVC': 'NZ',
                                                                                                
                                                                                         
                                                                                                   
                                                                                                                   
    'NSWLR(EQ)': 'AU', 'SR(NSW)': 'AU', 'SR,NSW': 'AU', 'CH,D': 'UK',
    'LJ(CH)': 'UK', 'LJ(KB)': 'UK', 'LJ(QB)': 'UK', 'LJ(EX)': 'UK', 'LJ(CP)': 'UK', 'LJ(PC)': 'UK',
    'LJ(BCY)': 'UK', 'LJ(EQ)': 'UK', 'LJ,QB': 'UK', 'LJ,KB': 'UK', 'LJ,CP': 'UK', 'LJ,CH': 'UK', 'LJ,EX': 'UK',
    'R(HL)': 'UK', 'R(CTOFSESS)': 'UK', 'S,D,&B': 'UK', 'BELL,APC': 'UK', 'HOFLCA': 'UK', 'MOORE,PC': 'UK',
    'SESSCA2DSERIES': 'UK', 'SESSCA,2DSERIES': 'UK', 'SESSCA3DSERIES': 'UK', 'SESSCA,3DSERIES': 'UK',
    'SESSCA4THSERIES': 'UK', 'SESSCA,4THSERIES': 'UK', 'COURTSESSCAS,2DSER': 'UK',
    'COURTSESSCAS,3DSER': 'UK', 'COURTSESSCAS,4THSER': 'UK',
    'FEDREP,2NDSERIES': 'USA', 'PAIGE(NEWYORK)': 'USA',
}
import os as _os_cr
if _os_cr.environ.get("ZF_NO_CITREP") != "1":
    for _k, _v in _CITREP_20261014.items():
        SUPPLEMENT.setdefault(_k, _v)
                                                                                                     
                                                                      
    SUPPLEMENT.setdefault('ROLLR', 'UK')
    SUPPLEMENT.setdefault('ROLLREP', 'UK')


def _classify_base(rep, form=None, context=None, at=None, citing_court=None):
    
                                                                                     
                                                                                    
                                                                                        
                                                               
    rep = str(rep or '').replace('’', "'")
                                                                                          
                                                                                               
                                                                                                  
                                                                                                  
                                                                                                
                                        
    if _CD_ON and form in ('cd', 'cd_court', 'unreported_au'):
        if form == 'unreported_au':
            j = classify(rep, form=None, context=context, at=at, citing_court=citing_court)
            if j is not None:
                return j
            words = rep
        else:
            words = rep.split(':', 1)[1] if ':' in rep else ''
        if words:
            for juri, rx in _CD_COURT_RE:
                if rx.search(words):
                    return juri
            j = _court_name_jurisdiction(words)
            if j:
                return j
            tok = re.sub(r"[^A-Za-z]", "", words.split()[0]).upper() if words.split() else ''
            if tok in _SELF_IDENTIFYING:
                return classify(tok, form='bracket', context='', at=0, citing_court=citing_court)
        return _CITING_COURT_JURI.get(str(citing_court or '').upper(), 'OTHER')
    rc, rn = _norm(rep)
    if not rn:
        return None

                                                                      
                                                                                           
                                                                                          
                                                                                           
                                                                                           
    if form == 'unreported_bare':
        j = _court_name_jurisdiction(rep)
        if j:
            return j
        return _CITING_COURT_JURI.get(str(citing_court or '').upper())

                                
     
                                                                                            
                                                                                         
                                                                                          
                                                                                     
                                                                                   
                                                                                     
                                                                                     
                                                                                         
     
                                                                                           
                                                                                             
                                                                                          
                                                                                       
                                                                                       
    _done, _ans = _rules_20261014(rep, rn, form, context, at, citing_court)
    if _done:
        return _ans

    if rn in FALSE_REPORTERS:
        _fr = FORM_RULES.get(rn)
        if _fr and form in _fr:
            return _fr[form]
        return None

                                                                                               
                                                              
    _done, _ans = _rules_20261013(rep, rn, form, context, at, citing_court)
    if _done:
        return _ans

                                                                                        
                                                                                         
                                                                                             
                                                                                             
                                                  
     
                                                                                          
                                                                                            
                                                                                         
                                                                                        
                                                                         
                                                                                               
                                                                                             
                                                                                            
                                                                                        
    if (rn not in JURI_MAP and rn not in SUPPLEMENT and rn not in CORRECTIONS
            and rc not in JURI_MAP and rc not in SUPPLEMENT and rc not in CORRECTIONS
            and rn not in _JOURNAL_HOMONYMS
            and _is_academic_abbrev(rn)):
        return None

                                                            
                                                                                       
                                                       
                                                                                            
                                                                                 
                                                                                         
                                                                                            
                                                         
                                                                                           
                                                                                          
    if rn in _NOT_LAW_REPORTS:
        return None

    if rn in _DATABASE_TAG:
        return None

                                                                                    
                                                                                 
                                                                                       
     
                                                                                      
                                                                                        
                                                                                        
                                                                                      
                                                   
     
                                                                                    
                                                          
    if _COURT_WORD.search(rep or ""):
        j = _court_name_jurisdiction(rep)
        if j:
            return j
                                                                                                
                                                                                               
                                                                                                 
                                                                                                  
                                                                                                
                                                                                       
        if context is not None and at is not None:
            seg = context[at:at + 190]
            if re.match(r"\(?\s*unreported", seg, re.I):
                d = re.search(r"\d{1,2}\s+[A-Z][a-z]+\s+(?:19|20)\d{2}", seg)
                j = _court_name_jurisdiction(seg[:d.start()] if d else seg[:120])
                if j:
                    return j

                                                                      
                                                                                               
                                                                                               
                                                                                               
                                                                                              
                                        
                                                                                       
                                                                                          
                                                                                         
                                     
                                                                     
                                                                                        
                                                                                       
                                                                                         
                                                                                         
                                   
    _curated = rn in JURI_MAP or rn in SUPPLEMENT or rn in CORRECTIONS
    parts = [p for p in re.split(r'[\s&]+', rc) if p]
    if len(parts) > 1 and not _curated:
        for p in parts:
            if p.replace('.', '') in FALSE_REPORTERS:
                return None

                                                        
                                                                                             
                                                                                     
                                                                                           
                                                                                            
                                                                                     
                                                                                            
                     
                                                                                           
                                                                                             
                                                                                               
                                                                                          
                                  
                                                                                 
                                                                                 
                                                                                 
                                                                                  
                                                                                   
                                                                                  
    if _PERIODICAL.search(rn) and rn not in _JOURNAL_HOMONYMS and not _curated:
        return None

                                                          
     
                                                                                          
                                                                                        
                                                                                     
                                                                                            
                                                                                            
                                                                                             
                                                           
    if context is not None and at is not None and rn not in _SELF_IDENTIFYING:
        origin = _origin(context, at)
                                                                                                
                                                                                                 
                                                                                                  
                                                                                                 
                                                                                                   
                                                                                               
                                                                                                 
                                                                                               
                                                                                                   
                                                                                            
                                                                                                    
                                                                                                      
                                                                                                        
                                                                                                   
        if origin == 'ECHR' and _ECHR_NATFIX and rn not in _HR_MIXED_SERIES:
            _plain = _classify_base(rep, form=form, context=None, at=None, citing_court=citing_court)
            if (_plain not in (None, 'ECHR', 'EU', 'OTHER')
                    and not _COE_CASE_NAME.search(context[max(0, at - 80):at])):
                origin = None
        if origin:
            return origin

                        
                                                                                        
                                                                                             
                                                                                               
                                                                                
    if rn in _ALWAYS_JOURNAL:
        return None
    if rn in _JOURNAL_HOMONYMS:
        if context is not None and at is not None and _looks_like_journal(rn, context, at):
            return None                                                          
                                                                          
    elif rc in JOURNAL_REPORTERS or rn in JOURNAL_REPORTERS:
        return None

                       
    if form:
        rule = FORM_RULES.get(rn)
        if rule and form in rule:
            return rule[form]

                                                                                 
    ch = _CONTEXT_HOMONYMS.get(rn)
    if ch:
        courts, juri = ch['citing_in']
        if citing_court in courts:
            return juri
        return ch['default']

                                                                              
                                                                                            
                                                   
    if rn in CORRECTIONS:
        return CORRECTIONS[rn]
    if rc in JURI_MAP:
        return JURI_MAP[rc]
    if rn in JURI_MAP:
        return JURI_MAP[rn]
    if rn in SUPPLEMENT:
        return SUPPLEMENT[rn]

                          
    p = _prefix_rule(rn)
    if p:
        return p

                           
                                                                                          
                                                                                        
                                                                                          
                                                                                         
                                                                                            
    if _external is not None:
        base = _SERIES_SUFFIX.sub('', rc).strip()
        fallback = None
        for cand in (rep, rn, base, base.replace('.', '')):
            if not cand:
                continue
            try:
                j = _external(cand)
            except Exception:
                continue
            if not j:
                continue
            if j != 'OTHER':
                return j
            if form in ('nominate', 'bare_rep'):
                                                                                           
                                                                                            
                                                                                        
                                                                                        
                                                                                         
                                 
                continue
                                                                                       
                                                                                      
                                                                                          
                                                                                           
            fallback = j
        if fallback:
            return fallback

                                                                   
     
                                                                                       
                                                                                         
                                                                            
     
                                                                                            
                                                                                         
                                                                                           
                                                                                        
                                                                       
     
                                                                                            
                                                                                       
                                                                                            
                                                                                         
                           
    if form in ('nominate', 'bare_rep'):
        return None
    return 'OTHER'


                                                                                
                                                                                                 
                                                                                                  
                                                                                                 
                                                                                                 
                                                                       
                                                                                                  
                                                                                            
                                                                                                    
                                                                                  
                                                                               
                                                                                               
                                                              
                                                                                       
                                                                                             
                                                                                                        
                                                                                        
                                                                                                    
                                                                                                       
                                                                                          
                                                                                       
                                                                                         
                                                                                                  
                     
                                                                                                     
                                                                                  
                                                            
                                                                                                            
                                                                                                          
                                                                                                        
                                                                                                         
                                                                                                         
                                                                                                     
                                                                                          
                                                                 
_JF_ON = _os_cr.environ.get("JR_JURFIX", "1") != "0"
                                                                                           
_ECHR_NATFIX = _os_cr.environ.get("JR_ECHR_NATFIX", "1") != "0"
_HR_MIXED_SERIES = frozenset({'BHRC', 'HRLR', 'UKHRR', 'EHRLR', 'IHRR', 'BHRR', 'HRCD', 'EHRLRSPEC'})
_MYFC_THISCOURT = _os_cr.environ.get("JR_MYFC_THISCOURT", "1") != "0"
_COE_CASE_NAME = re.compile(
    r"\bv\.?\s+(?:the\s+)?(?:United\s+Kingdom|U\.?K\.?|Albania|Andorra|Armenia|Austria|Azerbaijan|Belgium|"
    r"Bosnia(?:\s+and\s+Herzegovina)?|Bulgaria|Croatia|Cyprus|Czech\s+Republic|Denmark|Estonia|Finland|France|Georgia|"
    r"Germany|Greece|Hungary|Iceland|Ireland|Italy|Latvia|Liechtenstein|Lithuania|Luxembourg|Malta|Moldova|Monaco|"
    r"Montenegro|Netherlands|(?:North\s+)?Macedonia|Norway|Poland|Portugal|Romania|Russia|San\s+Marino|Serbia|Slovakia|"
    r"Slovenia|Spain|Sweden|Switzerland|Turkey|Türkiye|Ukraine)\s*(?:\((?:No\.?\s*\d+|[^()]{0,40})\)\s*)?,?\s*$")
_JF_UKCOURT = lambda cc: _is_uk_court(cc)
                                                                                                     
                                                                                                   
                                                                                                        
_JF_PC_AFTER = re.compile(r"^[^;\n]{0,45}?\d(?:,?\s*at\s+pp?\.?\s*[\d\-–, ]+)?\s*\(\s*P\.?\s?C\.?\s*\)")
_JF_YEAR_IN = re.compile(r"[\[(]\d{4}[\])]")
_JF_PC_TAG = re.compile(r"UKPC\w*\s*\d+\s*;\s*$")
                                                                                                        
                                                                                                      
                                                                                              
_JF_PC_WORDS = re.compile(r"Privy\s+Council(?:'s)?\s+(?:decision\s+|judgment\s+|advice\s+)?(?:in|of)\s+"
                          r"(?:the\s+case\s+of\s+)?[A-Z][^\d;:\[\(\]\)]{2,70}$")
_JF_AU = {'NSWR', 'QSR', 'QWN', 'STRQD', 'QJPR', 'SR(NSW)', 'VLR(L)', 'VLR(E)', 'ALT'}
_JF_HK = {'HKCFAR', 'HKLRD', 'HKLR', 'HKC', 'HKCU', 'HKCFA', 'HKCA', 'HKCFI', 'HKEC'}
_JF_UK = {'NI', 'RTR', 'PENSLR', 'NIJB', 'VESEY', 'VESEYSENIOR', 'VESSEN', 'LLOYDSREP', 'LLLREP'}
_JF_CAN = {'BCR', 'QUEKB', 'QUEQB', 'QUESC', 'OLR', 'OWN', 'OWR', 'BRQUE', 'RLQUE', 'CS'}


def classify(rep, form=None, context=None, at=None, citing_court=None):
    
    if _JF_ON:
        rep = str(rep or '').replace('`', "'")
    base = _classify_base(rep, form=form, context=context, at=at, citing_court=citing_court)
    if not _JF_ON or base is None:
        return base
    raw = str(rep or '')
    rn = _norm(raw)[1]
    cc = str(citing_court or '').upper()
    uk = _JF_UKCOURT(cc)
                                                         
    if context is not None and at is not None:
        _pa = _JF_PC_AFTER.search(context[at:at + 90])
        if _pa and _JF_YEAR_IN.search(_pa.group(0)[7:]):
            _pa = None
        if (_pa or _JF_PC_TAG.search(context[max(0, at - 40):at])
                or _JF_PC_WORDS.search(context[max(0, at - 160):at])):
            return 'UK'
                                                                                              
    if _JF2_ON and rn in _JF2_SERIES and base in ('SG', 'MY'):
        _j2, _why = _jf2_mlj(context, at, cc)
        if _j2:
            return _j2
    if rn == 'PC' and form == 'lrfull':
        return 'UK'
    if rn == 'TC':                                                          
        return 'USA' if cc in ('USSC', 'USA', 'US') else 'UK'
    if uk and rn == 'F' and base == 'USA':                                  
        return 'UK'
    if uk and rn == 'SLR' and form != 'bracket' and base == 'SG':
        return 'UK'
                                                                                                  
                                                                                             
                                                                                                
                                                                                                   
                                                                                              
                                                                                            
    _vm = re.match(r"[\[(]\d{4}[\])]\s*(\d+)?\s*", context[at:at + 30]) if context is not None and at is not None else None
    _vol = int(_vm.group(1)) if _vm and _vm.group(1) else (0 if _vm else None)
    if rn == 'P' and form in ('bracket', 'round') and _vol is not None and _vol < 10:        
        return 'UK'
    if rn == 'FLR' and form == 'bracket' and _vol is not None and _vol <= 4:        
        return 'UK'
                                                                                                   
                                                                                 
    _yr = re.match(r"[\[(](\d{4})[\])]", context[at:at + 8]) if context is not None and at is not None else None
    if rn == 'IR' and base == 'AU' and _yr and int(_yr.group(1)) < 1922:
        return 'UK'
    if rn == 'IR' and base == 'AU' and form == 'bracket':                   
        return 'OTHER'
    if rn in _JF_UK or (uk and rn == 'D' and form == 'round'):               
        return 'UK'
    if rn in _JF_AU or (rn.endswith('(NSW)') and base in ('OTHER', 'IND')):        
        return 'AU'
    if rn in _JF_HK:                                                        
        return 'HK'
    if cc == 'USSC':                                                         
        if base == 'OTHER' and re.search(r'(?:2D|3D|4TH|5TH)$', rn):
            return 'USA'
        if rn == 'BR' and base == 'AU':
            return 'USA'
    if cc == 'SCC':                                                          
        if rn in ('BLR', 'CLR') and re.search(r'\(\s*\d\s*[a-z]{1,2}\s*\)', raw):
            return 'CAN'
        if rn in _JF_CAN:
            return 'CAN'
    if rn == 'SSLR' and cc.startswith('SG'):                                 
        return 'SG'
    if rn == 'SCC' and base == 'CAN' and _vol:                               
        return 'IND'
    if rn.startswith(('SCCONLINE', 'SUPPSCC', 'SCC(CRI)', 'SCC(L&S)', 'SCC(TAX)')) or rn == 'SCCHYD':
        return 'IND'
    return base


                                                                                
                                                                                                         
                                                                                                        
                                                                                                     
                                                                                                   
                                                                             
                                                                                     
                                                                                               
                                                                                                      
                                                                               
                                                                                                    
                                                                                                    
                                                                                                       
                                                                                                  
                                                    
                                                                                     
                                                                                                        
                                                                                                   
                                                                                      
                                                                                        
                                                                                           
                                                                                          
                                                                                           
                                                                                                       
                                                                                                 
                           
_JF2_ON = _os_cr.environ.get("JR_JURFIX_MLJ", "1") != "0"
_JF2_SERIES = {'MLJ', 'MLJU', 'MLR'}
_JF2_SG_BENCH = frozenset([
    'a p rajah', 'a v winslow', 'abdul wahab ghows', 'aedit abdullah', 'aidan xu',
    'aidan xu aedit abdullah', 'alex', 'amarjeet singh', 'ambrose', 'amy seow wai peng',
    'amy tung chew ming', 'andre maniam', 'andrew ang', 'andrew phang boon leong',
    'ang cheng hock', 'ang ching pin', 'anselmo reyes', 'anthony james besanko',
    'anthony meagher', 'audrey lim', 'belinda ang saw ean', 'bernard rix', 'brenda chua',
    'bryan fang', 'buttrose', 'c r rajah', 'carolyn berger', 'chan sek keong', 'chan seng onn',
    'chan tai-hui jason', 'chan wei sern paul', 'chao hick tin', 'chew chin yee',
    'chi qiyuan douglas', 'ching sann', 'chong chin chin', 'choo han teck', 'choor singh',
    'christopher de souza', 'christopher lau', 'christopher scott sontchi', 'christopher tan',
    'chua f a', 'chua lee ming', 'colin liew', 'colin seow', 'crystal tan huiling', "d c d'cotta",
    'daphne hong fan sin', 'darius chan', 'david edmond neuberger', 'dawn tan ly-ru',
    'debbie ong', 'debbie ong siew ling', 'dedar singh gill', 'delphine ho', 'denise wong',
    'desmond chong', 'dominique has cher', 'dorcas quek', 'douglas jones', 'dyson heydon',
    'edmund leow', 'edwin san', 'elaine liew', 'elton tan xue', 'eunice chan swee en',
    'eunice chua', 'fong mian yi seraphina', 'foo chee hock', 'foo tuat yien',
    'francis ng yong kiat', 'g p selvam', 'george wei', 'gillian koh tan', 'goh joon seng',
    'goh phai cheng', 'goh yi han', 'goh yihan', 'henry bernard eder', 'ho may kim',
    'ho osheau peng', 'ho su ching', 'hoo sheau peng', 'hri kumar nair', 'james all sop',
    'james elisha lee', 'james michael peck', 'janice wong shi hui', 'jay lee yuxian',
    'jean chan lay koon', 'jeremy lionel cooke', 'jeyendran jeyapal', 'joel chen',
    'jonathan hugh mance', 'jonathan mance', 'jonathan ng pang ern', 'jordan tan',
    'joyce low wei lin', 'judith prakash', 'justin yeo', 'k s rajah', 'kan ting chiu',
    'kannan ramesh', 'karthigesu', 'kathryn thong', 'keith han', 'kenneth choo', 'kenneth yap',
    'kevin tan eu shan', 'kristy tan', 'kwek mean luck', 'l p thean', 'lai kew chai',
    'lai siu chiu', 'lee kee yeng', 'lee kim shin', 'lee seiu kin', 'lee yeow wee david',
    'leo zhen wei lionel', 'li yuen ting', 'lim jian yi', 'lim teong qwee', 'lionel yee',
    'low siew ling', 'low wan jun tammy', 'lp thean', 'm karthigesu', 'mavis chionh sze chyi',
    'michael hwang', 'miyapan ramu', 'mohamed faizal', 'mph rubin', 'nathaniel khng',
    'navin anand', 'nicholas poon', 'pang khang chau', 'patricia bergin', 'paul chan',
    'paul quan', 'paul tan', 'peh aik hin', 'phang hsiao chung', 'philip jeyaretnam',
    'philip pillai', 'punch coomaraswamy', 'quentin loh', 'rajendran s', 'robert french',
    'roger giles', 'ruth yeo', 's mohan', 's rajendran', 'saqib alam', 'sarah shi', 'scott tan',
    'see kee oon', 'seow zhixiang', 'sharon lim', 'shaun leong li shiong', 'shaun pereira',
    'sim khadijah', 'simon thorley', 'sinnathuray', 'sir henry bernard eder', 'sir vivian ramsey',
    'steven chong', 'sundaresh menon', 'sushil nair', 't kulasekaram', 't s sinnathuray',
    'tai wei shyong', 'tan ah tah', 'tan lee meng', 'tan puay boon', 'tan siong thye',
    'tan sze yao', 'tan teck ping karen', 'tan teow yeow', 'tay yong kwang', 'teh hwee hwee',
    'teo guan kee', 'teo guan siew', 'terence tan zhong wei', 'then ling', 'thian yee sze',
    'thomas bathurst', 'toh han li', 'v k rajah', 'valerie thean', 'vincent hoong',
    'vincent leow', 'vinodh coomar aswamy', 'vinodh coomaraswamy', 'vivian ramsey', 'vk rajah',
    'warren khoo', 'warren khoo l h', 'wee chong jin', 'wong baochen', 'woo bih li',
    'yap yew choh kenneth', 'yeong zee kin', 'yong pung how', 'zeslene mao', 'zhuang wenxiong',
    'zhuo wenzhao',
])


def _jf2_key(name):
    
                                                                                 
    t = [w for w in str(name).replace(".", " ").split() if not re.fullmatch(r"[A-Z]{1,3}", w)]
    t = re.sub(r"[^a-z' ]", " ", " ".join(t).lower()).split()
    return frozenset(w for w in t if len(w) > 1 and w not in ('bin', 'binti', 'al', 'a/l', 'the', 'mr', 'justice'))


_JF2_BENCH_KEYS = frozenset(_jf2_key(n) for n in _JF2_SG_BENCH)


def _jf2_long(k):
    
    return frozenset(w for w in k if len(w) > 3)


_JF2_BENCH_LONG = frozenset(x for x in (_jf2_long(k) for k in _JF2_BENCH_KEYS) if x)


def _jf2_on_bench(k):
    return k in _JF2_BENCH_KEYS or (bool(_jf2_long(k)) and _jf2_long(k) in _JF2_BENCH_LONG)
                                                                                               
                                                       
_JF2_TITLE = r"(?:Ag\.?[ \t]+CJ|C\.?J\.?|J\.?A\.?|F\.?J\.?|L\.?P\.?|S\.?C\.?J\.?|J\.?C\.?A\.?|F\.?C\.?J\.?|J\.?C\.?|J\.?)"                                                       
_JF2_JUDGE = re.compile(
    r"(?<![A-Za-z])((?:[A-Z][A-Za-z'’\-]+|[A-Z]\.?)(?:[ \t]+(?:[A-Z][A-Za-z'’\-]+|[A-Z]\.?|bin|binti|a/l)){0,5})"
    r"[ \t]*,?[ \t]+" + _JF2_TITLE + r"(?![A-Za-z])")
_JF2_NOT_NAME = frozenset({'the', 'in', 'per', 'see', 'and', 'by', 'of', 'v', 'pp', 'mr', 'lord', 'mlj',
                           'as', 'also', 'following', 'thus', 'then', 'where', 'when', 'there', 'here',
                           'that', 'this', 'since', 'but', 'which', 'learned', 'judge', 'justice'})
                                                                                                     
                                                                                                  
                         
_JF2_LORD = re.compile(r"\bLord[ \t]+[A-Z][a-z]+")
_JF2_PC = re.compile(r"Privy[ \t]+Council|Judicial[ \t]+Committee")
                                                                                       
_JF2_THIS_COURT = re.compile(r"\b(?:this|our)[ \t]+(?:court|Court)\b(?![ \t]+(?:below|of[ \t]+first))")
_JF2_MY_WORDS = re.compile(r"Malaysian|of[ \t]+Malaysia|Malaysia['’]s|Federal[ \t]+Court[ \t]+of[ \t]+Malaysia")
_JF2_SG_WORDS = re.compile(r"Singapore[ \t]+(?:Court[ \t]+of[ \t]+Appeal|High[ \t]+Court)|"
                           r"(?:High[ \t]+Court|Court[ \t]+of[ \t]+Appeal)[ \t]+of[ \t]+Singapore")


def _jf2_sentence(context, at):
    
    lo = max(0, at - 300)
    before = context[lo:at]
    ends = [m.end() for m in re.finditer(r"(?<![A-Z])(?<!\bv)(?<!\bNo)(?<!\bJ)(?<!\bCJ)(?<!\bJA)[.!?][ \t\n]+(?=[A-Z\[(])", before)]
    s = lo + ends[-1] if ends else lo
    after = context[at:at + 300]
    m = re.search(r"(?<![A-Z])(?<!\bv)(?<!\bNo)(?<!\bJ)(?<!\bCJ)(?<!\bJA)[.!?](?=[ \t\n]+[A-Z\[(]|$)|\n\n", after)
    e = at + (m.start() if m else len(after))
    return s, e


                                                                                              
_JF2_CITE = re.compile(r"[\[(<]\s*\d{4}(?:[-–]\d{2,4})?\s*[\])>]\s*\d{0,3}\s*[A-Z][A-Za-z.()&' ]{0,18}?[ \t]\d{1,5}")


def _jf2_paragraph(context, at):
    
    lo, hi = max(0, at - 1500), min(len(context), at + 1500)
    br = re.compile(r"\n[ \t]*\n|\n[ \t]*\[?\d{1,3}\]?\.?[ \t]+(?=[A-Z(\[])")
    starts = [m.end() for m in br.finditer(context, lo, at)]
    p0 = starts[-1] if starts else lo
    m = br.search(context, at, hi)
    p1 = m.start() if m else hi
    return p0, p1


def _jf2_mlj(context, at, citing_court=None):
    
    if context is None or at is None:
        return None, 'no context'
                                                                                                
                                                                                                    
                                                                                                    
                                                                                                      
                                                                                                       
                                                                                  
    _my_cc = _MYFC_THISCOURT and str(citing_court or '').upper() in ('MYFC', 'MY')
    s, e = _jf2_sentence(context, at)
    sent = context[s:e]
                                                                                                
                                                                                                    
                                                                                                   
                                                                                               
                                                                                               
                              
    p0, p1 = _jf2_paragraph(context, at)
    para = context[p0:p1]
    rel = at - p0
    own = _JF2_CITE.match(context, at)
    own_end = (own.end() if own else at + 4) - p0
    cands = []
    for m in _JF2_PC.finditer(para):
        cands.append((m.start(), m.end(), 'PC', None, m.group(0)))
    for m in _JF2_LORD.finditer(para):
        cands.append((m.start(), m.end(), 'LORD', None, m.group(0)))
    for m in _JF2_JUDGE.finditer(para):
        words = [w for w in m.group(1).split() if w.lower().strip('.') not in _JF2_NOT_NAME]
        if not words or all(len(w.strip('.')) == 1 for w in words):
            continue
        k = _jf2_key(" ".join(words))
        if not k:
            continue
                                                                                                 
                                                                                                    
        cands.append((m.start(), m.end(), 'JUDGE', k, m.group(0)))
    best = None
    for cs, ce, kind, k, txt in cands:
        if ce <= rel:
            gap, d = para[ce:rel], rel - ce
        elif cs >= own_end:
            gap, d = para[own_end:cs], cs - own_end
        else:
            continue                                                  
        if _JF2_CITE.search(gap):
            continue                                                                       
        if best is None or d < best[0]:
            best = (d, kind, k, txt)
    yr = re.match(r"[\[(<]\s*(\d{4})", context[at:at + 10])
    year = int(yr.group(1)) if yr else None
    if best is not None and best[1] in ('PC', 'LORD'):
        return 'UK', ('paragraph names the Privy Council: ' if best[1] == 'PC'
                      else 'a Law Lord beside the citation: ') + best[3]
                                                                                       
                                                                                                       
                                                                                                         
                                                                                       
                                                                                                          
                                                                                                  
                                                                                        
                                                                                                        
                                                                                                      
                                                                                                      
                                                                                                     
                               
    if _JF2B_ON:
        nm = context[s:at]
        _cs = [m.end() for m in _JF2_CITE.finditer(nm)]
        nm = nm[_cs[-1]:] if _cs else nm
        nm = nm[-160:]
                                                                                                 
        _lead = list(re.finditer(r"[;:]|\.[ \t]|\b(?:see|See|cf|eg|e\.g\.,?)[ \t]|\b(?:in|In)[ \t]+(?=[A-Z])|"
                                 r"\bcase[ \t]+of[ \t]+|\bdecision[ \t]+(?:of|in)[ \t]+|[“\"‘]", nm))
        nm = nm[_lead[-1].end():] if _lead else nm
        sg_judge = (best is not None and best[1] == 'JUDGE' and _jf2_on_bench(best[2]) and best[3] in sent)
        sg_sent = bool(_JF2_SG_WORDS.search(sent) or (not _my_cc and _JF2_THIS_COURT.search(sent)))
        if year is not None and year >= 1992 and not (sg_judge or sg_sent):
            return 'MY', 'R93: MLJ dated 1992 or later'
        if not sg_judge:
            if _JF2B_MY_NAME.search(nm):
                return 'MY', 'case name is Malaysian: ' + _JF2B_MY_NAME.search(nm).group(0)
            if _JF2B_SG_NAME.search(nm):
                return 'SG', 'case name is Singaporean: ' + _JF2B_SG_NAME.search(nm).group(0)
    if best is not None:
        _d, _kind, k, txt = best
        if _jf2_on_bench(k):
            return 'SG', 'judge on SG bench: ' + txt
        if year is not None and year < 1965:
            return 'OTHER', 'judge not on SG list, cited before 1965: ' + txt
        return 'MY', 'judge not on SG list: ' + txt
    if _JF2_MY_WORDS.search(sent):
        return 'MY', 'sentence says Malaysian'
    if _my_cc and _JF2_THIS_COURT.search(sent) and not _JF2_SG_WORDS.search(sent):
        return 'MY', 'this court = the citing Malaysian court'
    if _JF2_SG_WORDS.search(sent) or _JF2_THIS_COURT.search(sent):
        return 'SG', 'sentence names a Singapore court'
    return 'OTHER', 'no judge or court in the sentence'


_JF2B_ON = _os_cr.environ.get("JR_JF2B", "1") != "0"
_JF2B_MY_NAME = re.compile(r"\bSdn\.?[ \t]+Bhd\b|\bBhd\b|\bBerhad\b|\bMalaysia\b|\bKerajaan\b|\bPendakwa[ \t]+Raya\b|"
                           r"\bKuala[ \t]+Lumpur\b|\bSelangor\b|\bPenang\b|\bPulau[ \t]+Pinang\b|\bJohore?\b|\bPerak\b|"
                           r"\bKedah\b|\bKelantan\b|\bPahang\b|\bSabah\b|\bSarawak\b|\bMelaka\b|\bNegeri[ \t]+Sembilan\b|"
                           r"\bTerengganu\b|\bTrengganu\b|\bPerlis\b|\bIpoh\b|\bKota[ \t]+Kinabalu\b|\bKuching\b")
_JF2B_SG_NAME = re.compile(r"\bPte\.?[ \t]+Ltd\b|\bPte\b|\bSingapore\b")


                                                                                               
                                                                                        
                                                                                            
                                                                                                  
                                                                                                     
                                                                                                   
                                                                             
                                                                                                       
                                                                                                        
                                                                                                 
_MYFC_SERIES = {"MLJ", "MLJU", "LNS", "CLJU", "CLJSUPP", "CLJREP", "MLRA", "MLRAU", "MLRH", "MLRHU",
                "MLJSUPP", "AMR", "MLJCRL", "CLJ", "AMCR", "SUPP"}
_classify_core = classify


                                                                                                                
                                                                                                                 
                                                                                                                
                                                                                                     
_MY_ONLY_SERIES = {"LNS", "CLJU", "CLJSUPP", "CLJREP", "MLRA", "MLRAU", "MLRH", "MLRHU", "AMR", "AMCR"}
_MY_SERIES_ALL = _os_cr.environ.get("JR_MY_SERIES_ALL", "1") != "0"


def classify(rep, form=None, context=None, at=None, citing_court=None):
    res = _classify_core(rep, form=form, context=context, at=at, citing_court=citing_court)
    if res == 'OTHER':
        rn = re.sub(r"[^A-Z]", "", str(rep or "").upper())
        if str(citing_court or '').upper() == 'MYFC':
            if rn in _MYFC_SERIES or rn.startswith(("MLJ", "CLJ", "MLR", "LNS")):
                return 'MY'
        elif _MY_SERIES_ALL and rn in _MY_ONLY_SERIES:
            return 'MY'
    return res


                                                                                 
_classify_before_hkcfa = classify


def classify(rep, form=None, context=None, at=None, citing_court=None):
    result = _classify_before_hkcfa(rep, form=form, context=context, at=at, citing_court=citing_court)
    if citing_court != "HKCFA":
        return result
    rn = re.sub(r"[^A-Z&]", "", str(rep or "").upper())
    if rn in {"LLOYDSREINSURANCELAWREPORTS", "LLOYDSREPIR"}:
        return "UK"
                                                                         
                                                                          
    if rn in {"HKLR", "HKLRD", "HKC"} and context is not None and at is not None:
        before = context[max(0,at-240):at]
        if re.search(r"(?:Privy\s+Council\s+on\s+appeal\s+from\s+Hong\s+Kong\s+in\s+"
                     r"[A-Z][^\d;:\[\(\]\)]{2,100}|"
                     r"on\s+appeal\s+from\s+Hong\s+Kong\s+(?:in\s+the\s+)?Privy\s+Council"
                     r"\s+(?:in|of)\s+[A-Z][^\d;:\[\(\]\)]{2,100})$",before):
            return "UK"
    if rn == "HKCLR":
        return "HK"
    if result == "OTHER" and rn in {"P&CR", "PD", "PH", "DEG&J", "LJCHNS", "DOUGL", "SW&TR"}:
        return "UK"
                                                                                   
    if rn == "ELR" and context is not None and at is not None:
        paragraph = context[max(0,context.rfind("\n\n",0,at)):at+180]
        if re.search(r"\b(?:EWHC|EWCA|English|England|Sedley|Laws LJ|Lord Woolf)\b",paragraph):
            return "UK"
    return result
