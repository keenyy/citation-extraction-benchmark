                       
"""Citation counting.

Counts the distinct authorities a judgment relies on, by jurisdiction.

WHY THIS EXISTS. A field audit on 17 August 2026 read fourteen judgments by hand and compared
them with the stored Master values. The citation columns were wrong on most of them, in both
directions: 0 of 8 correct on the High Court of Australia, 4 of 8 on New Zealand, 6 of 8 on
Canada. One Canadian judgment recorded 7 citations where a reader counted about 38.

The faults, and where each is handled here:

  F1  old comma form   '(1897) 2 Ch., 12'                      -> _CITE_PAREN_COMMA
  F2  old English      Ch, App Cas, LT, L.J.K.B., Co Rep, TC   -> jr_reporters
  F3  provincial CAN   A.R., C.C.C., O.A.C., Man. R., A.P.R.   -> jr_reporters
  F4  unreported       'HC Auckland CIV-2010-404-3298'         -> _CITE_UNREPORTED
  F5  parallel/repeat  one case counted two or three times     -> the three dedup levels below
  F6  false positives  a jurisdiction with no authority in it  -> jr_reporters blocklists

DEDUPLICATION. Three levels, and the order matters.

  L0  span overlap.    Two patterns matching the same characters are one citation.
                       '(1971) 45 CLR 22' matches both the general parenthetical pattern and
                       the CLR-specific one.
  L1  exact citation.  The same authority cited again anywhere in the judgment counts once.
  L2  parallel form.   One decision given two references side by side is one authority:
                       '[2025] NZCA 31, [2025] 2 NZLR 308'.

⚠️ THE BUG THIS MODULE EXISTS TO FIX. The previous implementation skipped a repeated citation
without recording its character span. A narrower pattern then matched inside that unrecorded
span, found no overlap, and counted it again. So repeats were not suppressed at all -- they were
re-counted through a different pattern. Measured on Federal Commissioner of Taxation v York
Motors, where a reader counted 6 UK and 6 AU authorities, the old engine returned 21 and 13,
because '(1928) 41 CLR 540' appears four times and each repeat added one.

The rule that prevents it: A SPAN IS RECORDED WHENEVER IT IS CONSUMED, including when the match
is discarded as a duplicate. See _Counter.consume().
"""
import re

                                                                           

                                                                                        
                                        
                                                                                          
                                                               
                                                       
                                                                                       
                                                                                          
                                                            
                                                                                  
                                                                            
                                                                                        
                                                                                      
                                                                                       
                                                                                       
                                                                                    
                                 
 
                                                                                    
                                                                                        
                                                                  
                                                                                       
                                                                                           
                                      
                                                                                     
                                                                                 
                                                                                    
                                                                                   
                                                               
_PAGE = r"(?:\d{1,3},\d{3}|\d{1,5})"

                                                                                      
                                                                                         
                                                                                          
                                                                                        
                                                                                      
                                                                                        
                                                                                           
                                                                                         
                         
_PAGE_END = r"(?:[ab]\b|n\b|\b)"

                                                                 
 
                                                                                              
                                                                                               
                                                                                            
                                                                                               
                                                                                           
                                                                                     
                                                                                        
                                                                                            
                                                                                            
                                                                                          
                                                           
                                                                                                  
                                                                                 
                                                                                       
_REP = (r"[A-Z][A-Za-z.’\'`]*"
        r"(?:\s*&\s*[A-Za-z.’\'`]+|\s+[A-Za-z.’\'`]+"
        r"|\s*\((?:[A-Za-z.]{1,8}|[A-Za-z]{1,3}\s?\d{1,2}|\d\s?(?:st|nd|rd|th|d)\s?)\)){0,4}")

                                                                                      
                                                                                       
                                                                                       
                                                                              
                                                                                        
                                                                                        
                                                                                 
                                                                                                
                                                                                               
                                                    
                                                               
                                                                                                
                                                                          
                                                                            
                                                                                                  
                                                                                  
_CITE_BRACKET = re.compile(
    r'\[\s?(\d{4}(?:[\u2013\u2014-](?:\d{4}|\d{2}))?)\s?\]\s*(?:(\d+)\s+)?'
    r'(' + _REP + r')'
                                                                                                
                                                                                 
                                                                                                 
                                                                                            
                                                                                                  
    r'(?:[ \t]+|\s+(?!\d{1,3}[ \t]+[A-Z][a-z])|(?<=\.)(?<!\sp\.)(?<!\spp\.),[ \t]{0,2}|(?<=\.)(?<!\sp\.)(?<!\spp\.))(' + _PAGE + r')' + _PAGE_END)


                  
                                                                                 
                                                                                
                                                                                 
_CITE_PAREN = re.compile(
    r'\((\d{4})\)\s+(\d+(?:-[A-Z])?)\s+(' + _REP + r')\s+(' + _PAGE + r')' + _PAGE_END)

                                                                           
                                                                                         
_CITE_PAREN_COMMA = re.compile(
    r'\((\d{4})\)\s+(\d+)\s+(' + _REP + r')\.?,\s*(?:at\s+)?(?:p\.?\s*)?('
    + _PAGE + r')' + _PAGE_END)

                                                                                              
                                                                                          
                                                                                       
                                                                               
                                                                         
                                                                       
                                                                                       
                                                                                             
                                                                                           
 
                                                                                           
                                                                          
                                                                                           
                                                                                              
_MONTH = (r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|'
          r'Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)')
_CITE_MORISON = re.compile(
    r'\b(' + _MONTH + r')\.?[ \t]*(\d{1,2})?[ \t]*[.,]?[ \t]*(1[5-7]\d{2}|18[0-4]\d)'
    r'[ \t]*[.,;]?[ \t]*\((?:(\d{1,2},?\d{3}|\d{3})\b\.?|(F\.[ \t]?C\.))[^()\n]{0,40}?\)')

                                                                                         
                                                                                         
                                                                                       
                                                                                        
                                                                                       
                          
def _pattern_applies(name, citing_court):
    """False where a pattern is confined to courts that this one is not."""
    if name.startswith("cd_hk"):
        return citing_court == "HKCFA"
    if name == "unreported_nzold":                                                         
        return str(citing_court or "").upper().startswith("NZ")
    if name not in ("morison", "morison_abbr"):
        return True
                                                                                         
                                                                                         
                                                                                         
                 
    try:
        import jr_normalise
        if jr_normalise.court_key(citing_court) in ("HL", "UKSC"):
            return True
    except Exception:                                                              
        pass
    c = str(citing_court or "").upper()
    return c.startswith(("UK", "HL"))


                               
_CITE_US = re.compile(
    r'\b(\d{1,3})\s+(U\.\s?S\.|S\.\s?Ct\.|L\.\s?Ed\.(?:\s?2d)?|F\.\s?(?:2d|3d|4th)|F\.\s?Supp\.(?:\s?2d)?)\s+(' + _PAGE + r')(?:n\b|\b)')

                                              
                                                                                                  
                                                                                               
                                                            
_CITE_VOLFIRST = re.compile(
                                                                                              
    r'\b(\d{1,3})[ \t]+(CLR|ALR|ALJR|SCR|DLR|NZLR|SLR|WLR|AC|QB|KB|Ch)'
    r'(?:[ \t]+|\s+(?!\d{1,3}[ \t]+[A-Z][a-z]))(' + _PAGE + r')(?:n\b|\b)')

                                                                 
                                                                                        
                                                                                          
                                                                                     
                                                                                         
                                                                                       
                                      
_BAREYEAR_COURTS = ('SCC', 'CanLII', 'FCA', 'FC', 'TCC', 'CMAC', 'ONSCDC', 'ONCA', 'ONSC',
                    'ONCJ', 'ONWSIAT', 'HRTO', 'CHRT',
                    'BCCA', 'BCSC', 'BCPC', 'ABCA', 'ABKB', 'ABQB', 'ABPC',
                    'MBCA', 'MBKB', 'MBQB', 'SKCA', 'SKKB', 'SKQB',
                    'NSCA', 'NSSC', 'NSPC', 'NBCA', 'NBKB', 'NBQB',
                    'PESCAD', 'PESCTD', 'PESC', 'PECA', 'NLCA', 'NLSC', 'NLTD',
                    'YKCA', 'YKSC', 'YKTC', 'NWTCA', 'NWTSC', 'NUCA', 'NUCJ',
                    'QCTDP', 'QCCA', 'QCCS', 'QCCQ')
                                                                                          
                                                                                        
                                                                                     
                                                                                       
                                                                                       
_CITE_BAREYEAR = re.compile(
    r'(?<![\[\(\w])\b(\d{4})\s+(' + '|'.join(_BAREYEAR_COURTS) +
    r'|Carswell[A-Z][A-Za-z]{1,7})\s+(\d{1,6})(?:n\b|\b)')

                                                                                
 
                                                                                          
                                                                                        
                                                                                        
                                                                                            
                                                                                             
                                                                                         
                                                                                         
                                                                             
 
                                                                                           
                                                                                         
                                                                                       
                                                                                          
                                                                                           
                                                                              
_BARE_REP = r"(?:[A-Z]\.?){1,6}(?:\s*\((?:[A-Za-z.]{2,8}|\d(?:st|nd|rd|th|d))\))?"

                                                               
                                                                                           
                                                                                         
                                                                                           
                                        
                                                            
                                                                                    
                                                                                       
                                                                                   
                                                                                          
                                                                                     
                                                                                      
                                                                                        
                                                                      
_CITE_AIR_PC = re.compile(
    r'(?<![\[\w])\bAIR\s*(\d{4})\s+(PC)\s+(' + _PAGE + r')(?:n\b|\b)')

                                                                                             
                                                                                        
_CITE_AIR_IND = re.compile(
    r'(?<![\[\w])\bAIR\s*(\d{4})\s+([A-Z][A-Za-z]{1,11})\s+(' + _PAGE + r')(?:n\b|\b)')

_CITE_BAREYEAR_REP = re.compile(
                                                                                          
                                                                                          
                                                                                         
                                                                                           
                                                 
                                                                                                 
                                                                                       
    r'(?<![\[\w/])(?<!AIR )(?<!AIR)\b(1\d{3}|20\d{2}),?[ \t]+(' + _BARE_REP + r'),?[ \t]+(' + _PAGE + r')(?:n\b|\b)')

                                                                      
                                                              
                                                          
                                                                                          
                                                                                            
 
                                                                                     
                                                                                       
                                                           
                                                           
                                                                                            
                                                                                            
_CITE_UNREPORTED = re.compile(
    r'\b(HC|DC|FC|CA|SC|EmpC|CRT)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+'
    r'((?:CIV|CRI|FAM|SC|CA|CP|M)[-\s]?\d{4}[-\s]?\d{2,3}[-\s]?\d{3,6})'
    r'(?:\s*,\s*(\d{1,2}\s+[A-Z][a-z]+\s+\d{4}))?')


                                                                                       
                                     
                                                                                  
                                 
                                                                                      
                                                           
                                                                                  
                                                                                 
                                                                                      
                                                                
 
                                                                                      
                                                     
_CITE_UNREPORTED_AU = re.compile(
    r'\bunreported,?\s+'
                                                                                           
                                                                                      
                                                                                       
                             
    r'((?:[A-Z][A-Za-z]+\s+){0,4}(?:Court|Tribunal|Commission)'
    r'(?:\s+(?:of|for)\s+[A-Z][A-Za-z]+){0,3})'
                                                                                         
                                                                                       
                                                                                       
                                                                 
    r'(?:\s*\([^)\n]{0,80}\))?'
    r'[^;\n]{0,40}?,\s*'
    r'(\d{1,2}\s+[A-Z][a-z]+\s+(?:19|20)\d{2})', re.I)                                           

                                                                                
                                                                             
                                                                                          
                                                                                          
                                                                                      
                                                                                         
                                                                              
                                                                                
                                                                                 
                                                               
_CITE_PAREN_NOVOL = re.compile(
    r'\((\d{4})\)\s+' + '(' + _REP + ')' + r'\.?,?\s+(' + _PAGE + r')\b')

                                                                                 
                                                                                             
                                                
_CITE_YEARCOMMA = re.compile(
    r'\((\d{4})\),\s+(\d{1,4})\s+'
                                                                                               
                                                                                                
    r'([A-Z][A-Za-z.]*(?:\s*\((?:\d+[a-z]{1,2}|N\.\s?S\.)\))?(?:\s+[A-Za-z.]+(?:\s*\((?:\d+[a-z]{1,2}|N\.\s?S\.)\))?)?)'
    r'\s+(' + _PAGE + r')(?:n\b|\b)')

                                                                                            
                                                                                   
 
                                                                                             
                                                                                              
                                                                                               
                                                                                               
                                                         
 
                                                                                               
                                                                                              
                                                                                                
                                                                                           
                                                                           
                                                                                           
                                                                                       
                                                                                              
                                                                                    
                                                                                 
                                                                                           
                                                                                             
                                                                        
_ABBR_TOK = r"(?:[A-Z]\.){1,4}|[A-Z][A-Za-z']{1,11}\.?"
                                                                                               
                                                                                           
                                                                                          
                                                                                  
_ABBR = (r"(?:" + _ABBR_TOK + r")"
         r"(?:[ ]{0,2}&[ ]{0,2}(?:" + _ABBR_TOK + r")|[ ]{1,2}(?:" + _ABBR_TOK + r")){0,3}")

                                                                                              
                                                                                        
                                                                                              
                                                                                        
_CITE_NOMINATE = re.compile(
    r'\b(\d{1,3})[ ]{1,2}(' + _ABBR + r')[ ]{0,2},?[ ]{0,2}(\d{1,4})' + _PAGE_END)

                                                     
 
                                                                                               
                                                                                                
                                                                                             
                                                                                                
                                                                                              
                                               
 
                                                                                              
_CITE_NEWSPAPER = re.compile(
    r'\bThe\s+(Times|Independent|Guardian|Daily\s+Telegraph|Financial\s+Times)\s*,\s*'
    r'((?:\d{1,2}\s+[A-Z][a-z]+\s+\d{4})|(?:[A-Z][a-z]+\s+\d{1,2},?\s+\d{4}))')

                                                                                    
 
                                                                                           
                                                                                               
                                                                                           
                                                                                            
                                                                                        
 
                                                                                           
                                                                                           
                                                                                           
                                                                                     
 
                                                                                       
                                                                                      
                                                                                        
                                                                                       
                                                  
 
                                                                                       
                                                                                          
                                                                                          
                                                                        
 
                                                                                        
                                                                                           
                                                                                       
                                                                                          
                                                                                     
                                                       
_CITE_CJEU = re.compile(
    r'\bCase\s+([CT])[-‑](\d{1,4}/\d{2,4})'
    r'|\bECR\s+(I{1,2})[-‑](\d{1,6})'
    r'|\bEU:([CT]):(\d{4}):(\d{1,6})')

                                                                                         
                                                                                              
                                                                                              
                                                                                          
                                                                                         
                                                                                         
                                                                                       
                                                                                         
                                                                                    
                                                               
_CITE_STRASBOURG = re.compile(
                                                                                     
    r'(?i)\b(?:app(?:lication|n)?s?\.?|admissibility[ \t]+decision|application[ \t]+no)[ \t]*(?:nos?\.?[ \t]*)?(\d{1,5}/\d{2,4})\b')

                                                                             
                                                                                              
                        
                                                                                
                                                            
                                  
                                                                                          
                                                                                          
                                                                                      
                                
 
                                                                                          
                                                                                         
                                                                                          
                                                                                     
                                                                                        
                                                                                        
                                                                              
 
                                                                        
                                                                                   
                                                     
 
                                                                                          
                                                                       
_CITE_UNREPORTED_BARE = re.compile(
    r'\((?:([A-Z][A-Za-z]{1,6}(?:[ \t]+(?:of[ \t]+)?[A-Z][A-Za-z]{1,12}){0,3})[ \t]*,[ \t]*)?[Uu]nreported[ \t]*,?[ \t]*(?:[A-Z][a-z]+[ \t]+)?(\d{1,2}[ \t]+[A-Z][a-z]{2,8}\.?[ \t]+(?:1[89]|20)\d{2})[^)]{0,20}\)')

                                                                                          
                                                                                   
                                                                                   
                                                                                         
                                                                                          
                                            
 
                                                                                          
                                                          
_CITE_COMMISSIONER = re.compile(
    r'\bR\s*\([ \t]*([A-Z]{1,4})[ \t]*\)[ \t]*(\d{1,3})/(\d{2})\b')

                                                                                        
 
                                                                           
                                                                           
 
                                                                                          
                                                                                            
                                                                                             
                                                                                      
                        
 
                                                                                           
                                                                                              
                                                                                            
 
                                                                                         
                                                                                  
_CITE_US_SERIES = re.compile(
    r'(?<![\w.])(\d{1,4})[ \t]+((?:[A-Z][A-Za-z]{0,4}\.?[ \t]*){1,3}(?:2d|3d|4th))[ \t]+(\d{1,4})\b')

                                                                                  
 
                                                                        
                                                                          
 
                                                                                      
                                                                                        
                                              
                                                                                       
                                                               
                                                                                         
                                              
                                                                                  
                                                                     
                                                                                         
                                                            
 
                                                                                          
                                                                                          
                                                                                        
                                                                                        
                                                                                          
                                                                                  
 
                                                                                      
                                                                                      
                                                                                        
                                                                                       
                                                                                       
                                                                 
_CAN_TOK = r"(?:[A-Z]\.){1,5}|[A-Z][A-Za-z’\x27]{1,11}\.?"
_CITE_CAN_SERIES = re.compile(
    r'(?<![\w.])(\d{1,4})[ \t]+'
    r'((?:' + _CAN_TOK + r')'
    r'(?:[ \t]{0,2}&[ \t]{0,2}(?:' + _CAN_TOK + r')|[ \t]{1,2}(?:' + _CAN_TOK + r')){0,3}'
    r'[ \t]{0,2}\(\d{1,2}(?:st|nd|rd|th|d)\))'
    r'[ \t]+(' + _PAGE + r')(?:n\b|\b)')

                                                         
 
                                                                             
 
                                                                                       
                                                                                          
                                                                                        
                                                                                      
                                                                                       
                                                                                         
 
                                                                                      
                                                                                         
                                                                                           
                                                                                      
                                                                                         
                                                                                         
                                                                                          
                                                                                        
                          
_CITE_US_SLIP = re.compile(
    r'(?<![\w.])(\d{1,3})[ \t]+(U\.[ \t]?S\.)[ \t]*'
    r'(?:_{2,5}|-{2,5}|[–—]{1,4})')

                                                                                          
                                                                   
                                                                  
                                                                                         
                                                                                   
                                                                                       
                                                                                    
                                                                                        
_CITE_DECISION_PAGE = re.compile(
    r'(?<![\w.])(\d{1,4})[ \t]+((?:[A-Z]\.){2,5}|[A-Z][A-Za-z.]{1,10})[ \t]+D/(\d{1,4})\b')

                                                                                            
                                                                                                  
                                                                                                

                                                                                                
                                                                                    
                                                                                
                                      
                                                                                          
                                                                                               
                                                                                          
                                                                                        
_CITE_SPACED = re.compile(
    r'(?<![\w.])(\d{1,3})[ ]{1,2}(Q[ ]B[ ]D|Q[ ]B|K[ ]B|H[ ]L[ ]C(?:as)?|HL[ ]C(?:as)?|H[ ]L|C[ ]P[ ]D'
    r'|Ch\.?[ ]?D\.?|Cr[ ]App[ ]R(?:[ ]?\(S\))?|A[ ]Crim[ ]R'
    r'|F[ ]Supp(?:[ ][23]d)?|F[ ]Cas|[A-Z][ ]&[ ][A-Z][a-z]{0,3})[ ]{0,2},?[ ]{0,2}(\d{1,4})' + _PAGE_END)

                                                                                          
                                                                                                
                                                                                      
                                                                                            
                                                                                            
                                                                                                 
_CITE_NOMINATE_AND = re.compile(
    r'(?<![\w.])(?<!&[ ])(\d{1,3})\.?[ ]{1,2}([A-Z][a-z]{1,10}\.?[ ]and[ ][A-Z][a-z]{0,10}\.?)[ ]{0,2},?[ ]{0,2}'
    r'(?:pp?\.[ ]?)?(\d{1,4})' + _PAGE_END)

                                                                                             
                                                                                                 
                                                                                               
                                                                                                
                                                                                      
_CITE_MORISON_ABBR = re.compile(
                                                                                       
    r"\b(Morr?\.|Morrison['’]s[ ]Dictionary,)(?:[ ]?Dict\.)?[ ]?(?:p\.[ ]?)?(\d{1,2},\d{3}|\d{3,5})\b(?!,\d)")
_CITE_MORISON_M = re.compile(
    r'(?:^|(?<=,[ ])|(?<=;[ ]))(M)\.[ ](\d{1,2},\d{3}|\d{3,5})\b(?![,.]?\d)')
                                                                                           
                                                                                               
                                                                                             
                                                                                                 
                                                                      
_CITE_FACCOLL_DAYFIRST = re.compile(
    r'\b(?=\d{1,2}(?:st|nd|rd|th|d)?\.?[ ](' + _MONTH + r'))(\d{1,2})(?:st|nd|rd|th|d)?\.?[ ]'
    + _MONTH + r'\.?,?[ ](1[5-7]\d{2}|18[0-4]\d)[.,]?[ ]()(F\.[ ]?C\.|Fac\.[ ]?Coll\.)')

                                                                                               
                                                                                                 
                                                               
_CITE_WL = re.compile(r'(?<![\[\w/])\b((?:19|20)\d{2})[ \t]+(WL)[ \t]+(\d{4,9})\b')
_CITE_OHIO = re.compile(r'(?<![\[\w/-])\b((?:19|20)\d{2})-(Ohio)-(\d{1,5})\b')

                                                                                               
                                  
                                                                                        
                                                    
                                                                                          
                                                                                                  
                                                                                           
                                        
_NZ_DATE = r'(\d{1,2}[ \t]+[A-Z][a-z]+[ \t]+(?:19|20)\d{2})'
_CITE_NZ_FILE_REG = re.compile(
    r'\b(HC|DC|FC|CA|EmpC|EC)[ \t]+([A-Z][a-zāēīōū]+(?:[ \t]+[A-Z][a-z]+)?)[ \t]+'
    r'([A-Z]{1,4}[- ]?\d[\d/-]{1,13})[ \t]*,[ \t]*' + _NZ_DATE)
                                                                                                 
                                                                            
_CITE_NZ_FILE_BARE = re.compile(
    r'\b(CA)()[ \t]?(\d{1,4}/\d{2,4})[ \t]*,[ \t]*' + _NZ_DATE)

                                                                                                
                                                                                             
                                                                                               
                                                                                                     
_CITE_UNREPORTED_AFTER = re.compile(
    r'(?<![A-Za-z])\(?()[Uu]nreported\)?[ \t]*,?[ \t]*(?:given[ \t]+(?:on[ \t]+)?|delivered[ \t]+(?:on[ \t]+)?)?'
    r'(\d{1,2}[ \t]+[A-Z][a-z]{2,8}\.?[ \t]+(?:1[89]|20)\d{2})')

                                                                                           
                                                                                                       
                                             
                                                                                                  
                                                                                                 
                                                                                            
                                           
                                                                                              
                                                                                             
                                                                                    
_LR_SERIES = (r"(?:Q\.?[ ]?B\.?(?:[ ]?D\.?)?|C\.?[ ]?P\.?(?:[ ]?D\.?)?|Ex\.?(?:[ ]?D\.?)?"
              r"|Ch\.?(?:[ ]?D\.?|[ ]App\.?)?|Eq\.?|H\.?[ ]?L\.?|H\.[ ]of[ ]L\.|P\.?[ ]?C\.?|P\.?[ ]?&[ ]?D\.?"
              r"|A\.?[ ]?&[ ]?E\.?|Sc\.?[ ]?&[ ]?Div\.?|App\.?[ ]Cas\.?|C\.?[ ]?C\.?[ ]?R\.?|Ir\.?|P\.?[ ]?D\.?)")
_CITE_LR_FULL = re.compile(
                                                                            
    r"\((\d{4})\),?\s+L\.?[ ]?R\.?,?\s+(\d{1,3})\s+(" + _LR_SERIES + r"),?\s+(?:at\s+pp?\.?\s*)?(\d{1,4})" + _PAGE_END)

                                                       
                                                                                                
                                                                                                  
                                                                       
                                                                                              
                                                       
_CITE_NOMINATE_NS = re.compile(
    r'(?<![\w.])(\d{1,3})[ ]{1,2}((?:' + _ABBR_TOK + r')(?:[ ]{1,2}(?:' + _ABBR_TOK + r')){0,2}'
    r'[ ]?\((?:N\.[ ]?S\.|O\.[ ]?S\.)\))[ ]{0,2},?[ ]{0,2}(\d{1,4})' + _PAGE_END)
_CITE_UNREPORTED_BEFORE = re.compile(
    r'(?<![\w/])()(\d{1,2}[ \t]+[A-Z][a-z]{2,8}\.?[ \t]+(?:1[89]|20)\d{2})[ \t]*,[ \t]*\(?[Uu]nreported\)?(?![A-Za-z])')

                                                                                                         
                                                                                                   
                                                                                                
                                                                                             
                                                                                                     
                                
                                                                                                     
                                                                                                     
                                                                                                     
                                                                               
                                                                                            
                                                                                                    
                                       
                                                                                                 
                                                                                                 
                                                                                               
                                                                                                
                                                                                                  
                                                                                                   
                                                                                                 
                                                                                                   
                                                                                                    
                                                                                                   
                                                                                                  
                                                                                                     
                                                                                                
                                                                                                
                                                                                                
                                                                                                     
import os as _os
_CD_ON = _os.environ.get("JR_CIT_DATE", "1") != "0"
_CD_S = r"[ \t\u00a0]"
_CD_D = r"[-\u2010\u2011\u2012\u2013\u2014\u2212]"
_CD_MON = (r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
           r"Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)")
_CD_DMY = r"\d{1,2}(?:st|nd|rd|th|d)?" + _CD_S + _CD_MON + r"\.?,?" + _CD_S + r"(?:1[6-9]|20)\d{2}"
_CD_MDY = _CD_MON + r"\.?" + _CD_S + r"\d{1,2}," + _CD_S + r"(?:1[6-9]|20)\d{2}"
_CD_USNO = (r"(?:\d:)?\d{2}" + _CD_D + r"(?:cv|cr|mc|CV|CR|MC)" + _CD_D + r"\d{1,6}(?:" + _CD_D + r"[A-Za-z]{2,5})*"
            r"|\d:\d{2}(?:CV|CR)\d{3,6}|CV" + _CD_S + r"\d{2}" + _CD_D + r"\d{3,6}(?:" + _CD_S + r"[A-Z]{2,4})?"
            r"|\d{2}" + _CD_D + r"\d{2,6}")
_CD_PATTERNS = [
                                                                                                   
                           
    ("cd_dock_us", re.compile(
        r"\b(?:Case" + _CD_S + r"|Civ\." + _CD_S + r"(?:Action" + _CD_S + r")?)?Nos?\.?" + _CD_S + r"?(" + _CD_USNO + r")"
        r"(?:" + _CD_S + r"etc\.)?" + _CD_S + r"\(((?:[A-Z][A-Za-z0-9.]*" + _CD_S + r"?){1,4}),"
        + _CD_S + r"(" + _CD_MDY + r")\)"), "cd", "USA"),
                                                                                                 
                                              
    ("cd_dock_usb", re.compile(
        r"\(((?:[A-Z][A-Za-z.]*" + _CD_S + r"?){1,3}),"+ _CD_S + r"Case" + _CD_S + r"No\.?" + _CD_S + r"?(" + _CD_USNO + r"),"
        + _CD_S + r"(" + _CD_DMY + r")\)"), "cd", "USA"),
                                                        
    ("cd_dock_sg", re.compile(
        r"(?<![\w/])((?:Suit|Criminal" + _CD_S + r"(?:Appeal|Motion|Case)|Civil" + _CD_S + r"Appeal|Magistrate[’'`]?s"
        + _CD_S + r"Appeal|District" + _CD_S + r"Court" + _CD_S + r"Appeal|DC" + _CD_S + r"Appeal|Appeal|Originating"
        + _CD_S + r"(?:Summons|Motion))" + _CD_S + r"No\.?" + _CD_S + r"?[A-Z]{0,3}\d{1,7}(?:" + _CD_S + r"of" + _CD_S
        + r"(?:1[89]|20)\d{2}|/(?:1[89]|20)?\d{2})"
        r"|(?:DAC|MAC|MA|D|HC/CC|HC/S)" + _CD_S + r"?\d{1,7}/(?:1[89]|20)?\d{2})"
        r"\)?" + _CD_S + r"?(?:," + _CD_S + r"?|" + _CD_S + r"?[–—-]" + _CD_S + r"?|" + _CD_S + r"?\(|" + _CD_S
        + r")(?:as" + _CD_S + r"yet" + _CD_S + r")?[Uu]nreported\b"), "cd", None),
    ("cd_dock_sg", re.compile(
        r"(?:\(|^)[Uu]nreported," + _CD_S + r"((?:Suit|Originating" + _CD_S + r"(?:Summons|Motion)|Civil" + _CD_S
        + r"Appeal|Criminal" + _CD_S + r"Appeal)" + _CD_S + r"No\.?" + _CD_S + r"[A-Z]?\d[\d-]{1,14}(?:" + _CD_S
        + r"of" + _CD_S + r"(?:1[89]|20)\d{2})?)(?:\)|$)"), "cd", None),
                                                                     
    ("cd_dock_sgd", re.compile(
        r"(?<![\w/])((?:HC|SC|DC|MC)/[A-Z]{1,4}" + _CD_S + r"\d{1,6}/(?:19|20)\d{2}|(?:Magistrate[’'`]?s" + _CD_S
        + r"Appeal|Criminal" + _CD_S + r"(?:Appeal|Case)|Suit)" + _CD_S + r"No\.?" + _CD_S + r"\d{1,6}" + _CD_S + r"of"
        + _CD_S + r"(?:19|20)\d{2})" + _CD_S + r"\((" + _CD_DMY + r")\)"), "cd", None),
                                                                                                       
                           
    ("cd_dock_ca", re.compile(
        r"(?<![\w.])((?:[A-Z][A-Za-z]{0,4}\.\s?){1,5}(?:[ ]?[A-Z][a-z]{2,})?),\s(?:[A-Z][a-z]+\s)?(?:File\s|Reg\.\s)?"
        r"No\.\s?([A-Z]?\d[" + _CD_D[1:-1] + r"\d/]{1,12}\d),\s(" + _CD_MDY + r")"), "cd", "CAN"),
                                                                             
    ("cd_dock_ca2", re.compile(
        r"(?<![\w.])((?:[A-Z]\.){2,5}),\s(" + _CD_MDY + r"),\s[A-Z][a-z]+\s([A-Z]{0,2}" + _CD_D + r"?\d{3,7}(?:"
        + _CD_D + r"\d{2,4}){0,2})\b"), "cd", "CAN"),
                                                                                                   
                                                                                                     
    ("cd_dock_int", re.compile(
        r"\bCase" + _CD_S + r"No\.?" + _CD_S + r"?((?:IT|ICTR)-\d{2}-\d{1,3}(?:/\d)?(?:-[A-Z]{1,3}|/[A-Z]{1,2})?)"
        r"(?:" + _CD_S + r"\d{1,3})?," + _CD_S + r"(?:[Jj]udgment" + _CD_S + r"of" + _CD_S + r")?(" + _CD_DMY + r")"),
        "cd", "OTHER"),
    ("cd_dock_int2", re.compile(
        r"(?<![\w/])(" + _CD_DMY + r")," + _CD_S + r"Case" + _CD_S + r"No\.?" + _CD_S
        + r"?((?:IT|ICTR)-\d{2}-\d{1,3}(?:/\d)?(?:-[A-Z]{1,3}|/[A-Z]{1,2})?)"), "cd", "OTHER"),
                                                                                                     
    ("cd_dock_tr", re.compile(
        r"(?<![\w/])(" + _CD_DMY + r")," + _CD_S + r"(?:CA|Court" + _CD_S + r"of" + _CD_S + r"Appeal)" + _CD_S
        + r"(?:\(Civil" + _CD_S + r"Division\)" + _CD_S + r")?Transcript" + _CD_S + r"No\.?" + _CD_S
        + r"(\d{1,4}/\d{2,4})"), "cd", "UK"),
                                                                                           
    ("cd_jo", re.compile(
        r"(?:Eur\.?" + _CD_S + r"?Court" + _CD_S + r"?H\.?" + _CD_S + r"?R\.?|European" + _CD_S + r"Court" + _CD_S
        + r"of" + _CD_S + r"Human" + _CD_S + r"Rights|ECtHR|\bGC|Grand" + _CD_S + r"Chamber)\)?,?" + _CD_S
        + r"(?:\(GC\),?" + _CD_S + r")?[Jj]udgment" + _CD_S + r"of" + _CD_S + r"(" + _CD_DMY + r")"
        r"|[Jj]udgment" + _CD_S + r"of" + _CD_S + r"the" + _CD_S + r"European" + _CD_S + r"Court(?:" + _CD_S + r"of"
        + _CD_S + r"Human" + _CD_S + r"Rights)?" + _CD_S + r"of" + _CD_S + r"(" + _CD_DMY + r")"
        r"|[Jj]udgment" + _CD_S + r"of" + _CD_S + r"(" + _CD_DMY + r")(?=,?" + _CD_S + r"\(?GC\b|" + _CD_S
        + r"\(Grand" + _CD_S + r"Chamber\))"), "cd_court", "ECHR"),
                                                                                        
    ("cd_unrep_in", re.compile(
        r"\([Uu]nreported," + _CD_S + r"([A-Z](?:[^()\n\d]|\([A-Za-z]{1,6}\)){1,90}?)," + _CD_S + r"(" + _CD_DMY + r")\)"),
        "cd_court", None),
                                                                                                       
                
    ("cd_unrep_dt", re.compile(
        r"(?<![\w/])(" + _CD_DMY + r")" + _CD_S + r"?,?" + _CD_S + r"?(?:\((?:as" + _CD_S + r"yet" + _CD_S
        + r")?[Uu]nreported\)|[Uu]nreported(?:\)|(?![A-Za-z])))"), "cd_court", None),
] if _CD_ON else []
                                                                                               
                                                                                                 
                                                                            
_CD_AU_WIDE = re.compile(
    r'\bunreported,?\s+'
    r'((?:[A-Z][A-Za-z]+\s+){0,4}(?:Court|Tribunal|Commission)'
    r'(?:\s+(?:of|for)\s+(?:the\s+)?[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2}){1,4})'
    r'(?:\s*\([^)\n]{0,80}\))?'
    r'[^;\n]{0,40}?,\s*'
    r'(\d{1,2}\s+[A-Z][a-z]+\s+(?:19|20)\d{2})', re.I)

                                                                 
                                                                                 
_HK_CODE = (r'(?:CACC|CACV|CAAR|CAMP|CAQL|HCMA|HCAL|HCCL|HCCC|HCAJ|HCMP|HCCW|HCB|HCA|DCCC|DCCJ|DCMP|FACV|FACC|FAMV|FAMC|FAMP|ESCC|ESS|FCMC|FLCC|FLS|KCCC|KCS|KTCC|KTS|LDCS|LDMR|STCC|STS|TMCC|TMS|WKCC|WKS|'
                                                                                                            
                                                                                                       
            r'HCPI|HCCT|HCMC|HCAP|HCIA|HCLA|DCEC|FCJA|NKCC|TWCC|TWS)')
_HK_DOCKET = re.compile(
    r'(?<![A-Za-z])(' + _HK_CODE + r'|Crim[.]?[ \t]+App[.]?|Magistrate[\u2019\x27]s[ \t]+Appeal)'
    r'[ \t]*(?:Nos?[.]?[ \t]*)?(\d{1,7}(?:[ \t]*(?:,|and|&)[ \t]*\d{1,7})*)'
    r'[ \t]*(?:/[ \t]*|[ \t]+of[ \t]+)((?:19|20)?\d{2})\b', re.I)
_HK_MP = re.compile(r'\b((?:19|20)\d{2})[ \t]+(MP)[ \t]+No[.]?[ \t]*(\d{1,7})\b',re.I)
_HK_PATTERNS = [('cd_hk', _HK_DOCKET, 'cd', 'HK'),
                ('cd_hk_year', _HK_MP, 'cd', 'HK')]


def _hk_ids(name, groups):
    if name == 'cd_hk_year':
        year, code, nums = groups
    else:
        code, nums, year = groups
    code = re.sub(r'[^A-Z]', '', code.upper())
    code = {'CRIMAPP': 'CACC', 'MAGISTRATESAPPEAL': 'HCMA'}.get(code, code)
    if len(year) == 2:
        year = ('19' if int(year) >= 50 else '20') + year
    return tuple(sorted(code + str(int(n)) + '/' + year for n in re.findall(r'\d+',nums)))


class _HKContext:
    """Per-call docket aliases and header identity; no cross-judgment mutable state."""
    def __init__(self, text, header=None):
        self.header = header if header is not None else (text.split('CORE JUDGMENT',1)[0]
                      if 'HEADNOTES' in text else '')
        self.header_end = text.find('CORE JUDGMENT') if 'HEADNOTES' in text else 0
        self.own = set()
        for m in _HK_DOCKET.finditer(self.header):
            self.own.update(x for x in _hk_ids('cd_hk',m.groups()) if x.startswith('FA'))
                                                                             
                                                                                
                                                                               
        for pm in re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*', text):
            para = pm[0]
            direct = re.search(r'\bleave\b[^.;\n]{0,100}\b(?:this|the present) appeal\b|'
                               r'\b(?:this|the present) appeal\b[^.;\n]{0,100}\bleave\b', para, re.I)
                                                                                                                       
            certified = re.search(r'\bleave to appeal\b[^.;\n]{0,80}\b(?:granted|refused|certified)\b[^.;\n]{0,40}\bAppeal Committee\b|'
                                  r'\bAppeal Committee\b[^.;\n]{0,80}\b(?:granted|refused)\b[^.;\n]{0,40}\bleave\b', para, re.I)
            grant = re.search(r'\b(?:leave to appeal|leave)\b.{0,100}\b(?:granted|refused)\b|\b(?:granted|refused)\b.{0,100}\bleave\b', para, re.I)
            if not (certified or (direct and grant and re.search(r'Appeal Committee|this Court',para))):
                continue
            spans = [para]
            for call in re.finditer(r'\[(\d{1,3})\]', para):
                note = re.search(r'(?m)^\['+call[1]+r'\][^\n]*(?:\n(?!\n)[^\n]+)*',text)
                if note: spans.append(note[0])
            leave_ids = set()
            for span in spans:
                for m in _HK_DOCKET.finditer(span):
                    leave_ids.update(x for x in _hk_ids('cd_hk',m.groups())
                                     if x.startswith(('FAMV','FAMC','FAMP')))
                                                                           
                                                                                   
            if len(leave_ids) == 1:
                self.own.update(leave_ids)
        self.parent = {}
        self.events = []
        def union(ids):
            roots = sorted({self.root(x) for x in ids})
            for x in roots[1:]: self.parent[x] = roots[0]
        for name, pat, _form, _fixed in _HK_PATTERNS:
            for m in pat.finditer(text):
                ids = _hk_ids(name,m.groups())
                union(ids)
                self.events.append((m.start(),m.end(),ids))
        self.events.sort()
                                                                                  
                                                                                 
        for a,b in zip(self.events,self.events[1:]):
            gap = text[a[1]:b[0]]
            if re.fullmatch(r'[ \t,;]*(?:(?:and|&|consolidated with)[ \t]*)?',gap,re.I):
                union(a[2]+b[2])
                                                                                   
        below = {}
        for m in _HK_DOCKET.finditer(self.header):
            line = self.header[self.header.rfind('\n',0,m.start())+1:m.start()]
            if re.search(r'\bFROM\b',line,re.I):
                ids = _hk_ids('cd_hk',m.groups())
                below.setdefault(re.sub(r'\d.*','',ids[0]),[]).extend(ids)
        for ids in below.values(): union(ids)
        self.dates = {}
        self.at_date = {}
        for s,e,ids in self.events:
            if s < self.header_end:
                continue
            tail = text[e:e+150].split('\n\n',1)[0]
            date = re.search(_CD_DMY,tail,re.I)
            if date:
                key = self.root(ids[0]); value = _cd_date(date[0])
                self.at_date[s] = value
                self.dates.setdefault(key,[])
                if value not in self.dates[key]: self.dates[key].append(value)

    def root(self,x):
        while x in self.parent: x = self.parent[x]
        return x

    def fields(self,name,m):
                                                                              
        year, rep, vol, _number = _cd_fields(name, m.groups())
        ids = _hk_ids(name,m.groups()); root = self.root(ids[0])
        dates = self.dates.get(root,[])
                                                                             
                                                                                
        number = root + ('@' + self.at_date.get(m.start(),dates[0]) if len(dates)>1 else '')
        return year, rep, vol, number

    def reject(self,name,m,text):
        ids = _hk_ids(name,m.groups())
        if any(x in self.own for x in ids): return True
        if m.start() < self.header_end:
            line = text[text.rfind('\n',0,m.start())+1:m.start()]
            if not re.search(r'\bFROM\b',line,re.I): return True
        para = text[max(0,text.rfind('\n\n',0,m.start())):text.find('\n\n',m.end()) if '\n\n' in text[m.end():] else m.end()+250]
        foot = re.search(r'(?m)^\[(\d{1,3})\][^\n]*$',text[text.rfind('\n',0,m.start())+1:m.end()])
        if foot:
                                                                         
                                                                            
            for p in text[:m.start()].split('\n\n'):
                if '[' + foot[1] + ']' in p and re.search(r'\bsettled\b',p,re.I):
                    return True
                                                                                 
        return bool(re.search(r'\b(?:instituted|commenced|settled)\b',para,re.I)
                    and not re.search(r'\b(?:judgment|decided|decision|ordered|held)\b',para,re.I))


def _hk_mask_parallel(text):
                                                                                  
    text = re.sub(r"Lloyd[\u2019\x27`]s[ \t]+(?:Reinsurance[ \t]+Law[ \t]+Reports|Rep[.]?[ \t]+IR)\b",
                  lambda m: "Lloyd's Rep IR".ljust(len(m[0])), text)
    return re.sub(r'(?im)^Parallel Citation:[^\n]*',lambda m:' '*len(m[0]),text)


def _hk_finish(counter, text, hk):
    """Resolve a FROM docket to its explicitly reported decision below.

    Require a procedural Court of Appeal paragraph and a Hong Kong report,
    following an explicit footnote callout when the report is in a footnote.
    A judgment delivered in parts may still have several reported decisions;
    only the first is the alias of the otherwise undifferentiated caption.
    """
    result = counter.finish(text)
                                                                                                         
                                                                                                       
                                                                                                            
    for r in [x for x in result if x[3][1] == "ECHRAPP"]:
                                                                                        
        for e in [r[1]] + [e_ for _s, e_, k_ in counter.dups if k_ == r[3]]:
            m = re.match(r"[ ]?(?:v\.?|against)[ ](?:the[ ])?[A-Z][A-Za-z]+(?:[ ][A-Z][A-Za-z]+){0,2}[ ,]*\(?[ ]?", text[e:e + 60])
            if not m:
                continue
            at = [s_ for s_, _e, k_ in counter.dups if k_[1] != "ECHRAPP" and e + m.end() - 1 <= s_ <= e + m.end() + 8]
            nxt = [x for x in result if x is not r and x[3][1] != "ECHRAPP"
                   and (e + m.end() - 1 <= x[0] <= e + m.end() + 8
                        or any(k_ == x[3] and s_ in at for s_, _e, k_ in counter.dups))]
            if nxt:
                counter._alias(nxt[0][3], r[3])
                result.remove(r)
                break
    if hk is None:
        return result
    below = set()
    for m in _HK_DOCKET.finditer(hk.header):
        line = hk.header[hk.header.rfind('\n',0,m.start())+1:m.start()]
        if re.search(r'\bFROM\b',line,re.I):
            below.update(hk.root(x) for x in _hk_ids('cd_hk',m.groups()) if x.startswith(('CACV','CACC')))
    for docket in list(result):
        if docket[3][1] != 'DOCKET' or docket[3][3] not in below:
            continue
        candidates = []
        for pm in re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*',text):
            para = pm[0]
            if pm.start() < hk.header_end or not re.search(r'Court of Appeal',para,re.I): continue
            if not re.search(r'(?:\b(?:This appeal|seeks leave to appeal)\b.{0,80}\bfrom the judgment of the Court of Appeal\b|'
                             r'\bHis judgment was reversed by the Court of Appeal\b|'
                             r'\bThe Court of Appeal\b.{0,100}\bupheld the judge\b)',para,re.I): continue
            spans = [(pm.start(),pm.end())]
                                                                               
                                                                        
            ca = re.search(r'Court of Appeal',para,re.I).end()
            for call in re.finditer(r'\[(\d{1,3})\]',para[ca:]):
                note = re.search(r'(?m)^\['+call[1]+r'\][^\n]*(?:\n(?!\n)[^\n]+)*',text)
                if note: spans.append(note.span())
            candidates = [r for r in result if r[2]=='HK' and r[3][1] in {'HKLRD','HKC','HKCLR'}
                          and any(a<=r[0]<b for a,b in spans)]
            if candidates: break
        if candidates:
            report = candidates[0]
            counter._alias(report[3],docket[3])
            result.remove(docket)
                                                                                                                
                                                                                                             
                                                                                                                   
                                                                                                                 
                                                                                                              
                                                                                                                    
    if _HK_BARE_OWN_ON and not R108_ON:                                                  
        for r in list(result):
            k = r[3]
            if not (k[1] == 'HKCFA' or (k[1] == 'DOCKET' and str(k[3]).startswith(_HK_OWN_COURT))):
                continue
            if r[0] < hk.header_end:
                continue
            before = text[text.rfind('\n', 0, r[0]) + 1:r[0]]
            if _HK_LEAVE_IN.search(before):
                result.remove(r)
                continue
                                                                                                           
                                                                                                          
                                                                                                         
            call = re.match(r'[ \t]*\[(\d{1,3})\]', before)
            if not (call and _HK_BARE_LEAD.fullmatch(before)):
                continue
            for cm in re.finditer(r'\[' + call.group(1) + r'\]', text[:r[0]]):
                ls = text.rfind('\n', 0, cm.start()) + 1
                if re.match(r'[ \t]*$', text[ls:cm.start()]):
                    continue                                                                          
                sent = text[max(ls, text.rfind('. ', 0, cm.start()) + 1 if text.rfind('. ', 0, cm.start()) > ls else ls):cm.start()]
                if _HK_LEAVE_CALL.search(sent):
                    result.remove(r)
                break
    return result


_HK_BARE_OWN_ON = __import__("os").environ.get("JR_HK_BARE_OWN", "1") != "0"
                                                                                                                 
                                                                                                                    
                                                                                                                 
                                                                                                                    
                                                      
R108_ON = __import__("os").environ.get("JR_R108", "1") != "0"
                                                                                                                
                                                                                                                  
                                                                                                                 
                                                                                                                      
                                                                                                                    
                                                                                                                     
                                                                                                                     
                                                                  
R108_BARE_ON = __import__("os").environ.get("JR_BARE", "1") != "0"
_BARE_TI = None


def _bare_title_index():
    global _BARE_TI
    if _BARE_TI is None:
        import os as _o, sqlite3 as _sq
        import jr_barenames as _bn
        db = _o.environ.get("JR_TITLE_DB") or _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.dirname(
            _o.path.abspath(__file__)))), "Master_5.5.db")
        jur = {"HCA": "AU", "HKCFA": "HK", "HL 1709-1995": "UK", "HL 1996-2009": "UK", "UKSC": "UK", "MYFC": "MY",
               "NZSC": "NZ", "SCC": "CAN", "SGCA": "SG", "SGHC": "SG", "USSC": "USA"}
        pairs = []
        if _o.path.exists(db):
            con = _sq.connect("file:" + db + "?mode=ro", uri=True)
            for sh, t, i in con.execute("select j.sheet, f.value, j.id from judgment j join judgment_field f "
                                        "on f.id = j.id and f.column = 'Case'"):
                y = i.split("-")[1] if len(i.split("-")) > 2 else ""
                pairs.append((t, jur.get(sh, "OTHER"), int(y) if y.isdigit() else None))
            con.close()
        _BARE_TI = _bn.TitleIndex(pairs)
    return _BARE_TI


def _bare_names(text, spans, own_name, own_citation):
    """[(start, end, jurisdiction, display)] for the bare case names in `text` (R108b)."""
    if not R108_BARE_ON or own_name is None:
        return []
    import jr_barenames as _bn
    m = re.search(r"(?<!\d)(1[5-9]\d\d|20\d\d)(?!\d)", str(own_citation or "") + " " + str(own_name or ""))
    yr = int(m.group(1)) if m else None
    ti = _bare_title_index()
    out = []
    for disp, key, at in _bn.bare_names(text, spans, own_name=own_name):
        out.append((at, at + len(disp), ti.jurisdiction(key, yr), disp, key))
    return out
_HK_OWN_COURT = ('FAMC', 'FAMV', 'FAMP', 'FACV', 'FACC')
_HK_LEAVE_IN = re.compile(r'\bleave to appeal[ \t]+in[ \t]*$', re.I)
_HK_LEAVE_CALL = re.compile(r'\bleave\b|\bAppeal Committee\b', re.I)
                                                                                                              
_HK_BARE_LEAD = re.compile(
    r'[ \t]*(?:\[\d{1,3}\][ \t]*)?(?:(?:In|See|see)[ \t]+)?'
                                                                                                                    
    r"(?:(?:[A-Z][A-Za-z'’-]+(?:[ \t]+(?:CJ|N?PJJ?|JJ?A|JJ))?(?:[ \t]*,[ \t]*|[ \t]+and[ \t]+|[ \t]*&[ \t]*))*"
    r"[A-Z][A-Za-z'’-]+[ \t]+(?:CJ|N?PJJ?|JJ?A|JJ)[ \t]*,[ \t]*)?"
    r'(?:(?:FA(?:MC|MV|MP|CV|CC)[ \t]*(?:Nos?\.?[ \t]*)?[\d, and]+(?:[ \t]*(?:/|of)[ \t]*\d{4})?|\[\d{4}\][ \t]*HKCFA[ \t]*\d{1,4})'
    r'[ \t]*,?[ \t]*)*')


_ALL_PATTERNS = _HK_PATTERNS + [
    ("bracket",    _CITE_BRACKET,      "bracket", None),
    ("paren",      _CITE_PAREN,        "round",   None),
    ("parencomma", _CITE_PAREN_COMMA,  "round",   None),
    ("yearcomma",  _CITE_YEARCOMMA,    "round",   None),
    ("lrfull",     _CITE_LR_FULL,      "lrfull",  None),                                
    ("parennovol", _CITE_PAREN_NOVOL,  "round",   None),
                                                                                    
                                                                         
    ("morison",    _CITE_MORISON,      None,      "UK"),
                                                                               
    ("morison",    _CITE_FACCOLL_DAYFIRST, None,  "UK"),
    ("morison_abbr", _CITE_MORISON_ABBR, None,    "UK"),
    ("morison_abbr", _CITE_MORISON_M,  None,      "UK"),
                                                                            
    ("unreported_nzold", _CITE_NZ_FILE_REG,  None, "NZ"),
    ("unreported_nzold", _CITE_NZ_FILE_BARE, None, "NZ"),
    ("us",         _CITE_US,           None,      "USA"),
                                                                          
    ("us_slip",    _CITE_US_SLIP,      None,      "USA"),
                                                                      
    ("us_series",  _CITE_US_SERIES,    None,      None),
                                                                                    
    ("can_series", _CITE_CAN_SERIES,   "nominate", None),
                                                                      
    ("decision_page", _CITE_DECISION_PAGE, "nominate", None),
    ("volfirst",   _CITE_VOLFIRST,     None,      None),
    ("bareyear",   _CITE_BAREYEAR,     "bare",    None),
                                                             
    ("bareyear",   _CITE_WL,           "bare",    None),
    ("bareyear",   _CITE_OHIO,         "bare",    None),
                                                                                     
    ("air_pc",     _CITE_AIR_PC,       None,      "UK"),
    ("air_ind",    _CITE_AIR_IND,      None,      "IND"),
    ("bareyear_rep", _CITE_BAREYEAR_REP, "bare_rep", None),
    ("unreported", _CITE_UNREPORTED,   None,      "NZ"),
                                                                             
                                                                         
                                                                   
                                                                                                  
                                                                                               
    ("unreported_au", _CITE_UNREPORTED_AU, "unreported_au" if _CD_ON else None, None),
    ("newspaper",  _CITE_NEWSPAPER,    None,      "UK"),
    ("strasbourg", _CITE_STRASBOURG,   None,      "ECHR"),
    ("cjeu",       _CITE_CJEU,         None,      "EU"),
                                                                               
                                                                                          
                                                                                         
                                                                                    
                                                                                            
                                                                                        
                                       
    ("unreported_bare", _CITE_UNREPORTED_BARE, "unreported_bare", None),
                                                         
    ("unreported_bare", _CITE_UNREPORTED_AFTER, "unreported_bare", None),
    ("unreported_bare", _CITE_UNREPORTED_BEFORE, "unreported_bare", None),          
] + ([
                                                                                                   
                                                                                              
                                                                                  
    ("unreported_au", _CD_AU_WIDE, "unreported_au", None),
] + _CD_PATTERNS if _CD_ON else []) + [
    ("commissioner", _CITE_COMMISSIONER, None, "UK"),
                                                                                     
    ("nominate",   _CITE_NOMINATE_NS,  "nominate", None),                            
    ("nominate",   _CITE_SPACED,       "nominate", None),
    ("nominate",   _CITE_NOMINATE_AND, "nominate", None),
    ("nominate",   _CITE_NOMINATE,     "nominate", None),
]

                                                                                                  
                                                                                           
                                                                                                 
                                                           
                                                                                                       
                                                                                           
                                                                                                   
                                                                                                            
                                                                                                               
                                                                                                 
                                                          
                                                                                                 
                                                                                             
                                                                                        
                                                                                 
                                                                                                         
_CITREP_SERIES = (
    r"N\.[ ]?S\.[ ]?W\.[ ]?L\.[ ]?R\.(?:[ ]?\(Eq\.\))?"
    r"|S\.[ ]?R\.[ ]?\(N\.[ ]?S\.[ ]?W\.\)|S\.[ ]?R\.,[ ]N\.[ ]?S\.[ ]?W\."
    r"|Ch\.,[ ]D\."
    r"|L\.?[ ]?J\.?[ ]?\((?:Ch|K\.?[ ]?B|Q\.?[ ]?B|Ex|C\.?[ ]?P|P\.?[ ]?C|Bcy|Eq)\.?\)"
    r"|L\.[ ]J\.,[ ](?:Q\.[ ]B|K\.[ ]B|C\.[ ]P|Ch|Ex)\."
    r"|R\.[ ]?\((?:H\.[ ]?L\.|Ct\.[ ]of[ ]Sess\.)\)"
    r"|S\.,[ ]D\.,[ ]&[ ]B\.?"
    r"|Bell,[ ]Ap\.[ ]C\."
    r"|Sess\.[ ]Ca\.,?[ ][234](?:d|nd|rd|th)[ ][Ss]eries"
    r"|Court[ ]Sess\.[ ]Cas\.,[ ][234](?:d|nd|rd|th)[ ]Ser\."
    r"|H\.[ ]of[ ]L\.[ ]Ca\."
    r"|Moore,[ ]P\.[ ]?C\."
    r"|Fed\.[ ]Rep\.,[ ]2nd[ ]Series"
    r"|Paige[ ]\(New[ ]York\)")
_CITE_CITREP_QUAL = re.compile(
    r'(?<![\w.])(\d{1,3})[ ]{1,2}(' + _CITREP_SERIES + r')[ ]{0,2},?[ ]{0,2}(\d{1,4})' + _PAGE_END)
_CITE_CITREP_SA = re.compile(r'(?<![\w/])\b((?:19|20)\d{2})[ ]\((\d)\)[ ](S\.?[ ]?A\.?)[ ](\d{1,4})\b')
_CITE_CITREP_PIQR = re.compile(r'\[((?:19|20)\d{2})\][ ]()(PIQR)[ ]P(\d{1,4})\b')
_CITE_CITREP_US = re.compile(r'\b(\d{1,3})[ ](U\.[ ]S)[ ](\d{1,4})\b(?![.,]?\d)')
_CITE_CITREP_ICJ = re.compile(r'(?<![\[\w/])\b((?:19|20)\d{2})[ ](I\.?C\.?J\.?[ ]Rep\.?)[ ](\d{1,4})\b')
_CITE_CITREP_KB = re.compile(
    r'\b(?:1[89]\d{2}|20\d{2})(?:[ ]|[ ]:[ ])(\d)[ ]?(K\.[ ]?B\.|Q\.[ ]?B\.|Ch\.|A\.[ ]?C\.)(?:[ ]|[ ]:[ ])(\d{1,4})\b')
                                                                                                
                                                                                                
_CITREP_ALIAS = {
    'SR,NSW': 'SRNSW', 'CH,D': 'CHD',
    'LJ,QB': 'LJQB', 'LJ,KB': 'LJKB', 'LJ,CP': 'LJCP', 'LJ,CH': 'LJCH', 'LJ,EX': 'LJEX',
    'RCTOFSESS': 'R', 'S,D,&B': 'S', 'BELL,APC': 'BELLAPP',
    'SESSCA2DSERIES': 'D', 'SESSCA,2DSERIES': 'D', 'SESSCA3DSERIES': 'MACPH', 'SESSCA,3DSERIES': 'MACPH',
    'SESSCA4THSERIES': 'R', 'SESSCA,4THSERIES': 'R', 'COURTSESSCAS,4THSER': 'R',
    'COURTSESSCAS,3DSER': 'MACPH', 'COURTSESSCAS,2DSER': 'D',
    'HOFLCA': 'HLC', 'MOORE,PC': 'MOOPC', 'FEDREP,2NDSERIES': 'F2D', 'PAIGENEWYORK': 'PAIGE',
                                                                                                              
    'ROLLREP': 'ROLLR',
}
import os as _os_cr
if _os_cr.environ.get("ZF_NO_CITREP") != "1":
    _i_cr = [n for n, p, f, x in _ALL_PATTERNS].index("volfirst")
    _ALL_PATTERNS[_i_cr:_i_cr] = [
        ("nominate", _CITE_CITREP_QUAL, "nominate", None),
        ("us",       _CITE_CITREP_US,   None,       "USA"),
        ("bareyear_rep", _CITE_CITREP_ICJ, "bare_rep", None),
        ("nominate", _CITE_CITREP_KB,   "nominate", None),
                                                                                                
                                                                                                     
                                                                 
        ("paren",    _CITE_CITREP_SA,   "nominate", "OTHER"),                                                  
        ("bracket",  _CITE_CITREP_PIQR, "bracket",  None),
    ]

                                                                 
                                                                                            
                                                                                           
              
_PARALLEL_SEP = re.compile(
                                                                                              
                                                                                            
                                                                 
                                                                                                   
                                                                               
    r'^[ \t]*\)?[ \t]*[;,]?(?:[ \t]*,)?[ \t]*(?:\[\d{4}\][ \t]*)?'
                                                                                              
                                                                                        
                            
                                                                                        
                                                                                       
                                                                                      
                                                                                 
                                                                                
                                                                                        
    r'(?:at[ \t]+(?:pp?\.?[ \t]*)?\d{1,5}[ab]?(?:[ \t]*[-–][ \t]*\d{1,5}[ab]?)?[ \t]*)?'
                                                                                    
                                                                                      
                                          
                                                                                          
                                                                                        
                                                                                       
                                                                          
    r'\[?[ \t]*'
    r'[;,]?[ \t]*$', re.I)

                                                                               
_PINPOINT_SEP = re.compile(r'^[ 	]*,?[ 	]*at[ 	]+(?:pp?\.?[ 	]*)?$', re.I)

                                                                              
_AT_PIN = re.compile(r',\s*at\s+(?:pp?\.?\s*)?\d', re.I)

                                                                                             
                                                                                            
                                                                                     
                                                                                    
                                                                                
                                                                                
                                                                  
_PIN_CUE = re.compile(r"(?:\bat|\bante|\bpost|\bsupra|\bid\.|\bibid\.)\s*,?\s*$", re.I)
                                                                                             
                                                                                   
_PIN_REPEAT = re.compile(r"(\d{1,4})\s+([A-Za-z][A-Za-z.\s]{0,12}?)\s*(?:,\s*)?$")
                                                                                             
                                                                                            
                                                                                         
                                                                           
                                                             
                                        
                                                                                        
                                                                      
                                                                                             
                                                                                        
_PIN_AFTER_FULL = re.compile(
    r"(\d{1,4})\s+([A-Za-z][A-Za-z0-9.\s]{0,12}?)\s+(\d{1,5})"
                                                                                                       
    r"(?:\s*[-\u2013]\s*\d{1,5})?(?:\s*,?\s*(?:and\s+)?n+\.\s*\d+)?"
    r"(?:\s*,\s*\d{1,5}(?:\s*[-\u2013]\s*\d{1,5})?)?\s*,\s*(?:and\s+)?$")


                                                                                        
                                                                                        
                                                                                          
                                       
                                                                           
                                                                                           
                                                                
                                                                                    
                                                                                     
                                                                                   
                                                                                       
                                 
_TITLE_BEFORE = re.compile(
    r"(?<!\bThe )[“\"](?=[^”\"]*\s[^”\"]*\s)[^”\"]{10,180}[”\"][\s,]*$")


                                                                                                   
                                                                                                 
                                                                               
                                                                                              
                                                                                                
                                                                    
                                                                                           
                                                                                     
                                                         
                                                                                               
                                  
_TITLE_INNER = re.compile(r"[“\"]([^”\"]{10,180})[”\"][\s,]*$")


                                                                                             
                                                                                              
                                                                                              
                                                                                          
                                                       
                                                                                                               
                                                                                       
                                                                                            
_PIN_HARD = re.compile(
                                                                                               
                                                                                              
    r"(?:\b(?:[Ii]d|[Ii]bid)\.?,?\s+at|\b(?:[Aa]nte|[Pp]ost|[Ss]upra|[Ii]nfra),?\s+at|\b[Ss]upra,?\s+pp?\."
    r"|U\.\s?S\.\]?,?\s+at|\bat\s+pages?|\(pp?\.)\s*$")
                                                                                        
                                                      
_PIN_AND = re.compile(r"\bat\s+(\d{1,3})\s+U\.\s?S\.\s+\d{1,5}(?:\s?[-–]\s?\d{1,5})?\s*,?\s+and\s+$")
_PIN_NOMINATIVE = re.compile(r"\b\d{1,2}\s+(?:Dall|Cranch|Wheat|Pet|How|Black|Wall)\.\s+(\d{1,4}),\s*$")
_PIN_TELL = re.compile(
    r"\d{1,4}\s+[A-Z][A-Za-z. ]{0,14}?(?:\s+\d{1,5}(?:\s?[-–]\s?\d{1,5}|\s*,\s*n\.\s?\d)|(?<=U\.S\.),\s+\d)")
_PIN_RANGE = re.compile(
    r"\d{1,4}\s+(?:U\.\s?S\.|S\.\s?Ct\.|F\.\s?(?:2d|3d|4th)|F\.\s?Supp\.(?:\s?[23]d)?)\s+\d{1,5}\s?[-–]\s?\d")


def _article_title_before(text, start):
    """True where the citation is preceded by a quoted article title."""
    before = text[max(0, start - 220):start]
    if not _TITLE_BEFORE.search(before):
        return False
    m = _TITLE_INNER.search(before)
    if not m:
        return True
    inner = m.group(1).strip()
    core = inner.rstrip(" ,'’‘")
    if not inner[:1].isupper() and not inner[:1].isdigit():
        return False                                                        
    if core.endswith("."):
        return False                                         
    words = core.split()
    if len(words) < 3 or (words[0] == "The" and len(words) <= 3):
        return False                                         
    return True


def _pinpoint_before(text, start, vol, rep, num=None):
    """`_pinpoint_cue`, and where that finds nothing, 3 for a page reference by its FORM alone."""
    r = _pinpoint_cue(text, start, vol, rep, num)
    if r:
        return r
    if re.search(r",\s*\n\s*,\s*$|\b(?:[Aa]nte|[Pp]ost),?\s+pp?\.\s*$", text[max(0, start - 40):start]) \
            or _PIN_TELL.match(text[start:start + 60]):
        return 3
    return False


def _pinpoint_cue(text, start, vol, rep, num=None):
    """True where the words in front of a citation mark it as a page in one already given.

    (14 Oct 2026) Returns 2, not True, where the words say so OUTRIGHT (`_PIN_HARD`): such a
    reference is never an authority of its own, even where its volume is cited nowhere else
    (`consume` counts an ordinary pinpoint whose volume has not been seen)."""
    before = text[max(0, start - 40):start]
                                                                                                  
                                                                                                  
                                                                                                
                                                                                               
                                                              
    if _PIN_HARD.search(before):
        return True
    m = _PIN_AND.search(before)
    if m and vol and m.group(1) == str(vol):
        return True                                                                    
    m = _PIN_NOMINATIVE.search(before)
    if m and re.sub(r"[^A-Za-z]", "", str(rep or "")).upper() == "US" and str(num or "") != m.group(1):
        return 2                                                           
    if _PIN_CUE.search(before):
        return True
                                                                                                  
                                  
    if re.search(r"\bat\s+\d{1,5}\s?[-–]\s?\d{1,5},\s*$", before):
        return True
                                                                                                 
                                                                                               
                                                                                                 
                                                                                         
                                                                                                    
                                                                                                    
                                                                                        
                                                                                  
                                                                                               
                                                                                                
                                                                                             
                                                                                              
                                                                                          
    m = _PIN_REPEAT.search(before)
    if m and vol and m.group(1) == str(vol):
        a = re.sub(r"[^a-z]", "", m.group(2).lower())
        b = re.sub(r"[^a-z]", "", str(rep or "").lower())
        return bool(a) and a == b
    m = _PIN_AFTER_FULL.search(before)
    if m and vol and m.group(1) == str(vol):
        a = re.sub(r"[^a-z0-9]", "", m.group(2).lower())
        b = re.sub(r"[^a-z0-9]", "", str(rep or "").lower())
        if not (a and a == b):
            return False
                                                                                        
        if num is None:
            return True
        try:
            return int(re.sub(r"[^0-9]", "", str(num).split("-")[0]) or 0) >= int(m.group(3))
        except (TypeError, ValueError):
            return True
    return False

                                                                         
 
                                                                   
                                                         
 
                                                                                             
                                                                                             
                                                                                        
                                                                                            
                                                       
 
                                                                                               
                                                                                           
                                                                                              
                                                                                     
                                                                                  
                                                     
                                                                                          
                                                                                        
                                                                                        
                                                                                         
                                                                                      
                                                                                        
                                                                                       
                                                                                        
                                                                                          
                                                                                        
                                                                                               
 
                                                                                               
                                                                                               
                                                                                         
                                                                                              
                                                                                         
                                                                                         
                                                                                        
_FILENUM_SG = re.compile(
    r"\b(?:CA|HC|AD|SIC|DC|MC|FC)/(?:CCA|CAS|CA|CM|CS|OS|OA|OM|SUM|WA|RA|AS|MA|TA|CWU|"
    r"S|OSB|BC)\s?\d{1,5}/\d{4}\b")
_FILENUM_SPELLED = re.compile(
    r"\b(?:Criminal\s+(?:Motion|Appeal|Case|Revision|Reference)|Civil\s+Appeal|"
    r"Magistrate'?s?\s+Appeal|District\s+Arrest\s+Case|Originating\s+(?:Summons|Motion|"
    r"Application)|Suit|Bankruptcy\s+(?:No|Petition)|Companies\s+Winding\s+Up|"
    r"Summons\s+in\s+Chambers|Petition)\s+(?:No\.?s?\.?\s*)?\d{1,7}\s+of\s+(?:1[89]|20)\d{2}\b",
    re.I)
_FILENUM_LISTING = re.compile(r"\bCase\s+No:?\s*[A-Z]?\d{1,2}/\d{4}/\d{1,5}\b")
_FILENUM_ALL = (_FILENUM_SG, _FILENUM_SPELLED, _FILENUM_LISTING)

_DECIDED = re.compile(
    r"\b(?:was|were|is|are|had\s+been|has\s+been)\s+(?:\w+\s+){0,3}"
    r"(?:dismissed|allowed|granted|refused|struck\s+out|set\s+aside|upheld|decided|determined)"
    r"|\b(?:dismissed|allowed|granted|refused|upheld|affirmed|reversed)\s+(?:the\s+)?"
    r"(?:appeal|application|motion|summons|petition)"
    r"|\b(?:the\s+)?(?:judge|court\s+of\s+appeal|high\s+court|appellate\s+division|judge\s+"
    r"of\s+appeal|coram)\b[^.]{0,80}\b(?:held|dismissed|allowed|granted|refused|decided|"
    r"delivered|ordered)"
    r"|\b(?:decision|judgment|order|ruling)\s+(?:in|of|dated)\b", re.I)

_FILENUM_RECURS = 4                                                               


def _filenum_key(s):
    return re.sub(r"\s+", " ", s).strip().lower().rstrip(".")


                                                                                        
                                                                                           
                                                                                         
                                              
                                                                       
                                                                                            
                                                                                  
                                                                         
_FILENUM_SHORT = re.compile(
    r"([A-Z]{2,4}(?:/[A-Z]{1,4})?\s*\d+/\d{4})\s*\(\s*[“\"']\s*"
    r"([A-Z][A-Za-z/ ]{0,18}\d+)\s*[”\"']\s*\)")


                                                                                          
_OWN_STEP = re.compile(
    r"(?i)\b(?:filed|filing|commenced|issued|took\s+out|brought|lodged|"
    r"transferred\s+to|renamed|re-?named\s+as|registered\s+as|"
    r"transferred\s+to\s+the\s+[A-Za-z ]{0,40}\s+and\s+renamed)\s+"
    r"(?:[a-z]+\s+){0,3}$")


def _file_numbers(text):
    """Yield (start, end, key) for each file number that discloses a DECISION."""
    freq, raw = {}, []
    for pat in _FILENUM_ALL:
        for m in pat.finditer(text):
            k = _filenum_key(m.group(0))
            freq[k] = freq.get(k, 0) + 1
            raw.append((m.start(), m.end(), k))
    for m in _FILENUM_SHORT.finditer(text):
        k = _filenum_key(m.group(1))
        if k in freq:
                                                                                      
                                                                     
            short = r"\s+".join(re.escape(w) for w in m.group(2).split())
            freq[k] += len(re.findall(short + r"(?!\s*\d*/)", text)) - 1
                                                                                             
                                                                                            
                                                                                    
                                                                                             
    own = {k for s, _e, k in raw if _OWN_STEP.search(text[max(0, s - 90):s])}

    for start, end, k in raw:
        if k in own:
            continue
        if freq[k] >= _FILENUM_RECURS:
            continue
                                                                                         
                                                                                           
                                                                                         
                                                                                      
                                                                                         
                                                                                         
                                                                                           
                                                                        
        if not _DECIDED.search(text[max(0, start - 160):end + 160]):
            continue
        yield start, end, k


_RESIDUE_BAD = re.compile(r"[^;,:\s\[\]().–—\-0-9A-Za-z]")
_RESIDUE_WORD = re.compile(r"[A-Za-z]+")
_RESIDUE_MAX = 300                                                                      


                                                                                 
                                                                                      
                                                                                         
                                                             
 
                                                                               
                                                                                      
                                                                                   
                                                                                       
                                                                                         
                                                                                
                                                                                                               
                                                                                                       
_FOOTNOTE_MARK = re.compile(r"\[\d{1,3}\]|\([ \t]+[a-z]{1,2}[ \t]+\)|(?:^|\n)[ \t]*\([a-z]{1,2}\)")


                                                                                          
                                                                  
                                                                                 
                                                                            
                                                                                           
                                                                                           
                                                                                            
_PER_JUDGE = re.compile(
    r"(?i)\bper\s+(?:[A-Z][A-Za-z'’-]+(?:\s*,\s*|\s+and\s+|\s+)){1,6}"
    r"(?:JJ|J|CJ|LJJ|LJ|JA|P|A-CJ|ACJ)\b")


                                                                                    
_PINPOINT_PARA = re.compile(
    r'(?:\bat\s+)?\d{1,5}(?:\s*[-–]\s*\d{1,5})?\s*\[\d{1,3}\](?:\s*[-–]\s*\[\d{1,3}\])?'
                                                                                                         
                                                                                          
    r'|\bat\s+\[\d{1,3}\](?:\s*[-–]\s*\[\d{1,3}\])?')


                                                                                  
                                                                                     
                                                                                   
                                                                                
                                                                               
_NOMINATE_FRAG = re.compile(r'(?:\((?:1[5-9]|20)\d{2}\)\s*)?\d{1,4}\s+[A-Z][A-Za-z.\x27&]*(?:\s*,?\s+[A-Za-z.\x27&()]+){0,3}\s*,?\s+\d{1,5}[a-z]?')

                                                                                    
                                                                                    
_CASE_NAME_IN_RESIDUE = re.compile(r'\s[vV]\.?\s')


                                                                                        
                                                                                       
                                                                                          
                                                                                       
                                                  
                                                                                      
                                                                                       
                                                          
                                                                      
                                                                                          
                                                                                        
                                                                                          
                       
_RESIDUE_OK_WORDS = frozenset({"at", "p", "pp", "fn", "n", "note", "notes", "col",
                               "para", "paras", "and", "ff",
                                               
                               "qb", "kb", "ch", "admin", "comm", "tcc", "pat", "fam",
                               "ipec", "costs", "mercantile", "admlty", "qbd", "chd",
                                                                                           
                                                                                         
                                                                                          
                                                                                        
                                                                                    
                                                                                      
                                                                              
                               "ql", "wl", "lexis", "canlii", "soquij",
                                                                                
                               "can"})
                                                                                              
                                                                                               
                                                                                                
_QL_IN_CHAIN = re.compile(
    r"\[(?:19|20)\d{2}\][ \t]*(?:[A-Z]\.){1,5}[ \t]*(?:No\.|n[ \t]?o)[ \t]*\d{1,6}[ \t]*\(QL\)[ \t]*,?"
                                                                                  
    r"|\b(?:19|20)\d{2}[ \t]CLLC[ \t]¶?[ \t]?\d{3}[-‐‑]\d{3}[ \t]*,?")

                                                                                           
_DB_TAG_IN_CHAIN = re.compile(r"\[(?:19|20)\d{2}\][ \t]*AZ[-‐‑]\d{6,10}[ \t]*,?")
                                                                                               
_CAN_CHAIN_MARK = re.compile(r"\(QL\)|\bW\.[ ]?A\.[ ]?C\.|\bA\.[ ]?P\.[ ]?R\.")
_CAN_CHAIN_KEY = re.compile(r"^CARSWELL|JNO$|^WAC$|^APR$")
_EWHC_DIV = re.compile(
    r"^[ \t]*\((?:QB|KB|Ch|Admin|Comm|TCC|Pat|Fam|IPEC|Admlty|Costs|Mercantile|QBD)\)")
_BAREYEAR_SET = frozenset(c.upper() for c in _BAREYEAR_COURTS)
                                                                                    
_L2D_LONE = frozenset({"HCA", "UNREP", "FCA", "FCAFC", "NSWCA", "NSWSC", "VSC", "VSCA", "QCA",
                       "QSC", "WASC", "WASCA", "SASC", "ENGR", "UKHL", "UKPC"})


def _residue_word_ok(w):
    return len(w) == 1 or w.lower() in _RESIDUE_OK_WORDS


def _residue_is_parallel(s):
    """True when the residue between two citations is only punctuation, digits and at/p/pp."""
    if s is None or len(s) > _RESIDUE_MAX:
        return False
                                                                                       
                  
                                                                          
                                                                                          
                                                                                           
                                                                                         
                                                                        
    s = _DB_TAG_IN_CHAIN.sub(" ", s)                                                   
    s = _QL_IN_CHAIN.sub(" ", s)                                                    
    s = _PINPOINT_PARA.sub(" ", s)
    if _FOOTNOTE_MARK.search(s):
        return False                                                                        
    s = _PER_JUDGE.sub(" ", s)                                                    
                                                                                   
                                                         
                                                                                        
                                                                                    
                                             
                                                                                       
                                                                                        
                                                                                      
                                   
     
                                                                                    
                                                                                 
                                                                                  
    if _CASE_NAME_IN_RESIDUE.search(s): return False
    s = _NOMINATE_FRAG.sub(' ', s)
    if _RESIDUE_BAD.search(s):
        return False
    return all(_residue_word_ok(w) for w in _RESIDUE_WORD.findall(s))

                                                                                              
                                                                                
_CASE_NAME = re.compile(r"[A-Z][A-Za-z'’.&\-]+(?:\s+[A-Za-z'’.&\-]+){0,6}\s+v\.?\s+[A-Z]")
_NAME_WINDOW = 160


                                                                                         
                                                                                             
                                                                           
 
                                                                                             
                                                              
                                                                       
                                                                      
                                                                                               
 
                                                                                           
                                                                                            
                                                          
_REPORTER_ALIAS = {
    'VENTRIS': 'VENT',                   
    'B&ALD': 'B&A',                                   
    'B&ADOL': 'B&AD',                                 
    'BING NC': 'BINGNC',                             
    'MOOPCCNS': 'MOOPCNS',                                               
    'ELL&BL': 'EL&BL',                             
    'BOS&PNR': 'BOS&P',                                          
                                                                                                
                                                                                                   
    'RCS': 'SCR',
    'LLOYDSREPORTS': 'LLOYDSREP',                                                         
                                                                                                 
                                                                                        
    'CD': 'CHD',
    'OKL': 'OKLA',
    'CDK': 'DOCKET',                                                                                
    'CDKI': 'DOCKET',
}
if _os_cr.environ.get("ZF_NO_CITREP") != "1":                                              
    for _k_cr, _v_cr in _CITREP_ALIAS.items():
        _REPORTER_ALIAS.setdefault(_k_cr, _v_cr)


                                                                                           
                                                                                              
                                                                                        
                                                                                         
                                                                                          
                                                                 
_COMMA_PAGINATED = {"ATC", "BPR", "CCH", "ATR", "AITR", "ATPR", "ACLC"}


def _page_of(reporter_key, number):
    """The page, with a comma read as a separator only where the series warrants it."""
    num = str(number or "")
    if "," in num and str(reporter_key or "") not in _COMMA_PAGINATED:
        num = num.split(",")[0]
    return re.sub(r"[,\s]", "", num)


def _norm_key(year, reporter, volume, number):
    """L1 key. Dots and spacing are cosmetic; the volume is NOT --
    [1998] 1 WLR 100 and [1998] 2 WLR 100 are different cases."""
                                                                                         
                                                                                        
                                                                                     
                                                                                     
                                                                                     
                                                    
    rep = re.sub(r'[.()\s\u2019\x27`]', '', str(reporter or '')).upper()                                  
    rep = _REPORTER_ALIAS.get(rep, rep)
                                                                                           
                                                                                        
                                                                                          
                                                                                           
                                   
    num = _page_of(rep, number)
                                                                                        
                                                                                             
                                                                                            
                                                                                     
                                                                                          
                                                                                  
    yr = re.sub(r'[\u2010-\u2015\u2212]', '-', str(year or ''))
                                                                                            
                                                                                          
                                                                                                   
                                                                                                 
                                                                                           
                                                                                               
                                                                                                 
                                                                              
    if not yr and not volume and rep not in _NEWSPAPER_KEYS:
        _d = _DATE_KEY.match(num)
        if _d:
            return ('', 'UNREP', '', _d.group(1).lstrip('0') + _d.group(2)[:3].lower() + _d.group(3))
    return (yr, rep, str(volume or ''), num)


_NEWSPAPER_KEYS = frozenset({'THETIMES', 'INDEPENDENT', 'GUARDIAN', 'DAILYTELEGRAPH', 'FINANCIALTIMES'})
_DATE_KEY = re.compile(r'^(\d{1,2})([A-Za-z]{3,9})\.?((?:1[6-9]|20)\d{2})$')


                                                                                       
                                                                                         
                                                                                           
                                                                                 
                                                                                           
                                                                                   
_PERIODICAL = re.compile(r"(?i)JOURNAL|REVIEW|QUARTERLY")


def _is_plausible_authority(key):
    """False for a citation no law report could carry."""
    try:
        year, rep, _vol, _num = key
    except (TypeError, ValueError):
        return True
    y = str(year or "")
                                                                                           
    if y.isdigit() and (int(y) < 1500 or int(y) > 2100):
        return False
    r = str(rep or "")
    if len(r) > 24 or _PERIODICAL.search(r):
        return False
    return True


class _Counter:
    """Collects citations with the three dedup levels applied."""

    def __init__(self):
        self.spans = []                                                             
        self.keys = set()
        self.vols = set()                                                           
        self._rvn = set()                                                                
        self.kept = []                                                
                                                                                          
                                                                                           
                                                                                             
                                                                                         
        self.at_span = {}                    
        self.aliases = {}                                                        
                                                                             
                                                                             
                                                                   
        self._merged_into = {}
                                                                                           
                                                                                           
                                                                                      
                                                                                          
                                                                              
        self.pins = []                                    
        self.pinned = {}                                                              
                                                                                                
                                                                                                   
        self.dups = []
        self._rvn_key = {}                                                                      
                                                                                           
        self.promoted = set()
        self._lr_legacy = {}                                                                    

    def overlaps(self, start, end):
        return any(start < e and end > s for s, e in self.spans)

    def bridge(self, start, end):
        """Record a span that is NOT an authority but must not leave a hole.

        A database accession number sits between a case citation and its parallel.
        It is not counted, but the parallel test cuts consumed spans out of the gap
        before asking whether the remainder is punctuation, so the span has to be on
        the record even though the authority is not.
        """
        self.spans.append((start, end))

    def consume(self, start, end, juri, key, form, pinpoint=False):
        """Record the span whatever happens to the match.

        Recording on the discard path is the whole point. Skipping a duplicate without
        recording its span leaves a hole that a narrower pattern matches inside, which is
        how repeats were silently re-counted.

        L1b -- A PINPOINT IS NOT AN AUTHORITY. '(1964) 376 US, at p 228' is a page reference
        back to '(1964) 376 US 225', already counted. The two differ in the number, so the L1
        key does not catch it, and L2b only merges the pair when they happen to fall next to
        each other -- yet a judge typically pinpoints a case pages after first citing it. In
        Parkdale that left the United States column reading 8 where the judgment cites 5.
        So a citation written as a pinpoint counts only if its volume has not been seen."""
        if self.overlaps(start, end):
            return False
        self.spans.append((start, end))                                                
        self.at_span.setdefault(start, key)
                                                                                    
                                                                         
        if not _is_plausible_authority(key):
            return False
        if pinpoint and pinpoint != 3 and (pinpoint == 2 or key[:3] in self.vols):
                                                                                               
                                                                                                
            self.pins.append(key)
            return False                                                                     
        if pinpoint and key not in self.keys:
            self.promoted.add(key)                                                       
        if key in self.keys:
            self.dups.append((start, end, key))                                             
            if form == "lrfull":
                self._lr_alias(key)                                                     
            return False                                                             
                                                                                   
                                                                                          
                                                                                             
                                                                                             
         
                                                                                       
                                                                                              
                                                                                             
                                                                                           
        if not key[0] and key[1:] in self._rvn:
                                                                                
            self.dups.append((start, end, self._rvn_key.get(key[1:], key)))
            return False
        self.keys.add(key)
        self._rvn.add(key[1:])
        self._rvn_key.setdefault(key[1:], key)
        self.vols.add(key[:3])
        self.kept.append((start, end, juri, key, form))
        self.at_span[start] = key
        if form == "lrfull":
            self._lr_alias(key)
        return True

    def _lr_alias(self, key):
        """F18: the same citation as it was read before 14 Oct 2026, `(1867) LR 2`.
        ⚠ One case only may answer to that old key: `(1867) L.R. 2 Q.B. 580` and `(1867) L.R. 2
        H.L. 149` both read `(1867) LR 2`, and sharing it made the scorer join the two cases
        (measured). The first printed keeps it, as the old reading did."""
                                                                                             
                                                                                                
                                                                                                
        legacy = (key[0], "LR", "", key[2])
        self._lr_legacy.setdefault(legacy, key)

    def _alias(self, survivor, dropped):
        """Record that `dropped` is another name for `survivor`."""
                                                                                    
                                                                                    
                                                                       
                                                           
                                                                                  
                                                                                   
                                                                                    
                                                                                   
                                                                              
                  
        seen = set()
        while survivor in self._merged_into and survivor not in seen:
            seen.add(survivor)
            survivor = self._merged_into[survivor]
        if survivor == dropped:
            return
        self.aliases.setdefault(survivor, {survivor}).add(dropped)
        self._merged_into[dropped] = survivor
                                                                                   
        for k in self.aliases.pop(dropped, ()):
            self.aliases[survivor].add(k)
            if k != survivor:
                self._merged_into[k] = survivor

    def _fold(self, into, key):
        """Make `key` another name of `into` -- unless `into` already answers to `key` (it was
        merged INTO it as a parallel: `Budak v Turkey (unreported), 7 September 2004 (App No
        57345/00)`), where dropping `key` would lose the authority altogether (measured: 3)."""
        surv, seen = into, set()
        while surv in self._merged_into and surv not in seen:
            seen.add(surv)
            surv = self._merged_into[surv]
        if surv == key:
            return False
        self._alias(into, key)
        return True

    def _residue(self, text, a, b):
        """The text between a and b with every consumed citation span removed."""
        if text is None or b <= a:
            return "\x00"                                                                        
        cuts = sorted(s for s in self.spans if s[0] >= a and s[1] <= b)
        out, at = [], a
        for s, e in cuts:
            if s > at:
                out.append(text[at:s])
            at = max(at, e)
        out.append(text[at:b])
        return "".join(out)

    def finish(self, text=None):
        """L2 -- collapse a decision cited more than once in the same breath.

        Two sub-rules, and both test WHAT separates the citations, not how far apart they are.
        Distance alone is not safe: in a footnote list, consecutive footnotes are separated by
        '.\\n\\n[5] ' -- about seven characters -- so a length threshold merges different cases
        from adjacent footnotes. Measured on FCT v York Motors, a naive gap rule wrongly merged
        five unrelated pairs while catching the six real ones.

        L2a  PARALLEL FORM.  '[1946] HCA 6; (1946) 71 CLR 421' is one decision given its neutral
             citation and its report citation. The separator must be only punctuation -- a
             semicolon or comma and spaces. A newline, a full stop or a bracket means the next
             citation belongs to a different sentence or footnote, so it is a different case.

        L2b  PINPOINT.  '(1942) 1 KB 356 ... (1942) 1 KB, at p 362' is one decision cited twice,
             the second time at a page. Requires the same year, reporter AND volume, and an
             explicit pinpoint marker ('at') in between -- without the marker, two cases in the
             same volume of the same year would be merged wrongly.
        """
        self.kept.sort()
        drop = set()
                                                                                               
        if text is not None and len(text) >= 400:
            for legacy, key in self._lr_legacy.items():
                self.aliases.setdefault(key, {key}).add(legacy)
                                                                                                 
                                                                                                
                                                                                                
                                                                                                 
                                                                                           
                                                                                            
                                                                              
                                                                                              
                                  
        for i in range(len(self.kept) - 1):
                                                                                               
                                                                                               
                                                          
                                                                                
                                                                    
            s1, e1, j1, k1, _f1 = self.kept[i]
            s2, _e2, j2, k2, _f2 = self.kept[i + 1]
            if k1 == k2 or s2 < e1:
                continue
            between = text[e1:s2] if text is not None else None
            if between is None:
                continue

                                                                                                
                                                                                   
                                                                                           
                                                                                   
                                                                                               
                                                                                           
                                                                                       
                                                                                         
            named = bool(_CASE_NAME.search(text[max(0, s1 - _NAME_WINDOW):s1]))
            same_year = bool(k1[0]) and k1[0] == k2[0]
                                                                                                   
                                                                                            
                                                                                                
                          
            unrep = k1[1] == "UNREP" or k2[1] == "UNREP"
                                                                                              
                                                                                               
                                                                                                
                                                                                               
                                                                                              
                                                                                              
                                                             
                                                                                                    
                                                                                                    
            _res = self._residue(text, e1, s2)
                                                                                                   
                                                                                                   
                                                                                                   
            comma_run = bool(_res) and "," in _res \
                and not re.search(r"[;:\n]|\.\s+[A-Z]|\bat\b|\band\b", _res) \
                and str(k2[1]).upper() not in _BAREYEAR_SET \
                and bool(_CAN_CHAIN_MARK.search(_res) or _CAN_CHAIN_KEY.search(str(k2[1]))
                         or _CAN_CHAIN_KEY.search(str(k1[1])))
            if (named or same_year or unrep or comma_run) and _residue_is_parallel(_res):
                drop.add(i + 1)
                self._alias(k1, k2)
                continue

                                                                          
             
                                                                                         
                                                                                            
                                                                                               
                                                                                               
                                                                                              
                                                             
             
                                                                                              
                                                                                        
                                                                                         
                                                                                            
                                                                                    
            if len(between) > _RESIDUE_MAX:
                continue

                                                                                                 
                                                                                            
                                                                                        
            if _PARALLEL_SEP.match(_DB_TAG_IN_CHAIN.sub("", between)):
                drop.add(i + 1)
                self._alias(k1, k2)
                continue
                                                                     
                                                                                                  
                                                                                                 
                                                                    
                                                                                               
                                                                                
            if k1[1] == "EWHC" and _PARALLEL_SEP.match(_EWHC_DIV.sub("", between, 1)):
                drop.add(i + 1)
                self._alias(k1, k2)
                continue
            if k1[1] == "CJEU" and k2[1] == "CJEU" and re.match(r"[CT]-\d", str(k1[3])) \
                    and re.match(r"I{1,2}-\d", str(k2[3])) and len(between) <= 200 \
                    and not re.search(r"[.;]\s|\n\s*\n|\bCases?\s+[CT]-", between):
                drop.add(i + 1)
                self._alias(k1, k2)
                continue

                                                                                            
                                                                                           
            if j1 == j2 and k1[0] == k2[0] and k1[1] == k2[1] and k1[2] == k2[2] and k1[3] != k2[3]:
                if _PINPOINT_SEP.match(between):
                    drop.add(i + 1)
                    self._alias(k1, k2)

                                                                                              
                                                                                             
                                                                                            
                                                      
                                                                                    
                                                                                                   
                                                                                              
                                                                                                  
                                                                                              
                                                                                               
                                                                                              
                                                               
        if text is not None and self.dups:
            _dups = sorted(self.dups)
            _ds = [d[0] for d in _dups]
            _de = sorted((d[1], d[2]) for d in _dups)
            _dee = [d[0] for d in _de]
            import bisect
            for i, (s, e, _j, k, _f) in enumerate(self.kept):
                if i in drop or len(k) != 4:
                    continue
                lone = (not k[0]) and str(k[1]) in _L2D_LONE
                cands = []
                ix = bisect.bisect_left(_ds, e)
                if ix < len(_dups) and _dups[ix][0] - e <= 60:
                    cands.append((text[e:_dups[ix][0]], _dups[ix][2], False))
                ix = bisect.bisect_right(_dee, s) - 1
                if ix >= 0 and s - _de[ix][0] <= 60:
                    cands.append((text[_de[ix][0]:s], _de[ix][1], True))
                for between, dk, _after in cands:
                    if dk == k or len(dk) != 4:
                        continue
                                                                                                 
                                                                                                     
                                                                                                 
                                                                                                
                    _can = _after and str(dk[1]).upper() in _BAREYEAR_SET and not k[0]
                    if not (lone or (k[0] and k[0] == dk[0]) or _can):
                        continue
                    if _PARALLEL_SEP.match(_DB_TAG_IN_CHAIN.sub("", between)):
                                                                                             
                                                                                              
                                                                                              
                                                                                                  
                        surv, seen = dk, set()
                        while surv in self._merged_into and surv not in seen:
                            seen.add(surv)
                            surv = self._merged_into[surv]
                        if surv == k:
                            break
                        self._alias(dk, k)
                        drop.add(i)
                        break

                                                                                   
         
                                                                                       
                                                                                    
                                                                                       
                                                                                      
                                                                                   
                                                              
         
                                                                            
                                                                                     
                                               
         
                                                                              
                                                                                      
                                                                                   
                                                                 
        with_vol = {}
        for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
            if i in drop or not (k[0] and k[1] and k[2] and k[3]):
                continue
            with_vol.setdefault((k[0], k[1], k[3]), set()).add(k)
        for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
            if i in drop or k[2] or not (k[0] and k[1] and k[3]):
                continue
            cand = with_vol.get((k[0], k[1], k[3]))
            if cand and len(cand) == 1:
                self._alias(next(iter(cand)), k)
                drop.add(i)

                                                                                   
                                                                                    
                                                                           
         
                                                                               
                                                                                 
                                                                                
                                                            
        with_year = {}
        for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
            if i in drop or not (k[0] and k[1] and k[2] and k[3]):
                continue
            with_year.setdefault((k[1], k[2], k[3]), set()).add(k)
        for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
            if i in drop or k[0] or not (k[1] and k[2] and k[3]):
                continue
            cand = with_year.get((k[1], k[2], k[3]))
            if cand and len(cand) == 1:
                self._alias(next(iter(cand)), k)
                drop.add(i)
                                                                                             
                                                                                                  
                                                                                           
                                              
        by_rp = {}
        for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
            if i not in drop and len(k) == 4 and not k[0] and k[1] and k[2] in ("1", "2", "3") and k[3]:
                by_rp.setdefault((k[1], k[3]), set()).add(k)
        for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
            if i in drop or len(k) != 4 or not (k[0] and k[1] and k[3]) or k[2]:
                continue
            cand = by_rp.get((k[1], k[3]))
            if cand and len(cand) == 1:
                self._alias(next(iter(cand)), k)
                drop.add(i)
                                                                                             
                                                                                                    
                                                                                                  
                                                                                                  
                                                                                              
                                                                                        
        if text is not None:
            by_vol = {}
                                                                                             
                                                                                                
                                                                
                                                                                                 
                                                                                            
                                                                                           
                                                             
                                                                                                 
                                                                                                 
                                                                                               
                                                                                                  
                                                                                                   
                                                                                                 
                                                                                    
            for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
                if len(k) == 4 and k[1] and (str(k[2]).isdigit() or (not k[2] and k[0] and k[1] in _YEAR_VOLUME_SERIES)):
                    by_vol.setdefault((k[1], k[2] or ("y", k[0])), []).append(i)
            starts = {}
            for _s, _e, _j, k, _f in self.kept:
                starts.setdefault(k, []).append(_s)
            for _s, _e, k in self.dups:
                starts.setdefault(k, []).append(_s)
            for idxs in by_vol.values():
                if len(idxs) < 2:
                    continue

                def _p4(i_):
                    try:
                        return int(re.sub(r"[^0-9]", "", str(self.kept[i_][3][3]).split("-")[0]) or -1)
                    except (TypeError, ValueError):
                        return -1
                                                                                                    
                front = {}
                for i in idxs:
                    k = self.kept[i][3]
                    own = _front(text, self.kept[i][0])
                                                                                    
                    names = [f for f in (own,) + tuple(_front(text, s) for s in starts.get(k, ())[:6])
                             if f[0] in ("sig", "short")]
                    front[i] = (own, names)
                order = sorted((i for i in idxs if _p4(i) >= 0), key=_p4)
                for n_, i in enumerate(order):
                    if i in drop:
                        continue
                    ki, (own, _n) = self.kept[i][3], front[i]
                    usa = self.kept[i][2] == "USA"
                    flagged = ki in self.promoted
                    for j in reversed(order[:n_]):                                             
                        kb = self.kept[j][3]
                        gap = _p4(i) - _p4(j)
                        if ki == kb or gap <= 0 or (kb[0] and ki[0] and kb[0] != ki[0]) or kb in self.promoted:
                            continue
                        jn = front[j][1]
                        same = any(_same_front(own, f) for f in jn)
                                                                                             
                                                                                                
                                                                                                
                                                     
                                                                                               
                                                                                                
                                                                                                
                                                                                                      
                                                                                                  
                                                                                               
                                                                                   
                                                                                             
                                                                                                
                                                                                                       
                                                                                                  
                                                                                                
                                                                                               
                                                                                                
                                                                                                  
                                                                                               
                        yearless = not ki[0] and not any(a_[0] for a_ in self.aliases.get(ki, ()))
                        numbered = str(ki[2]).isdigit()
                                                                                                  
                                                                                              
                                                                                                    
                                                                                                     
                                                                                                  
                                                                                                   
                                                                                                 
                                                        
                                                                                                 
                                                                                                   
                                                                   
                        if own[0] in ("sig", "short") and same and numbered \
                                and ((gap <= 40 and yearless) or flagged) and self._fold(kb, ki):
                            drop.add(i)
                            break
                                       
                                                                                                    
                                                                              
                for i in idxs:
                    if i in drop or self.kept[i][3][3] != "SLIP" or front[i][0][0] != "sig":
                        continue
                    for j in order:
                        if any(_same_front(front[i][0], f) for f in front[j][1]) \
                                and self._fold(self.kept[j][3], self.kept[i][3]):
                            drop.add(i)
                            break
                                                                                                    
                                                                                                  
                                                                                        
        if text is not None:
            unrep = [i for i, c in enumerate(self.kept) if i not in drop and c[3][1] == "UNREP"]
            if unrep:
                apps = [(c[3], _name_sig(text, c[0])) for c in self.kept if c[3][1] == "ECHRAPP"]
                apps += [(k, _name_sig(text, s)) for s, _e, k in self.dups if k[1] == "ECHRAPP"]
                apps = [(k, sg) for k, sg in apps if sg]
                for i in unrep:
                    sg = _name_sig(text, self.kept[i][0]) if apps else None
                    for k, sg2 in apps:
                        if sg and sg == sg2 and self._fold(k, self.kept[i][3]):
                            drop.add(i)
                            break
                                              
        if self.promoted:
            def _pg(k):
                try:
                    return int(re.sub(r"[^0-9]", "", str(k[3]).split("-")[0]) or -1)
                except (TypeError, ValueError):
                    return -1
            firsts = {}
            for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
                                                                                                  
                                                    
                if k not in self.promoted and len(k) == 4 and k[2]:
                    firsts.setdefault(k[1:3], []).append((k[0], _pg(k)))
                                                                                              
                                                                                                  
                elif k not in self.promoted and len(k) == 4 and k[0] and k[1] and not k[2]:
                    firsts.setdefault((k[1], ("y", k[0])), []).append((k[0], _pg(k)))
            for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
                if i in drop or k not in self.promoted or len(k) != 4 or not k[2]:
                    continue
                if len(self.aliases.get(k, ())) > 1 or k in self._merged_into:
                    continue
                                                                                                   
                                                                                                
                                                                                               
                                                                         
                if text is None or not _AT_PIN.search(text[_s:_e]):
                    continue
                                                                           
                if any(0 <= p <= _pg(k) and (y == k[0] or not y or not k[0])
                       for y, p in firsts.get(k[1:3], ())) \
                        or (k[0] and any(0 <= p <= _pg(k) for y, p in firsts.get((k[1], ("y", k[0])), ()))):
                    drop.add(i)
                    self.pins.append(k)
                                                                                              
                                                                                                      
                                                                                                       
                                                                                                        
                                                                              
                                                                                                      
                                                                                                      
                                                                                                    
                                                                                   
                                                                                                  
                                                                                                    
                                                                                                  
        if text is not None and LS_P3:
            def _pg2(k):
                try:
                    return int(re.sub(r"[^0-9]", "", str(k[3]).split("-")[0]) or -1)
                except (TypeError, ValueError):
                    return -1
            for i, (_s, _e, _j, k, _f) in enumerate(self.kept):
                if i in drop or len(k) != 4 or not k[1] or _pg2(k) < 0:
                    continue
                if len(self.aliases.get(k, ())) > 1 or k in self._merged_into:
                    continue
                same = [(j, c[3]) for j, c in enumerate(self.kept) if j != i and j not in drop and len(c[3]) == 4
                        and c[3][1] == k[1] and (c[3][2] == k[2] if k[2] else (not c[3][2] and c[3][0] == k[0]))
                        and 0 <= _pg2(c[3]) < _pg2(k)]
                if LS_P3 and same:
                    mm = re.search(r"\b([A-Z][a-z]{2,})['’]s[ \t]+[Cc]ase[ \t]*\([ \t]*see[ \t]*$",
                                   text[max(0, _s - 60):_s])
                    if mm:
                        for j, kb in sorted(same, key=lambda x: -_pg2(x[1])):
                            if _pg2(k) - _pg2(kb) > 60:
                                break
                            if re.search(r"\b" + re.escape(mm.group(1)) + r"\b[^\n;]{0,12}$",
                                         " ".join(text[max(0, self.kept[j][0] - 160):self.kept[j][0]].split())) \
                                    and self._fold(kb, k):
                                drop.add(i)
                                break
        self._resolve_pins()
        return [c for i, c in enumerate(self.kept) if i not in drop]

    def _resolve_pins(self):
        """File each dropped pinpoint under the authority it is a page of.

        Two cases can share a volume -- Guest is 383 U.S. 745 and Price is 383 U.S. 787 -- so
        the volume alone does not say which. A pinpoint lies at or after the first page of
        its own report, so it belongs to the report in that volume with the LAST first page
        not beyond it: 383 U.S. 754 is Guest, 383 U.S. 803 is Price."""
        def page(k):
            try:
                return int(re.sub(r"[^0-9]", "", str(k[3]).split("-")[0]) or -1)
            except (TypeError, ValueError):
                return -1
        by_vol = {}
        for _s, _e, _j, k, _f in self.kept:
            by_vol.setdefault(k[:3], []).append(k)
        for pk in self.pins:
            pp = page(pk)
            cands = [k for k in by_vol.get(pk[:3], ()) if 0 <= page(k) <= pp]
            if not cands:
                continue
            parent = max(cands, key=page)
            seen = set()
            while parent in self._merged_into and parent not in seen:
                seen.add(parent)
                parent = self._merged_into[parent]
            if parent != pk:
                self.pinned.setdefault(parent, set()).add(pk)


def _fields(name, groups):
    """(year, reporter, volume, number) for whichever pattern matched."""
    g = groups
    if name.startswith("cd_"):
        return _cd_fields(name, g)                                              
    if name == "bracket":
                                                                     
        return g[0], g[2], g[1] or "", g[3]
    if name in ("paren", "parencomma"):
        return g[0], g[2], g[1], g[3]
    if name == "yearcomma":
        return g[0], g[2], g[1], g[3]
    if name == "parennovol":
        return g[0], g[1], "", g[2]
    if name == "lrfull":
                                                                                           
        return g[0], ("H.L." if " of " in g[2] else g[2]), g[1], g[3]
    if name in ("us", "volfirst", "nominate", "can_series", "decision_page"):
        return "", g[1], g[0], g[2]
    if name == "us_slip":
                                                                                      
        return "", g[1], g[0], "SLIP"
    if name == "cjeu":
                                                                            
        parts = [x for x in g if x]
        return "", "CJEU", "", "-".join(parts)
    if name == "strasbourg":
                                                      
        return "", "ECHRAPP", "", g[0]
    if name == "newspaper":
                                                                               
        return "", "THETIMES" if g[0] == "Times" else g[0].upper(), "", g[1]
    if name == "bareyear":
        return g[0], g[1], "", g[2]
    if name == "bareyear_rep":
        return g[0], " ".join(g[1].split()), "", g[2]
    if name == "us_series":
                                                                                      
        return "", g[1], g[0], g[2]
    if name == "morison":
                                                                                             
                                                                                     
        if g[3]:
            return g[2], "MOR", "", g[3].replace(",", "")
        return g[2], "FC", "", (g[0][:3].upper() + (g[1] or ""))
    if name == "morison_abbr":
                                                                                                  
        return "", "MOR", "", g[1].replace(",", "")
    if name == "commissioner":
                                                                                    
        return g[2], "RCOMM", g[0], g[1]
    if name == "unreported_bare":
                                                                                          
                                                                               
        return "", (g[0] or "UNREP"), "", " ".join((g[1] or "").split())
    if name in ("air_ind", "air_pc"):
                                                                                       
                                                                                   
        return g[0], "AIR", g[1], g[2]
    if name == "unreported_au":
                                                                                    
                                                                                      
                                                         
        return "", " ".join(g[0].split()), "", g[1]
                                                                                     
                                                                   
    return "", g[0], g[1], f"{g[2]}|{g[3] or ''}"


                                                                                               
_CD_MONTHS = {m: i for i, m in enumerate(
    "jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}


def _cd_date(s):
    """`March 29, 2021` / `21st May, 1958` / `7 May 1997` -> `29 March 2021` (F6's shape, so the key
    is the same `UNREP` date key whichever way the date was printed)."""
    s = " ".join(str(s or "").replace(",", " ").replace(".", " ").split())
    m = re.match(r"(\d{1,2})(?:st|nd|rd|th|d)?[ ]([A-Za-z]{3,9})[ ](\d{4})$", s) or None
    if m:
        return "%s %s %s" % (m.group(1), m.group(2), m.group(3))
    m = re.match(r"([A-Za-z]{3,9})[ ](\d{1,2})[ ](\d{4})$", s)
    if m:
        return "%s %s %s" % (m.group(2), m.group(1), m.group(3))
    return s


def _cd_docket(s):
    """A docket number as one token: dashes folded, `No` and spacing dropped, upper case."""
    s = re.sub(r"[‐-―−]", "-", str(s or ""))
    s = re.sub(r"\bNos?\b\.?", "", s, flags=re.I)
    return re.sub(r"[^A-Za-z0-9:/-]", "", s).upper()                                               


def _cd_fields(name, g):
    """(year, reporter, volume, number) for the F20 forms. Reporter `CDK` (-> `DOCKET` in
    `_norm_key`) for a docket number; `CDN[:court]` with a date, which `_norm_key` keys `UNREP`."""
                                                                                              
                                                                        
    if name.startswith("cd_hk"):
        return "", "CDK", "", "+".join(_hk_ids(name,g))
    if name == "cd_dock_us":
        return "", "CDK", "", re.sub(r"^\d:(?=\d{2}-)", "", _cd_docket(g[0]))
    if name == "cd_dock_usb":
        return "", "CDK", "", re.sub(r"^\d:(?=\d{2}-)", "", _cd_docket(g[1]))
    if name in ("cd_dock_sg", "cd_dock_sgd"):
        return "", "CDK", "", _cd_docket(g[0])
    if name == "cd_dock_int":                                                                       
        return "", "CDKI", "", _cd_docket(g[0])
    if name == "cd_dock_ca":
        return "", "CDK", "", _cd_docket(g[1])
    if name == "cd_dock_ca2":
        return "", "CDK", "", _cd_docket(g[2])
    if name == "cd_dock_int2":
        return "", "CDKI", "", _cd_docket(g[1])
    if name == "cd_dock_tr":
        return "", "CDK", "", "CATRANSCRIPT" + _cd_docket(g[1])
    if name == "cd_jo":
        return "", "CDN:European Court of Human Rights", "", _cd_date(next((x for x in g if x), ""))
    if name == "cd_unrep_in":
        return "", "CDN:" + " ".join(g[0].split()), "", _cd_date(g[1])
    return "", "CDN", "", _cd_date(g[0])                                    


                                                                                                   
                                                                                                     
                                                                                  
_CD_OFFICIAL = frozenset("collector land lands agency environmental protection president governor "
                         "sheriff mayor warden".split())
_CD_SAME = re.compile(
    r"\b(?:this|the[ ]present|the[ ]same|the[ ]instant)[ ](?:case|action|appeal|proceedings?|litigation|cause|"
    r"matter|suit)\b|\bbelow\b|\bunder[ ]appeal\b|\bappealed[ ]from\b|\bin[ ]these[ ]proceedings\b", re.I)


def _cd_reject(text, start, rep):
    """F20 (14 Oct 2026): True unless the match at `start` follows a printed case name that is not
    the judgment's own (R54 / R72)."""
    if len(text) < 600:
        return False                                                                                   
                                                                                  
    if rep == "CDKI":
        return False
    flat = " ".join(_para_before(text, start, 420).split()) + " "
    sent = re.split(r"(?<=[a-z0-9)])\.[ ]+(?=[A-Z])", flat)[-1]
    if _CD_SAME.search(sent[-220:]):
        return True
    sig = _name_sig(text, start)
    if sig is None:
                                                                                             
                                                                                               
        m = re.search(r"(?:^|[(“\"]|[.;:][ ])[ ]?((?:[A-Z][\w'’&.-]*[ ]){1,7}?(?:[\w'’&.-]+[ ]){0,2})v\.?[ ]"
                      r"((?:[\w'’&.-]+[ ]){1,6}?)[ ,]*$", _r72_chain_head(flat, "")[0])
        if m and m.group(2)[:1].isupper() and not re.search(
                r"\b(?:the|was|were|is|are|had|has|that|which|in|at)\b", m.group(2)):
            a_ = frozenset(_R72_ABBR.get(w, w) for w in _r72_tokens(m.group(1)))
            b_ = frozenset(_R72_ABBR.get(w, w) for w in _r72_tokens(m.group(2)))
            if a_ and b_:
                sig = (a_, b_, "")
    if sig is None:
        head = _r72_chain_head(flat, "")[0].rstrip(" ,([")
        m = re.search(r"\b(?:In[ ]re|Re|Ex[ ]parte)[ ]((?:[A-Z][\w'’.-]*[ ]?){1,4})$", head)
        if not m:
            return True
        ws = frozenset(_r72_tokens(m.group(1))) - _R72_GENERIC
        sides = _R72["sides"]
        return bool(not ws or (sides and ws & (sides[0] | sides[1])))
    a, b, _no = sig
    sides = _R72["sides"]
    if not sides:
        return True                                                                                      

    def _gen(ws):
        return frozenset(w for w in ws if w in _R72_GENERIC or w in _CD_OFFICIAL
                         or (re.fullmatch(r"[a-z]{2,6}", w) and w.upper() in text[max(0, start - 420):start]
                             and not re.search(r"\b%s\b" % w.capitalize(), text[max(0, start - 420):start])))
                                                                                                  
                                                                                                    
                                                                                                      
                                                                                                    
                                                                              
    for t in sides:
        for c in (a, b):
            shared = (t & c) - _gen(t & c)
            if shared and (_r72_side(t, c) or len(shared) >= 2):
                return True
    return False


class ContextRequired(ValueError):
    """Raised when a judgment cannot be classified without knowing which court is citing."""


                                                                                        
                                                                              
_NEEDS_COURT = re.compile(r'\bMLJU?\b')


                                                                                               
                                                                                         
                                                                                                 
                                                                                               
                                                                                                
                                                                                             
                                                                                             
                                                                       
                                                                                       
                                                                          
_DAMAGED_NAME_PREFIX = re.compile(r"\b\d{1,3}\s+U\.\s?S\.\s+(?=[A-Z][a-z])")


                                                                                                 
                                                                                            
                                                                                         
                                                                                             
                                          
                                                                                                
                                                                                             
                                                                                           
                                                                                                 
                                                                                               
                                                                                               
_SECTION_CUE = re.compile(
    r"(?<![A-Za-z]\.)(?<![A-Za-z.]\.[ ])"
    r"(?:\bss?|\bsections?|\bsubsections?|\bartt?|\barticles?|\bregs?|\bregulations?"
    r"|\brr?|\bparas?|\bparagraphs?|\u00a7{1,2})\s*\.?\s*$",
    re.I)


def _statute_section_before(text, start):
    """True where the number this match treats as a VOLUME is really a statute section number."""
    return bool(_SECTION_CUE.search(text[max(0, start - 18):start]))


                                                                                           
                                                                                          
                 
                                            
 
                      
                                                                                           
                                                                                         
                                                                                           
                                                                                             
                                                              
                                                                                           
                                                                           
_BROKEN_FSUPP = re.compile(r"(?<=\d F\.)[ \t]*\n\s*(?=Supp\.)")
                                                                                                 
                                                                 
                                                               
                                                                                     
                                                                                          
                                                                                              
                                                                                                
                                                                                                
                                                                                                 
                  
_WRAPPED_PAGE = re.compile(
    r"(\b\d{1,3}[ \t]+[A-Z][A-Za-z.&]*(?:[ \t][A-Z][A-Za-z.&]*){0,3}\.)([ \t]*\n[ \t]*)"
    r"(?=\d{1,4}\b)(?!\d{1,4}[ \t]+(?:Tax[ \t]Cases|-[ \t]\d))")


def _mask_damaged_prefix(text):
    """Blank `NNN U.S. ` where a NAME follows instead of a page number, and heal `F.` /
    `Supp.` split by a paragraph break. Length-preserving."""
    if not text:
        return text
    text = _BROKEN_FSUPP.sub(lambda m: " " * (m.end() - m.start()), text)
    text = _WRAPPED_PAGE.sub(lambda m: m.group(1) + " " * len(m.group(2)), text)
                                                                                           
                                                                                              
                                                                
                                                                                                 
                                                                                
                                                                                                    
                                                                                       
                                                                                              
                                                                                                
                                                                                           
                                                                                             
                                                                                                
                                                                                                
                                                                                           
                                                                                         
    if "at p" in text:
        _seen = set()

        def _promote(m):
            head = m.group(1).rstrip()
            bare = re.sub(r"^\((?:1[6-9]|20)\d\d\)[ \t]+", "", head)
            k = re.sub(r"\s+", "", head)
            if k in _seen:
                return m.group(0)
            _seen.add(k)
            if re.search(r"(?<![\w.])" + re.escape(bare).replace(r"\ ", r"[ \t]*") + r"[ \t]*,?[ \t]*(?:p\.?[ \t]*)?\d", text):
                return m.group(0)
                                                                                               
                                                                                                   
                                                                                                    
                                                                          
            _b = re.match(r"(\d{1,3})[ \t]+(.+)$", bare)
            if _b and re.search(
                    r"(?<![\w.])" + _b.group(1) + r"[ \t]+"
                    + r"[. \t]*".join(re.escape(ch) for ch in re.sub(r"[^A-Za-z]", "", _b.group(2)))
                    + r"\.?[ \t]*,?[ \t]*\d", text):
                return m.group(0)
            return (head + " " + m.group(2)).ljust(m.end() - m.start())
        text = _COMMA_AT_PAGE.sub(_promote, text)
    text = _ANGLE_YEAR.sub(lambda m: ("[" + m.group(1) + "]").ljust(m.end() - m.start()), text)
                                                                   
                                                                                                
                                                                                                 
                                                                                             
                                                                                          
                                                                                                        
    text = _VOLUME_I.sub(lambda m: m.group(1) + "1", text)
    text = _BARE_ENGR.sub(lambda m: " " * (m.end() - m.start()), text)
                                                                                                    
                                                                                                  
                                                                                 
    text = _JAMMED_VOL.sub(lambda m: m.group(2) + m.group(1), text)
                                                                                                 
                                                                                                
                                                                                                  
                                                                                            
                                                               
    text = _YEAR_RANGE.sub(lambda m: ("(" + m.group(1) + ")").ljust(m.end() - m.start()), text)
                                                                                                   
                                                                                 
                                                                        
                                                                                
                                                                        
                                          
                                                                                              
                                                                                           
                                                                                             
                                                                                        
    _t = text

    def _scr(m):
        pre = " ".join(_t[max(0, m.start() - 140):m.start()].split())
        clause = re.split(r"[.;](?=[ ])", pre)[-1]
        own = (not R108_ON) and bool(re.search(r"(?i)\bleave\b", clause)) \
            and bool(re.search(r"this[ ]Court|(?:was|were)[ ]granted|granted[ ]leave|with[ ]leave"
                               r"|pursuant[ ]to[ ]leave|application[ ]for[ ]leave", clause)) \
            and not re.search(r"[\d\])][,;]?[ ]\(?(?:application[ ]for[ ])?leave\b[^.;]*$", pre)
        if own or re.search(r"\bErratum[ ]?$", pre):
            return " " * (m.end() - m.start())
        return m.group(0)
    text = _SCR_ROMAN_ANY.sub(_scr, text)
    text = _SCR_ROMAN.sub(lambda m: m.group(1) + str(_roman(m.group(2))).ljust(len(m.group(2))), text)
                                                                                                            
                                                                                                            
                                                                                                  
                                                                                                 
                                                                
                                                                                    
                                                                 
    for _rx, _to in _OLD_REPORT_VARIANTS:
        text = _rx.sub(lambda m: (m.expand(_to)).ljust(m.end() - m.start()), text)                                             
                                                                                                            
    text = _SEC_SER_ROMAN.sub(lambda m: ("%d Sec. Ser. %s" % (_roman(m.group(1)), m.group(2))).ljust(m.end() - m.start()), text)
    return _DAMAGED_NAME_PREFIX.sub(lambda m: " " * (m.end() - m.start()), text)


_SEC_SER_ROMAN = re.compile(r"\bSecond[ \t]+Series,?[ \t]+vol\.[ \t]*([ivxl]{1,7})\.?,?[ \t]+p\.[ \t]*(\d{1,4})\b")
_OLD_REPORT_VARIANTS = [                                                                            
    (re.compile(r"(?<![\w.])(\d{1,3})[ \t]+R\.[ \t]*\(H\.[ \t]*of[ \t]*L\.\)[ \t]*(\d{1,4})\b"), r"\1 R. (H.L.) \2"),
    (re.compile(r"(?<![\w.])(\d{1,3})[ \t]+Macph\.[ \t]+p\.[ \t]*(\d{1,4})\b"), r"\1 Macph. \2"),
    (re.compile(r"(?<![\w.])(\d{1,3})[ \t]+Shaw[ \t]*(?:&|and)[ \t]*(?:D\.|Dunlop)[ \t,]*(\d{1,4})\b"), r"\1 S. & D. \2"),
    (re.compile(r"(?<![\w.])(\d{1,3})[ \t]+Robinson['’]s[ \t]+App(?:\.|eal)?[ \t]*(?:Ca(?:s|ses)?\.?)?,?[ \t]*(\d{1,4})\b"), r"\1 Rob. App. \2"),
    (re.compile(r"\bLaw[ \t]+Reports,?[ \t]+(\d{1,3})[ \t]+Appeal[ \t]+Cases,?[ \t]+(\d{1,4})\b"), r"\1 App. Cas. \2"),
]


                                                                                            
_COMMA_AT_PAGE = re.compile(
    r"((?:\((?:1[6-9]|20)\d\d\)[ \t]+(?:\d{1,3}[ \t]+)?|(?<![\w.(])\d{1,3}[ \t]+)(?:[A-Z][A-Za-z]{0,5}\.[ \t]?){1,4}),"
    r"[ \t]+at[ \t]+pp?\.?[ \t]*(\d{1,4})\b")
_ANGLE_YEAR = re.compile(r"<\s?((?:1[6-9]|20)\d{2})\s?>(?=\s*(?:\d+\s*)?[A-Z])")
_VOLUME_I = re.compile(r"(\[(?:1[89]|20)\d{2}\][ \t])I(?=[ \t](?:Ch\b|K\.?B\b|Q\.?B\b|W\.?L\.?R\b|All[ \t]E\.?R\b))")
_BARE_ENGR = re.compile(r"(?<=\d)[ \t]EngR[ \t]\d{1,5}(?=[ \t]?;)")
_LR_PREFIX = re.compile(r"(\((?:1[6-9]|20)\d{2}\)[ \t]+)(L\.?[ \t]?R\.?[ \t]+)(?=\d{1,3}[ \t]+[A-Z])")
_JAMMED_VOL = re.compile(r"(?<=\])([ \t]{1,3})(\d{1,2})(?=[A-Z][A-Za-z.]{1,9}[ \t]+\d)")
_YEAR_RANGE = re.compile(r"\(((?:1[6-9]|20)\d{2})[-–](?:\d{2}|\d{4})\)(?=\s+\d+\s+[A-Z])")
_SCR_ROMAN = re.compile(r"(\[\d{4}\]\s*\d\s+S\.\s?C\.\s?R\.\s+)([ivxl]{1,7})\b(?![.\w])")
                                                                                                
                                                                                         
_SCR_ROMAN_ANY = re.compile(r"(\[\d{4}\]\s*\d\s+S\.\s?C\.\s?R\.\s+)([ivxl]{1,7})\b(?!\w)")


def _roman(s):
    v = {"i": 1, "v": 5, "x": 10, "l": 50}
    n = 0
    for a, b in zip(s, s[1:] + " "):
        n += -v[a] if b in v and v[b] > v[a] else v[a]
    return n


def require_context(text, citing_court):
    """Refuse to guess when the answer depends on context we were not given.

    Teo Ee Hup v Syed Hussain Alkaff [1982] SGHC 10 cites five authorities, every one of them a
    Singapore decision reported in the Malayan Law Journal -- the MLJ was Singapore's own series
    before 1992. With citing_court='SGHC' the engine returns SG=5, which is right. Without it the
    engine returns MY=5, which is not merely imprecise, it is wrong on every authority in the
    judgment. There is no safe default, so there is no default.

    Independently verified for four of the five: The Happy World [1958] MLJ 155 and Ng Chik Puah
    [1962] MLJ 349 are Tan Ah Tah J, a puisne judge of Singapore who never sat in the Federation;
    Koh Chee Chong [1957] MLJ 197 is Whyatt CJ, Chief Justice of Singapore 1955-58.

    WARNING ON SOURCES. vLex Malaysia carries stub records for four of these five tagged
    'Jurisdiction: Malaysia', which is demonstrably false for the two attributed to Tan Ah Tah J.
    It is an auto-assigned database artefact applied to pre-1965 MLJ stubs, not a finding about
    the deciding court. Never treat a vLex jurisdiction tag on a pre-1992 MLJ citation as
    evidence -- it will confirm this exact error rather than correct it.
    """
    if citing_court is None and _NEEDS_COURT.search(text):
        raise ContextRequired(
            "text cites MLJ/MLJU, whose jurisdiction depends on the citing court; "
            "pass citing_court= (e.g. 'SGHC'). Defaulting would record Singapore "
            "authorities as Malaysian.")


                                                                                
                                                                                               
                                                                                               
                                                                                     
                                                                                             
                                                                                   
 
                                                                                             
                                                                                              
                                                                                              
                                                                                                
                                                           
 
                                                                                           
                                                                                              
              
_OWN_CIT = re.compile(r"(\d{1,4})\s+([A-Za-z][A-Za-z.\s]{0,12}?)\s+(\d{1,4})")


def _own_pagination_key(own_citation):
    """(reporter, volume, first page) for the judgment's own citation, or None."""
    if not own_citation:
        return None
    m = _OWN_CIT.search(str(own_citation))
    if not m:
        return None
    rep = re.sub(r"[^A-Za-z]", "", m.group(2)).upper()
    if not rep:
        return None
    try:
        return (rep, m.group(1), int(m.group(3)))
    except (TypeError, ValueError):
        return None


                                                                                                
                                                                                                 
                                                                                                
                                                                                              
                                                                                            
                                                                                            
                                                                                                
def _is_own_pagination(own, rep, vol, num, text=None, start=None):
    """True where this match is the judgment's own running head rather than an authority."""
    if not own:
        return False
    orep, ovol, opage = own
    if str(vol or "") != ovol:
        return False
    if re.sub(r"[^A-Za-z]", "", str(rep or "")).upper() != orep:
        return False
    try:
        return int(re.sub(r"[^0-9]", "", str(num or "") ) or -1) >= opage
    except (TypeError, ValueError):
        return False


                                                                                
                                                                                               
                                                                                        
                                                                          
                                                                                            
                                                                         
                          
                                                                                        
                                                                                          
                                                                                        
 
                                                                                            
                                                                                             
                                                                                              
                                                                                        
                                                                                              
                     
                                                                                                
                                                                                                   
                                                                                              
                                                                                                  
_OWN_GRANT = re.compile(
    r"\b(?:[Ww]e|[Tt]his\s+Court)\s+(?:granted|noted|postponed|took)\b((?:(?!\n[ \t]*\n)[\s\S]){0,260})$")
_OWN_GRANT_WHAT = re.compile(
    r"certiorari|probable\s+jurisdiction|question\s+of\s+jurisdiction|"
    r"jurisdictional\s+question", re.I)
_OWN_GRANT_CITE = re.compile(
    r"\d{1,3}\s+(?:U\.\s?S\.|S\.\s?Ct\.|L\.\s?Ed\.(?:\s?2d)?)\s+(?:\d{1,5}|_+|-{2,5}|[–—]{1,4})"
    r"(?:\s*,\s*\d{1,5}(?!\s+[A-Z]))*|\(\s*\d{4}\s*\)")
_OWN_GRANT_REPS = {"US", "SCT", "LED", "LED2D"}


                                                                                
                                                                                             
                                                                                               
                                                        
                                                                                                   
                                                                                                    
                                                                                               
                                                        
                                                                                                
                                                                          
                                                                                                 
                                                                                               
                                                                                                  
                                                         
                                                                                    
                                                                                                   
                                                                                         
                                                      
_REPORT_TAG = re.compile(
    r"\(?\b(H\.[ ]?L\.|C\.[ ]?A\.|Ch\.[ ]?D\.|K\.[ ]?B\.(?:[ ]?D\.)?|Q\.[ ]?B\.(?:[ ]?D\.)?|C\.[ ]?S\.|"
    r"S\.[ ]?C\.|P\.[ ]?C\.|P\.[ ]?D\.[ ]?A\.)\)?,?[ ]"
                                                                                       
                                                                                             
                                                                                      
    r"|\((HL|CA|ChD|KBD|QBD|CS|SC|PC|PDA|DC|Appeal[ ]Committee)\)[ ]")
_REPORT_TOK = re.compile(
    r"^(?:[\[(]?(?:1[6-9]|20)\d{2}[\])]?\d{0,2}[.,;:]?|[\[(]\d{4,5}[\])]?|\d{1,4}[a-z]?[.,;:]?"
    r"|\d{0,3}[A-Z][A-Za-z.'’]{0,9}\d{0,4}[.,;:]?|&|and|\(?[A-Z.]{1,6}\)[.,;:]?)$")
_SC_OWN = re.compile(
    r"(?:\bSee[ ]previous[ ]reports?\b[^\n]{0,160}?[.:;][ ]|(?:^|\n|\s)\d{1,2}[ ])S\.[ ]?C\.[ ]([^\n]{0,110})$")
_OWN_AFTER = re.compile(
    r"^[^\n]{3,48}?(?:[ ]?,?[ ]?\[(?:1[6-9]|20)\d{2}\][ ]?UKHL[ ]TC_\d|[ ]{1,3}Their[ ]assistance[ ]is[ ]gratefully)")


def _report_tokens_only(s):
    """True where `s` is nothing but citation matter: years, volumes, series, pages."""
    toks = s.split()
    return len(toks) <= 40 and all(_REPORT_TOK.match(t) for t in toks)


def _own_report_line(text, start):
    """True where this citation stands in the judgment's own report line (forms a-d above)."""
    if _OWN_AFTER.match(" ".join(text[start:start + 130].split())):
        return True                                                     
    before = text[max(0, start - 420):start]
    cut = before.rfind("\n\n")
    if cut >= 0:
        before = before[cut + 2:]
    flat = " ".join(before.split()) + " "
    m = _SC_OWN.search(flat)
                                                                                                  
                                                                                      
                                                                                                       
    if m and (not m.group(1).strip() or re.match(r"(?:L\.[ ]?R\.[ ])?\d{1,3}[ ][A-Z]", m.group(1))) \
            and _report_tokens_only(m.group(1)):
        return True                                                
                                                                                                     
                                                                                                
    if re.match(r"\d{1,2}[ ]S\.[ ]?C\.[ ]\d{1,3}[ ][A-Z][a-z]+\.[ ]", " ".join(text[start:start + 60].split())):
        return True
                                                                                                    
                                                                                                   
                                                                                               
                                             
    if re.match(r"\d{1,3}[ ]T\.[ ]?C\.[ ]\d{1,4}\.[ ]\([^()\s]{1,2}\)[ ](?:Reported|Beported)[ ]",
                " ".join(text[start:start + 60].split())) and re.search(r"\([^()\s]{1,2}\)[ ]$", flat):
        return True
    i = max(flat.rfind("Reported "), flat.rfind("Beported "))
    if i >= 0:
        seg = flat[i + 9:]
        last = None
        for last in _REPORT_TAG.finditer(seg):
            pass
        if last is not None and re.sub(r"[^A-Z]", "", last.group(1) or last.group(2)) in ("HL", "AC") \
                and _report_tokens_only(seg[last.end():]) \
                and re.match(r"\(?(?:[A-Z]|\[?\d)", seg):
            return True                                            
                                                                                             
                                                               
        if last is None and not seg.strip() and re.match(
                r"[\[(](?:1[5-9]|20)\d{2}[\])][ ]?A\.[ ]?C\.[ ]\d", " ".join(text[start:start + 30].split())):
            return True
    return False


                                                                                            
                                                                                                
                                                                                                   
                                                                                             
                                                                                                
                                                                                               
                                                                               
                                                                                          
                                                                            
                                                                                               
                                                                                              
                                                                          
 
                                                                                               
                                                                                                  
                                                                                                 
                                                                           
_R72 = {"sides": None, "thin": True, "ownrep": None, "owncite": None, "owncode": None,
        "gen": 0, "ids": set(), "usvol": None}
_R72_STOP = frozenset(
    "and another others other the of appeals appeal matter matters pte ltd limited inc co plc pty "
    "sdn bhd llp lp corp corporation company in liquidation re ex parte rel no anor ors et al bin "
    "binte bte for an de la on application see cf also as by from to at with v or his her its "
    "receivership liq rec deceased estate trustee trustees executor executors".split())
_R72_GENERIC = frozenset(
    "r queen king crown public prosecutor attorney general solicitor united states state "
    "commonwealth minister ministry secretary department commissioner commissioners comptroller "
    "police council city county board director prosecutions home immigration revenue inland "
    "customs excise taxation tax income canada ontario quebec alberta british columbia new zealand "
    "south wales victoria queensland australia singapore people government republic law society "
    "registrar official assignee receiver national federal border protection affairs justice "
    "services hksar".split())                                                                   
_R72_CROWN = re.compile(r"\b(?:The[ ]Queen|The[ ]King|THE[ ]QUEEN|THE[ ]KING|Regina|Rex|Reg\.|R\.)(?=[ ,]|$)")
_R72_PARENS = re.compile(r"\([^()]*\)|\[[^\[\]]*\]")


def _r72_tokens(s):
    """The words of a party name that identify it (lower case; company and joinder words out)."""
    s = _R72_CROWN.sub("R", str(s or "")).replace("PP", "Public Prosecutor")
    s = _R72_PARENS.sub(" ", _R72_PARENS.sub(" ", s))
    ws = [w for w in re.findall(r"[^\W_]+(?:'[^\W_]+)?", s.lower().replace("’", "'"))
          if len(w) > 1 or w == "r"]
                                                                                                 
                                                                                      
    return frozenset(w for w in ws if w not in _R72_STOP) or frozenset(ws)


def _para_before(text, start, width=520):
    """The text of the paragraph in front of `start`. Where the citation opens a paragraph (the
    cleaned files break some sentences after an initial, `for David H.\\n\\nWall. 488 U.S. 906`,
    and some footnotes between the name and the citation) the paragraph before it is kept too."""
    before = text[max(0, start - width):start]
    cut = before.rfind("\n\n")
    if cut >= 0 and len(before[cut + 2:].strip()) < 40:
        cut = before.rfind("\n\n", 0, cut)
    return before[cut + 2:] if cut >= 0 else before


def _r72_title_sides(header):
    """(left tokens, right tokens) of the title `A v B` in a `CASE:` line or a file name."""
    s = " ".join(str(header or "").split())
    s = re.sub(r"^\d{4}-\d{2}-\d{2}[ ]-[ ]", "", s)                                                
    s = re.sub(r"[ ]?(?:\[\[?(?:1[5-9]|20)\d{2}|\((?:\d{1,3}[ ]U\.[ ]?S\.|\d{1,3}[ ]L\.[ ]?Ed)).*$", "", s)
    parts = re.split(r"[ ]v\.?[ ]", s)
    if len(parts) != 2 and not re.search(r"[ ]v\.?[ ]", s):
                                                                                                          
                                                                                                     
                                                                                                             
                                                                                                      
        parts = re.split(r"[ ]V\.?[ ]", s.split(";")[0])
    if len(parts) != 2:
        return None
    a = frozenset(_R72_ABBR.get(w, w) for w in _r72_tokens(parts[0]))
    b = frozenset(_R72_ABBR.get(w, w) for w in _r72_tokens(parts[1]))
    return (a, b) if a and b else None


def set_own_case(header=None):
    """Hand the engine the title line of the judgment about to be read (None clears it)."""
    sides = _r72_title_sides(header) if header else None
    _R72["sides"] = sides
    _R72["gen"] += 1
    _R72["ids"] = set()
    _u = re.search(r"\((\d{1,3})[ ]U\.[ ]?S\.[ ]\d", " ".join(str(header or "").split()))
    _R72["usvol"] = int(_u.group(1)) if _u else None                                        
    _R72["thin"] = (not sides) or not ((sides[0] | sides[1]) - _R72_GENERIC)
                                                                                                   
                                                                               
    m = re.search(r"UKHL[ ](\d{1,3})_([A-Za-z&]+)_(\d{1,4})", str(header or ""))
    n = re.search(r"UKHL[ ]([A-Za-z&]+)_(\d{1,3})_(\d{1,4})", str(header or ""))
    if m:
        _R72["ownrep"] = (m.group(1), re.sub(r"[^A-Z]", "", m.group(2).upper()), m.group(3))
    elif n:
        _R72["ownrep"] = (n.group(2), re.sub(r"[^A-Z]", "", n.group(1).upper()), n.group(3))
    else:
        _R72["ownrep"] = None
                                                                                                  
                                                                                      
    c = None
    for c in re.finditer(r"\[?((?:1[5-9]|20)\d{2})\]?[ ](?:(\d{1,3})[ ])?([A-Z][A-Za-z().]{1,9})[ ](\d{1,5})(?![\d_])",
                         " ".join(str(header or "").split())):
        pass
    _R72["owncite"] = re.compile(
        r"\[?%s\]?\s*%s%s\s*%s(?!\d)" % (
            c.group(1), (c.group(2) + r"\s+") if c.group(2) else "",
            r"\s?".join(re.escape(x) for x in re.findall(r"[A-Za-z()]+\.?", c.group(3))),
            c.group(4))) if c else None
    _R72["owncode"] = re.sub(r"[^A-Z]", "", c.group(3).upper()) if (c and not c.group(2)) else None
    if _R72["owncode"] and not re.search(r"(?:CA|HC|SC|HL|HCA|SCC|HCF|HCR|HCI|HCA|CAI)$", _R72["owncode"]):
        _R72["owncode"] = None                                                                     


def _r72_court(citing_court):
    c = re.sub(r"[^A-Z]", "", str(citing_court or "").upper())
    if c.startswith(("UKHL", "HL")) or c == "UK":
        return "UKHL"
    return {"US": "USSC", "USA": "USSC", "SCOTUS": "USSC"}.get(c, c)


                                                                                        
_R72_OWN_SERIES = {"USSC": {"US", "SCT", "LED", "LEDD"}, "SCC": {"SCC", "SCR", "RCS"},
                   "HCA": {"HCA", "CLR", "HCASL", "ALJR"}, "UKHL": {"UKHL", "SCHL"},
                   "HKCFA": {"HKCFA", "HKCFAR"}}                                                               
_R72_COURT_WORDS = {"SGCA": r"Court[ ]of[ ]Appeal|\bCA\b", "SGHC": r"High[ ]Court",
                    "UKHL": r"[Yy]our[ ]Lordships|\bthe[ ]House\b", "USSC": r"this[ ]Court"}


def _r72_is_own_series(rn, cc):
    rn = re.sub(r"[^A-Z]", "", str(rn or "").upper())
    return bool(rn) and (rn == cc or rn in _R72_OWN_SERIES.get(cc, ()))


                                                                                         
_R72_TRAIL_CITE = re.compile(
    r"(?:[\[(](?:1[5-9]|20)\d{2}[\])][ ]?,?[ ]?|\b(?:1[5-9]|20)\d{2}[ ])?(?:\d{1,3}[ ])?"
    r"([A-Z][A-Za-z.&']{0,9}(?:[ ]?\([A-Za-z0-9.]{1,6}\)|[ ][A-Z][A-Za-z.]{0,7}|[ ]?2d|[ ]?3d){0,3})[ ]?"
    r"(?:\d{1,5}|-{2,5}|_{2,5}|[–—]{1,4})"
                                                               
    r"(?:,?[ ]at[ ](?:pp?\.?[ ]|pages?[ ])?[\d\[\] ,–-]+)?"
    r"(?:,[ ]\d{1,4}(?:[-–]\d{1,4})?)?[ ]?[,;]?[ ]?\(?[ ]?$")
_R72_TRAIL_OTHER = re.compile(
    r"(?:\((?:CA\d{1,2}|decided[ ][^()]{0,24}|[^()]{0,12}(?:1[5-9]|20)\d{2})\),?[ ]?"
    r"|cert(?:\.|iorari)?[ ]denied,?[ ]?"
                                                                                               
                                                                                       
    r"|\d{1,3}[ ]U\.[ ]?S\.\]?,?[ ]at[ ]|\b(?:[Aa]nte|[Pp]ost|[Ss]upra),?[ ](?:at|pp?\.)[ ])$")
_R72_NAME_WORD = frozenset(
    "and of the for de la van von bin binte bte a/l s/o d/o & ex rel rel. re d' et al al. "
    "another others other appeal appeals matter matters".split())
                                                                                      
_R72_CROWN_SIDE = frozenset(
    "r queen king crown public prosecutor attorney general solicitor united states state "
    "commonwealth people police".split())
                                                                                                 
                                                                                                
                                                                                                
                                                                                      
                                                                                                
                                                                                                 
                                                                                           
                                                                                              
                                                                                             
                                                                                             
_R72_PROC = re.compile(
    r"\b(?:I|[Ww]e)[ ](?:(?:had|have|also|then|previously|subsequently|summarily|accordingly|therefore)[ ]){0,2}"
    r"(?:dismissed|allowed|granted|refused|delivered|ordered|dealt[ ]with|clarified|heard|remitted|vacated"
    r"|remanded|reserved|recalled|convicted|issued|gave|explained|directed|invited|affirmed|set[ ]aside"
    r"|declined|noted[ ]in|found[ ]that)\b"
    r"|(?:\b[Oo]ur|\b[Mm]y)[ ](?:full[ ]|earlier[ ]|previous[ ]|first[ ]|written[ ])?"
    r"(?:grounds|reasons|decisions?|judgment)\b"
    r"|\b[Tt]his[ ][Cc]ourt(?:[ ]in[ ]turn)?[ ](?:gave|granted|refused|denied|dismissed|vacated|reversed|allowed)\b"
                                                                                  
                                                                                       
    r"|\b[Ll]eave[ ]to[ ]appeal[ ]to[ ]this[ ]Court[ ]was[ ](?:granted|refused)"
    r"|\bcontemporaneously[ ]with[ ]the[ ]delivery[ ]of[ ]this[ ]judgment\b"
    r"|\b(?:was|were)[ ](?:dismissed|allowed|refused|granted|heard)[ ]by[ ](?:the[ ]Court[ ]of[ ]Appeal|this[ ][Cc]ourt)"
    r"|\bsingle[ ]judge[ ]of[ ]this[ ]court\b"
                                                                                            
    r"|\b(?:recall[ ](?:of|application)|application[ ]for[ ](?:the[ ])?recall|is[ ]recalled"
    r"|[Ll]eave[ ](?:to[ ]appeal[ ])?(?:was[ ])?(?:granted|refused|denied))\b"
    r"|\b[Mm]otion\b[^.]{0,170}\b(?:issued|rendered|made)[ ]in\b"
    r"|\bin[ ]this[ ](?:matter|litigation)\b")
_R72_PROC_COURT = {
    "SGCA": re.compile(r"(?:decision|judgment)[ ]of[ ]the[ ]Court[ ]of[ ]Appeal[ ]in\b"
                       r"|Court[ ]of[ ]Appeal[’'`]s[ ](?:grounds|decision|judgment)"
                       r"|by[ ]the[ ]Court[ ]of[ ]Appeal[ ]on\b"),
                                                                                               
                                                                                
    "SGHC": re.compile(r"High[ ]Court[’'`]s[ ](?:decision|judgment)"
                       r"|\bthe[ ]High[ ]Court[ ](?:granted|dismissed|allowed|refused)\b"),
    "UKHL": re.compile(r"decision[ ]of[ ](?:this|the|your[ ]Lordships'?)[ ]House[ ]in\b")}
                                                                                              
                                                                                                   
_R72_STRICT = re.compile(
    r"(?:\b[Oo]ur|\b[Mm]y)[ ](?:full[ ])?(?:grounds|reasons)\b"
    r"|\b[Ww]e[ ](?:noted[ ]probable|granted[ ](?:the[ ])?(?:petition|certiorari)|postponed)")
_R72_AFTER = re.compile(
    r"^[^\n]{0,90}?(?:\b[Ll]eave[ ]to[ ]appeal\b|[Ll]eave[ ](?:was[ ])?(?:granted|refused|denied)"
    r"|results[ ]judgment|certiorari|approved[ ](?:question|ground)"
    r"|[,)][ ](?:I|we)[ ](?:dismissed|allowed|granted|refused|explained|ordered)\b)")
                                                                                               
                                                 
_R72_LABEL = re.compile(
    r"^[^\n()]{0,40}\)?[ ]?\((?:the[ ])?[“\"][^”\"\n]{0,40}(?:Judgment|GD|Grounds|Decision)[^”\"\n]{0,14}[”\"]\)")
_R72_LABEL_CA = re.compile(r"^[^\n()]{0,40}\)?[ ]?\((?:the[ ])?[“\"][^”\"\n]{0,30}\bCA\b[^”\"\n]{0,24}[”\"]\)")
_R72_BARE_OK = frozenset(
    "January February March April May June July August September October November December "
    "Originating Summons No Nos Grounds Decision Suit Criminal Civil Motion Appeal Application "
    "Judgment Court High Registrar".split())
                                                                                        
_R72_REPORTS = frozenset(
    "SLR SLRR MLJ NZLR NZCPR NZAR CRNZ TCLR NZTR WLR AC QB KB CH FAM ALLER ALJR ALR FLR PTSR BUSLR STC "
    "TC ICR IRLR SC SLT LLOYDSREP BCLC CRAPPR".split())
                                                                                                                 
                                                                                              
_R72_NZ_LABEL = re.compile(r"^(?:[^\n\[\]]|\[(?:1[5-9]|20)\d{2}\]){0,170}\[(?:SC[ ](?:leave[ ])?"
                           r"|(?:leave|recall|costs|stay|bail|suppression|substantive)[ ])judgment\]")


def _r72_chain_head(flat, cc):
    """Strip the citations that stand between a case name and this citation (its parallels).
    Returns (what is left, True where one of them is this court's own neutral or series)."""
    own, s = False, flat
    for _ in range(6):
        t = _R72_TRAIL_OTHER.sub("", s)
        m = _R72_TRAIL_CITE.search(t)
        if m and len(m.group(0)) < 70:
            own = own or _r72_is_own_series(m.group(1), cc)
            t = t[:m.start()]
        if t == s:
            break
        s = t
    return s, own


def _r72_cited_sides(s):
    """(left tokens, right tokens, right text) of the case name that runs up to the citation."""
    s = _R72_PARENS.sub(" ", _R72_PARENS.sub(" ", s[-460:])).rstrip(" ,([")
    i = max(s.rfind(" v "), s.rfind(" v. "))
    if i < 0:
        return None
    right = s[i:].split(" ", 2)[-1] if s[i:].count(" ") >= 2 else ""
    if not right or len(right) > 230 or re.search(r"[;:“”\"]|[a-z]{4,}\.[ ]+[A-Z]", right):
        return None
    run = []
    for w in reversed(s[:i].split()[-16:]):
        core = w.strip(",.;:()[]'’\"“”")
        if not core:
            continue
        if not (core[:1].isupper() or core[:1].isdigit() or w.lower() in _R72_NAME_WORD):
            break
        if run and w[-1:] in ";:" or (run and w.endswith(".") and len(core) > 4 and core.islower()):
            break
        run.append(w)
        if w[:1] in "([":                                                                     
            break
    left = " ".join(reversed(run))
    a = frozenset(_R72_ABBR.get(w, w) for w in _r72_tokens(left) if not w.isdigit())
    b = frozenset(_R72_ABBR.get(w, w) for w in _r72_tokens(right) if not w.isdigit())
    return (a, b, right) if a and b else None


                                                                                                        
_R72_ABBR = {"ct": "court", "comm'n": "commission", "commn": "commission", "dept": "department",
             "assn": "association", "ass'n": "association", "bd": "board", "univ": "university",
             "natl": "national", "nat'l": "national", "dist": "district", "cty": "county",
             "ins": "insurance", "mfg": "manufacturing", "intl": "international", "int'l": "international"}


def _name_sig(text, start):
    """The two parties printed straight in front of the citation at `start` (its parallels
    aside), as a pair of word sets -- or None where no case name stands there (L4 in finish())."""
    flat = " ".join(_para_before(text, start, 420).split()) + " "
    head, _own = _r72_chain_head(flat, "")
    head = re.sub(r"[ ]?\(?[ ]?(?:1[5-9]|20)\d{2},?[ ]?$", " ", head)                                      
    named = _r72_cited_sides(head)
    if named is None:
        return None
    a, b, right = named
    words = [w.strip(",.;:()[]'’\"“”") for w in right.split()]
    if len(words) > 8 or not all(
            (not w) or w[:1].isupper() or w[:1].isdigit() or w.lower() in _R72_NAME_WORD or w == "&"
            or len(w) == 1                                                                         
            for w in words):
        return None                                                                   
    if not ((a | b) - _R72_GENERIC):
        return None
                                                                                                   
                                                                                                
                                                                          
    no = re.search(r"[(\[]No\.?[ ]?(\d)[)\]][ ,(\[]*$", head)
    return (a, b, no.group(1) if no else "")


_YEAR_VOLUME_SERIES = frozenset({"AC", "QB", "KB", "CH", "P", "FAM", "ICR", "SC", "SCHL", "SLT", "STC"})
                                                                                              
                                                                                                 
                                                                                            
                                                                                   
_BARE_INLINE = re.compile(r"(?:\b[Ss]ee|[a-z,][ ]\()[ ,(\[]*$")
_SHORT_NAME = re.compile(
    r"((?:[A-Z][A-Za-z'’.&-]+[ ]){0,3}[A-Z][A-Za-z'’&-]+)(?:['’]s)?(?:[ ][Cc]ases?)?[ ,]*$")
_BARE_BEFORE = re.compile(r"(?:^|[.;:)\]]|\b[Ss]ee|\b[Cc]f\.?|\band|\bin|\bat)[ ,(\[]*$")
_FRONT_NOISE = frozenset("see per lord lords justice cf also in the at and case cases supra ibid id".split())


def _front(text, start):
    """What the judgment prints straight in front of the citation at `start`, its parallels
    aside: ("sig", parties) / ("short", words of a short name) / ("bare",) / ("other",)."""
    sig = _name_sig(text, start)
    if sig:
        return ("sig", sig)
    flat = " ".join(_para_before(text, start, 300).split()) + " "
    head, _own = _r72_chain_head(flat, "")
    head = re.sub(r"[ ]?\(?[ ]?(?:1[5-9]|20)\d{2},?[ ]?$", " ", head)
    if _BARE_INLINE.search(head):
        return ("bare",)
    if _BARE_BEFORE.search(head):
        return ("other",)
    m = _SHORT_NAME.search(head.rstrip(" ,(["))
    if m:
        ws = frozenset(_r72_tokens(m.group(1))) - _FRONT_NOISE - _R72_GENERIC
        if ws:
            return ("short", ws)
    return ("other",)


def _same_front(a, b):
    """The same case named before two citations: the two parties (one printing may be fuller),
    or a short name all of whose words are in the other's name."""
    if a[0] == "sig" and b[0] == "sig":
        return a[1][2] == b[1][2] and _r72_side(a[1][0], b[1][0]) and _r72_side(a[1][1], b[1][1])
    if a[0] == "short" and b[0] == "sig":
        return a[1] <= (b[1][0] | b[1][1])
    if a[0] == "sig" and b[0] == "short":
        return b[1] <= (a[1][0] | a[1][1])
    if a[0] == "short" and b[0] == "short":
        return a[1] <= b[1] or b[1] <= a[1]
    return False


def _r72_note_sentence(text, at, mark):
    """The words of the judgment in front of the marker of footnote `mark` (`...to this Court[1].`,
    `...refused the applicant leave to appeal (FN1).`): a citation alone in a footnote takes its
    cue from the sentence the footnote hangs on."""
    n = re.sub(r"\D", "", mark)
    if not n:
        return ""
                                                                                             
                                                                                           
    m = re.search(r"(?<=[^\s\[\]])\[%s\]|\(FN[ ]?%s\)" % (n, n), text[:at])
    if m is None:
        return ""
    return " ".join(text[max(0, m.start() - 300):m.start()].split())


LS_C6 = _os.environ.get("JR_LS_C6", "1") != "0"


def _ls_one_off(x, y):
    """Two words one letter apart (one changed, added or dropped), four letters or more."""
    if min(len(x), len(y)) < 4 or abs(len(x) - len(y)) > 1 or x == y:
        return x == y
    if len(x) == len(y):
        return sum(1 for p, q in zip(x, y) if p != q) == 1
    s, l_ = (x, y) if len(x) < len(y) else (y, x)
    return any(l_[:i] + l_[i + 1:] == s for i in range(len(l_)))


def _ls_fuzzy_side(t, c):
    """`_r72_side`, where at most one word of the cited name is one letter off a word of the title."""
    if not (t and c):
        return False
    odd = [w for w in c if w not in t]
    if len(odd) > 1:
        return False
    if odd:
        m = [w for w in t if _ls_one_off(odd[0], w)]
        if len(m) != 1:
            return False
        c = (c - {odd[0]}) | {m[0]}
    return c <= t or t <= c


def _r72_side(t, c):
    """One party of the title against one party of the cited name: the same, or one a fuller
    form of the other (`Barton` / `David Simon Barton`). Shared words alone are not enough --
    `Tan Ah Kow` is not `Tan Ah Teck`."""
    return bool(t and c) and (c <= t or t <= c)


                                                                                             
                                                                                               
                                                                                         
                                                                                             
                                                                                          
                                                                                              
                                              
_R72_ANY_CITE = re.compile(
    r"(?:\[[ ]?((?:1[5-9]|20)\d{2})[ ]?\]|\(((?:1[5-9]|20)\d{2})\)|\b((?:1[5-9]|20)\d{2}))?,?[ \t]*(?:(\d{1,3})[ \t]+)?"
    r"([A-Z][A-Za-z.]{0,7}(?:[ \t]?\([A-Za-z]{1,3}\))?(?:[ \t][A-Z][A-Za-z.]{1,5}){0,2})[ \t]+(\d{1,5})\b")
_R72_SCAN = {"key": None, "ids": frozenset()}


def _r72_cid(m):
    """What identifies a citation across its printings: volume (else year), series, page."""
    return (m.group(4) or m.group(1) or m.group(2) or m.group(3) or "",
            re.sub(r"[^A-Z]", "", m.group(5).upper()), m.group(6))


def _r72_own_ids(text, citing_court):
    key = (_R72["gen"], len(text), text[:80], text[-80:], str(citing_court))
    if _R72_SCAN["key"] != key:
        ids = set()
        if len(text) >= 400:
            cc = _R72["owncode"] or _r72_court(citing_court)
            for m in _R72_ANY_CITE.finditer(text):
                r = re.sub(r"[^A-Z]", "", m.group(5).upper())
                if not (_r72_is_own_series(r, cc) or r in _R72_REPORTS):
                    continue
                                                                                                
                                                                                    
                if _R72["owncite"] is not None and _R72["owncite"].match(
                        " ".join(text[m.start():m.start() + 60].split())):
                    continue
                                                                                                    
                                                                                                 
                                                                                                
                                             
                s0 = m.start()
                while s0 < m.end() and text[s0] in ", \t":
                    s0 += 1
                if _r72_own_core(text, s0, m.group(5), citing_court) or (
                        cc == "USSC" and r == "US" and _own_order_before(text, s0)):
                    ids.add(_r72_cid(m))
        _R72_SCAN["key"], _R72_SCAN["ids"] = key, frozenset(ids)
        if _R72["sides"] is not None:
            _R72["ids"] |= ids                                                           
    return _R72_SCAN["ids"] | _R72["ids"] if _R72["sides"] is not None else _R72_SCAN["ids"]


def _r72_own_case(text, start, rep, citing_court):
    """True where this citation is this court's own earlier step in the litigation (R72)."""
    if _r72_own_core(text, start, rep, citing_court):
        return True
    if len(text) < 400 or not _r72_court(citing_court):
        return False
    ids = _r72_own_ids(text, citing_court)
    if not ids:
        return False
    m = _R72_ANY_CITE.match(" ".join(text[start:start + 70].split()))
    if m and _r72_cid(m) in ids:
        return True
                                                                                   
    flat = " ".join(_para_before(text, start).split()) + " "
    head, _own = _r72_chain_head(flat, _r72_court(citing_court))
    if any(_r72_cid(p) in ids for p in _R72_ANY_CITE.finditer(flat[len(head):])):
        return True
    after = " ".join(text[start:start + 150].split())
    at = m.end() if m else 0
    for p in list(_R72_ANY_CITE.finditer(after))[1:4]:
        if re.search(r"[A-Za-z.]", re.sub(r"\bat\b|\bpp?\b", "", after[at:p.start()])):
            break
        if _r72_cid(p) in ids:
            return True
        at = p.end()
    return False


def _r108_self(text, start, rep, citing_court):
    """R108 (24 Nov 2026): THE JUDGMENT'S OWN CITATION is never an authority, even now that this court's earlier
    steps count. These are the self tests of `_r72_own_core`, unchanged: the own citation wherever printed (and the
    reports in front of it in the citation block, outside the House of Lords), the LawNet availability note, a
    parallel of the own citation in the same chain, and a House of Lords file's own report named in its citation."""
    cc = _r72_court(citing_court)
    if not cc:
        return False
    before = _para_before(text, start, 760)
    after = " ".join(text[start:start + 260].split())
    if _R72["owncite"] is not None:
        if _R72["owncite"].match(after):
            return True
        mo = _R72["owncite"].search(after[:190]) if cc != "UKHL" else None
        if mo and not re.search(r"(?<![A-Za-z])[a-z]{3,}", after[:mo.start()]):
            return True
    if re.match(r"[^\n]{6,26}[ ]is[ ]available[ ]on[ ]LawNet", after):
        return True
    fn = None
    for fn in re.finditer(r"(?:^|\n)[ \t]*(?:\[\d{1,3}\]|\d{1,3})[ \t]+(?=[A-Z(\[])", before):
        pass
    if fn is not None:
        before = before[fn.end():]
    flat = " ".join(before.split()) + " "
    cc = _R72["owncode"] or cc
    head, _chain_own = _r72_chain_head(flat, cc)
    if _R72["owncite"] is not None and cc != "UKHL" and _R72["owncite"].search(flat[len(head):]):
        return True
    orp = _R72["ownrep"]
    if orp and cc == "UKHL":
        m = re.match(r"(?:\((?:1[5-9]|20)\d{2}\)[ ])?(\d{1,3})[ ]([A-Za-z.&][A-Za-z.& ]{0,12}?)[ ](\d{1,4})\b", after)
        if m and m.group(1) == orp[0] and m.group(3) == orp[2]:
            r_ = re.sub(r"[^A-Z]", "", m.group(2).upper())
            if r_ and (r_.startswith(orp[1]) or orp[1].startswith(r_)):
                return True
    return False


def _r72_own_core(text, start, rep, citing_court):
    """True where the words round this citation say it is this court's own step (R72)."""
    cc = _r72_court(citing_court)
    if not cc:
        return False
    before = _para_before(text, start, 760)
    line = before[before.rfind("\n") + 1:]
                                                                                            
                                                                                               
                                                                                                 
                                                                                              
                                                                                               
    after = " ".join(text[start:start + 260].split())
                                                                                          
                                                                                                 
                                                                                                
                                                                                         
                                                                                                
                                  
                                                                                              
    if _R72["owncite"] is not None:
        if _R72["owncite"].match(after):
            return True
                                                                                 
        mo = _R72["owncite"].search(after[:190]) if cc != "UKHL" else None
        if mo and not re.search(r"(?<![A-Za-z])[a-z]{3,}", after[:mo.start()]):
            return True
    if re.match(r"[^\n]{6,26}[ ]is[ ]available[ ]on[ ]LawNet", after):
        return True
                                                                                         
    fn = None
    for fn in re.finditer(r"(?:^|\n)[ \t]*(?:\[\d{1,3}\]|\d{1,3})[ \t]+(?=[A-Z(\[])", before):
        pass
    note = ""
    if fn is not None:
        if not before[fn.end():].count("\n\n"):
            note = fn.group(0)
        before = before[fn.end():]
    flat = " ".join(before.split()) + " "
    rn = re.sub(r"[^A-Z]", "", str(rep or "").upper())
                                                                                             
                                                                                                  
                                                             
    cc = _R72["owncode"] or cc
    head, chain_own = _r72_chain_head(flat, cc)
    if _R72["owncite"] is not None and cc != "UKHL" and _R72["owncite"].search(flat[len(head):]):
        return True                                                                                             
    own = _r72_is_own_series(rn, cc) or chain_own
    if not own:                                                                             
        _c = r"[\[(]?(?:1[5-9]|20)?\d{0,2}[\])]?[ ]?\d{0,3}[ ]?[A-Z][A-Za-z.() ]{0,14}?[ ]\d{1,5}(?:[ ]at[ ][\d\[\] ,–-]+)?[;,][ ]"
        m = re.match(r"(?:" + _c + r"){1,3}\[(?:1[5-9]|20)\d{2}\][ ]?([A-Z][A-Za-z()]{2,8})[ ]\d", after)
        own = bool(m) and _r72_is_own_series(m.group(1), cc)
                                                                          
    orp = _R72["ownrep"]
    if orp and cc == "UKHL":
        m = re.match(r"(?:\((?:1[5-9]|20)\d{2}\)[ ])?(\d{1,3})[ ]([A-Za-z.&][A-Za-z.& ]{0,12}?)[ ](\d{1,4})\b", after)
        if m and m.group(1) == orp[0] and m.group(3) == orp[2]:
            r_ = re.sub(r"[^A-Z]", "", m.group(2).upper())
            if r_ and (r_.startswith(orp[1]) or orp[1].startswith(r_)):
                return True
    window = head[-480:]                                                                 
                                         
                                                                                                  
                                                                                                
                                                                                                 
                                                   
                                                                                            
    if cc == "HCA" and own and re.search(
            r"\bapplication[ ]was[ ]made\b.{0,800}?\bLeave[ ]was[ ](?:refused|granted)[ ]?\(+(?:\d{1,3}\))?[ ]?"
            r"(?:\((?:1[5-9]|20)\d{2}\)[ ]\d{1,3}[ ]ALJR[ ]\d{1,4};[ ]?)?$",
            " ".join(text[max(0, start - 1000):start].split()) + " "):
        return True
    if cc == "SGCA" and re.search(
            r"\b(?:review[ ]application|application[ ]to[ ]review|to[ ]review)\b[^.;]{0,90}\bearlier[ ]"
            r"(?:decision|judgment)[ ]of[ ]the[ ]Court[ ]of[ ]Appeal\b[^.;]{0,60}?[ ]in[ ][A-Z][^.;]{4,260}$", head):
                                                                                             
                                                                                                      
        return True
    if cc == "NZSC" and own:
        if _R72_NZ_LABEL.match(after) or re.search(r"\bLeave[ ]granted:[ ][^.;]{0,90}$", head):
            return True
    if cc == "UKHL":
        if re.search(r"(?:[Yy]our[ ]Lordships'?[ ]House(?:[:,]?[ ](?:see|reported[ ]at))?"
                     r"|the[ ]House[ ]dismissed[ ]the[ ]petition)[ (]*$", head):
            return True
        if rn == "UKHL" and re.search(r"\d(?:st|nd|rd|th)[ ]Report,[ ]Session[ ]\d{4}[-–]\d{2},[ ]?$", head):
            return True
                                                                                                   
                                                                                           
        if rn == "SLR" and "SCOTTISH_SLR" in flat and re.match(
                r"\d{1,3}[ ]SLR[ ]\d{1,4}[ ](?:[A-Z&][A-Za-z'’.&,-]*[ ]){1,8}v\.?[ ][A-Z]", after):
            return True
                                                                                             
                                             
                                                                                               
                                                                   
        if rn == "SCHL" and start >= 200 and re.match(
                r"\[(?:1[5-9]|20)\d{2}\][ ]?SC[ ]?\(HL\)[ ]\d{1,4}[ ]?(?:-{4,}[ ]?)?(?:INGEST[^\n]*)?$",
                " ".join(text[start:start + 200].split())):
            return True
    if cc == "SCC":
        if rn in ("SCR", "RCS") and re.match(r"(?:MOTIONS?|REHEARING)\b", line.lstrip()):
            return True                                                                                 
        if rn == "SCCBULL" and re.search(r"leave[ ]to[ ]appeal[ ]judgment,?[ ]$", head):
            return True
        if rn in ("SCR", "RCS") and re.search(
                r"\b[Tt]his[ ]Court[ ]issued[ ]a[ ]judgment\b[^.;]{0,300}\([ ]?$", head):
            return True
    named = _r72_cited_sides(head)
    if named is None and note and own and len(head.strip()) < 6:
                                                                                                  
                                                                                                   
                             
        hung = _r72_note_sentence(text, start, note)
        if re.search(r"[Ll]eave[^.]{0,80}(?:refused|granted)[ ]by[ ]this[ ]Court$"
                     r"|this[ ]Court[ ](?:refused|granted)[^.]{0,60}leave[^.]{0,40}$", hung):
            return True
    if named is None:
                                                                                          
                                                                                           
                                                                                        
                                                                                                
                                                                                                    
                                                                                                 
                                                                                           
        if own and (rn == cc or chain_own) and not re.search(r"[ ]v\.?[ ]|another[ ]case", head[-110:]):
            m = re.search(r"(?:(?:\bI|\b[Ww]e)[ ](?:had[ ]previously[ ])?(?:delivered|issued)\b"
                          r"|(?:\b[Mm]y|\b[Oo]ur)[ ](?:decision|judgment)\b)([^.;]{0,130})$", head)
            if m and all(w in _R72_BARE_OK for w in re.findall(r"\b[A-Z][A-Za-z]+", m.group(1))):
                return True
            if re.search(r"(?:first|earlier|previous|written)[ ]judgment[ (]*$", head) \
                    or re.match(r"[^.;\n]{0,40}\bdelivered[ ]by[ ]me\b", after):
                return True
        return False
    sides = _R72["sides"]
    if not sides:
        return False
    a, b, right = named
    full = (_r72_side(sides[0], a) and _r72_side(sides[1], b)) or \
           (_r72_side(sides[0], b) and _r72_side(sides[1], a))
    one = any(_r72_side(t, c) and ((t & c) - _R72_GENERIC) for t in sides for c in (a, b))
    pc = _R72_PROC_COURT.get(cc)
    proc = bool(_R72_PROC.search(window)) or bool(pc and pc.search(window))
    if not proc and note and full and own and len(head) < 200:
                                                                                              
        hung = _r72_note_sentence(text, start, note)
        proc = bool(_R72_PROC.search(hung)) or bool(pc and pc.search(hung)) \
            or bool(re.search(r"appealed[ ]to[ ]this[ ]Court$"
                              r"|this[ ]Court[’'`]s[ ](?:decision|judgment|orders?)$", hung))
                                                                                                 
                                                                                               
                                                                         
    held = bool(re.match(r"[^\n.;]{0,90}[”\"]\)?\)?,[ ](?:this[ ]court|we|the[ ]Court[ ]of[ ]Appeal)[ ]held\b", after))
    if own:
        label = (bool(_R72_LABEL.match(after)) or (cc == "SGCA" and bool(_R72_LABEL_CA.match(after)))) and not held
        if full and (proc or label or _R72_AFTER.match(after)):
            return True
        if one and (_R72_STRICT.search(window) or
                    (rn == "HCASL" and cc == "HCA") or
                    (cc == "NZSC" and re.match(r"[^\n]{0,90}?approved[ ](?:question|ground)", after)) or
                    (cc == "USSC" and re.search(r"cert(?:\.|iorari)?[ ]denied,?[ ]$", flat))):
            return True
        return False
                                                                                            
    if rn in _R72_REPORTS or re.match(r"[\[(]?(?:1[5-9]|20)\d{2}[\])]?[ ]\d{1,3}[ ][A-Z]", after):
        if full and (proc or (cc == "SGCA" and _R72_LABEL_CA.match(after) and not held)):
            return True
                                                                                             
                                                                                                    
                                                                                                   
                                                              
        if LS_C6 and not full and re.search(r"\b[Oo]ur[ ](?:earlier[ ]|previous[ ])?(?:decision|judgment)[ ]in[ ]", window) \
                and ((_ls_fuzzy_side(sides[0], a) and _ls_fuzzy_side(sides[1], b))
                     or (_ls_fuzzy_side(sides[0], b) and _ls_fuzzy_side(sides[1], a))):
            return True
        if one and _R72_STRICT.search(window):
            return True
    return False


                                                                                                  
                                                                                               
                                                                                                 
                                                                                            
                        
                                                                                           
                               
                                                                            
                                                                                                 
                                                                                    
                                                                                                 
                                                                                           
                                                                                               
                                                                                                 
                                                                                                 
                                      
_OWN_ORDER_CUE = re.compile(
    r"\b(?:[Ww]e|[Tt]his[ ]Court|[Tt]he[ ]Court)[ ](?:[a-z]+ly[ ])?(?:(?:granted|denied)[ ](?:[A-Za-z'’]+[ ]){0,4}"
    r"(?:certiorari|stay|motion|petition|application|review|rehearing|leave)"
    r"|noted[ ]probable[ ]jurisdiction|postponed|agreed[ ]to[ ](?:do[ ]so|take[ ]up|hear|review|decide)"
    r"|set[ ][^.]{0,80}for[ ](?:oral[ ])?(?:re)?argument|appointed[ ](?:an?[ ])?(?:amicus|[A-Z])"
    r"|heard[ ]oral[ ]argument|vacated[ ]the[ ]judgment)"
    r"|\b(?:[Hh]aving|us[ ]to)[ ]grant(?:ed)?[ ]certiorari"
    r"|\bhaving[ ](?:expressly[ ])?invited\b"
    r"|\b(?:certiorari|stay|petition|motion|application|rehearing)\b[^.]{0,160}\b(?:was|were)[ ](?:granted|denied)"
    r"|\bis[ ]here[ ]on[ ](?:a[ ])?(?:petition[ ]for[ ])?(?:a[ ])?(?:writ[ ]of[ ])?certiorari"
    r"|\bby[ ](?:appointment|invitation)[ ]of[ ]the[ ]Court"
    r"|\bfiled[ ]in[ ]this[ ]Court[ ]on\b")
_OWN_ORDER_VERB = re.compile(
    r"\b(?:[Ww]e|[Tt]his[ ]Court)[ ](?:granted|denied|noted[ ]probable|vacated|postponed)")
_OWN_ORDER_CAPTION = re.compile(
    r"^[^.]{0,200}\.[ ](?:[A-Z&][A-Za-z'’.&-]*,?[ ]){1,7}?v\.[ ](?:[A-Za-z'’.&-]+,?[ ]){0,7}?[A-Za-z'’.&-]+,[ ]$")
_OWN_ORDER_TAIL = re.compile(
    r"(?:\d{1,3}[ ](?:U\.[ ]?S\.|S\.[ ]?Ct\.|L\.[ ]?Ed\.(?:[ ]?2d)?)[ ](?:\d{1,5}|_+|-{2,5}|[–—]{1,4})"
    r"|\([ ]?\d{4}[ ]?\))[ ]?[,;]?[ ]?$")


def _own_order_before(text, start):
    """True where a bare United States Reports citation follows a sentence in which the Court
    says what it did in the case before it."""
    flat = " ".join(_para_before(text, start).split()) + " "
    cue = None
    for cue in _OWN_ORDER_CUE.finditer(flat):
        pass
    if cue is None:
        return False
                                                                                               
                                                                                                   
                                                                                                  
                                                                                                
                        
    v = re.match(r"(\d{1,3})\s+U\.", text[start:start + 12])
    if v and _R72["usvol"] and int(v.group(1)) < _R72["usvol"] - 20:
        return False
    rest = flat[cue.end():]
    for _ in range(4):                                                             
        t = _OWN_ORDER_TAIL.sub("", rest)
        if t == rest:
            break
        rest = t
    if len(rest) > 420:
        return False
    if re.search(r"[ ]v\.?[ ]", rest):
                                                                                          
                                                                                                  
                                                                                                 
                                                                                                
                                                                                                   
        return bool(_OWN_ORDER_CAPTION.match(rest) and _OWN_ORDER_VERB.search(cue.group(0)))
                                                                                                 
                                                                                      
    if re.search(r"\bin[ ](?!(?:Part|No|Rule|Section|Title|Article|Chapter|January|February|March|April"
                 r"|May|June|July|August|September|October|November|December)\b)[A-Z][a-z]+", rest):
        return False
                                                                                           
    if re.search(r"\bin[ ](?:that|those|another|the[ ]other|the[ ]earlier)[ ]", rest):
        return False
    if re.search(r"\d{1,3}[ ](?:[A-Z][A-Za-z]{0,5}\.[ ]?){1,3}(?:2d|3d)?[ ]?\d", rest):
        return False                                                                     
    if len(re.findall(r"[a-z]{3}\.[ ]", rest)) > 1:
        return False                                                                   
    return bool(re.search(r"(?:^|[.,:;”\"]|\b[Ss]ee)[ ]*$", rest))


_PENDING_CUE = re.compile(
    r"(?:would[ ]shortly[ ]come[ ]before|(?:is|are)[ ]now[ ]before|(?:is|are)[ ](?:currently[ ])?pending[ ]before)"
    r"[^.;]{0,160}?\b(?:[Aa]pp(?:lication)?s?\.?[ ]?[Nn]os?\.?[ ]?)(\d{1,5}/\d{2,4})(?:[ ]and[ ](\d{1,5}/\d{2,4}))?")
_PENDING_SCAN = {"key": None, "nums": frozenset()}


def _pending_applications(text):
    """Strasbourg application numbers the judgment itself says are still pending."""
    key = (len(text), text[:80], text[-80:])
    if _PENDING_SCAN["key"] != key:
        nums = set()
        if "before" in text:
            for m in _PENDING_CUE.finditer(" ".join(text.split())):
                nums.update(x for x in m.groups() if x)
        _PENDING_SCAN["key"], _PENDING_SCAN["nums"] = key, frozenset(nums)
    return _PENDING_SCAN["nums"]


                                                                                                 
                                                                                                  
                                                                                                  
                                                                                                      
                                                                                                    
                                                                                               
                                                                                                  
                                                                      
                                                                                                     
                                                                                                   
                                                                                                    
                                                 
LS_C1 = _os.environ.get("JR_LS_C1", "1") != "0"
LS_C2 = _os.environ.get("JR_LS_C2", "1") != "0"
LS_C3 = _os.environ.get("JR_LS_C3", "1") != "0"
LS_P3 = _os.environ.get("JR_LS_P3", "1") != "0"                            


def _ls_own_form(text, start, citing_court):
    cc = _r72_court(citing_court)
    if len(text) < 400:
        return False                                                                         
    before = text[max(0, start - 320):start]
    if LS_C1 and cc == "UKHL" and re.search(
            r"\bR\W{0,2}port\W{0,2}(?:e\W?)?d\b[^;]{0,250}\band\s+H\.[ \t]?L\.,?\s*$", before):
        return True
    if LS_C2 and cc == "UKHL":
        m = None
        for m in re.finditer(r"\bS\.[ \t]?C\.[ \t]+", before):
            pass
        if m is not None and len(before) - m.end() <= 120 and re.search(
                r"\bSee[ \t]+previous[ \t]+reports?\b[^\n]{0,200}$", before[:m.start()]) \
                and not re.search(r"[ \t]v\.?[ \t]|;|\b[a-z]{5,}\b", before[m.end():]):
            return True
    if LS_C3 and cc == "USSC" and _R72["usvol"]:
        v = re.match(r"(\d{1,3})[ \t]+U\.[ \t]?S\.[ \t]+\d{1,4}", text[start:start + 30])
        if v and int(v.group(1)) == _R72["usvol"]:
                                                                                                      
                                                                                                  
                                                                                                  
                                                                                  
            if re.search(r"(?:[.;”\"]\s+|\([ \t]*)[Pp]ost,?[ \t]+at[ \t]+$", before):
                return True
            if re.search(r"[a-z][.]\s+$", before) and re.match(
                    r"\d{1,3}[ \t]+U\.[ \t]?S\.[ \t]+\d{1,4}[ \t]*\.\s+\([a-z]\)[ \t]", text[start:start + 40]):
                return True
    return False


def _own_grant_before(text, start, rep, citing_court=None):
    """True where this citation is the court's own grant of review in the case before it."""
    if str(rep or "").startswith(("CDK", "CDN")):                                                  
        return _cd_reject(text, start, str(rep).split(":")[0])
    if citing_court is not None and _ls_own_form(text, start, citing_court):
        return True                                                        
    if _own_report_line(text, start):                                                        
        return True
    if not R108_ON and citing_court is not None and _r72_own_case(text, start, rep, citing_court):                         
        return True
    if R108_ON and citing_court is not None and _r108_self(text, start, rep, citing_court):
        return True
    _rep = str(rep or "")
                                                                             
                                                                                                  
                                                                                                    
                                                                                               
                                                                                            
                                                                                                  
                                                                             
    if _rep == "ECHRAPP":
        n = re.match(r"[^\d]{0,24}(\d{1,5}/\d{2,4})", text[start:start + 44])
        if n and n.group(1) in _pending_applications(text):
            return True
    elif _rep == "THETIMES":
        m = _CITE_NEWSPAPER.match(text, start)
        if m and re.match(r",?\s*pp?\.\s?\d", text[m.end():m.end() + 8]):
            return True
    if re.sub(r"[^A-Z0-9]", "", str(rep or "").upper()) not in _OWN_GRANT_REPS:
        return False
    if not R108_ON and _own_order_before(text, start):                                                                     
        return True
                                                                                      
                                                                                             
    if re.search(r"\bCite[ ]as:[ \t]*$", text[max(0, start - 14):start]):
        return True
                                                                                                    
                                                                                                
                                           
    if re.search(r"\bRules\b[^.;]{0,90}\beffective\b[^.;]{0,60}[.,][ ]$",
                 " ".join(text[max(0, start - 220):start].split()) + " "):
        return True
    if R108_ON:
        return False                                                                         
    m = _OWN_GRANT.search(text[max(0, start - 300):start])
    if not m:
        return False
    tail = m.group(1)
    w = None
    for w in _OWN_GRANT_WHAT.finditer(tail):
        pass
    if w is None:
        return False
    rest = tail[w.end():]
    if re.search(r"\bv\.?\s", rest):
        return False
    bare = _OWN_GRANT_CITE.sub("", rest)
    if bare != rest:
                                                                                         
        return not re.search(r"[A-Za-z]", bare)
    return len(rest) <= 200 and rest.count(". ") <= 1


def count(text, reporters, citing_court=None, own_citation=None, own_name=None, own_header=None):
    """Return {jurisdiction: distinct authorities}.

    `reporters` is the jr_reporters module. The full text and the match offset are handed to it
    so it can see the surrounding words -- that is what lets it tell a Court of Justice judgment
    reported in the Queen's Bench from an English one, and a journal reference from a law report.
    Classifying on the abbreviation alone cannot do either.

    `own_name` (14 Oct 2026, R72) is the judgment's own title line -- the file's `CASE:` line, or
    case name plus citation -- so that this court's earlier decisions in the same litigation are
    not returned as authorities. See `set_own_case`.

    Raises ContextRequired if the text needs a citing court and none was supplied.
    """
    if own_name is not None:
        set_own_case(own_name)
    require_context(text, citing_court)
    hk = _HKContext(text, own_header) if citing_court == "HKCFA" else None
    if hk is not None:
        text = _hk_mask_parallel(text)
    _own = _own_pagination_key(own_citation)
    text = _mask_damaged_prefix(text)
    out = {}
    c = _Counter()
    for name, pat, form, fixed in _ALL_PATTERNS:
        if not _pattern_applies(name, citing_court):
            continue
        for m in pat.finditer(text):
            year, rep, vol, num = hk.fields(name,m) if hk is not None and name.startswith("cd_hk") else _fields(name, m.groups())
            if hk is not None and name.startswith("cd_hk") and hk.reject(name,m,text):
                c.bridge(m.start(),m.end())
                continue
                                                                                           
                                                                                         
            if name == "nominate" and (vol in ("", "0") or num in ("", "0")):
                continue
                                                                                     
                                                                            
            if name == "nominate" and _statute_section_before(text, m.start()):
                continue
            juri = fixed or reporters.classify(rep, form=form, context=text, at=m.start(),
                                               citing_court=citing_court)
            if juri is None:
                if reporters.is_database_tag(rep):
                    c.bridge(m.start(), m.end())                                          
                continue                                                               
                                                                                          
                                                      
            if _article_title_before(text, m.start()):
                c.bridge(m.start(), m.end())                                                 
                continue
            if _is_own_pagination(_own, rep, vol, num, text, m.start()):
                c.bridge(m.start(), m.end())                                     
                continue
            if not name.startswith("cd_hk") and _own_grant_before(text, m.start(), rep, citing_court):
                c.bridge(m.start(), m.end())                                                 
                continue
            pin = bool(_AT_PIN.search(m.group(0))) or _pinpoint_before(
                text, m.start(), vol, rep, num)
            c.consume(m.start(), m.end(), juri, _norm_key(year, rep, vol, num), form,
                      pinpoint=pin)

                                                                                            
                                                                               
    home = reporters._CITING_COURT_JURI.get(str(citing_court or '').upper())
    if home:
        for s, e, k in _file_numbers(text):
            c.consume(s, e, home, ('filenum', k, '', ''), 'filenum')

    fin = list(_hk_finish(c, text, hk))
    for _s, _e, juri, _k, _f in fin:
        out[juri] = out.get(juri, 0) + 1
    for _s, _e, juri, _d, _k in _bare_names(text, [(f[0], f[1]) for f in fin], own_name, own_citation):          
        out[juri] = out.get(juri, 0) + 1
    return out


def items(text, reporters, citing_court=None, own_citation=None, own_name=None, own_header=None):
    """The SAME authorities `count` counts, returned individually instead of tallied.

    Yields dicts: {jurisdiction, citation, key, form, start, end, aliases}. `citation` is the
    text exactly as the judgment printed it; `aliases` holds the other names of the same
    authority where a parallel citation merged ('[1992] HCA 23; (1992) 175 CLR 1' is ONE
    authority with two names, and which one survives is an accident of what the court wrote
    first).

    ⚠️ THIS IS A DELIBERATE NEAR-COPY OF `count`, NOT A REFACTOR OF IT. The counting engine is
    frozen and its numbers are the published ones; rewriting `count` to delegate here would put
    every recorded citation figure at risk to save a dozen lines. The two are held together by a
    test instead: for any text, the per-jurisdiction tally of what this returns must equal what
    `count` returns. If the bodies ever drift, that check fails loudly rather than silently
    producing a list that disagrees with the column beside it.
    """
    if own_name is not None:
        set_own_case(own_name)                                       
    require_context(text, citing_court)
    hk = _HKContext(text, own_header) if citing_court == "HKCFA" else None
    if hk is not None:
        text = _hk_mask_parallel(text)
    _own = _own_pagination_key(own_citation)
    text = _mask_damaged_prefix(text)
    c = _Counter()
    for name, pat, form, fixed in _ALL_PATTERNS:
        if not _pattern_applies(name, citing_court):
            continue
        for m in pat.finditer(text):
            year, rep, vol, num = hk.fields(name,m) if hk is not None and name.startswith("cd_hk") else _fields(name, m.groups())
            if hk is not None and name.startswith("cd_hk") and hk.reject(name,m,text):
                c.bridge(m.start(),m.end())
                continue
            if name == "nominate" and (vol in ("", "0") or num in ("", "0")):
                continue
                                                                                     
                                                                            
            if name == "nominate" and _statute_section_before(text, m.start()):
                continue
            juri = fixed or reporters.classify(rep, form=form, context=text, at=m.start(),
                                               citing_court=citing_court)
            if juri is None:
                if reporters.is_database_tag(rep):
                    c.bridge(m.start(), m.end())
                continue
            if _article_title_before(text, m.start()):
                c.bridge(m.start(), m.end())
                continue
            if _is_own_pagination(_own, rep, vol, num, text, m.start()):
                c.bridge(m.start(), m.end())                                     
                continue
            if not name.startswith("cd_hk") and _own_grant_before(text, m.start(), rep, citing_court):
                c.bridge(m.start(), m.end())                                                 
                continue
            pin = bool(_AT_PIN.search(m.group(0))) or _pinpoint_before(
                text, m.start(), vol, rep, num)
            c.consume(m.start(), m.end(), juri, _norm_key(year, rep, vol, num), form,
                      pinpoint=pin)

    home = reporters._CITING_COURT_JURI.get(str(citing_court or '').upper())
    if home:
        for s, e, k in _file_numbers(text):
            c.consume(s, e, home, ('filenum', k, '', ''), 'filenum')

    out = []
    fin = list(_hk_finish(c, text, hk))
    for s, e, juri, k, f in fin:
        out.append({
            "jurisdiction": juri,
            "citation": re.sub(r"\s+", " ", text[s:e]).strip(),
            "key": " ".join(str(x) for x in k if x),
            "form": f,
            "start": s,
            "end": e,
            "aliases": sorted(" ".join(str(x) for x in a if x)
                              for a in c.aliases.get(k, ()) if a != k),
        })
    for s, e, juri, d, k in _bare_names(text, [(f[0], f[1]) for f in fin], own_name, own_citation):          
        out.append({"jurisdiction": juri, "citation": d, "key": "BARE " + k, "form": "barename",
                    "start": s, "end": e, "aliases": []})
    return out


def occurrences(text, reporters, citing_court=None, own_citation=None, own_name=None, own_header=None):
    """Citation events rather than distinct authorities -- L0 only, no L1 or L2.
    Kept because the ratio between the two measures citation style, and because the
    existing Master columns are occurrence counts."""
    if own_name is not None:
        set_own_case(own_name)                                       
    require_context(text, citing_court)
    hk = _HKContext(text, own_header) if citing_court == "HKCFA" else None
    if hk is not None:
        text = _hk_mask_parallel(text)
    _own = _own_pagination_key(own_citation)
    text = _mask_damaged_prefix(text)
    out = {}
    spans = []
    for name, pat, form, fixed in _ALL_PATTERNS:
        if not _pattern_applies(name, citing_court):
            continue
        for m in pat.finditer(text):
            if any(m.start() < e and m.end() > s for s, e in spans):
                continue
            spans.append((m.start(), m.end()))
            _y, rep, _v, _n = hk.fields(name,m) if hk is not None and name.startswith("cd_hk") else _fields(name, m.groups())
            if hk is not None and name.startswith("cd_hk") and hk.reject(name,m,text):
                continue
            juri = fixed or reporters.classify(rep, form=form, context=text, at=m.start(),
                                               citing_court=citing_court)
            if juri is None:
                continue
                                                                                         
                                                          
            if _is_own_pagination(_own, rep, _v, _n, text, m.start()):
                continue
            if not name.startswith("cd_hk") and _own_grant_before(text, m.start(), rep, citing_court):
                continue                                                                
            out[juri] = out.get(juri, 0) + 1
    return out
