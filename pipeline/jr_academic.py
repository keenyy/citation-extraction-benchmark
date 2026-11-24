                                                                                 
CARDIFF_ACAD_ABBREVS = set()
                                                                                      
                                                                                    
                                                                                  
                                                                          
CARDIFF_ACAD_TITLES = set()


                       
"""Academic reference counting — journal articles and treatises cited in a judgment.

PROVENANCE. Pattern tables and the counter lifted verbatim on 2026-08-17 from build_v5_all.py.
Nothing was retyped. This is the one counter that reproduces its Master column exactly: measured
100% on 300 rows across nine sheets.

⚠️ BUT REPRODUCING IS NOT THE SAME AS BEING RIGHT. The 17 August field audit read 24 judgments
and found this counter wrong on 10 of them, in both directions:

  PHANTOM COUNTS -- a number recorded where the judgment cites no academic work at all.
      Tan Chee Wee (stored 2): only statutes and cases in the whole judgment.
      Vasudevan (stored 1), Fornaris (stored 1), Irwin (stored 1): likewise nothing.
      Fornaris appears to be counting H.R. and S. Reps, which the Key expressly excludes.

  MISSES -- named treatises and law review articles not picked up.
      Palmer on Bailment, quoted twice at length in T Kishen -- stored 0.
      Two Sweet & Maxwell titles in Hin Leong -- stored 6, actual 8.
      Elder, 83 Dick. L. Rev. 387 in Munro -- stored 0.
      Haddad, 59 Chi. Kent L. Rev. 23 in Gilmore -- stored 0.
      Friendly, Bator and Oaks in Montgomery -- stored 1, actual 3.
      A 30-item "Authors Cited" block in Beliveau St-Jacques -- stored 0.

  The USSC hit rate is 2 of 8. The Canadian count runs at about 44% accuracy because the book
  patterns contain no Canadian or Quebec sources at all.

SO: this module is a faithful copy of the published behaviour, not a corrected one. Treat its
output as reproducing Master 4.0, and fix the patterns before treating it as accurate.

The one thing it does well, and must keep doing: the "v" guard. A short name beside " v " is a
party, not a book, which stops Snell v Beadle being read as Snell's Equity.
"""
import json
import os
import re

_YEAR_IN_CTX = re.compile(r'\b(1[89]\d{2}|20[0-2]\d)\b')
_CITE_ALR = re.compile(r'\b(\d+)\s+ALR\s+(\d+)')
_CITE_SCR = re.compile(r'\b(\d+)\s+SCR\s+(\d+)')
_CITE_CANLII = re.compile(r'\b(\d{4})\s+(CanLII)\s+(\d+)')

                                                                             
                                                 
 
                                                                                             
                                                                                        
                                                                                            
                                                                                              
                                                                        
 
                                                                                              
                                           
 
                                                                                          
                                                                                           
                                                                                             
_BAREYEAR_COURTS = (
    'SCC', 'FCA', 'FC', 'TCC', 'CMAC',                               
    'ONCA', 'ONSC', 'ONCJ', 'ONSCDC',                                
    'BCCA', 'BCSC', 'BCPC',                                                   
    'ABCA', 'ABQB', 'ABPC', 'ABKB',                                  
    'QCCA', 'QCCS', 'QCCQ',                                         
    'NSCA', 'NSSC', 'NBCA', 'NBQB', 'PECA', 'PESC',                   
    'MBCA', 'MBQB', 'SKCA', 'SKQB',                                   
    'NLCA', 'NLSC', 'YKCA', 'YKSC', 'NWTCA', 'NWTSC', 'NUCA', 'NUCJ',
)
_CITE_BAREYEAR = re.compile(
    r'(?<![\[\(\w])\b(\d{4})\s+(' + '|'.join(_BAREYEAR_COURTS) + r')\s+(\d{1,5})\b'
)


_ACAD_JOURNAL_PATTERNS = [
                                                             
    r'\(\d{4}\)\s+\d+\s+[A-Z][A-Za-z]+(?:\s+[A-Za-z]+)+\s+(?:Law|Legal|Journal|Review|Quarterly|University|Studies)[A-Za-z\s]*\d*',
                                            
                                                                                                      
                                                             
                                                                                                           
                                                                                                  
                                                                                                        
                                                                                                          
                                                                                                               
                                                                                             
                                                                                                       
                                                                                                              
                                                                                                                  
    r'\b[1-9]\d{0,2}[ \t]+(?:Law[ \t]+(?:Journal(?!,?[ \t]*\d)(?!,?[ \t]*(?:Exchequer|Chancery|Appeal|Common\s+Pleas|Queen.s\s+Bench|King.s\s+Bench|Privy\s+Council|House\s+of\s+Lords)\b)|Review|Quarterly)|Journal)\b',
                                                                                   
                                                                  
                                                                                 
                                                                                                   
                                                                                                
                                                                             
                                                                                
    r'\b(?:LQR|L\.Q\.R|MLR|M\.L\.R|OJLS|O\.J\.L\.S|SJLS|S\.J\.L\.S|SAcLJ|LMCLQ|L\.M\.C\.L\.Q|JBL|J\.B\.L|ICLQ|I\.C\.L\.Q|AJCL|A\.J\.C\.L|NZLJ|MULR|UNSWLJ|SydLR|UQLJ|UWALR|AdelLR|MonLR|MelbULawRw|CrimLR|NILQ|BTR|EHRLR|OttawaLR'
                                                                                                          
    r'|HKLJ|H\.K\.L\.J)\b',
                                                                                                   
    r'\bCrim\s+LR\b',                                                                             
    r'\bConv\b(?!\s+v[\s.])',                                                               
    r'\bFam\s+Law\b',                               
    r'\bTort\s+Law\s+Rev(?:iew)?\b',                   
    r'\bIRLR\b(?!\s+\d)',                                                                                    
    r'\bSLT\b(?!\s+\d)',                                                                                               
    r'(?<!\d )CLJ\b',
    r'(?<!\()(?<!["\'`])CLP\b',
                            
    r'\b(?:Law\s+Quarterly\s+Review|Cambridge\s+Law\s+Journal|Oxford\s+Journal\s+of\s+Legal\s+Studies)\b',
    r'\b(?:Singapore\s+Journal\s+of\s+Legal\s+Studies|Singapore\s+Academy\s+of\s+Law\s+Journal)\b',
    r'\b(?:Melbourne\s+University\s+Law\s+Review|Sydney\s+Law\s+Review|Australian\s+Law\s+Journal)\b',
    r'\b(?:Modern\s+Law\s+Review|New\s+Zealand\s+Law\s+(?:Review|Journal))\b',
                                                                                                            
    r'(?<!his )(?<!her )(?<!the )(?<!of )(?<!my )Legal\s+Studies\b',
    r'\b(?:Federal\s+Law\s+Review|Monash\s+University\s+Law\s+Review)\b',
    r'\b(?:Edinburgh\s+Law\s+Review|Criminal\s+Law\s+Review)\b',
    r'\b(?:Northern\s+Ireland\s+(?:Legal\s+)?Quarterly|British\s+Tax\s+Review)\b',
    r'\b(?:European\s+Human\s+Rights\s+Law\s+Review|British\s+Journal\s+of\s+Industrial\s+Relations)\b',
    r'\bIndustrial\s+Relations\s+Law\s+(?:Review|Reports)\b',                                                                         
    r'\bCanadian\s+Bar\s+Review\b',                                                                                   
    r'\bAustralian\s+Bar\s+Review\b',                                                              
    r'\bBritish\s+Journal\s+of\s+Criminology\b',                                                                       
    r'\bJournal\s+of\s+(?:Criminal\s+Law(?:\s+and\s+Criminology)?|International\s+Criminal\s+Justice)\b',
                                              
                                                                                                                 
                                                                                
                                                                                                
    r'\b(?:Harv|Yale|Stan|Colum|Mich|Cal|Geo|Duke|Va|Tex|Penn|Cornell|NYU|Chi|Nw|Wis|Minn)\s+L\.?\s*(?:Rev|J)\.?\b(?!\'s)(?!,)(?!\s+(?:observed|held|said|noted|stated|considered|doubted|suggested|opined|found|agreed|dismissed|allowed|affirmed|reversed|explained|warned|concluded|emphasised|emphasized|acknowledged|rejected|accepted|distinguished|adopted|disapproved|dissented|remarked|added|pointed|stressed|recognised|recognized))',
                                                                         
                                                                                         
                                                                                    
                                                                                         
                                                                      
    r"\b\d{1,3}\s+(?:[A-Z][A-Za-z.&'\-]{0,14}\s+){1,3}L\.?\s?(?:Rev|J|Q)\.?\s+\d{1,4}\b",
                                        
                                                                                     
                                                                                     
                                                                                     
                
                                                                                         
                                                                                          
                                                                                     
                                                                                      
                                                                                     
                                                                                         
                                                        
    r'[\x22“][^\x22“”]{10,}[\x22”]\s*[\(\[]\d{4}[\)\]]\s+\d*\s*(?:SAcLJ|Sing\s?JLS|LQR|CLJ|OJLS|SJLS|LMCLQ|JBL|ICLQ|MLR|CLP)\b',
                                                                                            
                                                                                           
                                                                                      
                                                        
                                                       
                                                                                          
                                                                                         
                                                                                          
                                                              
    r"(?-i:\b\d{1,3}\s+(?:[A-Z][A-Za-z.&'\-]{0,14}\s+){0,3}"
    r"(?:[A-Z][a-z]{1,9}L[JQ]\b\.?|[A-Z]{2,5}L\s?Rev\b\.?|[A-Z][a-z]{1,9}L\s?Rev\b\.?)"
    r"\s+\d{1,4}\b)",
                                                                             
    r"(?-i:\b\d{1,3}\s+(?:[A-Z][A-Za-z.&'\-]{0,14}\s+){1,3}\([A-Z][A-Za-z.]{1,6}\)\s+"
    r"L\.?\s?(?:Rev|J|Q)\.?\s+\d{1,4}\b)",
                                                                                   
                                                                                           
                                                                                          
                                                                                
    r"(?-i:\b\d{1,3}\s+(?:[A-Z][A-Za-z.&'\-]{0,14}\s+){0,2}[A-Z][a-z]{1,9}\.?\s+J\.\s+"
    r"(?:(?:of\s+|on\s+|&\s+)?[A-Z][A-Za-z.&'\-]{0,14}\s+){1,3}\d{1,4}\b"
    r"(?=(?:,\s*[\d\-\u2013, n.and]{1,30})?\s*\((?:1[89]|20)\d{2}\)))",
]


                                                                                         
                                                                                       
                                                                               
                                                                                        
                                                                                   
                                                                                     
                                                                  
                                                                                          
                                                                                        
                                                                 
_ACAD_BOOK_PATTERNS = [
                                         
                                                                                            
                                                                                              
                                                                                            
                                                                                               
                                                                                            
                                                                                        
                                                                                      
                                                
    r"[A-Z][A-Za-z'’\-]+(?:\s+[A-Z][A-Za-z'’\-]+)*"
    r"(?:\s*(?:&|and)\s*(?:[A-Z]\.?\s+)*[A-Z][A-Za-z'’\-]+)?"
    r"(?:\s+et\s+al)?"
    r",\s+[A-Z][A-Za-z'’\s:,\-]+\([A-Za-z&.\s]+,\s*"
    r"(?:\d{1,2}(?:st|nd|rd|th)\s+[Ee]d(?:ition)?\.?,\s*)?\d{4}\)",
                                                                                               
                                                                                              
    r'(?:[A-Z][a-z]+\s+and\s+)?[A-Z][a-z]+,\s+[A-Z][A-Za-z\x27\u2019\s:,\-]{5,}\((?:\d+(?:st|nd|rd|th)\s+[Ee]d(?:ition)?(?:,\s*)?)(?:1[89]\d{2}|20[0-2]\d)\)',
                                                                                     
                                                                                             
                                                                                            
                                                                                           
                                                                                            
    r'(?!(?:Australia|Britain|Commission|Organization|Organisation|Council|Tribunal|Actuary|Counsel|Parliament|Government|Department|Florida|Bhd|Series|Institute|Offences|Sale|Purchase|Supply)\b)[A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)?,\s+(?!Report\b|Review\b|Final\b|Interim\b|Working\b|A\s+Report\b|A\s+Review\b|Discussion\s+Paper\b|University\s+Press\b)[A-Z][A-Za-z\x27\u2019\s:,\-]{12,},?\s+\((?:1[89]\d{2}|20[0-2]\d)\)(?!\s*\d)',
                                                                                              
                                                                 
                                                    
                                                                                      
    r'(?<! v )(?<!v\. )\b[A-Z][a-z]{2,12}\s+[A-Z][a-z]{2,15},\s+(?!Report\b|Review\b|Final\b|Interim\b|Working\b)[A-Z][A-Za-z\x27\u2019\s:,\-]{12,},?\s+\((?:1[89]\d{2}|20[0-2]\d)\)(?!\s*\d)(?!\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',
                                                                                     
                                                                                       
                                                                                       
    r'(?<! v )(?<!v\. )\b[A-Z]{1,3}\.?\s+[A-Z][a-z]{2,15}(?:-[A-Z][a-z]+)?,\s+(?!Report\b|Review\b|Final\b|Interim\b|Working\b)[A-Z][A-Za-z\x27\u2019\s:,\-]{12,},?\s+\((?:1[89]\d{2}|20[0-2]\d)\)(?!\s*\d)',
                                                                         
                                                                                             
                                                                                       
                                                                     
                                                                                   
    r'(?<!Lord )(?<!of )\bHalsbury\b',                                                                 
    r'\bChitty\b(?!\s+(?:J|LJ|CJ)\b)',                                           
    r'\bSalmond\b(?!\s+(?:J|LJ|CJ)\b)',                                           
    r'(?<! v )(?<! v\. )\b(?:Dicey|(?:Mc|Mac)Gregor|Treitel|Winfield)\b(?!\s*[-,]?\s*(?:Doniger|Inc|Ltd|Pty|Pte|Co\b|Corp|Plc|LLC))(?!\s+v[\s.])(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',
    r'\bSnell\b(?!\s+v\s)',                                                            
    r'(?<! v )(?<! v\. )\b(?:Bowstead|Phipson|Archbold|Lewin|Gatley)\b(?!\s*[-,]?\s*(?:Inc|Ltd|Pty|Pte|Co\b|Corp|Plc|LLC))(?!\s+v[\s.])(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',
    r'\bScrutton\b(?!\s+(?:J|LJ|CJ|MR)\b)',                                         
    r'\bKeating\b(?!\s+(?:J|LJ|CJ)\b)',                                           
    r'(?<! v )(?<!v\. )\bUnderhill\b(?!\s+v[\s.])(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                                                     
    r'\b(?:MacGillivray|Bennion|Colinvaux|Williston|Corbin)\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',
    r'\b(?:Oppenheim|Pomeroy|Craies|Odgers)\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                                                  
    r'\bBrownlie\b(?!\s+v\s)',                                                            
                                                                               
    r'\b(?:Beal|Dymond|Passmore)\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',
    r'\bSatow\b',                                                                                                   
    r'(?<! v )(?<!v\. )\bHiggins\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                       
    r'(?<! v )(?<!v\. )\bBlackstone\b(?!\s+v[\s.])(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                              
                                                          
    r'\bGoode\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                              
    r'\bArnould\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                               
    r'(?<!Lord Justice )\bLewison\b(?!\s+(?:J|LJ|CJ|MR|Justice)\b)',                                                                     
    r'(?<!Lord )\bErskine\b(?!\s+(?:J|LJ|CJ|MR|May)\b)',                                                                               
                                    
    r'\bWigmore\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                          
    r'\bThayer\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                       
    r'\bHoldsworth\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                             
    r'\bMaitland\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                
    r'\bBentham\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                        
    r'\bHandley\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                          
    r'\bHanbury\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                     
    r'\bZines\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)',                                                          
                                                           
    r'\bGale\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)(?!\s+v\s)',                                                     
    r'\bOliver\s+Wendell\s+Holmes\b',                                                                                                           
                           
    r"\bBuckley\s+on\s+(?:the\s+)?Companies\s+Acts?\b",                                                                             
    r"\bBuckley\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)(?!\s+v[\s.])(?!\s+(?:Holdings|Ltd|Limited|Group|Corp|LLP|Plc)\b)",                                                                     
    r"\bGore-Browne\b(?!\s+(?:J|LJ|CJ|MR)\b)",                                                              
    r"\bPennington\b(?!\s*,?\s*(?:J|LJ|CJ|MR|JA|JSC|JJ)\b)",                                  
                                                                                       
                                                                                            
                                                                                            
                                                                                           
                                                                                        
                                                                                              
                                                                                          
                                                                                            
                                                                              
                                 
    r'\bBankton\b',                                                                                           
    r'\bStair\b(?!\s+(?:Memorial|Society)\b)',                                                                                     
                                                                                        
    r'\b(?:Clerk\s*[&and]+\s*Lindsell|Goff\s*[&and]+\s*Jones|Spencer\s+Bower|Smith\s*[&and]+\s*Hogan)\b',
    r'\b(?:Mustill\s*[&and]+\s*Boyd|Megarry\s*[&and]+\s*Wade|Wade\s*[&and]+\s*Forsyth|Cross\s*[&and]+\s*Tapper)\b',
    r'\b(?:Bullen\s*[&and]+\s*Leake|Charlesworth\s*[&and]+\s*Percy|Cheshire\s*[,&]+\s*Fifoot|de\s+Smith)\b',
    r'\b(?:(?:Mc|Mac)Gregor\s+on\s+Damages|Chitty\s+on\s+Contracts|Gatley\s+on\s+Libel|Erskine\s+May)\b',
                                                         
    r'\bLowndes\s*(?:&|and)\s*Rudolph\b',                                                              
                                                                   
    r"\bBenjamin'?s?\s+(?:Sale|on\s+Sale)\b",
    r"\bFleming'?s?\s+(?:Law\s+of\s+Torts|Torts)\b",
    r"\bGower'?s?\s+(?:Principles|Company|Modern\s+Company)\b",
    r'\bSingapore\s+Civil\s+Procedure\b',
    r"\bMallal'?s?\s+Digest\b",
                                                                    
    r'\bStair(?:,\s+|\s+)Institutions\b',                                                                                              
    r'\bStreet\s+on\s+(?:Torts|the\s+Law\s+of\s+Torts)\b',                                                   
    r'\bCross(?:,\s+|\s+on\s+)(?:Statutory\s+Interpretation|Evidence)\b',                                                
    r'\bHarris(?:,\s+|\s+on\s+)(?:Law\s+and\s+Practice|Disciplinary)\b',                                                        
    r'\bGordon(?:,\s+|\s+on\s+)Criminal\s+Law\b',                                                                             
    r'\bArnott\s+on\s+(?:Arbitration|Shipping)\b',                                         
    r'\bLewison\s+on\s+(?:Contracts?|Interpretation)\b',                                                                  
                                                                   
    r"\bPalmer'?s?\s+(?:Company\s+Law|Shareholders)\b",                                                        
    r"\bGore-Browne\s+on\s+Companies\b",                                                  
    r"\bCarter-Ruck\s+on\s+(?:Libel|Privacy|Defamation)\b",                          
    r"\bHarvey\s+on\s+(?:Industrial|Employment)\b",                                             
    r"\bMurphy\s+on\s+Evidence\b",                                                                                  
    r"\bHudson'?s?\s+(?:Building|Engineering)\b",                                            
    r"\bSimor\s+and\s+Emmerson\b",                                                                           
    r"\bWoodfall'?s?\s+(?:Law\s+of\s+)?Landlord\b",                                                   
    r"\bAppleman\s+on\s+Insurance\b",                                                       
    r"\bCoke(?:,\s+|\s+on\s+)(?:Institutes?|Littleton|Laws\s+of\s+England)\b",                                            
    r"\bStephen(?:,\s+|\s+on\s+)(?:History|Criminal\s+Law|Evidence|Digest)\b",                                             
    r"\bBacon'?s?\s+(?:Abridgment|Abridgement)\b",                                                         
                                                                                                   
    r"\bBell'?s?\s+Commentaries\b",                                                                        
    r"\bLindley\s+(?:and\s+Banks\s+)?on\s+Partnership\b",                                        
    r"\bBurrows'?\s+(?:Law\s+of\s+)?Restitution\b",                                        
    r"\bAtiyah'?s?\s+(?:Sale\s+of\s+Goods|Introduction\s+to\s+the\s+Law\s+of\s+Contract)\b",                          
    r"\bMerkin\s+on\s+(?:Arbitration|the\s+Arbitration\s+Act)\b",                             
    r"\bCretney'?s?\s+(?:Family\s+Law|Principles\s+of\s+Family\s+Law)\b",                        
    r"\bHayton\s+(?:and\s+(?:Mitchell|Marshall)\s+)?on\s+(?:Trusts?|the\s+Law\s+of\s+Trusts?)\b",                    
    r"\bCarver\s+on\s+(?:Bills?\s+of\s+Lading|Charterparties)\b",                             
    r"\bCopinger\s+(?:and\s+Skone\s+James\s+)?on\s+Copyright\b",                         
    r"\bByles\s+on\s+Bills\s+of\s+Exchange\b",                                             
    r"\bChalmers\s+(?:and\s+Guest\s+)?on\s+Bills\s+of\s+Exchange\b",                                 
    r"\bBriggs\s+(?:on\s+)?(?:Civil\s+Jurisdiction|Conflict\s+of\s+Laws)\b",                                
    r"\bBurrows'?\s+(?:Understanding|Casebook\s+on)\s+(?:the\s+Law\s+of|Contract)\b",                       
    r"\bCousins\s+on\s+(?:the\s+Law\s+of\s+)?Mortgages\b",                          
    r"\bFoskett\s+on\s+(?:the\s+Law\s+of\s+)?Compromise\b",                          
                                                                                             
             
                                                                 
                                                                                                 
                                                                                                   
                                                                                                   
                                                                                       
                                                               
                                                                                              
                                                                                             
                                                                                                   
                                                                                                
    r'(?<! v )(?<! v\. )\b(?!Sweet\b|Oxford\b|Cambridge\b|Hart\b|Thomson\b|Kluwer\b|Wolters\b|Butterworth\b|Stevens\b|Clarendon\b|Routledge\b|Springer\b|Elsevier\b|Longman\b|Blackwell\b|Macmillan\b)[A-Z][a-z]{2,15}(?:\s+[A-Z][a-z]{2,15})?\s+(?:and|&)\s+(?!Maxwell\b|Reuters\b|Sons\b|Brothers\b|Wales\b|Scotland\b|Ireland\b|England\b|Children\b|Women\b|Men\b|Education\b|Science\b|Health\b|Technology\b|Contracts\b|Trusts\b|Trust\b|Justice\b|Courts?\b|Parliament\b|Another\b|Others\b)[A-Z][a-z]{2,15}(?:\s+[A-Z][a-z]{2,15})?\b(?=\s*,\s*[A-Z])(?=[\s\S]{0,150}(?:\d+(?:st|nd|rd|th)\s+[Ee]d|\(\s*(?:1[89]\d{2}|20[0-2]\d)\s*\)))'
                                                                                         
                                                                                           
                                                                                         
                                                                                          
                                                                                
                                                                                    
                                                                
                                           
                                                                                            
                                                                                           
                                                                                       
                                                                                        
                                             
    r'(?!\s*,?\s*(?:Inc|Corp|Co|Ltd|LLC|Assn|Dept|Bd|Bros|Univ)\b)',
    r'(?<! v )(?<! v\. )\b(?!Sweet\b|Oxford\b|Cambridge\b|Hart\b|Thomson\b|Kluwer\b|Wolters\b|Butterworth\b|Stevens\b|Clarendon\b|Routledge\b|Springer\b|Elsevier\b|Longman\b|Blackwell\b|Macmillan\b)[A-Z][a-z]{2,15}(?:\s+[A-Z][a-z]{2,15})?\s+(?:and|&)\s+(?!Maxwell\b|Reuters\b|Sons\b|Brothers\b|Wales\b|Scotland\b|Ireland\b|England\b|Another\b|Others\b)[A-Z][a-z]{2,15}(?:\s+[A-Z][a-z]{2,15})?\b(?=\s+on\s+[A-Z])(?=[\s\S]{0,150}(?:\d+(?:st|nd|rd|th)\s+[Ee]d|\(\s*(?:1[89]\d{2}|20[0-2]\d)\s*\)))'
    r'(?!\s*,?\s*(?:Inc|Corp|Co|Ltd|LLC|Assn|Dept|Bd|Bros|Univ)\b)',
                                                         
                                                                                            
                                                                                           
                                                                                            
                                                                                                 
                                                                                 
                                                                                           
                                                                                              
                                                                                             
                               
                                                                                               
                                                                                            
                                                                                            
                                                                                         
                                                                     
                                                                                               
                                                                                             
                                                
                                                                                           
                                                                                         
                                                                              
                                                                                            
                                                                                                 
                                                                                 
                                                                                           
                                                                     
     
                                                                                               
                                                                                       
                                                                                              
                                                                                           
                                                       
     
                                                           
                                                                                 
                                                                                 
                                                                                              
                                                                                    
                                                                                  
                                                                                       
                                                                                       
                                                                                             
                                                                                     
                                                                                           
     
                                                                                           
                                                                                       
                                                                                              
                                                                                            
                                                                                        
                                                          
                                   
                                                                                           
                                                                          
                                                                                   
                                                                                             
                                                                                   
                                                                              
                                                                     
                                                                     
                                                                                                
                                                                                     
                                                                                         
                                                                                            
                                                                                       
                                                                                             
                                                                                         
                                                                                 
    r"(?:[A-Z][A-Za-z'’\-]+(?:\s+[A-Z][A-Za-z'’\-]+){0,3},?\s+)?"
    r"(?:Law\s+Reform\s+Commission|Law\s+Commission|Law\s+Reform\s+Committee"
    r"|Law\s+Institute|Sentencing\s+Commission|Law\s+Revision\s+Committee)"
    r",\s+[A-Z][A-Za-z'’\s:,\-]{6,90}?"
    r"(?:,\s*Report\s+No\s*\d+)?"
    r"\s*\((?:1[89]|20)\d{2}\)",
                                                                                            
                                                                                                      
                                                                               
                                                                                     
                                                                                      
                                                                                     
                                                            
                                                                                            
                                                                               
                                                                                             
                                                                                
                                                                                             
                                                                                           
    r"'[^']{10,240}',?\s+in\s+[A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)?\s+\(eds?\)",
                                                             
    r'[\x22“][^\x22“”]{10,240}[\x22”],?\s+in\s+[A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)?\s+\(eds?\)',
    r'\bAmerican\s+Law\s+Institute\b',                                             
                                                                                       
                                                                                         
                                                                                      
                                                                                         
                                                                                       
                                                                                    
                                                                                     
                                                                         
    r'\bRestatement\s+(?:\([A-Za-z]+\)\s+)?of\s+(?:the\s+)?(?-i:[A-Z])[A-Za-z\s]{2,30}',                                                              
    r"Sweet\s+(?:&|and)\s+Maxwell'?s?\s+Encyclop(?:ae|e)dia",                                                     
                                                                             
                                                                              
                                                                                         
                                                                                         
                                                                                         
    r"(?<! v )(?<! v\.)\b(?!Convention|Protocol|Agreement|Treaty|Regulation|Statute|Code|Ordinance)[A-Z][a-z]{2,20}(?:\s+(?:and|&)\s+[A-Z][a-z]{2,20})?(?:'s\s+|,\s+|\s+on\s+(?:the\s+)?)(?:The\s+)?Law\s+of\s+[A-Z][A-Za-z]{2,25}(?:\s+[A-Z][A-Za-z]{2,25}){0,2}(?=[\s\S]{0,200}(?:1[89]\d{2}|20[0-2]\d))",
                                                                                                      
                                                                                                   
                                                                                             

                                                                                
     
                                                                                          
                                                  
                                  
                                                                                  
                                                             
                                                               
                                                                                         
                                                                                       
                                                                                        
                                                                                          
                                                                                          
                                                                                            
                                                                                              
                                                                                            
                                                                                              
                                                                                               
                                                                  
    r"\b(?:[Vv]an\s+(?:[Dd]er\s+)?|[Vv]on\s+|[Dd]e\s+(?:la\s+)?|[Dd]u\s+)?"
    r"[A-Z][A-Za-z'’-]{2,20}"
    r"(?:\s+et\s+al\.?)?"
    r"(?:\s+(?:and|&)\s+[A-Z][A-Za-z'’-]{2,20})?"
    r"(?:\s*\(eds?\))?"
    r",\s+(?:The\s+|An?\s+)?[A-Z][A-Za-z]{2,24}"
                                                                                              
                                                                                          
                                                                                             
                                                                    
                                                                                            
                                                                                             
                                                   
                                                                                          
                                                                                           
                                                                                           
                                                                                       
                  
                                                                                         
                                                                                             
                                                                                              
                                                                                               
                                                                                      
    r"(?:\s+(?:of|on|and|the|in|to|into|for|their)\s+[A-Za-z]{2,24}|\s+[A-Z][A-Za-z]{2,24}){1,7}"
                                                                                                
                                                                                      
                                                                                                
                                                                                            
                                                                                                
                                                                                       
    r"(?::\s+(?:The\s+|An?\s+)?[A-Z][A-Za-z]{2,24}"
    r"(?:\s+(?:of|on|and|the|in|to|into|for|their)\s+[A-Za-z]{2,24}"
    r"|\s+[A-Z][A-Za-z]{2,24}){0,6})?"
    r"(?:\s*;\s*[a-z][A-Za-z\s]{4,60})?"
                                                                                   
                                                                                      
                                                                                   
                                                                                      
                                                                                   
                                                                           
    r"(?:\s+[IVX]{1,4}\b)?"
    r"(?:[,;]?\s*(?:1[6-9]|20)\d{2}\s*[-\u2013]\s*(?:1[6-9]|20)?\d{2})?"
    r"[,;]?\s*(?:\d{1,2}(?:st|nd|rd|th)\s+ed(?:ition)?\.?\s*)?,?\s*\((?:1[6-9]|20)\d{2}",

                                                                                   
                                                                                   
                                                                                   
                                                                                     
                                                                                      
                                                               
    r"\b[A-Z][A-Za-z'’-]{2,20}(?:\s+(?:and|&)\s+[A-Z][A-Za-z'’-]{2,20})?"
    r"\s+in\s+(?:his|her|their|its)\s+(?:[a-z]+\s+(?:edition|work)\s+of\s+)?"
    r"(?:The\s+|An?\s+)?[A-Z][A-Za-z]{2,24}"
    r"(?:\s+(?:of|on|and|the|in|to|for)\s+[A-Za-z]{2,24}|\s+[A-Z][A-Za-z]{2,24}){1,7}"
    r"[,;]?\s*\((?:1[6-9]|20)\d{2}",

                                                                                     
                                                                                     
                                                                                  
                                           
                                                                                     
                                                                                    
                                     
    r"\b[A-Z][A-Za-z'’-]{2,20}[’']s\s+(?:work\s+|book\s+|treatise\s+)?"
    r"(?:The\s+|An?\s+)?[A-Z][A-Za-z]{2,24}"
    r"(?:\s+(?:of|on|and|the|in|to|into|for)\s+[A-Za-z]{2,24}|\s+[A-Z][A-Za-z]{2,24}){1,7}"
    r"[,;]?\s*(?:\d{1,2}(?:st|nd|rd|th)\s+ed(?:ition)?\.?\s*)?,?\s*\((?:1[6-9]|20)\d{2}",

                                                                                 
                                                                                
                                                                                 
                                                         

                                                                        
                                                                                     
                                                                                      
                                                                                          
                                                                                       
                                                                               
                                                
     
                                                                               
     
                                                       
                                                       
                                                                         
                                                                    
                                                                    
     
                                                                                         
                                                                                        
                                                                                        
                                                         
                                                                        
                                                                                         
                                                                                           
                                                                                           
                                                                                        
                                                                    
     
                                                                                          
                                                                                        
                                                                                          
                                                                                 
                                                                                          
                                                                                        
    r'\b(?:Institutes?|Commentaries)\b[ \t,.]*[IVXLivxl]{1,6}\s*[.\s][ \t]*[IVXLivxl0-9]',

                                                                            
                                                                                
                                                                                      
                                                                                      
                                                                                  
                                                                                     
                                                                            
                                                   
     
                                                                                       
                                                                                    
                                                           
                                                                                   
                                                                                   
                                                                                      
                                                              
    r'\b(?:Coke|Erskine|Stair|Bankton|Blackstone|Hume)(?:[\x27\u2019]s)?\s*,?\s*(?:on\s+)?(?:[Tt]he\s+(?:First|Second|Third|Fourth)\s+[Pp]art\s+of\s+the\s+)?(?:the\s+)?(?:Institutes?|Commentaries)\b(?:[ ,.]*[IVXLivxl]+(?:[ .,]+[IVXLivxl0-9]+)+)?',
                                                                                                        
                                                                                                       
                                                                                                         
                                                                                                       
                                                                                                          
    r"(?-i:(?<! v )(?<! v\. )\b(?!(?:Commission|Committee|Report|Convention|Conference|Council|Covenant|Statement|Treaty|"
    r"Comment|Commentary|Note|Rules|Panel|Inquiry|Paper|Agreement|Protocol|Code|Guidelines|Directive|Declaration|Charter|"
    r"Court|Tribunal|Board|Decision|Position|Law|Act|Bill|Speech|Address|Lecture|Seminar|Symposium|Essays?|Notes|Remarks|"
    r"Finally|However|Similarly|Further|Indeed|Thus|Again|Moreover|Accordingly|Authority)\b)"
                                                                                                            
                                                                                                     
                                                                                                           
                                                                                                 
                                                                                                              
                                             
    r"(?P<fho1>[A-Z][a-z]{2,15})(?:,\s+[A-Z][a-z]{2,15},?\s+(?:and|&)\s+(?!(?P=fho1)\b)[A-Z][a-z]{2,15}"
    r"|\s+(?:and|&)\s+[A-Z][a-z]{2,15})?"
    r"\s+on\s+(?:the\s+)?[A-Z][a-z]+(?:\s+(?:of|and|the|[A-Z][a-z]+)){0,4}"
    r"(?:\s*[–—-]\s*[A-Z][a-z]+(?:\s+(?:and|of|[A-Z][a-z]+)){0,3})?)"
    r"(?=\s*\((?:[^()]{0,80}?(?:\b[Ee]d\b|[Ee]dition|[Ll]ooseleaf|[Ll]oose-leaf|Sweet|Maxwell|Brookers|Butterworths?|"
    r"LexisNexis|Thomson|Lawbook|Federation|Press|Publishing|Publishers)))",

                                                                                   
                                                                                    
                                                                                
                                                                                    
                                                                                        
     
                                                                                           
                                                                                         
                                                                                           
                                                                                          
                 
                                                                                          
                                                        
                                                                                      
                                                       
                                                                                          
                                                            
                                                                                           
                                                                                            
                                                
    r"\b[A-Z][A-Za-z'’-]{2,20}(?:\s+[A-Z][A-Za-z'’-]{2,20}){0,3}"
    r"\s+on\s+(?:the\s+)?[A-Z][A-Za-z]{2,24}"
    r"(?:\s+(?:of|and|the|in|for)\s+[A-Za-z]{2,24}|\s+[A-Z][A-Za-z]{2,24}){0,5}"
    r"\s*\([^()]{2,45}\s+gen(?:eral)?\s+ed(?:itor)?s?\s*\)",

                                                                                  
                                                                                  
                                                                                      
                                                                                   
                                                                                      
                                                                                         
                                                                                        
                                                                                         
                                                                                   
                                                     
    r'\((?:[A-Z][A-Za-z]+\s*[:/]\s*)?(?:Oxford\s+University\s+Press|Cambridge\s+University\s+Press|Hart\s+Publishing|Sweet\s*[&and]+\s*Maxwell|LexisNexis|Butterworths|Thomson\s+Reuters|Clarendon\s+Press|Stevens\s+[&and]+\s*Sons|Law\s+Book\s+Co|Academy\s+Publishing|Kluwer(?:\s+Law\s+International|\s+Academic)?)(?:\s+(?:Asia|Singapore|Australia|International))?,\s*(?:\d+(?:st|nd|rd|th)\s+[Ee]d(?:ition)?,?\s*)?\d{4}\s*[)(]',
    r'\([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s+University\s+Press,\s*(?:\d+(?:st|nd|rd|th)\s+[Ee]d(?:ition)?,?\s*)?\d{4}\)',
                                                                                       
                                                                                         
                                                                              
                                                                                         
                                                                                          
                                                                                    
                                      
     
                                                                                   
                                                                                       
                                                               
    r'\((?:[^()]|\([^()]{0,25}\)){3,70}?,\s*\d{1,2}(?:st|nd|rd|th)\s*[Ee]d(?:ition)?\b[^)]{0,25}\d{4}\)',
]


_DOT_ABBREV_RE = re.compile(
                                                                                               
    r'\b([A-Z][a-z]{1,9})\.[ \t]?([A-Z])\.[ \t]?([A-Z])\.[ \t]?([A-Z])\b\.?'
    r'|\b([A-Z][a-z]{1,9})\.[ \t]?([A-Z])\.[ \t]?([A-Z])\b\.?'
                                           
    r'|\b([A-Z])\.[ \t]?([A-Z])\.[ \t]?([A-Z])\.[ \t]?([A-Z])\.[ \t]?([A-Z])\b\.?'
    r'|\b([A-Z])\.[ \t]?([A-Z])\.[ \t]?([A-Z])\.[ \t]?([A-Z])\b\.?'
    r'|\b([A-Z])\.[ \t]?([A-Z])\.[ \t]?([A-Z])\b\.?'
    r'|\b([A-Z])\.[ \t]?([A-Z])\b\.?'
)


def _normalize_dotted_abbrevs(text):
    """Convert dotted uppercase abbreviations to plain form: L.Q.R. → LQR, M.L.R. → MLR."""
    def _join(m):
        return ''.join(g for g in m.groups() if g)
    return _DOT_ABBREV_RE.sub(_join, text)


                                                                     
                                                    


                                                                                            
                                                                                               
                                                                                               
                                                                                             
                                                                            
 
                                                                                           
                                                                                      
                                                                                       
                                                                                          
                                                                                             
            
                                                                                        
                                                                        
 
                                                                                       
                                                                                              
                                                                                          
                                                                                            
                                                                                             
                                                                                          
                                                                            
 
                                                                            
                                                                
                                                                        
                                                                              
                                                                                             
                                                                  
 
                                                                                          
                                                                                         
                                                                                       
                                                                                            
                                                                                           
                                                                                      
                                                                                            
                                                                                              
                                             
 
                                                                                          
                                                                                          
                                                                                
                                                                                             
                                                                                         
                                                                                         
 
                                                                                              
                                                                            
_NOT_A_WORK_RE = re.compile(
    r'^\s*constitution\s+of\s+the\b'
    r'|\bsecond\s+reading\b'
    r'|\bparliamentary\s+debates\b'
    r'|^\s*(?:would|provides|which)\b',
    re.I)
                                                                                      
                                                                                        
                                                                                           
                                                                                           
                                                                                           

                                                                                            
                                                                                        
                                                                                           
 
                                                                                         
                                                                       
                                                                                                    
                                                                  
                                                                                             
                                                                                            
                                                                            
                                                                                           
                                                                                              
                                                          
                                                                                        
 
                                                                                            
                                                                                             
                                                                                            
            
                                                                                  
                                                                                       
 
                                                          
                                                                                          
                                                                           
 
                                                                                            
                                                                                  
                                                                                            
                                                                                         
                                                                                 
                                                                                           
                                                                                          
 
                                                                                            
                                                                                                
                                                                                          
                                                           
_US_REPORTER_IN_TITLE = re.compile(
    r'\b\d{1,4}\s+(?:u\.?\s?s\.?|f\.?\s?\d?d|s\.?\s?ct\.?|wl)\s+\d'
    r'|\bfed\.?\s?reg\.?\b'
    r'|\bgao[\u2013\u2014-]\d',
    re.I)
                                                                                     
                                                                                        
                                                                                        
                                                                                            
                                                                       
_NEWS_OUTLET = re.compile(
    r'\bnpr\b|\bidaho\s+statesman\b|\bmissouri\s+independent\b'
    r'|\bnew\s+york\s+times\b|\bwashington\s+post\b|\bwall\s+street\s+journal\b',
    re.I)

_GOV_REPORT_RE = re.compile(
    r'\bcommission\s+of\s+inquiry\b'
    r'|\broyal\s+commission\b'
    r'|\btruth\s+and\s+reconciliation\s+commission\b'
    r'|\bcalls\s+to\s+action\b'
    r'|\breport\s+of\s+the\s+(?:review|inquiry|committee|commission)\b'
    r'|\breport\s+of\s+proceedings\s+of\s+the\s+committee\b'
    r'|\b(?:white|green)\s+paper\b'
    r'|\bannual\s+report\b'
    r'|\bprivy\s+council\s+office\b'
    r'|\bguide\s+to\s+making\s+federal\s+acts\b'
    r'|\bdepartment\s+of\s+[a-z]+\s*,?\s*report\b',
    re.I)

                                                                                                                        
                                                                                              
                                                                                                
                                                                                      
                                                                                               
                                                                                                 
                                
                                                                                               
                                                                                                 
                            
                                                                                                             
                                                                                                               
                                                                                                                  
                                                                  
_ENCYCLOPAEDIA_BARE = re.compile(
    r"^\s*(?:\d{1,3}\s+)?(?:halsbury(?![\'’`]?s?,?\s+(?:the\s+)?laws?\b)|corpus\s+juris|am(?:erican)?\s?jur)\b",
    re.I)

_ENCYCLOPAEDIA_RE = re.compile(
                                                                                                               
                                                                                                       
    r"\bHalsbury\'?s\s+Statutes\b"
    r"|\bCorpus\s+Juris\b"
    r"|\bAm(?:erican)?\.?\s?Jur(?:isprudence)?\.?\s?2?d?\b"
    r"|\bEncyclopaedia\s+of\s+\w+\s+Law\b",
    re.I)

                                                                                                              
                                                                                                                  
                                                                                                             
                                                                                                                
                                                                                                                 
                                                                                                                 
                                                                 
ENCYCLOPAEDIAS_IN = os.environ.get("JR_ENCYC_IN", "1") != "0"
                                                                                                               
_ENCYCLOPAEDIA_BARE_IN = re.compile(r"^\s*(?:\d{1,3}\s+)?halsbury(?![\'’`]?s?,?\s+(?:the\s+)?(?:laws?|statutes)\b)\b", re.I)
                                                                                                            
                                         
_ENCYC_NAME_RE = re.compile(
    r"\bHalb?sbury[’'`]?s?\s+(?:Laws?|Statutes)\b|\bCorpus\s+Juris\b|\bAm(?:erican)?\.?\s?Jur(?:isprudence)?\b"
    r"|\bStair\s+Memorial\s+Encyclop|\bEncyclop(?:a|æ)?edia\b|\bWikipedia\b", re.I)

                                                                                         
                                                                                         
                                                                             
_ALI_COMMENT = re.compile(
    r"(?:\bALI\b|\bAmerican\s+Law\s+Institute\b)[^.;]{0,80}?\bComments?\b"
    r"|\bModel\s+Penal\s+Code\b[^.;]{0,60}?\bComments?\b"
    r"|\bRestatement\b[^.;]{0,60}?\bComments?\b",
    re.I)


_NON_LEGAL_EXCLUDE_RE = re.compile(
    r'\bEnglish\s+Grammar\b'
    r'|\bGrammar\s+of\s+(?:the\s+)?English(?:\s+Language)?\b'
    r'|\b(?:Principles?|Theory|Introduction)\s+of\s+(?:Economics?|Political\s+Economy|Linguistics?)\b'
    r'|\bOxford\s+English\s+Dictionary\b'
                                                                                             
                                                                                         
                                                                                             
                                                                                           
                                                                                          
                                                                                            
                                              
    r'|^\s*(?:the\s+|a\s+|le\s+|la\s+|les\s+)?dicti?onn?ary?\b'
    r'|^\s*(?:the\s+|a\s+|le\s+|la\s+|les\s+)?dictionnaire\b'
    r'|\bdictionn?aire\s+d[eu]\b'
                                                                                      
                                                                                          
                                                                                
                                                                                            
                                                                                         
                                                                              
                                                                                           
                                                                                           
                                                                                            
                                                                                       
                                                                                           
                                                                         
    r'|\bModern\s+English\s+Usage\b'
    r'|\bGuide\s+to\s+Grammar\b'
                                                                                          
                                                                                           
                                                                                          
                                                                     
    r'|\bChicago\s+Manual\s+of\s+Style\b'
    r'|\bManual\s+of\s+Style\b',
    re.IGNORECASE
)

_JOURNAL_ABBREV_ALIASES = {
                                                                     
                                                                  
                                                                         
                                                                                        
                                                              
                                                                             
                                                                                  
                                                                                         
                                                                                        
                                                                                        
                                                                                        
    'melbulawrw':  'melbourne university law review',
    'mulr':        'melbourne university law review',
    'sydlawrw':    'sydney law review',
    'sydlr':       'sydney law review',
    'unswlawjl':   'university of new south wales law journal',
    'unswlj':      'university of new south wales law journal',
    'adellawrw':   'adelaide law review',
    'fedlawrw':    'federal law review',
    'monashulawrw': 'monash university law review',
    'undaulawrw':  'university of notre dame australia law review',
    'uwalawrw':    'university of western australia law review',
    'qutlawjjl':   'queensland university of technology law journal',

    'clj':   'cambridge law journal',
    'lqr':   'law quarterly review',
    'mlr':   'modern law review',
    'ojls':  'oxford journal of legal studies',
    'sjls':  'singapore journal of legal studies',
    'saclj': 'singapore academy of law journal',
    'iclq':  'international and comparative law quarterly',
    'jbl':   'journal of business law',
    'lmclq': 'lloyd maritime and commercial law quarterly',
    'nzlj':  'new zealand law journal',
    'clp':   'current legal problems',
    'edinlr': 'edinburgh law review',
    'edinburghlrev': 'edinburgh law review',
    'crimlr':   'criminal law review',
    'nilq':     'northern ireland legal quarterly',
    'btr':      'british tax review',
    'ehrlr':    'european human rights law review',
    'ottawalr': 'ottawa law review',
}

                                                                                   
                                                                                  
                                                                               
                                                                   
                                                                                      


_J3_PATTERN_INDICES = frozenset({2, 3, 4})

                                                                                               
                                                                                         
                                                                                                
                                                                                               
                                                                                          
                                                                                        
                                                                                        
                                                                                       
                                                                               
_US_FORM_JOURNAL_INDICES = frozenset(
    range(len(_ACAD_JOURNAL_PATTERNS) - 3, len(_ACAD_JOURNAL_PATTERNS)))
_TITLE_YEAR_BEFORE = re.compile(
    "[\"'\u201d\u2019][ \t\u00a0]*[(][ \t]*[0-9]{4}(?:[ \t]*[-\u2010\u2011\u2013][ \t]*[0-9]{2,4})?"
                                                                                            
                                                                              
    "[ \t]*[)][ \t\u00a0]*,?[ \t\u00a0]*(?:[0-9]{1,3}[ \t]*:[ \t]*)?$")

def _j3_has_context(work, s, e, window=100):
    """Return True if a J3 bare abbreviation appears in a citation context
    (year in parens/brackets, volume number immediately before, or page number
    immediately after — within window chars)."""
    pre  = work[max(0, s - window):s]
    post = work[e:min(len(work), e + window)]
    year_nearby = bool(re.search(r'[\(\[]\d{4}[\)\]]', pre + post))
    vol_before  = bool(re.search(r'\b\d{1,3}[ \t]+$', pre))
    page_after  = bool(re.search(r'^[ \t]*\d{1,5}\b', post))
    return year_nearby or vol_before or page_after


                                                                                          
                                                                                          
                                                            
                                                       
                                                  
                                              
                                                                                             
                                                                                           
                                                                                     
                                       
_LEAD_JUNK = re.compile(r"^(?:[a-z][a-z']*[\s,]+){1,6}(?=[A-Z])")
                                                                             
                                                                                  
                                                                           
                                                                             
                                                                        
                                                                  
_LEAD_CUE = re.compile(r"(?i)^(?:see\s+also|but\s+see|see|cf|compare|contra|"
                       r"accord|eg|generally|especially|also|further|citing|"
                       r"quoting|quoted\s+in)[\s,:.]+")


                                                                                       
                                                                                      
                                                                                        
                                                                            
                                                                        
                                                   
                                                                                          
                                                                                      
_OFFICIAL_REPORT = re.compile(
    r"(?i)\b(?:royal\s+commission|law\s+reform\s+commission|advisory\s+committee|"
    r"select\s+committee|standing\s+committee|joint\s+committee|"
    r"committee\s*,|commission\s*,|working\s+party|green\s+paper|white\s+paper|"
    r"command\s+paper|Cmnd|Cmd\b|H\.?R\.?\s+Rep|S\.?\s+Rep|"
    r"parliamentary\s+debates|hansard|european\s+convention|convention\s+for\s+the|convention\s+on\s+|code\s+of\s+guidance|guidance\s+note|practice\s+direction|(?<!American\s)law\s+institute|law\s+council|health\s+organi[sz]ation|commonwealth\s+of\s+australia|model\s+penal\s+code|law\s+commission|interagency|discussion\s+paper|"
                                                                                           
                                                                       
                                                                                             
                                                                
                                                                               
                                                                         
                                                                                            
                                          
                                                                                             
                                                                                      
                                                                                          
                                                            
    r"audit\s+office|\bactuary\b|committee\s+(?:for|of|on)\s+|"
                                                                                             
                                                                
                                                                            
                                                     
                                                                                            
                                                                                        
                                                                                     
    r"cabinet\s+office|hm\s+treasury|home\s+office|department\s+of\s+state\s+bulletin|"
                                                                           
                                                                         
                                                     
                                                                                
                                                                                 
                                                                              
                                                           
    r"remuneration\s+tribunal|(?:initial|interim|final)\s+report|"
    r"department\s+of\s+finance|office\s+for\s+national\s+statistics|"
    r"handbook\s+on\s+procedures|enforcement\s+guide|"
                                                                                          
                                                                                            
                                                                                            
                                                                           
                                                                                     
                           
                                                                                   
                                                                                      
                                                                        
                                                                                    
                                                                                         
                                
    r"united\s+nations|general\s+assembly|security\s+council|"
    r"convention\s+against\s+|model\s+law\b|international\s+law\s+commission)\b")


                                                                            
 
                                                                                  
                                                                                   
                                                                                     
                                                                                         
                                                                                        
                                                             
                                                                                        
                                                                                     
                                                                                             
                                                                                     
_R22_GOVT_DOC = re.compile(
    r"(?i)\b(?:"
    r"memorandum\s+from|congressional\s+research\s+service|crs\s+report"
    r"|office\s+of\s+legal\s+counsel|assistant\s+attorney\s+general"
    r"|deputy\s+solicitor\s+general|solicitor\s+general\s+to"
    r"|clerk\s+of\s+court|special\s+message|delegation\s+of\s+authority"
    r"|general\s+order\s+no|exchange\s+act\s+release|bureau\s+of\s+justice\s+statistics"
    r"|comm(?:'|’)?r\s+of|commissioner\s+of\s+indian\s+affairs"
    r"|field\s+manual|statistical\s+tables"
                                                                                              
                               
                                                                                                
                                                                                             
                                                                                               
                                                                  
    r"|bureau\s+of\s+(?:the\s+)?census|department\s+of\s+justice"
    r"|office\s+of\s+the\s+governor|journals\s+of\s+the\s+continental\s+congress"
    r"|commencement\s+proclamation|executive\s+order|federal\s+register"
    r"|digest\s+of\s+contested-election|historical\s+population\s+density"
                                                                                         
                                                                                          
                                                                                          
                               
    r"|royal\s+commission|task\s+force|commission\s+of\s+inquiry"
    r"|select\s+committee|standing\s+committee|departmental\s+committee"
    r"|committee\s+of\s+inquiry"
    r")\b")
_NEWS_MASTHEAD = re.compile(
    r"(?i)\b(?:"
    r"cnnmoney|cnn\.com|boston\s*herald|boston\.com|bostonherald|smithsonian\s+magazine"
    r"|abcnews|abc\s+news|news\s+on\s+6|huffpost|huffington\s+post|bloomberg"
                                                                                                
                                                                                            
    r"|(?<!thomson\s)reuters|associated\s+press|npr\.org|politico|the\s+guardian|nytimes|wate\.com"
    r"|washington\s+post|wall\s+street\s+journal|usa\s+today|newsweek|slate\.com|vox\.com"
    r")\b")

_NOT_A_WORK = re.compile(
                                                                                               
                                                                                      
                                                                                           
                                                                                              
                                                                          
                                                                                           
                                                      
                                                                               
                                                                                           
                                                                                      
                                                                             
    r"(?i)\b(?:dictionary|thesaurus"
                                                                                            
                                                                                           
                                                                                           
                                                                                           
                                                                                            
                                                                                          
                                                                
                                                                                             
                                                                                             
                                                                                         
                                                                                           
                                                                                       
                                           
                                                
                                                            
                                                
                                                                         
    r"|restatement\s+of\s+(?:the\s+)?"
    r"(?:law(?!\s*,\s*[A-Za-z]{2,}\s*,?\s*[23]d\b)|requirement|a\s+passage)"
    r"|S\.?L\.?T\.?\s*\(\s*Notes\s*\)"
    r"|(?:__CRIMLR_HANDLED_SEPARATELY__)"
                                                                                   
                                                                                         
                                                                                        
                                                           
    r"|\bAct\s*\(\s*Cap|\bRev\s+Ed\s*\)"
    r"|\b(?:General\s+Laws|Revised\s+Statutes|Consolidated\s+Laws)\s+of\s+[A-Za-z]"
                                                                                           
                                                                                              
                                                                                              
                                                                         
    r"|\bAct\b\s*[,(]\s*(?:1[6-9]|20)\d{2}|\bAmendment\b\s*[,(]\s*(?:1[6-9]|20)\d{2}"
                                                                                           
                                                                               
    r"|^\s*(?:International\s+)?(?:Covenant|Convention|Protocol|Treaty|Charter)\s+on\b"
    r"|\bCovenant\s+on\s+(?:Civil|Economic|Human)\b"
                                                                    
    r"|\bSdn\s+Bhd\b|\bPte\s+Ltd\b"
    r"|\b(?:Selected|Collected)\s+Poems\b"
                                                                      
    r"|\b[A-Z][A-Za-z]+\s+v\.?\s+[A-Z][A-Za-z]+(?:\s+[A-Za-z]{2,}){0,6}\s*\((?:1[6-9]|20)\d{2}\)"
                                                     
    r"|\bM(?:r|rs|s|iss)\s+[A-Z][a-z]+,?\s+(?:QC|SC|KC)?\s*,?\s*for\s+the\b)")


                                                                                          
                                                                                             
                                                                                           
                                                                                          
                                                                                            
                                                                                              
                                                                                          
                                                                                              
                                                                                         
                                                                                          
                                                                                           
_NAMED_STATUTE = re.compile(r"(?i)\bAct\s+(?:1[6-9]|20)\d{2}\b"
                            r"|\b(?:1[6-9]|20)\d{2}\s+Act\b")


                                                                                 
                                                                     
                                                                          
                                                                                      
                                                                                       
                                                          
                                                                                 
                                                                                             
                                                                                              
                                                                                      
                                                                                         
_TITLE_BY_AUTHOR = re.compile(
    r"\b(?:[Tt]he|[Aa]n|[Aa])\s+[A-Z][A-Za-z'\u2019\-]{2,}"
    r"(?:\s+(?:of|on|and|the|in|to|for|a|an)\s+[A-Za-z][A-Za-z'\u2019\-]{1,24}"
    r"|\s+[A-Z][A-Za-z'\u2019\-]{1,24}){2,8}"
    r"\s+by\s+"
    r"(?:Sir\s+|Dr\s+|Professor\s+|Prof\s+|Lord\s+)?"
    r"[A-Z][A-Za-z'\u2019.\-]*(?:\s+[A-Z][A-Za-z'\u2019.\-]*){1,4}"
    r"(?=[^.;]{0,30}?(?:published|(?:1[6-9]|20)\d{2}|\d{1,2}(?:st|nd|rd|th)\s+ed))")

_QUOTED_TITLE = re.compile(
    r"[\u201c\"\u2018'](?=[^\u201d\"\u2019']*\s[^\u201d\"\u2019']*\s)"
    r"[^\u201d\"\u2019']{10,180}[\u201d\"\u2019']")

                                                                                          
                                                                                              
                        
_CRIMLR_CASE = re.compile(
    r"(?i)\b(?:R|Reg(?:ina)?|Rex|DPP|The\s+Queen)\s+v\.?\s+[A-Z][A-Za-z'\u2019\-]+"
    r"[^.;]{0,40}\[\d{4}\]\s*Crim|"
    r"\b[A-Z][A-Za-z'\u2019\-]+\s+v\.?\s+[A-Z][A-Za-z'\u2019\-]+[^.;]{0,40}"
    r"\[\d{4}\]\s*Crim")

_CRIMLR_CITE = re.compile(r"\[\d{4}\]\s*Crim\.?\s*\.?\s*L\.?\s*R\.?\s+\d")
_HAS_AUTHOR = re.compile(
    r"(?i)\b(?:Dr|Professor|Prof|commenting|commentary|noted\s+by|"
    r"in\s+a\s+(?:note|case\s+note)|editor)\b"
                                                                                  
                                                                                     
                                                                                       
                                                                                      
            
    r"|(?<![A-Za-z])[A-Z][a-z]{2,}\s*,\s*[‘“\x27\"]"
                                                                                          
                                                                                          
                                                                                            
                                                                                          
                                                                                          
                                                                                
    r"|\b(?:an?|his|her|their|the|this)\s+(?:\w+\s+){0,2}"
    r"(?:article|essay|comment(?:ary)?|note)\s+(?:in|at|published)\b")

                                                                                         
                                                                                         
_ARTICLE_CUE = re.compile(
    r"(?i)^(?:an?|his|her|their|the|this)\s+(?:\w+\s+){0,2}"
    r"(?:article|essay|case\s+note|note|comment(?:ary)?)\s+(?:in|at)\b")


                                                                                       
                                                    
                                                                         
                                                                              
                                                                                      
                                                                                        
                                                                                       
                                                                                         
                                         
                                                                                   
                                                          
_FOOTNOTE_MARK = re.compile(r"\[\d{1,3}\]")

_AUSTLII_TAG_ONLY = re.compile(
                                                                                       
                                                                                      
    r"(?i)^\s*(?:\[?\d{4}\]?\s*)?(?:MelbULawRw|SydLawRw|UNSWLawJl|AdelLawRw|FedLawRw|"
    r"MonashULawRw|UNDAULawRw|UWALawRw|QUTLawJJl|BondLawRw|DeakinLawRw|JCULawRw|"
    r"MqLawJl|NewcLawRw|UTasLawRw|CanterLawRw|VUWLawRw|OtaLawRw|WkoLawRw)\s*\d*\s*$")


                                                                                     
                                                                                            
                                                                                          
                                                                                            
                                                                                            
                                                                                             
                                                                                      
_FN_MARK = re.compile(r"\[(\d{1,4})\]\s")


def _footnote_cut(back):
    """Index of the rightmost footnote marker in BACK, ignoring a bracketed year, or -1."""
    best = -1
    for m in _FN_MARK.finditer(back):
        if 1500 <= int(m.group(1)) <= 2100:
            continue                                                                
        best = max(best, m.end() - 2)                                             
    return best


                                                                                      
                                                                                  
                                                                                          
                                 
                                                                                         
                                                                                              
                                                                      
                                                                                                      
_PRACTITIONER_TITLE = re.compile(r"(?!)")
                                                                                                       
                                                                                                          
                                                                                            
                                                                                                                
                                                         
_COURT_PAPER = re.compile(r"(?i)\b(?:Magistrate|Judge|Recorder|Tribunal|Court|Coroner)[\x27’]?s?\s+"
                          r"(?:Statement\s+of\s+Findings|Reasons\s+for\s+(?:Verdict|Sentence|Decision|Judgment)|Findings)\b")
                                                                                                                       
                                                                                                                    
                                                                                                                  
                                                                                                                  
                                                               
_STANDARD_FORM_BARE = re.compile(r"(?i)(?:Law\s+Society|Real\s+Estate\s+Institute)[^()]{0,60}?\bAgreement\s+for\s+(?:the\s+)?"
                                 r"Sale\s+(?:and|&)\s+Purchase\b|\bJCT\s+Standard\s+Form\b")
_STANDARD_FORM = re.compile(r"[\x22“‘']\s*(?:Agreement|Deed|Contract|Lease|Form)\s+(?:for|of)\s+(?:the\s+)?"
                            r"(?:Sale|Purchase|Lease|Hire|Building|Construction|Tenancy|Charter|Mortgage|Real|Residential)\b")
                                                                                                                  
                                                                                                                
                            
                                                                                                              
                                                                                                      
_FHO_EDITOR_BEFORE = re.compile(r"(?:\b[A-Z]{1,3}\.?|\b(?!(?:In|See|As|Cf|Per|And|Also|From|By|Following|Under|Of|The|"
                                r"Accord|Compare|Contra|Generally|Eg|Thus|Finally|Similarly|However)\b)[A-Z][a-z]+)\s+$")
_PUBLISHER_ONLY = re.compile(r"(?i)^\W*(?:(?:Lexis|Nexis|LexisNexis|Butterworths?|Sweet|Maxwell|Thomson|Reuters|"
                             r"Brookers|Lawbook|Co|Federation|Press|Oxford|Cambridge|University|Hart|Publishing|Ltd|"
                             r"Limited|Carswell|Juta|London|Sydney|Wellington|Toronto|Hong|Kong|and|&|\d+(?:st|nd|rd|th)|"
                             r"Edn?|Edition|\d{4})\W*)+$")
                                                                                               
                                                                                              
                                                                                          
_PRACTICE_ANNUAL = re.compile(
    r"\b(?:(?:The|Singapore|Hong\s+Kong|Malaysian|Atkin[\x27\u2019]s)\s+)?"
    r"(?:Supreme\s+Court\s+Practice|Civil\s+Procedure|Court\s+Practice|County\s+Court\s+Practice)"
    r"\s+(?:19|20)\d{2}\b(?!\s*\(\s*(?:Cap|No)\b)")


                                                                                           
                                                                                                 
                                                                                              
                  
                                                                                            
                                                                                 
                                                                                           
                                                                                       
                                                                                             
                                                                                            
_LAW_COM_PAPER = re.compile(
    r"(?:[\"“](?P<q>[^\"“”\n]{8,160})[\"”]\s*)?"
    r"\(?\s*(?P<b>(?:Scot(?:tish)?\.?\s+)?Law\s+Com(?:mission|\.)?(?:\s+Report)?\s*,?\s+[Nn]o\.?\s*(?P<n>\d{1,3})\b"
    r"|LCCP\s+(?P<n2>\d{1,3})\b"
    r"|(?P<wp>Working|Consultation)\s+Paper\s+[Nn]o\.?\s*(?P<n3>\d{1,3})\b)")
_LAW_COM_NEAR = re.compile(r"(?i)\blaw\s+commission\b")

                                                                                                   
                                                                                                   
                                                                                                 
                                                                                                    
                                                                                     
                                                                                                
                                                            
                                                                                            
                                                             
                                                                                          
                                                                                               
                                         
                                                                                                 
                                                                                                  
                                                                                                
_LR_BODY = (r"(?:(?:[A-Z][A-Za-z]+\s+){0,4}Law\s+Reform\s+(?:Commission(?:er)?|Committee|Institute|Advisory\s+Council)"
            r"(?:\s+of\s+(?:the\s+)?[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3})?"
            r"|(?:Scottish\s+|English\s+)?Law\s+Commission(?:\s+(?:of|for)\s+[A-Z][A-Za-z]+(?:\s+(?:and\s+)?[A-Z][A-Za-z]+){0,3})?"
            r"|(?:Criminal\s+)?Law\s+Revision\s+Committee"
            r"|ALRC|NSWLRC|VLRC|QLRC|LRCWA|WALRC|NZLC|SALRC|TLRI|ALRI|LRC)")
_LR_PAPER = (r"(?:(?:Final\s+|Interim\s+)?Report|Working\s+Paper|Discussion\s+Paper|Issues\s+Paper|"
             r"Consultation\s+Paper|Consultative\s+Memorandum|Miscellaneous\s+Paper|Occasional\s+Paper|"
             r"Study\s+Paper|Research\s+Paper|Background\s+Paper|Preliminary\s+Paper|Project|Publication|"
             r"NZLC\s+(?:R|PP|SP|IP)|LRC|DP|IP|WP)")
_LAW_REFORM_PAPER = re.compile(
    r"(?<![A-Za-z])(?P<body>" + _LR_BODY + r")(?:\s*,\s+|\s+(?:noted\s+|observed\s+|stated\s+|said\s+)?in\s+(?:its\s+)?)"
    r"(?P<title>[\"“]?[A-Z][^()\[\];\n]{2,200}?)[\"”]?\s*,?\s*\(?"
    r"(?P<kind>" + _LR_PAPER + r")\s*(?:No\.?\s*)?(?P<n>\d{1,3})\b\s*,?\s*"
    r"(?:\((?:Interim|Final|Summary|Vol(?:ume)?\.?\s*\d)\)\s*,?\s*)?"
    r"\(?\s*(?:[A-Z][a-z]+\s+)?(?P<y>(?:1[89]|20)\d\d)\s*\)?")

                                                                                                                   
                                                                                                                    
                                                                                                                     
                                                                                                                     
                                                                                    
                                                                                                     
                                                                  
                                                                                              
                                                                                                
                                                                                                                            
                                                                                                               
                                                                                                  
                                                                                                             
                                                                                                                           
_LR2_ORD = (r"(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|"
            r"Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|\d{1,2}(?:st|nd|rd|th))")
_LR2_BODY = (r"(?:(?<!Statute\s)(?<!Statutes\s)(?:Criminal\s+)?Law\s+Revision\s+Committee"
                                                                                                                 
             r"|(?:Criminal|Indian|Mercantile)\s+Law\s+Commissioners"
             r"|(?:Her\s+Majesty[’'`]?s\s+)?Commissioners\s+on\s+Criminal\s+Law"
             r"|(?:Scottish\s+|English\s+|Mercantile\s+)?Law\s+Commission(?!er)(?:\s+(?:of|for)\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})?"
             r"|(?:[A-Z][A-Za-z]+\s+){0,3}Law\s+Reform\s+Commission(?:\s+of\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})?)")
_LR2_REP = r"(?:Interim\s+|Final\s+)?Report\b"
                                                                                                                     
                                                                                                                         
_LR2_YEAR = r"(?:[^;\[\]\n()]{0,90}?\(?(?P<y>(?:1[89]|20)\d\d)\)?)?"
_LAW_REFORM_ORD = [
    re.compile(r"(?P<body>" + _LR2_BODY + r")\s*,\s+(?P<ord>" + _LR2_ORD + r")\s+" + _LR2_REP + _LR2_YEAR),
    re.compile(r"(?P<ord>" + _LR2_ORD + r")\s+" + _LR2_REP + r"\s+(?:(?:on|upon)\s+[^;\[\]\n]{3,80}?\s+)?(?:of|by)\s+the\s+"
               r"(?:[A-Z][A-Za-z]+\s+){0,2}?(?P<body>" + _LR2_BODY + r")" + _LR2_YEAR),
    re.compile(r"(?P<body>" + _LR2_BODY + r")(?:[’'`]s|(?:\s+[^.;\[\]\n]{0,80}?)?\s+in\s+(?:its|their))\s+"
               r"(?:(?P<ord>" + _LR2_ORD + r")\s+" + _LR2_REP + r"|Report\s+No\.?\s*(?P<n>\d{1,3})\b)"
               r"(?:\s*(?:of\s+|\()?(?P<y>(?:1[89]|20)\d\d)\)?)?"),
    re.compile(r"(?P<body>" + _LR2_BODY + r")\s*,?\s+(?P<kind>Consultation\s+Paper|Working\s+Paper|Discussion\s+Paper|Report)\s+"
               r"(?:No\.?\s*)?(?P<n>\d{1,3})\s*,\s+[A-Z][^()\[\];\n]{2,160}?\s*\(\s*(?P<y>(?:1[89]|20)\d\d)\s*\)"),
]
_LR2_WORDS = {w: i + 1 for i, w in enumerate(("first second third fourth fifth sixth seventh eighth ninth tenth eleventh "
                                              "twelfth thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth "
                                              "nineteenth twentieth").split())}


def _law_reform_ord(work):
    """B24: (start, end, label, key) for each law-reform report printed in forms A-D above, one per report."""
    out, seen = [], set()
    for rx in _LAW_REFORM_ORD:
        for m in rx.finditer(work):
            gd = m.groupdict()
            body = re.sub(r"\s+", " ", gd["body"]).strip()
            o = (gd.get("ord") or "").lower()
            num = str(_LR2_WORDS.get(o) or (re.match(r"\d+", o).group() if o else gd.get("n") or ""))
            if not num:
                continue
            bi = "".join(w[0] for w in body.split() if w[:1].isupper())
            k = (bi, (gd.get("kind") or "report").split()[0].lower(), num)
            if k in seen or any(not (m.end() <= s or m.start() >= e) for s, e, _l, _k in out):
                continue
            seen.add(k)
            y = gd.get("y")
            if gd.get("kind"):
                label = re.sub(r"\s+", " ", m.group()).strip()
            else:
                label = "%s, %s %s%s" % (body, gd.get("ord") or "Report No", "Report" if gd.get("ord") else num,
                                         " (%s)" % y if y else "")
            out.append((m.start(), m.end(), label, k))
    return out


_QUOTE_CHARS = "“”‘’\"'"


def _mask_quoted(s):
    """S with the inside of every quotation blanked, same length.

    ⚠️ A SEPARATOR INSIDE A TITLE IS NOT A BOUNDARY. Article titles carry subtitles --
    "Hunting the Snark; the Elusive Statutory Exception" -- and a rule that trims context
    at the last "; " lands in the middle of the title, loses the author with it, and the
    article is then read as a law report. Masking the quoted spans first means only
    separators in running text can cut.

    Length-preserving, so offsets computed on the mask are valid in the original.
    """
    out, inside = [], False
    for ch in str(s or ""):
        if ch in _QUOTE_CHARS:
            inside = not inside
            out.append(ch)
        else:
            out.append("_" if inside else ch)
    return "".join(out)


                                                                      
                                                                                       
                                                                                      
                                                                                     
                                                                                    
                                           
_PER_JUDGE = re.compile(r"(?i)\bper\s+[A-Z][A-Za-z'\u2019-]+\s*"
                        r"(?:LJ|LJJ|J|JJ|CJ|JA|JSC|MR|P|B)\b")


                                                                                
                                                                  
                                                                
                                          
                                                                                       
                                                                                      
                                               
 
                                                                             
                                                                                        
                                          
_PARTY_OFFICE = re.compile(
    r"(?i)^\s*(?:ex\s+parte\b|director[- ]general\b|secretary[, ]+department\b|commissioner\s+of\b|governor\s+(?:of\b|[a-z]+\s+correctional)|registrar\s+of\b)"
    r"|;\s*ex\s+parte\b")


                                                                             
                                                                                   
                                                                                      
                                                         
_ACAD_PARALLEL_SEP = re.compile(r"^[ \t]*\)?[ \t]*[;,][ \t]*(?:\[\d{4}\][ \t]*)?$")

                                                                             
                                                                             
                                                               
                                                             
                                                                              
                                                                             
                                                                                 
                             
 
                                                              
                                                                               
                                                                                  
                                                                             
                                                                                 
                                                                             
                                                                        
                                                                                   
                                                                                
_AUSTLII_NEUTRAL_TAIL = re.compile(r"\[(\d{4})\]\s*[A-Z][A-Za-z&]{2,}\s*\d{1,4}\s*$")
_JOURNAL_YEAR_HEAD = re.compile(r"^\(?\s*\(?(\d{4})\)")
_PARALLEL_SEMI = re.compile(r"^[ \t]*\)?[ \t]*;[ \t]*$")
                                                                    
_JOINT_AUTHORS = re.compile(
    r"^(?:[A-Z][A-Za-z'’.\-]*\s+){0,3}[A-Z][A-Za-z'’\-]+"
    r"(?:\s*,\s*(?:[A-Z][A-Za-z'’.\-]*\s+){0,3}[A-Z][A-Za-z'’\-]+){0,2}"
    r"\s*(?:&|and)\s*(?:[A-Z][A-Za-z'’.\-]*\s+){0,3}[A-Z][A-Za-z'’\-]+$")
                                                                                           
_TITLE_THEN_CITE_SEP = re.compile(
    r"^[ \t\n]*[\"'”’]?[ \t\n]*\)?[ \t\n]*,?[ \t\n]*(?:in[ \t\n]+)?"
    r"(?:[\(\[]?(?:1[6-9]|20)\d\d(?:[-–]\d{2,4})?[\)\]]?[ \t\n]*,?[ \t\n]*)?"
    r"(?:\d{1,3}(?:\(\d{1,2}\))?[ \t\n]*)?[\(\[]?$")


                                                                              
                                                                                
                                                              
                                                                               
                                                 
                                                 
                                                                            
                                                                                 
 
                                                                                   
                                                                           
 
                                                                                   
                                                                                   
                                                                                    
                                                                                   
                                          
_BARE_AUTHOR_NAME = re.compile(
    r"^(?:de|van|von|le|la)?\s*[A-Z][A-Za-z'\u2019\-]{2,20}"
    r"(?:\s+(?:and|&)\s+[A-Z][A-Za-z'\u2019\-]{2,20}){0,2}$")
_AUTHOR_COMMA = re.compile(r"^[ \t]*,[ \t]*$")
_LIST_ITEM_AFTER = re.compile(r"^\s*,\s*[A-Z][A-Za-z'\u2019\-]{2,20}\s*[,)]")


def _party_tail_before(pre):
    """True where the text immediately before a match is the front of a case name.

    'McDowell v Hirschfield ' -- a versus, then capitalised words and nothing else. ANY
    punctuation ends it, because a treatise cited after a case is introduced by one:
    '... Ltd v Jones, Treitel, The Law of Contract' must not be caught.
    """
    s = str(pre or "")
    i = max(s.rfind(" v "), s.rfind(" v. "))
    if i < 0:
        return False
    tail = s[i + 3:]
    if len(tail) > 32 or any(c in tail for c in ".,;:()[]\u201c\u201d\"'"):
        return False
    words = tail.split()
                                                                                           
                                                                                  
    if not words:
        return True
    return all(w[:1].isupper() for w in words)


                                                                                  
                                                                                           
                                            
                                                                                           
                                                                                            
                                                                                           
                                                                                       
                                                                                        
                                                                                        
                                                                                       
                                             
 
                                                                                          
                                                                                         
                                                                                   
                                                                  
_CASE_REPORT_TAIL = re.compile(
    r"^\)\s{0,3}\d{1,4}\s+"
    r"([A-Z][A-Za-z&'.]{0,14}(?:\s+[A-Z][A-Za-z&'.]{0,14}){0,4})"
    r"\s{0,3}(?:\((?:NS|OS|NF|2d|3d|4th)\)\s{0,3})?\d{1,4}\b")

_OPEN_YEAR_TAIL = re.compile(r"\((?:1[6-9]|20)\d{2}$")


def _is_case_report_tail(work, end):
    """True where the text right after a '... (YEAR' match is a LAW REPORT citation."""
    m = _CASE_REPORT_TAIL.match(work[end:end + 70])
    if not m:
        return False
    name = m.group(1)
                                                                                        
                                                                                  
    if not name.strip():
        return False
    ab = name.upper().replace(".", "").replace(" ", "")
    if ab in CARDIFF_ACAD_ABBREVS or _names_a_periodical(name):
        return False                                                                   
    return True


                                                                                                  
                                                                                                 
                                                                                              
                                                                                                 
                                                         
                                                                                            
                                                                                                    
                                                                                                    
                                                                                          
                                                              
                                                                                           
                                                                                                
                            
_CASE_TAIL_VOL = re.compile(
    r"^\)?\s{0,3},?\s{0,3}\d{1,4}\s+"
    r"([A-Z][A-Za-z&'.]{0,14}(?:\s+[A-Z][A-Za-z&'.]{0,14}){0,4})"
    r"\s{0,3}(?:\((?:NS|OS|NF|N\.S\.|2d|3d|4th|5th|6th|7th)\)\s{0,3})?\d{1,4}\b")
_CASE_TAIL_NOVOL = re.compile(
    r"^\)\s{0,3}([A-Z][A-Za-z&'.]{0,14}(?:\s+[A-Z][A-Za-z&'.]{0,14}){0,3})"
    r"\s{0,3}(?:,\s{0,3}at\s+pp?\.?\s{0,3}\d|\d{1,4}\b)")
_CASE_TAIL_NEUTRAL = re.compile(r"^\s{1,3}[A-Z]{2,6}(?:\s?\([A-Za-z]{1,6}\))?\s{1,3}\d{1,5}\b")
_ENDS_ON_YEAR = re.compile(r"(?:1[6-9]|20)\d{2}(\)?)\s*$")


def _case_cite_follows(work, end, t):
    """True where a match ending on a year is followed by a law-report citation, not a journal's."""
    my = _ENDS_ON_YEAR.search(str(t or ""))
    if not my:
        return False
    tail = work[end:end + 80]
    if not my.group(1) and _CASE_TAIL_NEUTRAL.match(tail):
        return True                                                                         
    tail = (")" if my.group(1) else "") + tail
    m = _CASE_TAIL_VOL.match(tail) or _CASE_TAIL_NOVOL.match(tail)
    if not m or not m.group(1).strip():
        return False
    name = m.group(1)
                                                                                                 
    if re.match(r"(?i)(?:vols?|volume|pp?|paras?|ch|chapter|part|pt|book|no|nos|cmn?d|cm|hc|hl|law|"
                r"report|working|consultation|discussion|issues|paper|title|art|section|sect?|tome|bk|col|cols)\b\.?",
                name.strip()):
        return False
    ab = name.upper().replace(".", "").replace(" ", "")
    return not (ab in CARDIFF_ACAD_ABBREVS or _names_a_periodical(name))


                                                                                          
                                                                                           
                                                                                      
                                                                              
                                                                                           
                                                                                         
                                                                                    
_SEE_CUE_CUT = re.compile(r"[:;]\s{1,3}see\s+(?=[A-Z\u201c\u2018\"])")


def _is_author_of_next(t1, sep, t2, tail):
    """t1 is a bare surname and t2 the citation that follows it after a comma."""
    if not _AUTHOR_COMMA.match(sep):
        return False
    if not _BARE_AUTHOR_NAME.match(t1.strip()):
        return False
    return not _LIST_ITEM_AFTER.match(tail)


def _is_austlii_parallel(t1, sep, t2):
    """t1 and t2 are ONE article printed under AustLII's two citations."""
    if not _PARALLEL_SEMI.match(sep):
        return False
    m1 = _AUSTLII_NEUTRAL_TAIL.search(t1)
    m2 = _JOURNAL_YEAR_HEAD.match(t2)
    return bool(m1 and m2 and m1.group(1) == m2.group(1))


def _is_not_a_work(text):
    """True for a dictionary, an annotated practice work, judicial prose or a law report."""
    s = str(text or "")
    if _PER_JUDGE.search(s):
        return True                                                    
    if _STANDARD_FORM.search(s) or _STANDARD_FORM_BARE.search(s):
        return True                                                                          
    if re.search(r"(?i)\bReader[’'�]?s\s+Digest\b", s):
        return True                                                                                    
    if _PARTY_OFFICE.search(s):
        return True                                                          
    if _AUSTLII_TAG_ONLY.match(s):
        return True
    if _PRACTITIONER_TITLE.search(s):
        return True
    if _NOT_A_WORK.search(s):
        return True
    if _SPEECH_THEN_YEAR.search(s):
        return True                                                               
                                                                                    
                                                                                           
                                                                                    
                                                                                           
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                  
                                                                                           
                         
                                                                                           
                                                                                                
                                                                   
                                                                                               
                                                                                               
                                                   
    if _R22_GOVT_DOC.search(s) or _NEWS_MASTHEAD.search(s):
        return True
                                                                                
                                                                                             
                                                                                                
                                                                                            
    if _NAMED_STATUTE.search(s) and not (_authored_article(s) or _authored_edition(s)
                                         or _authored_book(s) or _authored_chapter(s)
                                         or _SF_AUTHOR_TITLE_YEAR.search(s)
                                         or _SF_ATY_BARE.fullmatch(s.strip())):
        return True
                                                                                       
                                                                                          
                                                                                            
                                                                                        
                                                                    
    if _CRIMLR_CITE.search(s) and (_CRIMLR_CASE.search(s)
                                   or not (_HAS_AUTHOR.search(s)
                                           or _QUOTED_TITLE.search(s)
                                           or _UNQUOTED_ARTICLE_CITE.search(s))):
        return True                                                                  
    return False


                                                                                  
                           
 
                                                                            
                                                                                  
                                                                                        
                                                                                    
                                                                     
                                                                                 
                                                                       
 
                                                                                        
                                                                                     
 
                                                                   
                                                                                      
                                                                                
                                                
 
                                                                                          
                                                                                                   
                                                                           
 
                                                             
                                                                                   
                                                                      
                                                                           
                                                                             
                                                                              
                                                                                 
                              
                                                                                         
                                                                                   
_GOVERNMENT_GUIDANCE = re.compile(
    r"(?i)\b(?:guidelines?\s+for|guidance\s+(?:for|on|entitled)|"
    r"code\s+of\s+practice|explanatory\s+(?:notes?|memorandum))\b")

COUNT_OFFICIAL_REPORTS = False


def set_count_official_reports(flag):
    """True counts law-reform and agency reports as academic references."""
    global COUNT_OFFICIAL_REPORTS
    COUNT_OFFICIAL_REPORTS = bool(flag)
    return COUNT_OFFICIAL_REPORTS


def _authored_article(s):
    """True for a quoted title followed by a journal citation -- an ARTICLE.

    ⚠️ AN ARTICLE HAS NO EDITION, so `_authored_edition` cannot vouch for it, and
    without a voucher `_is_official_report` vetoes any article whose TITLE happens to
    name an institution -- 'The Legal Personality of the Commonwealth of Australia'
    (2019) 47 Federal Law Review 4. Titles naming the Crown, the Commonwealth, Parliament
    or the Union are ordinary in legal scholarship.
    """
    s = str(s or "")
    if _ARTICLE_TITLE_CITE.search(s):
        return True
                                                                                           
                                                                                        
                                                                                            
    if _UNQUOTED_ARTICLE_CITE.search(s):
        return True
                                                                                       
                                                                                            
                                                                                      
                                                                                           
                                                                                            
                                                                                        
             
    return bool(_ARTICLE_CUE.search(s))


                                                                                          
                                                                                        
                                                                                        
                               
                                                                                            
                                                                                           
                                                                                           
                                                                                            
                                                         
                                                                                             
                                                                                             
                 
_LAW_REFORM_BODY = re.compile(
    r"(?i)\b(?:law\s+reform\s+commission"
    r"|law\s+commission\s+(?:of|for|\()"
                                                                                                  
    r"|law\s+commission(?=,)|law\s+com(?:mission|\.)?(?:\s+report)?\s*,?\s+no\b|\blccp\s+\d"
    r"|law\s+reform\s+committee"
                                                                                             
                                                                                               
                                               
    r"|(?:criminal\s+)?law\s+revision\s+committee"
    r"|law\s+reform\s+institute"
    r"|international\s+law\s+commission"
    r"|australian\s+law\s+reform"
    r"|new\s+south\s+wales\s+law\s+reform"
    r"|ontario\s+law\s+reform"
    r"|scottish\s+law\s+commission"
    r"|singapore\s+academy\s+of\s+law"
    r"|american\s+law\s+institute"
    r"|\bALI\b"
    r"|restatement\s+(?:of\s+the\s+law|second|third|first)"
    r"|model\s+penal\s+code)\b")


def _is_official_report(text):
    """True for a committee, commission or parliamentary publication."""
    if COUNT_OFFICIAL_REPORTS:
        return False                                                       
    t = str(text or "")
    if _LAW_REFORM_BODY.search(t):
        return False                                                                      
    return bool(_OFFICIAL_REPORT.search(t))


                                                                                        
                                                                                    
                                                                 
                                                                                      
                                                 
                                                                                           
                                                                                         
                                                                                  
                                                                                     
                                                                                   
                                                                                    
                                                                                    
                                                                                
                                                                                      
                                                                                    
                                                                                       
                                                                                     
_BARE_NAME = re.compile(r"^[A-Z][a-z]{2,19}$")
                                                                                        
                                        
                                                                             
                                                                               
                                                                              
                                                                                       
                                                                                   
_BARE_OK = re.compile(
    r"^(?:\s*,\s*|\s+on\s+)(?:the\s+)?[A-Z]"
                                                                        
                                                                               
                                                                               
                                                                          
    r"|^(?:'|’)s?\s+(?:the\s+)?[A-Z]"
    r"|^\s*,?\s*\d{1,2}(?:st|nd|rd|th)\s+[Ee]d"
                                                                                          
                                                                                       
                                                                             
    r"|^\s*\((?:1[6-9]|20)\d{2}\)(?!\s*\d{1,4}\s+[A-Z])"
                                                                     
                                                          
    r"|^\s*\([A-Z][A-Za-z&. ]{3,40},")

                                                                                         
                                                                                       
                                  
_JUDICIAL_NEAR = re.compile(r"\b(?:JJ|LJJ|LJ|CJ|JA|JSC|QC|KC|SC)\b")

                                                                                      
                                                                     
_BARE_IN_LIST = re.compile(
    r"[A-Z][a-z]{2,19}(?:['’]s)?\s*,\s+[A-Z][A-Za-z'’\-]{2,19}(?:['’]s)?\s*,\s+$")


_HONOURED_NOT_AUTHOR = re.compile(
    r"(?i)\b(?:in\s+(?:honour|honor|memory)\s+of|festschrift\s+for|"
    r"essays\s+(?:for|presented\s+to))\b[^.;]{0,45}$")


def _bare_name_corroborated(text, matched, start, end):
    """True when a one-word surname match is followed by something naming a WORK."""
    if not _BARE_NAME.match(str(matched or "").strip()):
        return True                                                                 
    if ENCYCLOPAEDIAS_IN and str(matched or "").strip() == "Wikipedia":
        return True                                                                                
                                                                                         
                                                                                      
                                                                                         
    if _HONOURED_NOT_AUTHOR.search(text[max(0, start - 60):start]):
        return False
    after = text[end:end + 60]
                                                                   
    if _BARE_IN_LIST.search(text[max(0, start - 60):start]) and not (
            _JUDICIAL_NEAR.search(after[:40])):
        return True
                                                                                        
                                                                                     
                                                                   
    if _JUDICIAL_NEAR.search(after[:40]):
        return False
    return bool(_BARE_OK.match(after))


                                                                                     
                                                                                   
                                                                                       
_INST_KEY = re.compile(r'\b(institutes?|commentaries)\b[ ,.]*([ivxl]+(?:[ .,]+[ivxl0-9]+)+)')


                                                                                     
                                                                                  
                                                                                        
                                                                                       
                                                                         
_JOURNAL_YEAR = re.compile(r"\b(1[6-9]\d{2}|20[0-2]\d)\b(?=.*?\d)")


def _journal_years(k):
    """The years of any JOURNAL-shaped citation in a dedup key."""
    return frozenset(_JOURNAL_YEAR.findall(k or ""))


def _contains_words(haystack, needle):
    """True where `needle` appears in `haystack` as a whole run of words.

    Dedup keys are space-separated words, so containment has to align on word boundaries.
    'wade' is inside 'wadesworth' as characters and is a different author.
    """
    if not needle:
        return False
    h = " " + haystack + " "
    n = " " + needle + " "
    if n in h:
        return True
                                                                                        
                                                                                        
                                                                                        
                                                                       
                                                                                            
                                                                                          
                                                                                         
                                                                                              
                                                                                         
                                                                                           
                                                                                           
                                                              
                                                                                      
                                                          
                                                                                
                                                                             
                                                                                    
                                                                                 
                                                                                     
                                
                                                                                        
                                                                                 
    if _journal_years(haystack) and _journal_years(needle) \
            and not (_journal_years(haystack) & _journal_years(needle)):
        return False
                                                                                               
                                                                                       
     
                                                                                          
                                                                               
                                                                                  
                                                                                      
                                                                                             
                                                           
                                                                                             
                                                                                       
                                                                           
                                                                                            
                                                                                        
    _vh, _vn = _VOL_JOURNAL_PAGE.match(haystack), _VOL_JOURNAL_PAGE.match(needle)
    if _vh and _vn and (_vh.group(1), _vh.group(2)) != (_vn.group(1), _vn.group(2)):
        return False
                                                                                           
                                                                                                 
                                                                
                                                                                                         
                                                                                             
                                                   
    if _vn and not _vh:
        _hn = set(re.findall(r"\d+", haystack))
        if not (_vn.group(1) in _hn and _vn.group(2) in _hn):
            return False
                                                                                              
                                                                                    
    _ph, _pn = set(_PAPER_NO.findall(haystack)), set(_PAPER_NO.findall(needle))
    if _ph and _pn and not (_ph & _pn):
        return False
    hs, ns = _skeleton(haystack), _skeleton(needle)
    if len(ns) < 2 or len(ns) > len(hs):
        return False
                                                                                             
                                                                                            
                                                                                      
                                                                                              
                                                                                             
                                                                                            
    return any(hs[i:i + len(ns)] == ns for i in range(len(hs) - len(ns) + 1))


                                                                                             
                                                                                              
                          
_VOL_JOURNAL_PAGE = re.compile(r"^\s*(\d{1,3})\s+[a-z][a-z.&' \-]*?\s+(\d{1,4})(?:_+\d*)?\s*$")
_PAPER_NO = re.compile(r"\b(?:report|paper|memorandum|project|publication)\s+(?:no\.?\s*)?(\d{1,3})\b")


                                                                    
                                                                  
                                                                                            
                                                                                       
                                                                  
_JOIN_WORDS = frozenset(("the", "of", "a", "an", "and", "on", "in", "to", "for", "its",
                         "new", "vol", "no", "ed", "eds", "edn",
                         "pp", "p", "para", "paras", "at", "n", "fn", "ff",
                         "ch", "chap", "art", "sect", "section", "pt"))


def _skeleton(s):
    """A key's words with the connecting words dropped, for the second containment test."""
    return [w for w in re.findall(r"[a-z][a-z']+", (s or "").lower()) if w not in _JOIN_WORDS]


def _norm_key(t):
    """Normalise a matched string to a canonical dedup key.
    Strips possessives, edition ordinals, normalises connectors (&/and/comma),
    collapses whitespace. Allows text-based dedup to collapse repeated citations
    of the same work across different surface forms:
      'Phipson' x13 → 1
      'Goff & Jones' == 'Goff and Jones' == 'Goff, Jones'
      'CLJ' == 'Cambridge Law Journal' (via _JOURNAL_ABBREV_ALIASES)
    """
    k = _LEAD_JUNK.sub('', str(t or '')).lower()
    prev = None
    while prev != k:                                                          
        prev = k
        k = _LEAD_CUE.sub('', k)
    k = re.sub(r"'s?\b", '', k)                          
    k = re.sub(r'&', 'and', k)                                                      
    k = re.sub(r'\s*,\s*', ' ', k)                                                                         
    k = re.sub(r'\s+and\s+', ' ', k)                                                                
    k = re.sub(r'\b\d+(?:st|nd|rd|th)\b', '', k)                              
    k = re.sub(r'\bed(?:ition)?\b', '', k)                                 
    k = re.sub(r'\s+', ' ', k).strip()

                                                                                    
                                                                                        
                                                                                       
                                                                                        
                                                                                      
                                                                    
                                                   
    m = _INST_KEY.search(k)
    if m:
        title = 'commentaries' if m.group(1).startswith('commentar') else 'institute'
        ref = re.sub(r'[^a-z0-9]+', ' ', m.group(2)).strip()
        return (title + ' ' + ref).strip()

                                                                             
                                                                                 
                                                                                   
                                                                                
                                                                              
                                                         
                                                      
                                                        
    k = re.sub(r'[()\[\]\u201c\u201d\u2018\u2019"\']', ' ', k)
    k = re.sub(r'\s+', ' ', k).strip()

                                                                               
                                                                        
                                                                                      
                                                                                     
                                                                                  
                                                                                     
    m2 = re.match(r'^(.+?)_(\d{4})_(\d*)$', k)
    if m2:
        j = m2.group(1)
        j = _JOURNAL_ABBREV_ALIASES.get(j.replace(' ', ''),
                                        _JOURNAL_ABBREV_ALIASES.get(j, j))
        return '%s_%s_%s' % (j, m2.group(2), m2.group(3))
    return _JOURNAL_ABBREV_ALIASES.get(k.replace(' ', ''),
                                       _JOURNAL_ABBREV_ALIASES.get(k, k))


                                                                                              
                                                                             
                                                                                           
                                                                                            
                                                                                         
                                                                                  
                                                
_AUTHORED_EDITION = re.compile(
    r"(?i)^\s*(?:[A-Z][A-Za-z'\u2019\-]+\s+){0,3}[A-Z][A-Za-z'\u2019\-]+,\s+"
    r"[^,]{6,90},?\s+\d+(?:st|nd|rd|th)\s+ed(?:ition)?\b")


def _authored_edition(s):
    """True if this reads as 'Author, Title, Nth ed' -- the treatise form, not a report."""
    return bool(_AUTHORED_EDITION.search(str(s or "")))


                                                                                       
                                                                                          
                                                                                     
                                                                                        
                                                                                       
                                                                                          
_AUTHORED_BOOK = re.compile(
    r"^\s*(?:[A-Z][A-Za-z'\u2019\-]*\.?\s+){0,3}[A-Z][A-Za-z'\u2019\-]+,\s+"
    r"(?:The\s+|An?\s+)?[A-Z][^,]{6,90},?\s*\((?:1[6-9]|20)\d{2}\)")


def _authored_book(s):
    """True if this reads as 'Author, Title (year)' -- a book, not a report."""
    return bool(_AUTHORED_BOOK.search(str(s or "")))


                                                                                         
                                                                                          
                                                                                    
                                                                                        
                                                                 
                                                                                      
                                                                                       
 
                                                                                             
                                                                                            
          
                                                                   
                                                                                 
                                                                                             
                                        
 
                                                                                              
                                                                                             
                                                                                           
                                                                                   
                                                                             
                                                                                      
                                                                                       
                                                        
                                                                  
                                                                                             
                                                                                             
                              
_AUTHORED_CHAPTER = re.compile(
    "(?:“[^”]{10,240}”|\"[^\"]{10,240}\"|‘[^’]{10,240}’|\'[^\']{10,240}\')"
    ",?\\s+in\\s+"
    "[A-Z][A-Za-z\'’\\-]+(?:[ ][A-Za-z\'’&\\-]+){0,8}"
    "\\s*\\(eds?\\b[^()]{0,120}?\\)")


def _authored_chapter(s):
    """True for '"Title", in Editor (ed)' -- a chapter in an edited collection."""
    return bool(_AUTHORED_CHAPTER.search(str(s or "")))


                                                                                      
                                                                      
                                                                           
                                                                                    
                                                                                       
                                                                                    
_CORPORATE_AUTHOR = re.compile(
    r"(?i)\b(?:Commission|Committee|Council|Board|Authority|Actuary|Department|Ministry|"
    r"Office|Bureau|Agency|Organisation|Organization|Secretariat|Association|Society|"
    r"Institute|Institution|Parliament|Government|Commonwealth|Kingdom|States|Nations|"
    r"Tribunal|Inquiry|Taskforce|Task\s+Force|Working\s+Party|Group|Federation|Corporation|"
    r"Service|Centre|Center|Trust|Foundation|Bank|Fund|Court|Registry|Panel|"
    r"Statistics|Inspectorate|Ombudsman|Registrar)\b")


def _person_authored_book(s):
    """'Author, Title (year)' where the author is a PERSON, not a body."""
    m = _AUTHORED_BOOK.search(str(s or ""))
    if not m:
        return False
    head = m.group().split(",", 1)[0]
    return not _CORPORATE_AUTHOR.search(head)


                                                                                  
                                                                                         
                                                                                       
                                                                                       
                               
 
                                                                                    
                                                                              
_DIACRITIC_FOLD = {ord(a): b for a, b in zip(
    "àáâãäåèéêëìíîïòóôõöùúûüýÿçñÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÝÇÑ",
    "aaaaaaeeeeiiiiooooouuuuyycn"
    "AAAAAAEEEEIIIIOOOOOUUUUYCN")}


def _fold_diacritics(t):
    """Accented Latin letters to plain, character for character."""
    return str(t or "").translate(_DIACRITIC_FOLD)


                                                                             
                                                                        
 
                                                                              
 
                                                                                   
                                                  
 
                                                                                      
                                                                                            
                                                                                             
                       
 
                                                                                       
                                                        
 
                                                                                          
                                                
 
                                                                                              
                                                                                        
                                                                                           
                                                                                  
_DEFN_PAREN_RE = re.compile(r"\(([^()]{0,240})\)")
_DEFN_TERM_RE = re.compile(r"[\"“'‘]\s*(?:[Tt]he\s+)?([A-Za-z][A-Za-z0-9.&'\- ]{0,40}?)\s*[\"”'’]")
_DEFN_IS_PERIODICAL = re.compile(
    r"(?i)\b(?:review|journal|quarterly|reporter|reports|bulletin|gazette|periodical|"
    r"yearbook|law\s+times)\b")
_ABBREV_HEAD = re.compile(r"^([A-Z][A-Za-z.&'\-]*)")


def _defined_abbrevs(text):
    """Abbreviations THIS judgment defines for itself, normalised as the journal table is.

    ⚠️ EVERY QUOTED TERM IN THE PARENTHESIS COUNTS, NOT JUST THE FIRST. The first version
    anchored on the opening bracket and read one term, which missed the case this guard was
    written for: [2021] SGCA(I) 5 defines two at once --

        "(the "CLPA claim" and the "CLP Act" respectively)"

    -- and it is the SECOND, "CLP Act", that collides with Current Legal Problems. So the
    parenthetical is taken whole and every quoted term inside it is read.

    Both the whole term and its leading token are returned: the court writes ("CLP 581")
    once and "CLP 581" thereafter, but the pattern that fires is on the bare "CLP", so the
    head has to be vetoed as well as the phrase.
    """
    out = set()
    for pm in _DEFN_PAREN_RE.finditer(text or ""):
        inner = pm.group(1)
        if not _DEFN_TERM_RE.search(inner):
            continue
        before = text[max(0, pm.start() - 90):pm.start()]
        if _DEFN_IS_PERIODICAL.search(before) or _DEFN_IS_PERIODICAL.search(inner):
            continue                                                                          
        for m in _DEFN_TERM_RE.finditer(inner):
            term = m.group(1).strip()
            if not term or term.islower():
                continue
            out.add(term.upper().replace(".", "").replace(" ", ""))
            h = _ABBREV_HEAD.match(term)
            if h and len(h.group(1)) >= 2:
                out.add(h.group(1).upper().replace(".", ""))
    return out


                                                                               
                                                                                          
                                                                                             
 
                                                                                      
 
                                                                                          
                                                                                             
                                                                                             
                                                                                            
                     
                                                                                     
                                                                                     
_DEFINED_SHORT = re.compile(
    "^[ \t]{0,3}[(][ \t]{0,2}[\u201c\u2018\"']"
    "[ \t]{0,2}([A-Za-z][A-Za-z0-9.&'\u2019 -]{1,40}?)[ \t]{0,2}"
    "[\u201d\u2019\"'][ \t]{0,2}[)]")

                                                                                   
                                                                                       
                               
                                                                                            
                                                                                          
                                                                                          
                                                                                         
                                                                                          
                                                                                       
_DEFINED_SHORT_US = re.compile(
    "^(?:[ \t]*,[ \t]*[0-9\u2013, n.-]{1,30})?[ \t]*[(][ \t]*(?:[A-Za-z. ]{0,12}[ ])?"
    "(?:1[89]|20)[0-9]{2}[ \t]*[)][ \t]*[(][ \t]*"
    "([A-Z][A-Za-z'\u2019.-]+(?:(?:[ \t]*,[ \t]*(?:&[ \t]*)?|[ \t]*&[ \t]*|[ \t]+and[ \t]+|"
    "[ \t]+)[A-Z][A-Za-z'\u2019.-]+){0,4})[ \t]*[)]")

_BRACKET_INSTRUMENT = re.compile(r"\[\s*$")
_BRACKET_INSTRUMENT_TAIL = re.compile(r"^\s*\d{1,5}\s*\]")


                                                                                           
                                                                                          
                                                                                        
                    
                                                                                 
                                              
                                                                                              
                                                                                        
                                                                                            
_SCOTS_INST = re.compile(
                                                                                           
                                                                                            
                                                                                            
    r"(?<![\w.])[1-6]\.?\s+(?:(Stair)\s*[.,]\s*(?=\d{1,2}\s*\.\s*\d)"
    r"|(Ersk(?:ine)?|Bankt?(?:on)?|Craig|Mack(?:enzie)?\.?\s+Inst|Hume)"
    r"\s*[.,]\s*,?\s*(?:(?:p|tit|vol)\.\s*)?(?=\d))")
_SCOTS_NAME = {"sta": "stair", "ers": "erskine", "ban": "bankton", "cra": "craig",
               "mac": "mackenzie", "hum": "hume"}


def _scots_institutional(text):
    out = []
    for m in _SCOTS_INST.finditer(text or ""):
        k = _SCOTS_NAME[(m.group(1) or m.group(2))[:3].lower()]
        if k not in out:
            out.append(k)
    return out


                                                                                                  
                                                                                               
                                                                                                 
                                                                                            
                                                                                                   
                                                                              
                                             
                                                                                          
                                                                                                
                                                                                                     
                                                                                               
                                                                                          
                                                                                                   
                                                                                                
                                                              
                                                                                                         
                                                                                        
                                                                                                   
                                                                              
                                                                                                         
                                                                                         
ACAD_OLD = os.environ.get("JR_ACAD_OLD", "1") != "0"
_OLD_SCOTS = re.compile(
    r"(?<![\w.])(Stair|Ersk(?:ine)?|Bankt?(?:on)?|Craig|Mack(?:enzie)?|Hume)\.?\s*,?\s*"
    r"(?:Inst(?:itutes?|itutions?)?\.?\s*,?\s*)?\(?\s*(?:[Bb](?:ook)?\.?\s*|lib\.\s*)?"
    r"(?:[ivx]{1,4}|[1-6])\s*[.,]\s*(?:t(?:it)?\.\s*|dig\.\s*)?\d")
_OLD_FORMS = (
                                                                                                
    (re.compile(r"\bBell(?:['’]s)?\s*,?\s*\(?\s*(?:Prin(?:ciples)?|Pr)\b\.?(?:\s+of\s+the\s+Law\s+of\s+Scotland)?"
                r"\s*,?\s*\(?\s*(?:\d{1,2}(?:st|nd|rd|th)\s+ed\.?,?\s*)?(?:§|sect(?:ion)?s?\.?\s*\d|s\.\s*\d)"
                                                                                     
                r"|\bBell\b[^.;]{0,30}\bof\s+his\s+Principles\b"),
     "bell principles", (("bell",), ("principles", "scotland"))),
    (re.compile(r"(?<![\w.])(?:\d\s+)?Bell(?:['’]s)?\s*[,(]?\s*(?:\d\s+)?Comm?\.|\bBell['’]s\s+Commentaries\b(?!\s+on\b)"),
     "bell commentaries", (("bell",), ("commentaries", "scotland"))),
                                                                                                   
                                                                                                       
                                                                                                     
                                                                  
    (re.compile(r"\bCo\.\s?Litt?\.?\s*,?\s*\d") if os.environ.get("JR_ACAD_OLD_COLITT", "1") != "0"
     else re.compile(r"(?!x)x"), "coke upon littleton", (("coke",), ("littleton",))),
    (re.compile(r"\bStaundford\s*,?\s*Praerog\b"), "staundford prerogative", (("staundford",),)),
    (re.compile(r"\bCoke\s*,\s*Inst\.\s*\d|(?<![\w.])[1-4]\s+Inst\.?\s+\d{1,3}\b"), "coke institutes", (("coke",),)),
    (re.compile(r"(?<![\w.])[1-4]\.?\s+Bl(?:ackst)?\.\s*Comm?\.?\s*\d|(?<![\w.])[1-4]\.?\s+Blackstone\s*,\s*(?:\d|c\.\s*\d)"),
     "blackstone commentaries", (("blackstone",),)),
    (re.compile(r"\bVattel\s*,\s*(?:(?:The\s+)?Law\s+of\s+Nations\b|[Bb]ook\s+[\divx]+)"),
     "vattel law of nations", (("vattel",),)),
    (re.compile(r"\bVoet\.?\s*,?\s*\d{1,2}\s*\.\s*\d"), "voet", (("voet",),)),
    (re.compile(r"\bCruise(?:['’]s)?\s*,?\s*Dig(?:est\b|\.)"), "cruise digest", (("cruise",),)),
    (re.compile(r"\bComyn(?:s|['’]s|s['’]s?)?\s*(?:,\s*|\s+in\s+his\s+)?Dig(?:est\b|\.)"),
     "comyns digest", (("comyn",), ("comyns",))),
    (re.compile(r"(?<![\w.])\d\s+Chitty\s*,?\s*Com\.?\s+Law\b"), "chitty commercial law",
     (("chitty", "commercial"), ("chitty", "com"))),
    (re.compile(r"\b(?:American\s+)?Restatement\s+of\s+the\s+Law\s+of\s+Torts?\b(?!\s*,?\s*\(?(?:Second|Third|2d|3d))"),
     "restatement of the law of torts", (("restatement", "torts"), ("restatement", "tort"))),
    (re.compile(r"\bHackworth(?:['’]s)?\s*,?\s*Digest\s+of\s+International\s+Law\b"),
     "hackworth digest of international law", (("hackworth",),)),
)
                                                                                                
_OLD_WORK_ON_BY = re.compile(
    r"\bwork\s+on\s+((?:[A-Z][a-z]+\s+){0,3}[A-Z][a-z]+)\s+by\s+([A-Z][a-z]{2,})\s+\(((?:1[6-9]|20)\d\d)\)")
                                                                                                       
                                                                                           
                                                                                                     
                                                                                             
                                                                                                    
                                                                                                
                                                                                               
_OLD_ON_PAGE = re.compile(
    r"(?<![A-Za-z.])(?:\d{1,2}\s+)?(?!(?:Committee|Subcommittee|Commission|Commissioners|Convention|Covenant|"
    r"Comment|Commentary|Report|Reports|Years|Ban|Centre|Center|Institute|Guidelines|Treatise|Commentaries|"
    r"Essay|Lectures|Observations|Remarks|Court|Senate|House|Board|Bench|Issues|Reasons|Position|Conference|"
    r"Justice|Judge|Appeals?|Discovery|Register|Hearing|Hearings|Debate|Statement|Decision|Rules|Act|"
    r"Section|Part|Article|Chapter|Schedule|Order|Note|Singapore|England|Scotland|Canada|Australia)\b)"
    r"([A-Z][a-z]{2,})\s+on\s+(?!(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Appeal|Section|Article)\b)"
    r"([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?)\s*,\s*(?:p\.\s*|s\.\s*|§+\s*)?"
    r"(?!(?:1[6-9]|20)\d\d\b)\d{1,4}(?![\dA-Za-z])")
                                                                                                           
                                                                                                  
_OLD_A_TREATISE = re.compile(
    r"(?<![A-Za-z.])([A-Z][a-z]{2,}),\s+(A\s+(?:Practical\s+)?Treatise\s+(?:on|of|upon)\s+[^;()\[\]\n]{3,140}?)"
    r"\s*,?\s*(?:\d{1,2}(?:st|nd|rd|th)\s+ed\.?\s*)?\(((?:1[6-9]|20)\d\d)\)")
                                                                                                 
                                                                                                       
                                                                                                         
                                                                                                
                                                                                                      
_OLD_POSSESSIVE = re.compile(
    r"(?<![A-Za-z])(Kames|Blackstone|Coke|Hale|Hawkins|Burn|Dalton|Comyns?|Bacon|Viner|Cruise|Erskine|Stair|"
    r"Bankton|Bell|Hume|East|Chitty|Story|Kent|Staundford|Bracton|Littleton|Fitzherbert|Pothier|Vattel|"
    r"Grotius|Puffendorf|Domat|Voet)['’]s\s*[\"“]?\s*"
    r"((?:[A-Z][a-z]{2,}\s+(?:of\s+(?:the\s+)?|on\s+|and\s+|in\s+)?){1,5}[A-Z][a-z]{2,})")
_OLD_POSS_NOT = re.compile(r"\b(?:Cases?|Reports?|Appeals?|Decisions|Dictionary|Practice|Tit)\b")
                                                                                                       
_OLD_IN_HIS = re.compile(
    r"(?<![A-Za-z])([A-Z][a-z]{2,})\s+in\s+his\s+((?:[A-Z][a-z]+\s+(?:of\s+(?:the\s+)?|on\s+|and\s+)?){0,5}[A-Z][a-z]+)"
    r"\s*,?\s*\(?\d{1,2}(?:st|nd|rd|th)\s+ed\b")
                                                                                                     
                                                                                                   
_OLD_ON_EDN = re.compile(_OLD_ON_PAGE.pattern.split(r"\s+on\s+")[0] + r"\s+[oO]n\s+"
                         r"([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?)\s*\(\s*\d{1,2}(?:st|nd|rd|th)?\s*Edn?\b")


def _old_short_forms(text, distinct):
    """Keys for the ACAD_OLD shapes, each added once and only where no key already holds the writer."""
    text = text or ""
    have = [set(re.findall(r"[a-z]+", k)) for k in distinct]
    out = []

    def _held(guard, mine=True):
                                                                                 
        return any(set(g) <= w for g in guard for w in have + ([set(k.split()) for k in out] if mine else []))

    for m in _OLD_SCOTS.finditer(text):
        k = _SCOTS_NAME[m.group(1)[:3].lower()]
        if k not in out and not any(_contains_words(_o, k) for _o in list(distinct) + out):
            out.append(k)
    for rx, key, guard in _OLD_FORMS:
                                                                                             
                            
        if key not in out and not _held(guard, mine=False) and rx.search(text):
            out.append(key)
    for m in _OLD_WORK_ON_BY.finditer(text):
        key = ("%s %s %s" % (m.group(2), m.group(1), m.group(3))).lower()
        if key not in out and not _held(((m.group(2).lower(),),)):
            out.append(key)
    for rx in (_OLD_ON_PAGE, _OLD_A_TREATISE):
        for m in rx.finditer(text):
            a = m.group(1).lower()
            key = ("%s on %s" % (a, m.group(2)) if rx is _OLD_ON_PAGE
                   else "%s %s %s" % (a, re.sub(r"[,.]", "", m.group(2)), m.group(3))).lower()
                                                                                                     
                                                                           
            _stop = {"a", "an", "the", "of", "on", "in", "and", "upon", "to", "practical", "treatise"}
            tw = set(re.findall(r"[a-z]+", m.group(2).lower())) - _stop
            if (key not in out and not _held(((a,),)) and not any(k.split()[0] == a for k in out)
                    and not (tw and any(tw <= w for w in have))
                                                                                                                
                    and not any(len(w - _stop) >= 3 and (w - _stop) <= tw for w in have)):
                out.append(key)
    for rx in (_OLD_POSSESSIVE, _OLD_IN_HIS, _OLD_ON_EDN):
        for m in rx.finditer(text):
            a, t = m.group(1).lower(), m.group(2)
            if rx is _OLD_POSSESSIVE and _OLD_POSS_NOT.search(t):
                continue
            key = ("%s on %s" if rx is _OLD_ON_EDN else "%s %s") % (a, t.lower())
            if a == "bell":                                                                     
                key = ("bell principles" if t.startswith("Principles")
                       else "bell commentaries" if t.startswith("Commentaries") else None)
            if a in ("comyn", "comyns"):
                a = "comyn"
                                                                                                 
                                                              
            _st = {"a", "an", "the", "of", "on", "in", "and"}
            tw = set(re.findall(r"[a-z]+", t.lower())) - _st
            if tw and any(tw == w - _st for w in have):
                continue
            if key and not _held(((a,),) if a != "comyn" else (("comyn",), ("comyns",))):
                out.append(key)
    return out


                                                                                                 
                                                                                            
                                                                            
                                                                                            
                                                                                    
                                                                                                   
                                                                                          
                                                                                               
 
                                                                                              
                                                                                              
                                                                                              
                                                                                          
_SF_CUE = (r"(?:\(?\d{1,2}\s*(?:st|nd|rd|th|d)\s*[Ee]d(?:n|ition)?\b"
           r"|[A-Z][a-z]+(?:ieth|th|rst|ond|ird)\s+[Ee]dition\b"
           r"|(?:at\s+)?pp?\.?\s*\d|(?:at\s+)?pages?\s+\d"
           r"|[Vv]ol(?:ume|s)?\.?\s*[IVXLCivxlc\d]+\b"
           r"|c(?:h(?:ap)?)?\.\s*[IVXLC\d]+\b"
           r"|(?:§+|secs?\.|pars?\.|paragraphs?)\s*\d)")
_SF_TW = r"(?:[A-Z][A-Za-z'’\-]*|of|the|in|and|on|to|for|under|between|over|upon|&)"
_SF_NAME = r"(?:O['’]|Mc|Mac|De\s|Van\s)?[A-Z][a-z][A-Za-z\-]+"                           
_SF_AUTHOR_TITLE = re.compile(
    r"(?<![A-Za-z.])(?:\d{1,2}\s+)?(?P<a>" + _SF_NAME + r"(?:\s+(?:and|&)\s+" + _SF_NAME + r")?)"
                                                                                                
                                                                                                 
    r"(?:\s?,\s+|\s+\(\s*(?:in\s+)?)"
    r"(?P<t>(?:The\s+|A\s+|An\s+)?[A-Z][A-Za-z'’\-]+(?:\s+" + _SF_TW + r"){1,11}?)"
    r"(?P<c>\s?,?\s*\(?" + _SF_CUE + r")")
_SF_POSSESSIVE = re.compile(
    r"(?<![A-Za-z])(?P<a>" + _SF_NAME + r")(?:['’`]s|s['’`]|['’`])\s+[\"“'`]?\s?"
    r"(?P<t>[A-Z][A-Za-z\-]+(?:\s+" + _SF_TW + r"){0,8}?)[\"”'`]?"
    r"(?P<c>,?\s*\(*(?:\((?:1[5-9]|20)\d\d\)\s*)?" + _SF_CUE + r")")
_SF_ON = re.compile(
    r"(?<![A-Za-z])(?:\d{1,2}\s+)?(?P<a>" + _SF_NAME + r"(?:\s+(?:and|&)\s+" + _SF_NAME + r")?)\s+"
    r"(?:in\s+his\s+(?:well-known\s+)?(?:work|book|treatise)\s+)?(?:up)?on\s+"
    r"(?:the\s+)?(?P<t>[A-Z][A-Za-z\-]+(?:\s+" + _SF_TW + r"){0,6}?)"
    r"(?P<c>\s?,?\s*\(?" + _SF_CUE + r")")
_SF_AUTHOR_EDITION = re.compile(
    r"(?<![A-Za-z.])(?P<a>" + _SF_NAME + r"),\s+(?P<c>\d{1,2}\s*(?:st|nd|rd|th|d)\s+ed\.?,?"
    r"\s*\(?(?:1[6-9]|20)\d\d\)?)")
                                                                                               
                                                                    
                                                                                           
                                                                                            
                                                                                 
                                                                                    
_SF_ORD = r"\d{1,2}\s*(?:st|nd|rd|th|d)\s*[Ee]d(?:n|ition)?\b\.?"
_SF_TITLE = r"(?:The\s+|A\s+|An\s+)?[A-Z][A-Za-z'’\-]+(?:\s+" + _SF_TW + r"){1,9}?"
_SF_AUTHOR_PAREN_EDITION = re.compile(
    r"(?<![A-Za-z.])(?P<a>" + _SF_NAME + r")\s+\(\s*(?P<c>" + _SF_ORD + r"\s*,\s*(?:at\s+)?pp?\.?\s*\d)")
_SF_TITLE_BY = re.compile(
    r"(?<![A-Za-z])(?P<t>" + _SF_TITLE + r")\s+by\s+(?P<a>(?:[A-Z][A-Za-z.\-]*\s+){0,3}" + _SF_NAME + r")"
    r"(?P<c>\s*,?\s*\(\s*" + _SF_ORD + r")")
_SF_PAREN_TITLE_EDITION = re.compile(
    r"\(\s*(?P<t>" + _SF_TITLE + r")\s*,\s*(?P<c>" + _SF_ORD + r"\s*,?\s*\(?(?:1[6-9]|20)\d\d\)?)")
_SF_SAYS_IN = re.compile(
    r"(?:says?|said|states?|stated|writes?|wrote|observes?|observed)\s+in\s+"
    r"(?P<t>" + _SF_TITLE + r")(?P<c>\s+at\s+pp?\.?\s*\d)")
                                                                                         
                                                                                    
                                                                                  
                                                                  
                                                                                
_SF_TITLE_ED_YEAR = re.compile(
    r"(?<![A-Za-z])(?P<t>" + _SF_TITLE + r")(?P<c>\s*\(\s*" + _SF_ORD + r"\s*,?\s*(?:1[6-9]|20)\d\d\s*\))")
_SF_TITLE_YEAR_PAGE = re.compile(
    r"(?<![A-Za-z])(?P<t>" + _SF_TITLE + r")(?P<c>\s*\(\s*(?:1[6-9]|20)\d\d\s*\)\s*,?\s*(?:at\s+)?pp?\.?\s*[\divxlc])")
                                                                                        
                                                                                 
                                                                                           
                                                                                   
_SF_CLASSIC = re.compile(
    r"(?<![A-Za-z.])(?P<a>Blackstone|Coke|Hale|Hawkins|Bracton|Kames|Comyns?|Littleton|Pothier|"
    r"Story|Stephen|Chitty|Dalton|Fleta|Glanvill|Britton)"
    r"(?P<c>,\s*(?:[Vv]ol(?:ume)?\.?\s*[IVXLCivxlc\d]+|(?:at\s+)?pp?\.\s*\d|fo\.\s*\d"
    r"|[Bb]ook\s+[IVX\d]+|c\.\s*[IVX\d]+))")
                                                                                           
                                                                                             
                                                                         
_SF_US_BOOK = re.compile(
    r"(?<![A-Za-z.])(?P<a>" + _SF_NAME + r"(?:\s+(?:and|&)\s+" + _SF_NAME + r")?),\s+"
    r"(?P<t>" + _SF_TITLE + r")"
                                                                                              
                                                                                                
                                                                         
    r"(?P<c>\s+\d{1,4}(?:\s*[-–]\s*\d{1,4})?(?:\s+et\s+seq\.)?\s*\(\s*(?:\d\w{1,2}\s+ed\.\s*)?"
    r"(?:1[6-8]\d\d|19[0-7]\d)\s*\))")
                                                                                             
                                                                                              
                                                                                        
_SF_PROF_PAREN = re.compile(
    r"(?:Professor|Prof\.?|Dr\.?|Sir|Mr\.?)\s+(?:[A-Z][A-Za-z.]*\s+){0,2}(?P<a>" + _SF_NAME + r")\s+"
    r"\(\s*(?:in\s+)?(?P<t>" + _SF_TITLE + r")(?P<c>\s*,\s*" + _SF_ORD + r")")
                                                                                               
                                                                                               
                                                                                                 
                                                                                   
                                                                                                          
                                                     
                                                                                              
                                                                                              
_SF_TITLE_RICH = (r"(?:The\s+|A\s+|An\s+|the\s+)?[A-Z][A-Za-z'’\-]+:?(?:\s+(?:" + _SF_TW[3:-1]
                  + r"|(?:1[6-9]|20)\d\d):?){1,14}?")
_SF_AUTHOR_TITLE_YEAR = re.compile(
    r"(?<![A-Za-z.])(?P<a>" + _SF_NAME + r"(?:,\s+" + _SF_NAME + r"){0,3}(?:\s+(?:and|&)\s+" + _SF_NAME + r")?)"
    r"\s?,\s+(?P<t>" + _SF_TITLE_RICH + r")"
    r"(?P<c>\s?,?\s*\(\s*(?:1[6-9]|20)\d\d(?:\s*[-–]\s*\d{2,4})?\s*\)\s*,?\s*(?:at\s+)?"
    r"(?:pp?\.?\s*\d|pages?\s+\d|paras?\.?\s*[A-Z]?\d|paragraphs?\s+\d|ch(?:apter)?\.?\s*\d|vol\b))")
                                                                                          
                                                                    
                                                                                       
                                                               
_SF_TITLE_ED_THEN_YEAR = re.compile(
    r"(?<![A-Za-z])(?P<t>" + _SF_TITLE + r")(?P<c>\s?,?\s*\(?\s*" + _SF_ORD + r"\s*\)?\s*,?\s*"
    r"\(\s*(?:1[6-9]|20)\d\d\s*\))")
                                                                                   
_SF_ATY_BARE = re.compile(
    r"(?P<a>" + _SF_NAME + r"(?:,\s+" + _SF_NAME + r"){0,3}(?:\s+(?:and|&)\s+" + _SF_NAME + r")?)"
    r"\s?,\s+(?P<t>" + _SF_TITLE_RICH + r")\s?,?\s*\(\s*(?:1[6-9]|20)\d\d(?:\s*[-–]\s*\d{2,4})?\s*\)")
                                                                                                
                                                                            
                                                                                
                                                                                                    
                                                                                 
                                                                                               
                                                                                               
                                                                                            
                                                             
                                                                                             
                                                                                              
                                                          
_SF_SAY = (r"(?:noted|notes|said|says|wrote|writes|observed|observes|comments|commented|explains|explained|"
           r"argued|argues|suggested|suggests|states|stated|described|describes|remarked|remarks|concluded|"
           r"concludes|put\s+it|puts\s+it|pointed\s+out|points\s+out|summarised|summarized|discussed|discusses)")
_SF_TITLE_W = (r"(?:The\s+|A\s+|An\s+)?[A-Z][A-Za-z'’\-]+(?:\s+(?:" + _SF_TW[3:-1]
               + r"|a|an|as|by|or|with|from|its)){1,9}?")
_SF_NAME_IN_TITLE_YEAR = re.compile(
    r"(?<![A-Za-z.])(?:(?P<by>by\s+(?:[A-Z][a-z]+\s+)?))?(?P<a>" + _SF_NAME + r"(?:\s+(?:and|&)\s+" + _SF_NAME + r")?)\s+"
    r"(?(by)|(?:[a-z]+ly\s+)?" + _SF_SAY + r"\s+(?:that\s+)?)in\s+"
    r"(?:[Cc]hapter\s+\d{1,2}\s+of\s+)?(?:(?:his|her|their)\s+(?:book|work|text|treatise|monograph)\s*,?\s+)?"
    r"(?P<t>" + _SF_TITLE_W + r")(?P<c>\s*\(\s*(?:1[6-9]|20)\d\d\s*\))(?!\s*\d)(?!\s*[A-Z][A-Za-z.]*\.?\s+\d)")
                                                                                                  
                                                                         
                                                                       
                                                                                             
                                                                                              
                                                                            
_SF_FN_TITLE_YEAR = re.compile(
    r"\[\d{1,4}\]\s+(?P<t>" + _SF_TITLE_W + r")(?P<c>\s?,?\s*(?:\d{1,2}\s*(?:st|nd|rd|th)\s+(?:[A-Z][a-z]+\s+)?ed\s*)?"
    r"\(\s*(?:1[6-9]|20)\d\d\s*\))(?=\s*,?\s*(?:at\s+\d|vol\b|bk\b|ch\b|pp?\s*\d))")
_SF_JUDGE_BEFORE = re.compile(r"(?:Justice|Judge|Lord|Lady|Baron|Chief|Mr|Mrs|Ms|J\.|JJ\.?|LJ|CJ|v\.?)\s+$")
_SF_NOT_TITLE_LIGHT = re.compile(
    r"\b(?:Acts?|Ordinances?|Regulations?|Rules|Bill|Code|Statutes?|Reports?|Cases?|Hansard|Debates|"
    r"Ltd|Limited|Inc|Court|Committee|Commission)\s*$|^(?:Chief|Mr|Lord|Justice|Judge|Sir)\b")
                                                                                             
                                                                                           
                                                                                               
                                                                                       
_SF_TITLE_FIRST = (_SF_TITLE_BY, _SF_PAREN_TITLE_EDITION, _SF_SAYS_IN, _SF_TITLE_ED_YEAR,
                   _SF_TITLE_ED_THEN_YEAR)
                                                               
_SF_NOT_AUTHOR = re.compile(
    r"^(?:See|In|The|But|And|Thus|Also|Section|Sections|Act|Chapter|Part|Article|Schedule|Rule|"
    r"Rules|Order|Lord|Mr|Mrs|Sir|Dr|Queen|King|Crown|Court|Lloyd|Majesty|Parliament|Plaintiff|"
    r"Defendant|Appellant|Respondent|Counsel|Judge|Justice|Footnote|Ibid|Compare|Contra|Note|"
    r"Comment|Hansard|January|February|March|April|May|June|July|August|September|October|"
    r"November|December|Statute|Statutes|Government|Commonwealth|State|Bill|Code|Congress|"
    r"Senate|House|Committee|Commission|Department|Board|Company|Bank|Appellants?|Respondents?|"
    r"Plaintiffs|Defendants|Petitioners?|Claimants?|Applicants?|Prosecution|Accused|Exhibits?|"
    r"List|States|Hearing|England|Australia|Canada|Singapore|Ltd|Pte|Inc|Bureau)\b")
                                                                                              
_SF_NOT_TITLE = re.compile(
                                                                                                 
                                                                                         
    r"\b(?:Acts?|Ordinances?|Regulations?|Rules|Bill|Code|Statutes?)\s*$|"
    r"\b(?:Reports?|Rep|App|Appeals|"
    r"Cases?|Bench|Digest|Dictionary|Abridge?ment|Will|Trusts?|Settlement|Estate|Patents?|"
    r"Application|Claim|Hansard|Debates|Gazette|Times|Ltd|Limited|Co|Company|Corporation|Inc|"
    r"Bank|Railway|Hospital|Charity|Commissioners?|Board|Council|Committee|Department|Minister|"
    r"Secretary|Attorney|Solicitor|Court|Division|Counsel|Inspector|Surveyor|JJ?|LJ|CJ|"
    r"Convention|Treaty|Charter|Amendment|Clause|Section|Article|Schedule|"
                                                                                
    r"Record|Factum|Transcript|Affidavit|Brief|Trials?|Sup|Supp|Synopsis|Decisions|Manual|"
    r"Exhibits?|Bundle|Doc|ECF|Library|Submissions?)\b"
    r"|^(?:Chief|Mr|Lord|Justice|Judge|Sir)\b")
_SF_CASE_BEFORE = re.compile(r"(?:\bv\.?|\b[Ii]n\s+re|\b[Rr]e|\b[Ee]x\s+parte|\b[Ii]n\s+the\s+matter\s+of)\s*$")


B20_SHORT_FORM = os.environ.get("JR_B20", "1") != "0"                                            
PASS_1J = os.environ.get("JR_1J", "1") != "0"                                               
CASE_TAIL = os.environ.get("JR_CASETAIL", "1") != "0"                                                    
RESTATEMENT_TRIM = os.environ.get("JR_RESTTRIM", "1") != "0"
_RESTATEMENT_TITLE = re.compile(
    r"Restatement\s+(?:\([A-Za-z]+\)\s+)?of\s+(?:the\s+)?(?:Law\s+(?:of\s+)?)?[A-Z][a-z]+"
    r"(?:\s+(?:and|of|&)\s+[A-Z][a-z]+|\s+[A-Z][a-z]+){0,5}")
                                                                                              
                                                                                            
                                                                                               
                                                                               
CASE_KEY = os.environ.get("JR_CASEKEY", "1") != "0"
_CASE_KEY_TAIL = re.compile(r"(?:1[6-9]|20)\d\d (?:\d{1,3} )?(?:ac|clr|scr|fca|qb|kb|wlr|nswlr) \d{1,4}$")
B20_SIXTH = os.environ.get("JR_B20SIX", "1") != "0"                                                       
B23_LAW_REFORM = os.environ.get("JR_B23", "1") != "0"                                                 
B24_LAW_REFORM_ORD = os.environ.get("JR_B24", "1") != "0"                                                             
US_PIN = os.environ.get("JR_USPIN", "1") != "0"                                                        
                                                                                                 
                                                                                        
                                                                                                 
                                                                                                 
                                                                                                   
RAW_KEYS = os.environ.get("JR_RAWKEYS", "0") == "1"                                       
_SPLIT_JOURNAL_CITE = re.compile(
    r"(\b\d{1,3}[ \t]+(?:[A-Z][A-Za-z&\-]*\.[ \t]?){1,6})[ \t]*\n[ \t]*\n[ \t]*"
    r"(?=(?:[A-Z][A-Za-z&]*\.[ \t]?){1,4}[ \t]*\d{1,4}\b)")
_SF_SURNAME = re.compile(r"(?:^|\s)([A-Z][a-z][A-Za-z\-]+)")                                    
_REPORT_PINPOINT_TAIL = re.compile(
    r"\(?(?:1[6-9]|20)\d\d\)?\s*(?:\d{1,3}\s+)?([A-Z][A-Za-z.&() ]{0,16}?)\s*,\s*at\s+pp?\.?\s*\d+\s*$")
                                                                                                 
_SPEECH_THEN_YEAR = re.compile(
    r"\b(?:said|says|say|stated|observed|remarked|added|continued|wrote|admitted)\s*[:,]?\s*"
    r"\(?(?:1[6-9]|20)\d\d\)?\s*$")


def _short_form_treatises(work):
    """(start, end, text) for each B20 match that survives its own guards."""
    out = []
    for rx in (_SF_AUTHOR_TITLE, _SF_POSSESSIVE, _SF_ON, _SF_AUTHOR_EDITION,
               _SF_AUTHOR_PAREN_EDITION, _SF_CLASSIC, _SF_US_BOOK, _SF_PROF_PAREN,
               _SF_AUTHOR_TITLE_YEAR) + _SF_TITLE_FIRST + ((_SF_NAME_IN_TITLE_YEAR, _SF_FN_TITLE_YEAR)
                                                         if B20_SIXTH else ()):
        for m in rx.finditer(work):
            if rx is _SF_NAME_IN_TITLE_YEAR and _SF_JUDGE_BEFORE.search(work[max(0, m.start() - 12):m.start()]):
                continue
                                                                                                      
                                                                                                     
                                                                                                          
            if re.match(r"\d*\s*/\s*(?:1[89]|20)?\d{2}\b", work[m.end():m.end() + 10]) and m.group()[-1:].isdigit():
                continue
            if rx is _SF_CLASSIC and re.match(
                    r"\s*(?:,\s*)?(?:J|JJ|LJ|CJ|L\.\s?J|C\.\s?J)\b|\s+v\.?\s", work[m.end("a"):m.end("a") + 8]):
                continue
            a = m.groupdict().get("a") or ""
            t = m.groupdict().get("t") or ""
                                                                                            
                                                                                                    
            if (rx in _SF_TITLE_FIRST or rx is _SF_FN_TITLE_YEAR) and re.search(
                    r"\b(?:Rules|Guide|Usage|Statement|Handbook)\b", t):
                continue
            if a and _SF_NOT_AUTHOR.match(a):
                continue
            if t:
                last = t.split()[-1]
                                                                                               
                                                                                            
                _bad = _SF_NOT_TITLE_LIGHT if rx is _SF_AUTHOR_TITLE_YEAR else _SF_NOT_TITLE
                if not (last[:1].isupper() or last[:1].isdigit()) or _bad.search(t):
                    continue
            if _SF_CASE_BEFORE.search(work[max(0, m.start() - 16):m.start()]):
                continue
            g = m.group()
            if _NAME_ON_CASE.search(g) or _NOT_SCHOLARSHIP.search(g) or _NOT_A_WORK.search(g):
                continue
            if _REFERENCE_WORK.search(g):
                continue
            if rx is _SF_ON:
                                                                                              
                                                                  
                g = "%s on %s%s" % (a, t, m.group("c"))
            if rx is _SF_NAME_IN_TITLE_YEAR:
                                                                              
                out.append((m.start(), m.end(), "%s, %s%s" % (a, t, m.group("c")), None))
                continue
            if rx is _SF_FN_TITLE_YEAR:
                out.append((m.start("t"), m.end(), t + m.group("c"), t))
                continue
            if rx is _SF_SAYS_IN:
                g = t + m.group("c")                                                       
            elif rx is _SF_PAREN_TITLE_EDITION:
                g = g.lstrip("( ")
            elif rx is _SF_CLASSIC:
                                                                                         
                                                                                  
                out.append((m.start(), m.end(), g, "\x00supersede"))
                continue
            elif rx is _SF_PROF_PAREN:
                g = "%s, %s%s" % (a, t, m.group("c"))
                                                                                         
                out.append((m.start(), m.end(), g, "\x00supersede"))
                continue
            elif rx is _SF_AUTHOR_TITLE_YEAR:
                                                                                               
                                                                                              
                                                                                              
                                                                                        
                out.append((m.start(), m.end(), g[:g.rindex(")") + 1], "\x00full"))
                continue
                                                                                               
            out.append((m.start(), m.end(), g, t if rx in _SF_TITLE_FIRST else None))
    return out


                                                                                         
                                                                                                
                                               
                                                                                                
                                                                                              
                                                                                              
                                                                                               
                                                                                                
                                                                                                 
                                                                                              
                                                                                                 
                                                                                         
                                                                                        
                                                                                              
                         
                                                                                             
                                                                             
_IMPRINT_ONLY = re.compile(
    r"^\(\s*(?:[A-Z][A-Za-z.]+\s*[:/]\s*)?[A-Z][A-Za-z&.'’/\- ]{2,48}(?:\s*\([A-Za-z ]{2,20}\)[A-Za-z .]{0,12})?"
    r"\s*,\s*(?:[A-Za-z0-9 .\-]{0,30},\s*)?(?:1[6-9]|20)\d\d\s*[)(]?\s*$")
_IMPRINT_WORD = (r"(?:Maxwell|Butterworths?|LexisNexis|Press|Publishing|Publishers|Sons|Reuters|Carswell|"
                 r"Kluwer|Routledge|Blackwell|Hart|Tottel|Stevens|Thomson|West|Juta|Informa|LBC|CCH)")
_IMPRINT_PIECE = re.compile(r"^" + _IMPRINT_WORD + r"\b")
_IMPRINT_OPEN = re.compile(r"\(\s*(?:[A-Z][A-Za-z.]+\s*[:/]\s*)?(?:[A-Z][A-Za-z&.]*\s+(?:&\s+|and\s+)?){0,3}$")
_RUN_CONNECT = frozenset(("of", "and", "the", "in", "on", "to", "for", "a", "an", "vol", "vols", "de", "la",
                          "le", "du", "des", "et", "al", "gen", "ed", "eds", "edn", "editor", "editors",
                          "rev", "with", "by", "under", "at", "its", "or", "as", "from"))
_RUN_NOT_HEAD = frozenset(("In", "See", "Cf", "As", "From", "By", "Per", "Also", "And", "But", "The",
                           "Mr", "Ms", "Dr", "Prof", "Professor", "Sir", "Lord"))
_RUN_ENCYC = re.compile(r"(?i)\bhalsbury|\bcorpus\s+juris\b|\bam(?:erican)?\.?\s?jur(?:isprudence)?\b")


def _imprint_span(work, s, e, t):
    """(start, end) of the imprint bracket a match is, or is a piece of; None for anything else."""
    ts = str(t or "").strip()
    if _IMPRINT_ONLY.match(ts):
        return s, e
    if _IMPRINT_PIECE.match(ts) and "(" not in ts:
        op = work.rfind("(", max(0, s - 30), s + 1)
        if op >= 0 and ")" not in work[op:s] and _IMPRINT_OPEN.search(work[op:s] if op < s else "("):
            cl = work.find(")", e, e + 45)
            if cl >= 0 and "(" not in work[e:cl]:
                return op, cl + 1
            return op, e
    return None


def _run_before(work, s):
    """Start of the capitalised run that ends where the bracket at `s` opens (or `s`, if none)."""
    lo = max(0, s - 260)
    toks = [(m.start() + lo, m.group()) for m in re.finditer(r"\S+", work[lo:s])]
    if toks and toks[0][0] == lo and lo > 0:
        toks = toks[1:]                                                                       
    start, content, depth = s, 0, 0
    for pos, tok in reversed(toks):
                                                                            
        depth += tok.count(")") - tok.count("(")
        core = tok.strip("“”\"'‘’(),:–—-")
        if "[" in tok or "]" in tok or tok.endswith(";") or tok.endswith(";)"):
            break
        if tok.endswith(".") and not re.fullmatch(r"\(?[A-Z]\.", tok) and core.lower() not in ("ed.", "eds.", "vol."):
            break
        if core and not (core[:1].isupper() or core[:1].isdigit() or core.lower() in _RUN_CONNECT
                         or core in ("&", "v", "v.")):
            break
        if core in ("v", "v."):
            return s                                                            
        start = pos
        if core[:1].isupper() and core not in _RUN_NOT_HEAD and len(core) > 1:
            content += 1
        if depth < 0:
            depth = 0
    if content < 2:
        return s
                                                                                            
    for pos, tok in toks:
        if pos < start:
            continue
        core = tok.strip("“”\"'‘’(),:–—-")
        if core[:1].isupper() and core not in ("In", "See", "Cf", "As", "From", "By", "Per", "Also", "And", "But"):
            return pos + (len(tok) - len(tok.lstrip("“”\"'‘’(")))
    return s


                                                                                                  
                                                                                                    
                                                                                                
                                                                                               
                                                                              
ZERO_FALSE = os.environ.get("JR_ZEROFALSE", "1") != "0"
SAME_WORK = os.environ.get("JR_SAMEWORK", "1") != "0"                                    
_ZF_MONTH =r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
                                                                   
_ZF_MONTH_LIST = re.compile(r"^(?:" + _ZF_MONTH + r"\s*,?\s*(?:and\s+)?){2,6},?\s*\(?(?:1[6-9]|20)\d\d\)?$")
_ZF_ENDS_YEAR = re.compile(r"\(\s*(?:1[6-9]|20)\d\d\s*\)?\s*$")
                                                                                                 
                                                                                   
_ZF_COMPANY_AFTER = re.compile(r"^\)?\s{0,2},?\s{0,2}(?:Ltd|Limited|Inc|Pty|Pte|Corp|Corporation|LLC|plc|PLC)\b"
                               r"|^\)?\s{1,3}v\.?\s+[A-Z]")
                                                                            
                                                                                    
                                                 
                                                                                 
                                                                                 
                                                                                                     
_ZF_TAIL_PIN = re.compile(
    r"^\)?\s{0,3},?\s{0,3}\d{1,4}\s+([A-Z][A-Za-z&'.]{0,14}(?:\s+[A-Z][A-Za-z&'.]{0,14}){0,3})"
    r"\s{0,3},\s{0,3}(?:at\s+)?pp?\.?\s{0,3}\d")
_ZF_TAIL_AMP = re.compile(
    r"^\)?\s{0,3},?\s{0,3}\d{1,4}\s+([A-Z][A-Za-z'.]{0,14}\s+&\s+[A-Z][A-Za-z'.]{0,14})"
    r"\s{0,3}(?:\((?:2d|3d|4th|5th)\)\s{0,3})?\d{1,4}\b")
_ZF_TAIL_LR = re.compile(r"^\)?\s{0,3},?\s{0,3}L\.?\s?R\.?\s+\d{1,2}\s+[A-Z][A-Za-z.]{0,8}\s+\d{1,4}\b"
                         r"|^\)?\s{1,3}Ch\s+\d{3,4}\b")
_ZF_LOCATOR = re.compile(r"(?i)(?:vols?|volume|pp?|paras?|ch|chapter|part|pt|book|no|nos|cmn?d|cm|hc|hl|law|"
                         r"report|working|consultation|discussion|issues|paper|title|art|section|sect?|tome|bk|col|cols)\b\.?")
                                                                                                  
                                                      
_ZF_PROBATE = re.compile(r"\[(?:1[89]|20)\d\d\]\s+P\s+\d{1,4}\s*$")
                                                                                                    
                                                                                    
                                                                                                    
                                                                                                
                                                                                                    
                                                                                           
                                          
_ZF_CASE_IN = re.compile(r"\b(?:In\s+re|Ex\s+parte)\s+[A-Z][^,;:]{2,40}\(?(?:1[6-9]|20)\d\d\)?$"
                         r"|^(?:[^\s,]+\s+){1,6}v\.?\s+[A-Z]"
                         r"|^[^,]{1,40},\s+(?:[^\s,]+\s+){0,2}v\.?\s+[A-Z]")
                                                                                                 
_ZF_US_CASE = re.compile(r"\((?:CA(?:\d{1,2}|DC|FC)|D\.?\s?C\.?|[SNEW]D\s?[A-Z][A-Za-z.]*)\s+(?:1[89]|20)\d\d\)$"
                         r"|\b\d{1,3}\s+(?:NLRB|FCC|FTC|ICC|IBIA|BIA)\s+\d{1,4}\b")
                                                                                              
                                                                       
_ZF_NAMES_ONLY = re.compile(r"^[A-Z][A-Za-z'’\-]+(?:(?:\s*,\s*|\s+(?:and|&)\s+)[A-Z][A-Za-z'’\-]+){0,3}$")
_ZF_JUDGE_AFTER = re.compile(
    r"^\s?,?\s*(?:(?:and\s+)?[A-Z][A-Za-z'’\-]+\s*,?\s+){0,3}(?:JJA|JJ|LJJ)\b"
    r"|^\s?,\s*(?:J|LJ|CJ|MR|JA)\.?,"
    r"|^\s?,\s*LJ[A-Z]\d")
                                                                                                     
_ZF_COUNSEL_BEFORE = re.compile(
    r"\bFor\s+(?:the\s+)?(?:Appellants?|Respondents?|Plaintiffs?|Defendants?|Pursuers?|Defenders?|Petitioners?)"
    r"\s*[,:—–\-]\s*(?:[A-Z][A-Za-z.]*\.?\s*,?\s+){0,8}$")
                                                                                                   
                                                          
_ZF_AFTER_NOT_AUTHOR = re.compile(r"^\s?,\s*Solicitors?\b")
                                                                                                   
                                                                                          
_ZF_FIRM_AFTER = re.compile(
    r"^\s?,\s*(?:PA|PC|PLC|LLP|LLC|LPA|LP|P\.\s?[AC]\.|L\.\s?L\.\s?[PC]\.|L\.\s?P\.\s?A\.|P\.\s?L\.\s?C\.|Publishers)"
    r"(?![A-Za-z])")
                                                                                               
                                                                                                
                                                                                             
_ZF_BODY_BEFORE = re.compile(
    r"\b(?:Secretary\s+of\s+State|Ministers?|Ministry|Department|Dept\.?|Office|Bureau|Bank|Centers?|Centre|"
    r"Board|Commission(?:er)?|Committee|Institute|Association|Society|Council|Agency|Division|Panel)"
    r"\s+(?:for|of|on)\s+(?:the\s+)?$|\bMinisters?\s+for\s+[A-Z][a-z]+,\s+$")
                                                                                                 
                                                                                                   
                                                                                            
_ZF_INSTRUMENT = re.compile(
    r"\b(?:Treaty|Convention|Covenant|Protocol|Directive|Final\s+Agreement|Code\s+of\s+Practice|"
    r"Statute\s+of\s+the\s+International\s+Criminal\s+Court|COM|Session)\s*\(\s*(?:1[6-9]|20)\d\d\s*\)?\s*$")
                                                  
_ZF_LEGISLATION = re.compile(
    r"\bStat(?:u|ut)es\s+at\s+Large\b|\bCollection\s+of\s+Statutes\b|\bN\.?\s?Y\.?\s+[A-Z][a-z]+\s+Law\s+§"
    r"|^An\s+Act\s+to\b|\bpromulgated\s+by\b"
    r"|\bClerk\s+of\s+this\s+Court\b|\bGazette\s+Notification\b|\b(?:[A-Z][a-z]+\s+and\s+)?[A-Z][a-z]+\s+Amendments?$"
    r"|\b[A-Za-z]*LawRp\b")
                                                                                                 
_ZF_YEAR_NOT_PUB = re.compile(r"^\s+Rev\s+Ed\b|^/\d{1,4}/E[CU]\b")
                                                                                
_ZF_REPORTER_POSS = re.compile(r"^[A-Z][a-z]+['’]s\s+(?:Sup|Supp|App|Rep|Dec)\.")
                                                                                               
_ZF_MEMO_BEFORE = re.compile(r"\b(?:Memorandum|Letter)\s+(?:from|of)\s+(?:[A-Z][a-z]+\s+){0,2}$")
                                                                          
_ZF_PROSE_WORD = frozenset((
    "was", "were", "is", "are", "has", "have", "had", "that", "which", "whether", "will", "would", "should",
    "be", "been", "it", "we", "this", "those", "these", "their", "his", "me", "he", "she", "they", "there",
    "when", "where", "who", "not", "such", "any", "may", "shall", "can", "could", "did", "does", "its"))
_ZF_CONNECT = frozenset(("of", "the", "and", "in", "on", "to", "for", "a", "an", "at", "by", "with", "from", "under",
                         "de", "la", "le", "les", "du", "des", "et", "en", "au", "aux", "der", "und", "von", "van",
                         "ed", "eds", "edn", "vol", "pp", "p", "al", "or", "as", "v"))
                                                                                            
_ZF_HYPHEN_YEAR = re.compile(r"[a-z]-\s+\((?:1[6-9]|20)\d\d\)$")
_ZF_LAST_WORD_YEAR = re.compile(r"\b(this|that|be|deemed|said|held|it)\s*\((?:1[6-9]|20)\d\d\)?$")
                                                                                                   
                                                                                           
_ZF_ABBREV_ONLY = re.compile(r"^[A-Z]{2,6}$")
_ZF_CITE_BEFORE = re.compile(r"(?:[\])]|\b(?:1[6-9]|20)\d\d|\b\d{1,3})\s*,?\s*$")
_ZF_CITE_AFTER = re.compile(r"^\s*,?\s*(?:\d|at\s+\d|\(\s*(?:News|Notes)\s*\))")
                                                                                                   
                                                                                                  
                                                                                
_ZF_HYBRID = re.compile(r"^(?:SLT|Sol\.?\s?J(?:o)?\.?|SJ)$")
_ZF_CASE_NAME_BEFORE = re.compile(
    r"(?:\sv\.?\s+[A-Z][^.;()“”\"]{0,45}|\bEx\s+parte\s+[A-Z][^.;()“”\"]{0,30})[\[(]?(?:1[6-9]|20)\d\d[\])]?\s*(?:\d{1,3}\s*)?$")
_ZF_SLT_COURT_AFTER = re.compile(r"^\s*\((?:Sh\s?Ct|Land\s?Ct|Lyon\s?Ct|Notes)\)")
                                                                                                  
                                 
_ZF_HOLMES_OK = re.compile(r"^\s*(?:,?\s*J(?:n)?r\.?)?\s*,\s*[“\"‘']?(?:The\s+|A\s+)?[A-Z]|^['’]s\s+[“\"]?[A-Z]")
                                                                                                     
_ZF_HEADING = re.compile(r"\b(?:HOUSE\s+OF\s+LORDS|COURT|APPEAL)\b")
_ZF_BARE_STRONG = re.compile(
    r"^(?:['’]s\s+(?!Case\b)[A-Z]|\s+on\s+(?:the\s+)?[A-Z][a-z]+(?:\s*[,(]|\s+at\s|\s+\d)"
    r"|\s*,\s*(?:The\s+|A\s+)?[A-Z][A-Za-z]+(?:\s+[A-Za-z&]+){0,8}?,?\s*\(?\d{1,2}\s?(?:st|nd|rd|th)\s+[Ee]d)")


                                                                                              
                                                                  
                                                                                                   
                                                                                                     
                                                                                                    
                                                                                                        
                                                                              
                                                                                    
                                                                       
                                                                    
_ZF_LEAD_CUE = re.compile(
    r"(?:\bin\s+(?:his|her|their)\s+(?:[a-z\-]+\s+){0,2}(?:work|book|textbook|text|treatise)\s*,?\s+"
    r"|\bquoting\s+from\s+|\bthe\s+discussion\s+in\s+|\bhad\s+adduced\s+the\s+work,\s+|\bentitled\s+"
    r"|\b(?:suggested|explained|discussed)\s+by\s+[^,()]{3,40}?\s+in\s+"
    r"|\b(?:expresses|puts|put)\s+it,?\s+in\s+|\b(?:drawn|given|set\s+out|found)\s+[^,()]{0,50}?\s+in\s+"
    r"|^For\s+instance,\s+in\s+)(?=[“\"]?(?:The\s+|A\s+|An\s+)?[A-Z])")
_ZF_HAS_DATE = re.compile(r"(?:1[5-9]|20)\d\d|\b[Ee]d\b")


def _zf_lower_words(s):
    """The lower-case words of `s` that are not connectors."""
    w = [x.strip(",.;:()'’\"“”") for x in str(s or "").split()]
    return [x for x in w if x[:1].islower() and x not in _ZF_CONNECT]


def _zf_trim(ts):
    """Offset in `ts` at which the work starts (0 where no lead-in is printed)."""
    cut = 0
    for m in _ZF_LEAD_CUE.finditer(ts):
        cut = m.end()
                                                                                              
                                                                                                   
                                                                                                 
                                                                                                     
    if cut and len(ts) - cut >= 10 and _ZF_HAS_DATE.search(ts[cut:]):
        return cut
    return 0


def _zf_is_defined(work, short, cache):
    """The judgment defines `short` as its own short name for a work: `("Trindade, Cane &
    Lunney")`, `("Gold on Statistical Evidence")`, `("Malek & Quest, Jack: Documentary Credits")`."""
    key = "\x00" + short
    if key not in cache:
        n = r"\s+".join(re.escape(w) for w in short.split())
        cache[key] = bool(re.search(r"\(\s*(?:the\s+|hereinafter\s+)?[“\"]\s?" + n + r"(?:[,:][^”\"()]{0,60})?\s?[”\"]\s*\)", work))
    return cache[key]


                                                                                                 
                                                                                             
                                                                                           
                                                                                
                                                                                            
                                                                                                           
                                                                                                                      
                                                                                                              
                                                                               
                                                                                               
                                                                                               
                                                                                           
                                          
                                                                                                 
                                                                             
_ZF_R20_BODY = re.compile(
    r"\bRoyal\s+Commission\b(?!s)|\bCommission\s+of\s+Inquiry\b|\bCommittee\s+of\s+(?:Inquiry|Enquiry)\b"
    r"|\b(?:Public|National|Justice)\s+Inquiry\b"
    r"|\b(?:Inter)?[Dd]epartmental\s+Committee\b|\b(?:Select|Standing|Joint)\s+Committee\b"
    r"|\bReview\s+Comm(?:ittee|ission)\b|\bDevelopment\s+Committee\b|\bTrade\s+Committee\b"
    r"|\bHome\s+Office\b|\bCabinet\s+Office\b|\bScottish\s+Executive\b|\bAudit\s+(?:Commission|Office)\b"
    r"|\bMinist(?:ry|er|ere)\s+(?:of|for|des?|du)\b|\bDepartment\s+(?:of|for)\b|\bDept\.\s+of\b"
    r"|\bOffice\s+of\s+(?:the\s+)?[A-Z]|\bBureau\s+of\s+(?!Economic\s+Research)[A-Z]|\bService\s+des\b"
    r"|\bStatistics\s+Canada\b|\bHealth\s+Canada\b|\bLibrary\s+of\s+Parliament\b"
    r"|\bSolicitor\s+General(?:['’]s)?\s+Office\b|\bSecretary\s+of\s+State,|\bState\s+Archives\b"
    r"|\bCongressional\s+Research\s+Service\b|\bIRS,|\bWildlife\s+Service\b|\bIncome\s+Bulletin\b"
    r"|\bTruth\s+(?:and|&)\s+Reconciliation\s+Commission\b|\bSentencing\s+(?:Commission|Council)\b"
    r"|\bStanding\s+Council\s+on\b|\bSCAG,|\bCanadian\s+Panel\s+on\b|\bNational\s+Council\s+of\s+Welfare\b"
    r"|\bSecurity\s+Intelligence\s+Organisation\b|\bCommission\s+de\s+(?:la|consultation)\b"
    r"|\bGroupe\s+de\s+travail\b|\bTask\s+Force\s+on\b")
_ZF_R20_TITLE = re.compile(
    r"\bCmn?d\.?\s*\d|\bCm\s+\d{2,5}\b|\bHL\s+Paper\s+\d|\bHC\s+\d{2,4}\b|\bWhite\s+Paper\b|\bGreen\s+Paper\b"
    r"|\bAnnual\s+(?:Report|Threat\s+Assessment)\b|\bReport\s+to\s+[Tt]he\s+(?:Minister|Secretary\s+of\s+State)\b"
    r"|\bReport\s+by\s+Sir\b|\bInterim\s+Report,|:\s+Final\s+Report\b|\bConsultation\s+Document\b"
    r"|\bImpact\s+Assessment\b|\bDefinitive\s+Guideline\b|\bGuidance\s+Document\b|\bOfficial\s+Voter\s+Information\b"
    r"|\bFindings\s+(?:and|&)\s+Recommendations\b|\bExplanatory\s+Notes\b|\bStatement\s+of\s+Policy\s+by\s+the\s+Government\b"
    r"|\bReport\s+(?:of|on)\s+the\s+[^,;()]{3,70}\bInquiry\b|\bRapport\s+(?:Faribault|du\s+groupe)\b")
                                                                                             
                                                                                                     
                                                                                              
_ZF_R20_NOT = re.compile(
    r"\b(?:Universit[yé]|Institute|Institut|Centre|Center|College|School\s+of|Foundation|Academy|Society|"
    r"Research\s+Council|Policy\s+Lab|World\s+Customs\s+Organi[sz]ation|International\s+Labour\s+"
    r"(?:Office|Organi[sz]ation|Conference)|ILO|United\s+Nations|UNHCR|World\s+Health\s+Organi[sz]ation|"
    r"OECD|World\s+Bank|International\s+Monetary\s+Fund|World\s+Trade\s+Organi[sz]ation|Council\s+of\s+Europe)\b")
_ZF_REF_STOP = re.compile(
    r";|\[\d{1,4}\]|(?<![A-Za-z])[a-z]{4,}\.[”\"]?\s+(?=[A-Z“\"(])"
    r"|\b(?:[Ss]ee(?:\s+also|\s+generally)?(?:,?\s+e\.?\s?g\.?,?)?|[Cc]iting|[Qq]uoting|quoted\s+in|cited\s+in|[Cc]f\.?)\s+(?=[A-Z])")


_ZF_REF_FILL = frozenset(("of", "the", "and", "for", "on", "to", "in", "into", "de", "des", "du", "la", "les", "et",
                          "sur", "&", "its", "his", "her", "their", "report", "by", "with", "a", "an", "al", "others"))


def _zf_ref_left(pre):
    """The part of `pre` that belongs to the reference a match stands in (see `_ZF_R20_BODY`)."""
    cut = 0
    for m in _ZF_REF_STOP.finditer(pre):
        cut = m.end()
    left = pre[cut:]
    op = left.rfind("(")
    if op >= 0 and ")" not in left[op:]:
        left = left[op + 1:]                                                                      
    else:
        cl = left.rfind(")")
        if cl >= 0:
            left = left[cl + 1:]                                                                 
                                                                                          
                                                                                              
                                                                                          
                                                                                     
                                                                                         
                                                                                 
    mf = re.search(r"\b(?:Commission|Minist[eè]re|Service|Comit[eé]|Conseil|Groupe)\s+(?:de|des|du|d['’])\b", left)
    if mf:
        return left[mf.start():]
    toks = list(re.finditer(r"\S+", left))
    start = len(left)
    for m in reversed(toks):
        tok = m.group()
        core = tok.strip(",:'’\"“”()—–-+")
        if core and not (core[:1].isupper() or core[:1].isdigit() or core.lower() in _ZF_REF_FILL
                         or core.lower().rstrip(".") in ("vol", "vols", "no")):
            break
        if tok.endswith(".") and not re.fullmatch(r"(?:[A-Z]\.)+|[Vv]ol\.|Dept\.|eds?\.|No\.", tok):
            break
        start = m.start()
    return left[start:]


def _zf_official(pre, ts, after, quoted):
    """True where the printed reference names a government or official body (R20)."""
    left = _zf_ref_left(pre)
    ref = left + ts
    if _LAW_REFORM_BODY.search(ref) or _ZF_R20_NOT.search(ref):
        return False
    if _ZF_R20_TITLE.search(ts) or _ZF_R20_TITLE.search(after[:22]):
        return True
    if quoted:
        return False
                                                                                                  
                                                                                                 
                                                                                                 
                                                                                                 
                                                                                                  
                                                                                              
    prose = len(_zf_lower_words(ts)) >= 6
    for m in _ZF_R20_BODY.finditer(ref):
                                                                                             
                                                                                               
                                                 
        if (m.group().startswith("Office of") and not m.group().startswith("Office of the")
                and ref[:m.start()].rstrip()[-1:] not in ("", ",")):
            continue
        if m.start() < len(left):
            return True
        if prose:
            continue
        rest = ref[m.end() - 1:]
        if re.search(r"[,:]", rest) or re.fullmatch(r".{0,60}?\(\s*(?:1[6-9]|20)\d\d\s*\)?", rest) \
                or (len(rest) < 45 and after.lstrip()[:1] == ","):
            return True
    return False


def _zf_is_party(work, name, cache):
    """The judgment itself uses `name` as a party: `Snell v. Farrell`, `R. v. McGregor`, or as a
    defined short name: `(collectively, "Bentham")`."""
    if name not in cache:
        n = re.escape(name)
        cache[name] = bool(re.search(
            r"\b" + n + r"\s+v\.?\s+[A-Z(]|\sv\.?\s+" + n + r"\b"
            r"|\(\s*(?:collectively,?\s+|the\s+)?[“\"‘']\s?" + n + r"\s?[”\"’']\s*\)", work))
    return cache[name]


def _zf_party_before(pre):
    """`... v. United Association of Journeymen and Apprentices of the | Plumbing and Pipefitting
    Industry`: a versus, then nothing but name words up to the match."""
    s = str(pre or "")
    i = max(s.rfind(" v "), s.rfind(" v. "))
    if i < 0:
        return False
    tail = s[s.index("v", i) + 1:].lstrip(". ")
    if not tail.strip() or any(c in tail for c in ".,;:()[]“”\""):
        return False
    return all(w[:1].isupper() or w in ("of", "and", "the", "for", "in", "&", "de", "du", "la") for w in tail.split())


                                                                                             
ZF_ROUND2 = os.environ.get("JR_ZFR2", "1") != "0"
_ZF_NEWS_URL = re.compile(
    r"https?://(?:www\.)?(?:huffingtonpost|nytimes|washingtonpost|wsj|usatoday|latimes|theguardian|cnn|foxnews|"
    r"nbcnews|cbsnews|abcnews|reuters|apnews|politico|bbc)\.")
_ZF_DAY_PAREN = re.compile(r"\((?:Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s+(?:19|20)\d\d\)\s*$")
                                                                                                    
                                                                                                              
_ZF_CASE_NAME_TIGHT = re.compile(
    r"\sv\.?\s+[A-Z][^.,;()“”\"\[\]]{0,45}[\[(](?:1[6-9]|20)\d\d[\])]\s*(?:\d{1,3}\s*)?$")
                                                                                                  
_ZF_CASE_LIST_BEFORE = re.compile(
    r"\((?:1[6-9]|20)\d\d\)\s+\d{0,3}\s*[A-Z][A-Za-z.]{0,5}\s+\d{1,4},\s+[A-Z][a-z]+\s+\((?:1[6-9]|20)\d\d\)\s*$")
_ZF_LEAD_WIDEN = (
                                                                                                
    re.compile(r"(?:[A-Z][A-Za-z.\-‑]*\.?\s+)?[A-Z][A-Za-z\-]+,\s+in\s+collaboration\s+with\s+$"),
                                                                         
    re.compile(r"(?:(?:[A-Z]\.\s?)+[A-Z][A-Za-z\-]+(?:,\s+|\s+and\s+|\s+&\s+))*(?:[A-Z]\.\s?)*[A-Z]\.[\-‑]$"),
                                                       
    re.compile(r"(?<![A-Za-z])O['’]$"),
)
                                                                            
_ZF_POSS_NAMES_BEFORE = re.compile(r"(?:[A-Z][a-z]+\s*(?:,|&|and)\s+)*[A-Z][a-z]+\s+(?:and|&)\s+$")
                                                                                                              
_ZF_COLON_AUTHORS_BEFORE = re.compile(
    r"(?:(?:[A-Z]\.\s?)*[A-Z][A-Za-z\-]+(?:\s+[A-Z][A-Za-z\-]+){0,2}\s*,\s+)+(?:[A-Z][A-Za-z\-]+\s+){1,3}and\s+(?:[A-Z][a-z]+\s+){1,2}$")
                                                                                                      
                                                                   
_ZF_QUOTE_END = re.compile(r"[”\"]\s*\d{0,2}\s+(?=(?:\d{1,3}\s+)?[A-Z])")


                                                                                                 
                                                                                                
                                                                                                    
ACAD_FP = os.environ.get("JR_ACAD_FP", "1") != "0"
                                                                                              
                                                                               
                                                                                                    
                                                                                                 
                                                                                            
                                                                                                    
                                                                                             
                                                                                                        
_FP_RECORDS = re.compile(
    r"\bAmerican\s+State\s+Papers\b|\bColonial\s+Laws\s+of\s+Massachusetts\b"
    r"|\bFederal\s+and\s+State\s+Constitutions\b"
    r"|\bOfficial\s+Journal\s+of\s+the\s+Proceedings\s+of\s+the\s+Constitutional\s+Convention\b"
    r"|\(H\.\s?Hearsey\s+ed\.\s*1898\)")
                                                                                                   
                                                                                                 
                                                                                                     
                                                                               
_FP_ASSOC = re.compile(
    r"(?:American\s+Civil\s+Liberties\s+Union|National\s+Conference\s+of\s+State\s+Legislatures"
    r"|Liberty\s+Counsel)\s*,\s+[A-Z“\"]")
                                                                                                   
                                                                                                     
                                                                          
_FP_SHORT_REPORT = re.compile(
    r"(?:See,?\s+(?:also,?\s+)?)?(?:e\.?g\.?,?\s+)?"
    r"((?:[A-Z][A-Za-z'’\-]+\s+){1,3}Report)\s*\(\s*(?:19|20)\d\d\s*\)?")
                                                                                                               
_FP_LITERARY = re.compile(r"\bThe\s+Deserted\s+Village\b")
                                                                                                        
                           
_FP_FOREIGN_CASE = re.compile(r"\sv\.?\s+[A-Z][^;()]{2,60}?,\s*(?:Giurispru[n]?denza|Giurisprundenzia|Foro)\s+Italian[ao]\b")
                                                                                                       
                                                                                                  
_FP_PROSE_EDITION = re.compile(
    r"(?:More\s+particularly|In\s+fact|Moreover|Furthermore|Indeed|However|Accordingly|Thus),\s+[a-z]"
    r".*\bthe\s+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth"
    r"|[a-z]+teenth|twentieth)\s*\(\s*(?:1[6-9]|20)\d\d\s*\)?$")


                                                                                            
                                                                                                   
                                                                                             
                                                                                                      
                                                                                                  
                                                                                                     
                                                                                             
                                                                                                       
                                                                                                 
                                                                                             
                         
_FP_GOV_TITLE = re.compile(
    r"\bThe\s+Trade\s+Practices\s+Act:\s+Proposals\s+for\s+Change\b"
    r"|\bStrengthening\s+[Ss]tatutory\s+[Uu]nconscionable\s+[Cc]onduct\s+and\s+the\s+Franchising\s+Code\b"
    r"|\bProportionate\s+Liability:\s+Proposals\s+to\s+Achieve\s+National\s+Uniformity\b"
    r"|\bCharge\s+Screening\s+Practices\s+and\s+Crown\s+Evidentiary\s+Thresholds\b"
    r"|\bExemptions\s+from\s+Mandatory\s+Minimum\s+Penalties:\s+Recent\s+Developments\b"
    r"|\bA\s+Review\s+of\s+the\s+Principles\s+and\s+Purposes\s+of\s+Sentencing\s+in\s+Sections\s+718\b"
    r"|\bPlea\s+Bargaining\s+and\s+Sentencing\s+Guidelines\b")


                                                                                               
                                                                                                   
                                                                                                      
                                                                                                     
                                                                                      
                                                                                                      
                                                                                                  
                                     
                                                                                                    
                                                                    
_FP_RST_KEY = re.compile(
    r"^(?:american\s+law\s+institute\s+)?restatement\s+(?:first|second|third|1st|2nd|3rd)\s+"
    r"(?:of\s+)?(?:the\s+)?(?:law\s+)?(?:of\s+)?([a-z][a-z ]*?)\s*$")


def _acad_fp_merge(distinct, work):
    out, dead, seen = list(distinct), set(), {}
    for k in sorted(out, key=lambda x: (-len(x), x)):
        m = _FP_RST_KEY.match(k)
        if not m:
            continue
        subj = m.group(1).strip()
        _sub = re.search(r"Restatement\s*\(?\s*(?:First|Second|Third|1st|2nd|3rd)\s*\)?\s+of\s+(?:the\s+Law\s+of\s+)?"
                         + r"\s+".join(re.escape(w) for w in subj.split()) + r"\s*:\s*[A-Z]", work, re.I)
        if _sub:
            continue                                                                      
        if subj in seen:
            dead.add(k)
        else:
            seen[subj] = k
    for k in out:
        if k in dead or re.search(r"\d", k):
            continue
        j = k.strip()
        if not (j in _JOURNAL_ABBREV_ALIASES or j in _JOURNAL_ABBREV_ALIASES.values() or _names_a_periodical(j)):
            continue
        abbrs = {j} | {_ab for _ab, _fu in _JOURNAL_ABBREV_ALIASES.items() if _fu == j}
        if j in _JOURNAL_ABBREV_ALIASES:
            abbrs.add(_JOURNAL_ABBREV_ALIASES[j])
        if any(o != k and o not in dead and re.search(r"\d", o) and any(_contains_words(o, _ab) for _ab in abbrs)
               for o in out):
            dead.add(k)
    if dead and len(dead) < len(out):
        out = [k for k in out if k not in dead]
    return out


                                                                                                       
                                                                                                        
                                                                                                      
                                                                                                     
                                                                                                          
                                                                                                    
                                                                          
                                                                                                    
                                                                                                    
                                                                                                         
                                                                                                    
                                                                                                          
                                                                                                         
                                                                                                          
                                                                                                       
                                                                                             
                                                                                                          
                                                                                                          
                                                                                                            
                                                                                                     
                                                                                              
                                                                                                     
                                                                                              
                                                                                                        
                                                                                                      
                                                          
                                                                                               
                                                                                                          
                                                                                                        
                                                                                                    
                                                                                       
                                                                                                    
                                                                                        
                                                                                                      
                                                                                                      
                                                                                                       
                                                                                                        
                                                                                      
                                                                                          
                                                                                                  
                     
                                                                                              
                                                                                              
                                                                                                    
                                                                                                    
                                                                                                        
                                                                                                     
                                                                                                    
                
ACAD_ED = os.environ.get("JR_ACAD_ED", "1") != "0"
_ED_YEAR = re.compile(r"^(?:1[5-9]|20)\d\d$")
_ED_ORD = re.compile(r"^\d{1,2}(?:th|st|nd|rd|d)?$")
_ED_EDW = frozenset(("th", "st", "nd", "rd", "ed", "ed.", "edn", "edn.", "edition", "rev", "rev.", "gen", "gen.",
                     "eds", "eds.", "vol", "vol.", "loose-leaf", "looseleaf", "supp", "am.", "am"))
_ED_IMPRINT = frozenset((
    "sweet", "maxwell", "lexisnexis", "butterworths", "butterworth", "oxford", "cambridge", "university", "press",
    "hart", "publishing", "publishers", "thomson", "reuters", "carswell", "academy", "tottel", "kluwer",
    "routledge", "stevens", "sons", "informa", "lbc", "cch", "irwin", "emond", "lawbook", "federation",
    "toronto", "london", "scarborough", "ont", "ont.", "montreal", "singapore:"))
_ED_STOP = frozenset(("of", "the", "on", "a", "an", "and", "in", "to", "s", "&", "for", "with", "at", "by",
                      "upon", "its", "le", "la", "les", "de", "du", "des", "et", "."))
_ED_LEAD = frozenset(("see", "also", "moreover", "further", "cf", "cf.", "eg", "e.g.", "generally", "in",
                      "contra", "and", "however", "but", "compare"))
_ED_ORDW = {"first": "1", "second": "2", "third": "3", "fourth": "4", "fifth": "5", "sixth": "6",
            "seventh": "7", "eighth": "8", "ninth": "9", "tenth": "10", "eleventh": "11", "twelfth": "12"}
_ED_FILLER = frozenset(("practical", "treatise", "law", "laws", "principles", "relating", "the", "of", "on"))
_ED_FR = frozenset(("de", "du", "des", "la", "le", "les", "d", "l", "et", "une", "un", "sur", "dans", "en", "au",
                    "aux"))
_ED_PIN = re.compile(r"\s+at\s+(?:pp?|paras?|para|§|ch|chap)\.?\s*[\d\-–, .]+$|__\d+$|\s+at\s+\d[\d\-–, ]*$")
_ED_EPON = re.compile(r"(?:^|\s)([a-z][a-z\-]{2,}) (s|on) ")
_ED_EPON_NOT = frozenset(("law", "laws", "notes", "comment", "essays", "treatise", "commentaries", "lectures",
                          "report"))
_ED_BLK = re.compile(r"\bblackstone(?: s)? commentaries\b|\bblackstone .*\bcommentaries on the laws? of england\b")
_ED_BLK_BARE = re.compile(r"^(?:\d{1,2} )?commentaries on the laws? of england\b(?!.*\b(?:new|stephen|kent)\b)")
_ED_GAPW = r"[\W_]+(?:(?:of|the|and|on|in|&|a|an|to)[\W_]+)*"


def _ed_toks(k):
    t = _ED_PIN.sub("", k.replace("_", " ").strip()).split()
    while t and t[0] in _ED_LEAD:
        t = t[1:]
    return t


def _ed_content(k):
    """the key's author and title words: no year, edition, imprint, connector, initial, editor"""
    s = " ".join(_ed_toks(k))
    s = re.sub(r"(?:\b[a-z]{1,2}\.?\s+){0,3}[a-z][a-z'\-]+\s+(?:gen|eds?)\.?(?=\s|$)", " ", s)
    out = []
    for w in s.split():
        w = w.strip(".,:;()")
        if (not w or w in _ED_STOP or w in _ED_EDW or w in _ED_IMPRINT or w in _ED_ORDW
                or w in ("no", "no.", "report") or _ED_YEAR.match(w) or _ED_ORD.match(w)
                or re.fullmatch(r"\d+|[a-z]\.?|[a-z]\.[a-z]\.?", w)):
            continue
        out.append(w)
    return out


def _ed_years(k):
    return {w for w in k.replace("_", " ").split() if _ED_YEAR.match(w)}


def _ed_eponym(k):
    """(names, name, title words) for `<names> <name>'s <title>` / `<names> <name> on <title>`"""
    t = " ".join(_ed_toks(k))
    m = _ED_EPON.search(t + " ")
    if not m or m.group(1) in _ED_EPON_NOT:
        return None
    names = [w for w in t[:m.start(1)].split() if len(w.strip(".")) >= 3 and not _ED_YEAR.match(w)]
    title = _ed_content(t[m.end():])
    if len(names) > 4 or not title:
        return None
    return names + [m.group(1)], m.group(1), title


def _ed_journalish(k):
    """a volume or page beside the year (an edition `35 th` and a paper `no 7` are not)"""
    s = re.sub(r"\b\d{1,3} ?(?:th|st|nd|rd|d)\b|\bno\.? ?\d+\b", " ", " ".join(_ed_toks(k)))
    return any(re.fullmatch(r"\d+", w) and not _ED_YEAR.match(w) for w in s.split())


def _ed_numbers(k):
    """paper numbers: `report no 7`, `seventh report`"""
    s = " ".join(_ed_toks(k))
    out = set(re.findall(r"\bno\.? ?(\d+)\b", s))
    out |= {_ED_ORDW[w] for w in re.findall(r"\b(" + "|".join(_ED_ORDW) + r") (?:interim |final )?report\b", s)}
    return out


def _ed_d1(a, b):
    ea, eb = _ed_eponym(a), _ed_eponym(b)
    if not ea and not eb:
        return False
    if ea and eb:
        if not (ea[1] in eb[0] or eb[1] in ea[0]):
            return False
        sa, sb = set(ea[2]), set(eb[2])
        if sa == sb:
            return True
        small, big = (sa, sb) if len(sa) < len(sb) else (sb, sa)
        return small < big and (big - small) <= _ED_FILLER
    if _ed_journalish(a) or _ed_journalish(b):
        return False
    e, o = (ea, b) if ea else (eb, a)
    ot = _ed_toks(o)
    if not ot or (ot[0] != e[1] and not (len(ot) > 1 and ot[0] in e[0] and ot[1] == e[1])):
        return False
    oc = [w for w in _ed_content(o) if w not in e[0]]
    return set(oc) == set(e[2]) and len(oc) >= 2


def _ed_d3(a, b):
    ya = _ed_years(a)
    if not ya or ya != _ed_years(b) or _ed_journalish(a) or _ed_journalish(b):
        return False
    ca, cb = set(_ed_content(a)), set(_ed_content(b))
    small, big = (ca, cb) if len(ca) <= len(cb) else (cb, ca)
    if len(small) < 4 or not small <= big:
        return False
    na, nb = _ed_numbers(a), _ed_numbers(b)
    return not (na and nb and not (na & nb))


def _ed_d4(a, b):
    if _ed_journalish(a) or _ed_journalish(b):
        return False
    for k in (a, b):
        tk = _ed_toks(k)
        if "in" in tk or "—" in k or sum(1 for w in tk if w in _ED_FR) >= 2:
            return False
    ca, cb = _ed_content(a), _ed_content(b)
    ra, rb = _ed_toks(a), _ed_toks(b)
    if not ca or not cb or len(ra) < 2 or len(rb) < 2:
        return False
    if not ((ra[0] == rb[0] and len(ra[0]) >= 4 and ra[0] == ca[0])
            or (ra[1] == rb[1] and len(ra[1]) >= 4 and ra[0][0] == rb[0][0]
                and (re.fullmatch(r"[a-z]\.", ra[0]) or re.fullmatch(r"[a-z]\.", rb[0])))):
        return False
    n = 0
    while n < min(len(ca), len(cb)) and ca[-1 - n] == cb[-1 - n]:
        n += 1
    return 3 <= n < min(len(ca), len(cb)) and len(ca) - n <= 8 and len(cb) - n <= 8


def _ed_wre(w):
    return r"\b" + re.escape(w).replace(r"\-", r"[\-‐‑–]") + r"\b"


def _ed_d5(k, o, work, cache):
    tk = _ed_toks(k)
    if not 2 <= len(tk) <= 5 or any(re.search(r"\d", w) or len(w) < 3 for w in tk):
        return False
    co = [w for w in _ed_content(o) if w not in tk and len(w) >= 3]
    if not co or (len(co) < 2 and not _ed_eponym(o)):
        return False
    if (k, o) not in cache:
        kp = r"[^;()\[\]\n]{0,40}?".join(_ed_wre(w) for w in tk)
        op = _ED_GAPW.join(_ed_wre(w) for w in co[:2])
        try:
            cache[(k, o)] = bool(re.search(
                r"(?i)(?:" + kp + r"(?:['’]s?\s+|\s+on\s+|[\s,.:–—\-]{1,5})" + op
                + r"|" + op + r"[^;\n]{0,40}?\bby\s+[^;()\n]{0,12}?" + kp + r")", work))
        except re.error:
            cache[(k, o)] = False
    return cache[(k, o)]


def _ed_d6(k, o, work):
    eo = _ed_eponym(o)
    yo = _ed_years(o)
    if not eo or not yo or _ed_journalish(k):
        return False
    ck = _ed_content(k)
    if eo[1] in ck or len(ck) < 3 or not set(eo[2]) <= set(ck):
        return False
    for m in re.finditer(r"(?i)" + _ED_GAPW.join(_ed_wre(w) for w in ck[:3]), work):
        if re.search(r"\b" + re.escape(eo[1]) + r"\b", work[max(0, m.start() - 40):m.start()], re.I) \
                and any(y in work[m.end():m.end() + 60] for y in yo):
            return True
    return False


def _ed_d7(k, o, work):
    if _ed_journalish(k) or _ed_journalish(o):
        return False
    ck, co = _ed_content(k), _ed_content(o)
    if len(ck) < 3 or len(co) != len(ck) + 1:
        return False
    diff = [(p, q) for p, q in zip(ck, co[1:]) if p != q]
    if len(diff) != 1:
        return False
    p, q = diff[0]
    if len(p) != len(q) or len(p) < 4 or sum(1 for x, y in zip(p, q) if x != y) != 1:
        return False
    return bool(re.search(r"(?i)" + _ed_wre(co[0]) + r"[\s,]{1,3}(?:the\s+)?"
                          + _ED_GAPW.join(_ed_wre(w) for w in ck), work))


def _acad_ed_merge(distinct, work):
    """`distinct` with the second key of one book (rule 7) taken out; see the note above."""
    keys, dead, cache = list(distinct), set(), {}
    bl = [k for k in keys if _ED_BLK.search(k) and not re.search(r"\bnew commentaries|\bstephen\b|criminal practice", k)]
    if bl:
        fam = bl + [k for k in keys if _ED_BLK_BARE.match(k) and k not in bl]
        if len(fam) > 1:
            keep = max(fam, key=lambda k: (len(_ed_content(k)), len(k), k))
            dead |= {k for k in fam if k != keep}                                              
    for k in keys:
        if k in dead:
            continue
        for o in keys:
            if o != k and o not in dead and (_ed_d5(k, o, work, cache) or _ed_d6(k, o, work)
                                             or _ed_d7(k, o, work)):
                dead.add(k)                                                                          
                break
    order = sorted(keys, key=lambda k: (len(_ed_content(k)), len(k), k), reverse=True)
    for i, o in enumerate(order):
        if o in dead:
            continue
        for k in order[i + 1:]:
            if k not in dead and (_ed_d1(o, k) or _ed_d3(o, k) or _ed_d4(o, k)):
                dead.add(k)                                                                          
    if dead and len(dead) < len(keys):
        return [k for k in keys if k not in dead]
    return keys


                                                                                                   
                                                                                                   
                                                                                                     
                                                                                                     
                                                                                                           
                                                                                                        
                                                                                                    
                                                                                                 
                                                                 
                                                                                                      
                                                                                   
                                                                                                      
                                                                                                    
                                                                                                
                                                                                                
                                                                                                  
                                                                                              
                              
LS_FAM = os.environ.get("JR_LS_FAM", "1") != "0"
_LS_FAMILIES = (
    lambda k: "conflict of laws" in k and "morris" in k and ("dicey" in k or "collins" in k) and "F1",
    lambda k: "jacobs law of trusts" in k and "F2",
    lambda k: "markesinis" in k and "german law of torts" in k and "F3",
                                                                                                      
                                                                                               
    lambda k: "maitland" in k and "equity" in k and "F4",
                                                                                                         
                                                                                                     
                                                         
    lambda k: re.match(r"(?:\d+ )?goff (?:and |& )?jones\b", k) and "burrows" not in k
    and ("restitution" in k or "unjust enrichment" in k) and "F6",
)
_LS_DICEY_NEED_NOW = os.environ.get("JR_LS_DICEY_NOW", "0") == "1"
_LS_EDITOR = re.compile(r"\bthe editor of the (?:[a-z0-9]+ ){1,2}of ([a-z][a-z\-]{2,}) ")
_LS_DICEY_NOW = re.compile(r"\bDicey\s*(?:&|and)\s*Morris\b[^;]{0,80}\(\s*now\s+Dicey,\s+Morris\s*(?:&|and)\s*Collins\b")


def _ls_fam_merge(distinct, work):
    keys, dead = list(distinct), set()
    for fam in _LS_FAMILIES:
        mem = [k for k in keys if fam(k)]
                                                                                                      
                                                                                                   
                                                           
        if fam is _LS_FAMILIES[0] and _LS_DICEY_NEED_NOW and not (
                any("dicey" in k for k in mem) and _LS_DICEY_NOW.search(work)):
            continue
        if len(mem) > 1:
            keep = max(mem, key=lambda k: (len(_ed_content(k)), len(k), k))
            dead |= {k for k in mem if k != keep}
    for k in keys:                                                                             
        m = _LS_EDITOR.search(k)
        if m and k not in dead and any(o != k and o not in dead and re.match(r"(?:\d+ )?" + re.escape(m.group(1)) + r"\b", o)
                                       for o in keys):
            dead.add(k)
    if dead and len(dead) < len(keys):
        return [k for k in keys if k not in dead]
    return keys


                                                                                      
                                                                                                   
                                                                                                       
                                                                                                    
                                                 
                                                                                                  
                                                                                                       
                                                                                                 
                                              
                                
LS_SHORT = os.environ.get("JR_LS_SHORT", "1") != "0"
_LS_BARE_JNL = re.compile(r"(\d{1,4}) ([a-z][a-z.&' ]{1,40}?) (\d{1,5})")


def _ls_short_merge(distinct, work):
    keys, dead = list(distinct), set()
    for k in keys:
        m = _LS_BARE_JNL.fullmatch(k.strip())
        if not m:
            continue
        for o in keys:
            mo = re.search(r"([a-z][a-z'\-]+)\W* ([a-z][a-z'\-]+)\W* " + re.escape(m.group(1) + " " + m.group(2)) + r" \d", o)
                                                                                                         
                                                                                                     
                                                                                                       
                                                    
            if o != k and o not in dead and mo and re.search(
                    r"(?i)" + _ed_wre(mo.group(1)) + r"\W+" + _ed_wre(mo.group(2)) + r"\W+" + re.escape(m.group(1))
                    + r"\b[^;\d]{0,30}" + re.escape(m.group(3)) + r"\b", work):
                dead.add(k)                                                                    
                break
    for k in keys:
        if k in dead:
            continue
        tk = _ed_toks(k)
        if not 2 <= len(tk) <= 4 or any(not re.fullmatch(r"[a-z][a-z'\-]{2,}", w) for w in tk if w not in ("and", "&")) \
                or not re.search(r"\s+at\s+(?:pp?\.?\s*)?\d", k):
            continue
        names = [w for w in tk if w not in ("and", "&")]
        kp = r"[^;()\[\]\n]{0,40}?".join(_ed_wre(w) for w in names)
        if not re.search(r"(?i)" + kp + r"\s*,?\s*supra\b", work):
            continue
        for o in keys:
            if o == k or o in dead or not _ed_years(o):
                continue
            co = [w for w in _ed_content(o) if w not in names and len(w) >= 3]
            if len(co) < 2 or any(w in _ed_content(o) for w in names):
                continue
            op = _ED_GAPW.join(_ed_wre(w) for w in co[:2])
            if re.search(r"(?is)" + kp + r".{0,500}?" + op, work):
                dead.add(k)                                                                    
                break
    if dead and len(dead) < len(keys):
        return [k for k in keys if k not in dead]
    return keys


                                                                                                      
                                                                                                   
                                                                            
                                                                                                        
                                                                                                       
                                                                                                     
                                                                                                       
                                     
                                                                                                      
                                                                                                 
                            
                               
LS_DROP = os.environ.get("JR_LS_DROP", "1") != "0"
_LS_NEWS = re.compile(
    r"(?:[A-Z]\.\s?){1,2}[A-Z][A-Za-z'’\-]+,\s+[A-Z][^\d()“”\"]{5,120}?\s+"
    r"\((?:Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s+(?:19|20)\d\d\)")
_LS_BODY_BEFORE = re.compile(
    r"\b(?:Institute|Foundation|Center|Centre|Council|Association|Society|University|Commission|Committee|"
    r"Department|Bureau|Office|Agency|Service|League|Union|Organi[sz]ation)\s*,\s*$")


def _ls_drop(work, s, e, ts, pre):
    if re.search(r"\bbrought\s+out\s+(?:[a-z]+\s+){0,3}editions?\s+of\s+$", pre):
        return True                                                                            
    if _LS_NEWS.fullmatch(ts) and re.match(r"\s*\((?:describing|reporting|noting|recounting)\b", work[e:e + 40]) \
            and not _LS_BODY_BEFORE.search(pre) and not re.search(r"https?://|www\.", work[e:e + 330].split(";")[0]):
        return True                                                                            
    if re.search(r"\bJournals\s+of\s+the\s+Continental\s+Congress\b", ts) or re.search(
            r"\bJournals\s+of\s+the\s+Continental\s+Congress\s+\d{1,4}\s*\(\s*(?:[A-Z]\.\s?)*$", pre):
        return True                                                                            
    return False


def _acad_fp_drop(work, s, e, ts, pre, cache):
    """True where the match is one of the ACAD_FP not-a-work forms (see the notes above)."""
    if _FP_RECORDS.search(ts):
        return True
                                                                                                     
                                                                 
    if re.match(r"Archives\s+\d", ts) and re.search(r"\bMd\.\s*$", pre):
        return True
                                                                                                 
    if re.fullmatch(r"(?:the\s+)?House\s+and\s+Senate\s+Conferees", ts):
        return True
                                                                                                  
                                                                                       
    if re.match(r"its\s+(?:(?:Final|Interim|First|Second|Third)\s+)?Report\b", ts):
        if _ZF_R20_BODY.search(pre) and not (_LAW_REFORM_BODY.search(pre) or _ZF_R20_NOT.search(pre)):
            return True
                                                                                                      
                                                                                  
    if re.match(r"(?:the\s+)?Exercise\s+of\s+the\s+Royal\s+Prerogative\s+of\s+Mercy\b", ts) \
            and re.search(r"\bPetitions?\s+for\s+$", pre):
        return True
                                                                                                      
    if re.match(r"Headquarters,\s+[A-Z]", ts) and re.search(r"\bDiary,\s*$", pre):
        return True
                                                                                                     
    if re.fullmatch(r"(?:U\.?\s?S\.?\s+)?Customs\s+and\s+Border\s+Protection", ts):
        return True
    _m = _FP_SHORT_REPORT.fullmatch(ts)
    if _m:
        _k = "\x02" + _m.group(1)
        if _k not in cache:
            _hit = False
            for _d in re.finditer(r"\(\s*[“\"](?:the\s+)?" + re.escape(_m.group(1)) + r"[”\"]\s*\)", work):
                _w = work[max(0, _d.start() - 300):_d.start()]
                if _ZF_R20_BODY.search(_w) and not (_LAW_REFORM_BODY.search(_w) or _ZF_R20_NOT.search(_w)):
                    _hit = True
                    break
            cache[_k] = _hit
        if cache[_k]:
            return True
    _cut = len(pre[-45:])
    for _a in _FP_ASSOC.finditer(pre[-45:] + ts):
        if _a.start() <= _cut < _a.end():
            return True
                                                                                                     
                              
    if re.search(r"\bKiplinger['’]s\s+(?:[A-Z][a-z]+\s+){0,2}$", pre):
        return True
                                                                                                         
                                         
    if re.search(r"\bpublisher\s+of\s+(?:a|the)\s+book\b", pre):
        return True
    if _FP_LITERARY.search(ts) or _FP_FOREIGN_CASE.search(ts) or _FP_PROSE_EDITION.match(ts):
        return True
                                                                                               
                                                          
    if ts.startswith("Edition") and re.search(r"\bStandard\s+Form\s+of\s+Building\s+Contract\b", pre):
        return True
                                                                                                    
    if re.fullmatch(r"(?:the\s+)?[A-Z]{2,6}\s+Members['’]?\s+Handbook", ts):
        return True
                                                                                                       
                                
    if re.fullmatch(r"[A-Z][a-z]+(?:,\s+[A-Z][a-z]+)*,?\s+(?:and|&)\s+[A-Z][a-z]+\d{1,2}", ts):
        return True
                                                                                                         
    if ts.startswith("Martial") and re.search(r"\bCourts?-\s*$", pre):
        return True
                                                         
    if re.match(r"[A-Z][a-z]+s['’]\s+Group\b", ts):
        return True
                                                                                                    
    if re.search(r"\b(?:slogan|motto|catchphrase)\s+$", pre):
        return True
                                                                                             
                                                                                                  
                                                                         
    _b = re.match(r"the\s+[A-Z][^\d“”\"]*\sby\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})$", ts)
    if _b and re.search(r"\bby\s+" + re.escape(_b.group(1)) + r"\b", pre):
        return True
                                                                                                   
                                                                                                
                                                                                                       
                                                                                                       
                                                                                                         
                                                                    
    if _FP_GOV_TITLE.search(ts):
        return True
                                                                                                     
                                         
    if re.match(r"[A-Z][a-z]+\s*\(\s*Technical\s+Paper\b", ts):
        return True
                                                                                               
    if re.fullmatch(r"Crim\.?\s?L\.?\s?R\.?|Criminal\s+Law\s+Review", ts) and re.search(
            r"\[(?:19|20)\d\d\]\s+(?:EWCA|EWHC|UKHL|UKSC|UKPC)\s+(?:Crim|Civ|Admin)?\s*\d{1,4}\s*;\s*\[(?:19|20)\d\d\]\s*$", pre):
        return True
                                                                                          
                                                                         
    if re.fullmatch(r"[A-Z][A-Z'’\-]+", ts) and re.search(r"\bBETWEEN\s+(?:[A-Z][A-Z'’\-]*\s+){1,4}$", pre):
        return True
    return False


def _zf_round2(work, s, e, t, ts, ij, vouched, cache, pre, after, quoted, trimmed):
    """None to drop the match, (s, e, t) to re-read it from a new start, True to leave it."""
                                                                                                          
                                                                                                      
    if not ENCYCLOPAEDIAS_IN and ("Stair Memorial Encyclopaedia" in ts
                                  or re.match(r"\s*[,:]?\s*Stair\s+Memorial\s+Encyclopaedia", after)):
        return None
                                                                                                    
    if re.search(r"(?i)\b(?:lexicon|dictionar\w*|thesaurus)\b", ts) and not quoted and not re.search(r",\s+in\s", ts):
        return None
                                                                                                  
                                                                                           
                                                         
    _jc = bool(ij and (re.search(r"\d\s*$", ts) or _ZF_ABBREV_ONLY.match(ts)) and not re.search(r"\bHL\s+Paper\b", ts))
    if not _jc and _zf_official(work[max(0, s - 240):s], ts, after, quoted):
        return None
    if re.search(r"\b(?:[Dd]epartment|[Mm]inistry)['’]s\s+$", pre) or re.match(r"(?:the\s+)?(?:[Dd]epartment|[Mm]inistry)['’]s\s", ts):
        return None                                                                                                         
    if re.search(r"\bAJHR\b", ts):
        return None                                                                                             
                                                                                             
                                                                                                  
                                                                                                    
    _aft = work[e:e + 110]
    _mb = re.match(r"\)?\s*,?\s*(?:by\s+(?:the\s+)?)?", _aft)
    if _mb and _mb.end() > 0 and _ZF_R20_BODY.match(_aft[_mb.end():]) and not _ZF_R20_NOT.search(_aft[:90]) \
            and not _LAW_REFORM_BODY.search(_aft[:90]):
        if re.match(r"\)?\s*,?\s*by\s", _aft) or (
                not re.search(r"\d", ts) and re.fullmatch(r"[A-Z][A-Za-z'’\-]+(?:\s+(?:and\s+|&\s+)?[A-Z][A-Za-z'’\-]+){1,4}", ts)):
            return None
    if ij:
        if (re.fullmatch(r"[A-Z][A-Za-z]{1,7}", ts) and sum(c.isupper() for c in ts) >= 2
                and (_ZF_CASE_NAME_TIGHT.search(pre) or _ZF_CASE_LIST_BEFORE.search(pre))):
            return None
        if _ZF_HYBRID.match(ts) and e - s > len(ts) + 4:
                                                                                                  
                                                                                        
            _k = "\x01" + work[s:e]
            if _k not in cache:
                cache[_k] = bool(re.search(r"\sv\.?\s+[A-Z][^.;()“”\"]{0,45}" + re.escape(work[s:e]), work))
            if cache[_k]:
                return None
        if re.fullmatch(r"\d{1,3}\s+Journal(?:\s+of)?", ts):
            return None                                                                                   
        if re.match(r"\s+(?:Division|Committee|Board|Unit|Branch)\b", after):
            return None                                                                                                   
        return True
    if len(ts.split()) == 1 and _ZF_NAMES_ONLY.match(ts):
                                                                                           
        if re.search(r"(?:\b(?:Mr|Mrs|Ms|Miss|Messrs)\.?|\bnamed)\s+(?:[A-Z]{1,3}\s+)?$", pre):
            return None
    if ts == "American Law Institute":
                                                                                                       
        _ma = re.match(r"\s?['’]s\s+Restatement[^.;,]{0,60}?\((?:1[6-9]|20)\d\d\)", work[e:e + 90])
        if _ma and not trimmed:
            return s, e + _ma.end(), work[s:e + _ma.end()]
        if not _ma and not re.match(r"\s*,\s*[“\"]?[A-Z]", after):
            return None                                                                              
    if re.search(r"\bResponse\s+to\s+$", pre) or re.search(r"\bMinistry\s+of\s+[A-Z][a-z]+,\s+$", pre):
        return None
    if _ZF_ENDS_YEAR.search(ts) and re.match(r"\)?,\s+a\s+(?:decision|judgment)\s+of\b", after):
        return None                                                                                   
                                                                                               
    if _ZF_DAY_PAREN.search(ts) and _ZF_NEWS_URL.search(work[e:e + 330].split(";")[0]):
        return None
    if trimmed or vouched or work[s:e] != t:
        return True
    for _rx in _ZF_LEAD_WIDEN:
        _m = _rx.search(pre)
        if _m and _m.end() == len(pre) and _m.end() > _m.start() and len(ts.split()) >= 3:
            _ns = s - (len(pre) - _m.start())
            return _ns, e, work[_ns:e]
    _m = None
    if re.match(r"[A-Z][a-z]+['’]s\s+[A-Z]", ts):
        _m = _ZF_POSS_NAMES_BEFORE.search(pre)
    elif re.match(r"[A-Z][a-z]+:\s+[A-Z]", ts):
        _m = _ZF_COLON_AUTHORS_BEFORE.search(pre)
    if _m and _m.end() == len(pre):
        _ns = s - (len(pre) - _m.start())
        return _ns, e, work[_ns:e]
    if quoted:
        _q = None
        for _q in _ZF_QUOTE_END.finditer(t):
            pass
        if _q is not None:
            _rest = t[_q.end():]
            _mm = _US_EDITED_WORK.match(_rest) or _US_BLUEBOOK_BOOK.match(_rest)
            if _mm and _mm.end() >= len(_rest.rstrip()) - 1:
                return s + _q.end(), e, _rest
    return True


def _zf_fix(work, s, e, t, ij, vouched, cache, _trimmed=False):
    """None where the match is one of the adjudicated not-a-work forms; else (s, e, t), with a
    sentence lead-in trimmed off the front where the file prints one."""
    ts = re.sub(r"\s+", " ", str(t or "")).strip()
    if not ts:
        return s, e, t
    if not ij and not vouched and not _trimmed and work[s:e] == t:
        _cut = _zf_trim(t)
        if _cut:
            return _zf_fix(work, s + _cut, e, t[_cut:], ij, vouched, cache, True)
                                                                                                 
                                                                                            
    _base = re.sub(r",?\s+at\s+(?:pp?|paras?)\.?\s*\d+$", "", ts)
    if (1 < len(_base.split()) <= 6 and not re.search(r"\d", _base) and _zf_is_defined(work, _base, cache)
            and not re.match(r"[^.;]{0,50}?\((?:[^()]{0,40},\s*)?(?:1[6-9]|20)\d\d\)", work[e:e + 90])
                                                                                                          
                                                                                                       
                                                                           
            and not re.match(r"\s*\([^()]{0,80}?(?:\b[Ee]d\b|[Ee]dition|[Ll]oose-?leaf|Sweet|Maxwell|Brookers|"
                             r"Butterworths?|LexisNexis|Thomson|Lawbook|Federation|Press|Publishing|Publishers)",
                             work[e:e + 90])):
        return None
    after = work[e:e + 60]
    pre = work[max(0, s - 110):s]
                                                                                        
                                                                                              
                                                                                              
                                                                    
    if ij and len(str(t)) + 2 < e - s:
        _span = work[s:e]
        _at = _span.rfind(str(t))
        if _at >= 0:
            pre = pre + _span[:_at]
            after = _span[_at + len(str(t)):] + after
    quoted = any(c in ts for c in "“”\"")
    words = ts.split()
    if ACAD_FP and _acad_fp_drop(work, s, e, ts, pre, cache):
        return None                                                       
    if LS_DROP and _ls_drop(work, s, e, ts, pre):
        return None                                                  
    if ZF_ROUND2:
        _r2 = _zf_round2(work, s, e, t, ts, ij, vouched, cache, pre, after, quoted, _trimmed)
        if _r2 is None:
            return None
        if _r2 is not True:
            return _zf_fix(work, _r2[0], _r2[1], _r2[2], ij, vouched, cache, True)
                                                                                                  
                                                                                            
    if not any(c.isupper() for c in ts):
        return None
                                                                                               
                                                                                              
                                                                             
    if ts.startswith("restatement ") or re.match(r"[“\"]\s?[a-z]", ts):
        return None
                                                                             
                                                      
    if re.search(r"\[(?:19|20)\d\d\]\s+(?:UKSC|USKC|UKHL|UKPC|EWCA|EWHC|HCA|SGCA|SGHC|NZSC|NZCA|SCC|FCA|FCAFC)\s+\d{1,4}$", ts):
        return None
                                                                                          
    _mp = re.match(r"(.{4,60}?),?\s+at\s+pp?\.?\s*\d+$", ts)
    if _mp and not ij and _zf_is_party(work, _mp.group(1).strip(), cache):
        return None
    if _ZF_MONTH_LIST.match(ts):
        return None
    if ts.isupper() and len(words) >= 4 and _ZF_HEADING.search(ts):
        return None
    if _ZF_PROBATE.search(ts) or _ZF_REPORTER_POSS.match(ts) or _ZF_LEGISLATION.search(ts):
        return None
    if _ZF_NAMES_ONLY.match(ts):
        if _ZF_JUDGE_AFTER.match(after) or _ZF_AFTER_NOT_AUTHOR.match(after):
            return None
        if len(words) <= 4 and ("&" in ts or " and " in ts) and _ZF_FIRM_AFTER.match(after):
            return None
        if len(words) == 1:
            if _ZF_COUNSEL_BEFORE.search(pre):
                return None
            if _zf_is_party(work, ts, cache) and not _ZF_BARE_STRONG.match(after):
                return None
            _semi = work[e:e + 170].split(";")[0]
            if _NEWS_MASTHEAD.search(_semi):
                return None                                                                                          
    if ts == "Oliver Wendell Holmes" and not _ZF_HOLMES_OK.match(after):
        return None
    if len(words) <= 5 and not any(c.isdigit() for c in ts) and not quoted:
        if _ZF_BODY_BEFORE.search(pre) or _zf_party_before(pre):
            return None
    if ij:
        if _ZF_ABBREV_ONLY.match(ts) and not (_ZF_CITE_BEFORE.search(pre) or _ZF_CITE_AFTER.match(after)):
            return None
        if _ZF_HYBRID.match(ts) and (_ZF_CASE_NAME_BEFORE.search(pre) or _ZF_SLT_COURT_AFTER.match(after)):
            return None
        return s, e, t
    if vouched:
        return s, e, t
    if _ZF_ENDS_YEAR.search(ts):
        if _ZF_COMPANY_AFTER.match(after) or _ZF_YEAR_NOT_PUB.match(after) or _ZF_INSTRUMENT.search(ts):
            return None
        if re.search(r"\bCode\s+of\s+Practice\s+$", pre):
            return None                                                                           
                                                                                                  
    if re.search(r"(?:1[6-9]|20)\d\d$", ts) and re.match(r"\s{1,3}CanLII\s+\d", after):
        return None
    if _ZF_ENDS_YEAR.search(ts):
        if not quoted:
            for _rx in (_ZF_TAIL_PIN, _ZF_TAIL_AMP):
                _m = _rx.match(after)
                if _m and not _ZF_LOCATOR.match(_m.group(1).strip()):
                    _ab = _m.group(1).upper().replace(".", "").replace(" ", "")
                    if not (_ab in CARDIFF_ACAD_ABBREVS or _names_a_periodical(_m.group(1))):
                        return None
            if _ZF_TAIL_LR.match(after) or _ZF_HYPHEN_YEAR.search(ts) or _ZF_LAST_WORD_YEAR.search(ts):
                return None
    if not quoted:
                                                                                                  
                                                                                                  
                                                                                              
        if _ZF_CASE_IN.search(ts) or _ZF_US_CASE.search(ts):
            return None
        if _ZF_MEMO_BEFORE.search(pre):
            return None
                                                                                               
                                                                                             
                                                                                                  
                                                                                                
                                                                                          
                                                                             
                                                                                        
                                                                                           
                                                      
        _lc = _zf_lower_words(ts)
        if work[s:e] == t and (
                (len(_lc) >= 6 and len({w for w in _lc if w in _ZF_PROSE_WORD}) >= 2)
                or (ts[:1].islower() and len(_lc) >= 5 and re.search(r"[a-z]:\s+[A-Z]", ts))):
            if _trimmed:
                return None
            _lim = t.rfind("(")
            _cut = 0
            for _m in re.finditer(r"\S+", t[:_lim if _lim > 0 else len(t)]):
                _w = _m.group().strip(",.;:()'’\"“”")
                if _w[:1].islower() and _w not in _ZF_CONNECT and _w not in ("gen", "rev"):
                    _cut = _m.end()
            _rest = t[_cut:]
            _lead = len(_rest) - len(_rest.lstrip(" \t\r\n,;:—–-("))
            _mc = re.match(r"(?:(?:by|in|from|of|to|on|at|with|and)\s+)+", _rest[_lead:])
            if _mc:
                _lead += _mc.end()                                                              
            _rest = _rest[_lead:]
            if (len(re.findall(r"(?<![A-Za-z])[A-Z][A-Za-z'’\-]+", _rest[:_rest.rfind("(") if "(" in _rest else len(_rest)])) >= 2
                    and _ZF_HAS_DATE.search(_rest)):
                return _zf_fix(work, s + _cut + _lead, e, _rest, ij, vouched, cache, True)
            return None
    return s, e, t


                                                                                                 
                                                                                                  
                                                                                               
                                                                                 
                                                                                      
                                                                                             
                                                                                                
                                                                                            
                                                                                                      
                                                                                           
                                                                                                 
                                                                                         
                                                                                             
                                                                                                    
                                                                                                      
                                                                              
                                                                                                       
                                                          
                                                                                                              
                                                                                               
                                                                                               
_ZF_SK_DROP = frozenset(("th", "st", "nd", "rd", "see", "also", "cf", "eg", "rev", "gen", "al", "et", "ibid",
                         "supra", "de", "la", "le", "les", "du", "des", "en", "au", "aux", "dans", "sur"))
_ZF_IMPRINT_TAIL = frozenset((
    "sweet", "maxwell", "lexisnexis", "butterworths", "butterworth", "oxford", "cambridge", "university", "press",
    "hart", "publishing", "publishers", "thomson", "reuters", "carswell", "academy", "tottel", "kluwer", "routledge",
    "stevens", "sons", "informa", "lbc", "cch", "loose-leaf", "looseleaf"))
_ZF_GENERIC_FIRST = frozenset((
    "report", "reports", "restatement", "note", "notes", "comment", "papers", "works", "law", "laws", "journal",
    "review", "commentaries", "institute", "american", "australian", "canadian", "united", "new", "royal", "final",
    "interim", "national", "international", "commission", "committee", "department", "principles", "essays",
    "studies", "history", "treatise", "introduction", "handbook", "manual", "federalist", "records", "letter"))
_ZF_KEY_SUFFIX = re.compile(r"_\d*_\d*$")
_ZF_ARTICLE_TAIL = re.compile(r"((?:1[6-9]|20)\d\d (?:\d{1,3} )?[a-z][a-z0-9 .&']*? \d{1,4})$")
_ZF_CHAPTER_PIECE = re.compile(r"^(.{6,}?) in ([a-z][a-z'\-]+(?: [a-z][a-z'\-]+){0,3})(?: eds?\.?)?$")


_ZF_SKEL_MEMO = {}


def _zf_skel(k):
    if k not in _ZF_SKEL_MEMO:
        if len(_ZF_SKEL_MEMO) > 20000:
            _ZF_SKEL_MEMO.clear()
        _ZF_SKEL_MEMO[k] = _zf_skel_raw(k)
    return _ZF_SKEL_MEMO[k]


def _zf_skel_raw(k):
    b = _ZF_KEY_SUFFIX.sub("", k)
    toks = b.split()
    for i, w in enumerate(toks[:5]):
        if w in ("eds", "eds.", "ed", "ed."):
            b = " ".join(toks[i + 1:])                                                              
            break
    w = [x for x in _skeleton(b) if x not in _ZF_SK_DROP]
    while len(w) > 2 and w[-1] in _ZF_IMPRINT_TAIL:
        w.pop()
                                                                                                  
                                                                                                    
    return [x[:-1] if len(x) > 3 and x.endswith("s") and not x.endswith("ss") else x for x in w]


def _zf_one_work(a, b, keys):
    """True where keys `a` and `b` name one work (forms E1-E7 above)."""
    if ZF_ROUND2:
        for _x, _y in ((a, b), (b, a)):
                                                                                                   
                                                                                                
                                                                      
            _mj = re.match(r"^([a-z][a-z .&']+)_(\d{4})_(\d+)$", _x)
            if _mj and not re.match(r"^[a-z .&']+_\d*_\d*$", _y):
                _ty = re.findall(r"[a-z0-9]+", _y)
                if _mj.group(2) in _ty and _mj.group(3) in _ty:
                    _j = _mj.group(1)
                    _ab = {k for k, v in _JOURNAL_ABBREV_ALIASES.items() if v == _j} | {"".join(w[0] for w in _j.split())}
                    if _j in _y or any(k in _ty for k in _ab):
                        return True
                                                                                                      
                                                                                                       
            _ms = re.match(r"^([a-z][a-z'\-]+(?: [a-z][a-z'\-]+){1,3}) at pp?\.? \d+$", _x)
            if _ms:
                _it = iter(_skeleton(_y)[:8])
                if all(w in _it for w in _ms.group(1).split()) and len(_skeleton(_y)) >= 5:
                    return True
    ba, bb = _ZF_KEY_SUFFIX.sub("", a), _ZF_KEY_SUFFIX.sub("", b)
    ta, tb = _ZF_ARTICLE_TAIL.search(ba), _ZF_ARTICLE_TAIL.search(bb)
                                                                                              
                                                                                   
                                                  
    for _x, _y in ((ba, bb), (bb, ba)):
        _tx, _ty = _x.split(), _y.split()
        if len(_tx) >= 4 and re.fullmatch(r"(?:1[6-9]|20)\d\d", _tx[-1]) and len(_ty) > 3:
            for _k in range(min(len(_tx) - 1, len(_ty) - 1), 2, -1):
                if _tx[-_k:] == _ty[:_k] and len(_tx) - _k <= 4 and not re.search(r"\d", " ".join(_tx[:-1])):
                    return True
                                                                                                    
                                                                                                  
                                                    
    _va = re.match(r"^\d{1,3}[a-z]? ((?:[a-z][a-z':.\-]* ){3,10}?)\d", ba)
    _vb = re.match(r"^\d{1,3}[a-z]? ((?:[a-z][a-z':.\-]* ){3,10}?)\d", bb)
    if _va and _vb and "." not in _va.group(1) and "." not in _vb.group(1):
        _sa, _sb = _skeleton(_va.group(1)), _skeleton(_vb.group(1))
        _n = min(len(_sa), len(_sb))
        if _n >= 2 and _sa[:_n] == _sb[:_n] and _sa[0] not in ("law", "report", "reports", "harvard", "yale"):
            return True
    if ta and tb:
        if ta.group(1) == tb.group(1) and len(ta.group(1).split()) >= 3:                  
            return True
                                                                                              
                                                                                                    
        _pa, _pb = _skeleton(ba[:ta.start()]), _skeleton(bb[:tb.start()])
        return len(_pa) >= 4 and _pa == _pb and ta.group(1)[:4] == tb.group(1)[:4]
    if ta or tb or (ba != a and bb != b) or _VOL_JOURNAL_PAGE.match(a) or _VOL_JOURNAL_PAGE.match(b):
        return False
    if _journal_years(a) and _journal_years(b) and not (_journal_years(a) & _journal_years(b)):
        return False
    pa, pb = set(_PAPER_NO.findall(a)), set(_PAPER_NO.findall(b))
    if pa and pb and not (pa & pb):
        return False
                                                                                                  
                                                                               
    pa, pb = set(re.findall(r"\bvol\.? (\d{1,3})\b", a)), set(re.findall(r"\bvol\.? (\d{1,3})\b", b))
    if pa and pb and not (pa & pb):
        return False
    wa, wb = _zf_skel(a), _zf_skel(b)
    if not wa or not wb:
        return False
    if len(wb) > len(wa):
        wa, wb, ba, bb = wb, wa, bb, ba
                                                                                       
                                                                                                 
                                                                                              
    for _p, _o in ((ba, bb), (bb, ba)):
        mc = _ZF_CHAPTER_PIECE.match(_p)
                                                                                                 
                                                                                                
                                                                     
        if mc and not re.search(r"\d", _p) and (" " in mc.group(2) or re.search(r" eds?\.?$", _p)):
            _ed = mc.group(2)
            if (_o.startswith(_ed + " ") or _o.startswith(_ed + " eds ")) and len(_o.split()) >= len(_ed.split()) + 2 \
                    and not _ZF_CHAPTER_PIECE.match(_o):
                return True
    if wa[0] == wb[0] and wa[0] not in _ZF_GENERIC_FIRST and len(wa[0]) >= 3:
        if len(wb) == 1:
                                                                                           
                                                                                                
                                               
            if (len(wa) >= 3 and re.fullmatch(r"[a-z .']*?" + re.escape(wb[0]) + r"[ .\d]*", bb)
                    and re.search(r"\d", bb)):
                return sum(1 for k in keys if _zf_skel(k)[:1] == wb[:1]) == 2
            return False
                                                                                             
                                                                                            
                                                                                             
                                                                                             
                                                                   
        if len(wb) >= 3 and wa[-1] == wb[-1]:
            it = iter(wa)
            if all(x in it for x in wb):
                return True
                                                                                                 
                                                                                                  
                                                                                               
                                                                                             
                              
                                                                                     
    if " on " in bb and 2 <= len(wb) <= 3 and len(wa) <= len(wb) + 2 and wb[0] not in _ZF_GENERIC_FIRST:
        it = iter(wa)
        if all(x in it for x in wb):
            return True
                                                                                                
                                                                                             
                                                                                                
                                                                                   
    for i in range(min(4, len(wa))):
        for j in range(min(4, len(wb))):
            n = 0
            while i + n < len(wa) and j + n < len(wb) and wa[i + n] == wb[j + n]:
                n += 1
                                                                                                
                                                                         
                                                                                                
                                                                                                 
                                                                                                  
                                                                                                
                                                                                                   
            if (n >= 5 or (n >= 4 and (i == 0 or j == 0))) and min(i, j) <= 1 \
                    and (i + n == len(wa) or j + n == len(wb)):
                if len([x for x in wa[i:i + n] if x not in _ZF_GENERIC_FIRST]) >= 3:
                    return True
    return False


                                                                                                
                                                                                                
                                                                                
                                                                                                     
                                                                                
                                                                              
                                                                         
                                                                                                         
                                                                                                             
                                                                                                                     
                                                                                                        
                                                              
                                                                                
                                                                                                
                                                                             
                                                                                           
                                                                                             
                                                                                             
                                                                                                   
                                                                                             
STITCH = os.environ.get("JR_STITCH", "1") != "0"
_ZF_GAP_CONNECT = frozenset(("of", "the", "and", "in", "on", "to", "for", "a", "an", "at", "by", "with", "from",
                             "under", "de", "la", "du", "des", "et", "&", "ed", "eds", "edn", "gen", "rev", "vol",
                             "al", "th", "st", "nd", "rd", "s"))
_ZF_CHAPTER_HEAD = re.compile(
    r"\bin\s+[A-Z][A-Za-z'’\-]+(?:(?:\s*,\s*|\s+(?:and|&)\s+)[A-Z][A-Za-z'’\-]+){0,3}(?:\s+et\s+al\.?)?"
    r"\s*,?\s*\(?eds?\.?\)?\s*$")


def _zf_gap_ok(gap):
    """True where the text between two matches is title text only."""
    if len(gap) > 90 or any(c in gap for c in ";[]"):
        return False
    toks = gap.split()
    if len(toks) > 13:
        return False
    for tok in toks:
        core = tok.strip(",:'’\"“”()—–-")
        if not core or core.lower() in _ZF_GAP_CONNECT or re.fullmatch(r"\d{1,2}(?:st|nd|rd|th)?", core):
            continue
        if core in ("v", "v.") or (tok.endswith(".") and not re.fullmatch(r"[A-Z]\.", tok)):
            return False
        if core[:1].isupper() and re.fullmatch(r"[A-Za-z][A-Za-z'’\-]*", core):
            continue
        return False
    return True


def _zf_stitch(t1, gap, t2, j1, j2):
    """True where match `t1`, the text `gap` and match `t2` are one printed citation."""
    a = re.sub(r"\s+", " ", str(t1)).strip()
    b = re.sub(r"\s+", " ", str(t2)).strip()
    g = gap.strip()
    if ZF_ROUND2:
                                                                                        
                                                                                                 
        if (re.search(r"\[(?:19|20)\d\d\]\s*[A-Z][a-z]+[A-Za-z]*\s*\d{1,4}$", a)
                and (re.fullmatch(r";\s*\((?:19|20)\d\d\)\s*\d{1,3}(?:\(\d{1,2}\))?", g) or (g == ";" and j2))):
            return True
                                                                                              
                                                                         
                                                                                                                  
        if (j2 and re.search(r"(?:1[6-9]|20)\d\d\)?$", a) and len(a.split()) >= 4
                and (re.fullmatch(r"\)?,?\s*\d{1,3}(?::\d{1,3})?\s+[A-Z][a-z]{1,5}\.", g)
                     or re.fullmatch(r"\)?,?\s*[Vv]ol\.?\s*\d{1,3}\s*\.?\s*(?:The)?", g))):
            return True
                                                                                                                  
        if (re.fullmatch(r"\((?:after|from|since|now|formerly|previously|later)\b[^()]{0,45}", g)
                and _ZF_NAMES_ONLY.match(b)):
            return True
    if not _zf_gap_ok(gap):
        return False
    if ZF_ROUND2 and not (j1 and re.search(r"\d\s*$", a)):
                                                                                                 
                                                                                        
        if g in (", in", "in", ", reprinted in") and re.search(r"\beds?\.\s*(?:1[5-9]|20)\d\d\)$", b):
            return True
                                                                                            
        if re.match(r"\s*(?:on|of|upon)\s", gap) and re.search(r"['’]s\s+[A-Z][A-Za-z]+$", a):
            return True
                                                                                                                   
        if (not re.search(r"[)\d]$", a) and len(a.split()) >= 3
                and re.match(r"\(?\s*(?:Sweet\s*&\s*Maxwell|LexisNexis|Butterworths?|Oxford\s+University\s+Press|"
                             r"Cambridge\s+University\s+Press|Hart\s+Publishing|Thomson|Carswell|Academy\s+Publishing)\b", b)):
            return True
        if a == "American Law Institute" and g == "," and re.match(r"(?:Restatement|Principles|Model\s+Penal\s+Code)\b", b):
            return True
                                                                                                
                                                                                            
    j1 = bool(j1 and (re.search(r"\d\s*$", a) or _ZF_ABBREV_ONLY.match(a)))
    j2 = bool(j2 and (re.search(r"\d\s*$", b) or _ZF_ABBREV_ONLY.match(b)))
    if j1:
        return False
                                                                                                    
    if re.fullmatch(r"[A-Z][A-Za-z\-]+(?:\s+[A-Z][A-Za-z\-]+){1,2}", a) and re.match(r"['’]s?\s", gap):
        return True
    if _ZF_NAMES_ONLY.match(a) and len(a.split()) <= 5:
        if _ZF_NAMES_ONLY.match(b):
            return False                                                     
        if g in ("", ","):
            return False                                                                      
        if g in ("and", "&"):
            return bool(re.match(r"[A-Z][A-Za-z\-]+['’]s?\s", b))                                            
        return True
    if j2:
        return False
    if _ZF_CHAPTER_HEAD.search(a):
        return True
    if g == ":" or (ZF_ROUND2 and g.startswith(":") and not re.search(r"[)\d]$", a)):
                                                                                                                   
        return b[:1].isupper()
    if re.fullmatch(r",?\s*eds?\.?", g):
        return True
    return g.startswith("(") and ")" not in g and bool(_IMPRINT_PIECE.match(b))


def _zf_same_work(distinct, alias):
    """`distinct` with a second key for one work folded into the first (the fuller one is kept)."""
    order = sorted(distinct, key=lambda k: (len(_zf_skel(k)), len(k), k), reverse=True)
    kept = []
    for k in order:
        hit = next((o for o in kept if _zf_one_work(o, k, distinct)), None)
        if hit is None:
            kept.append(k)
        else:
            alias.setdefault(hit, set()).add(k)
    return [k for k in distinct if k in kept] if len(kept) < len(distinct) else distinct


                                                                             
                                                                                      
                                                                                           
                                                                                             
                                                                                            
                                                                                       
                                                                                             
                                                                                         
ACAD_MOD = os.environ.get("JR_ACAD_MOD", "1") != "0"
ACAD_MOD_BREAK = os.environ.get("JR_ACAD_MOD_BREAK", "1") != "0"                                    
                                                                                              
                                                                                                 
                                                                                                  
                                                                                                   
                                                                                                   
                                                 
_MOD_NBH = re.compile(r"(?<=\d)[‐‑](?=\d)|[‐‑](?=[A-Z])")
                                                                                              
                                
                                                                                               
                                                                                             
                                                                                               
                                                                                  
_MOD_MIDBREAK = re.compile(r"(?<=[a-z,])[ \t]*\n[ \t]*\n[ \t]*(?=[A-Za-z(])")
                                                                                                   
                                                                                                 
                                                                                                
                                          
_MOD_COLON_ISSUE = re.compile(
    r"(?<!\bThe )[“\"](?=[^”\"]*\s)[A-Z‘'][^”\"]{9,180}[”\"]\s*,?\s*"
    r"\((?:1[89]|20)\d\d(?:\s*[-–]\s*\d{2,4})?\)\s*,?\s*"
    r"\d{1,3}:\d{1,2}\s+[A-Z][A-Za-z.&'’ ]{1,50}?\s+\d{1,4}\b")
                                                                                               
                            
                                                                                                
                                                                             
                                                                                               
                                          
                                                                         
                                                                                 
                                                                                                
                                                                                               
                                          
_MOD_US_AUTH = r"(?:(?:[A-Z]\.\s*){1,3}|[A-Z]{1,3}\s+)?[A-Z][A-Za-z'’\-]{2,}"
_MOD_US_TITLE = r"[A-Z][A-Za-z0-9'’\-]*(?:[ ,;:\-–()]{1,3}[A-Za-z0-9'’]+){2,30}?"
_MOD_US_ARTICLE = re.compile(
    r"(?<![A-Za-z.])" + _MOD_US_AUTH + r"(?:\s*(?:&|and)\s*" + _MOD_US_AUTH + r")?"
    r",\s+(?P<t>" + _MOD_US_TITLE + r"),\s+"
    r"(?:(?P<v>\d{1,3})\s+(?P<j>[A-Z][A-Za-z.&'’ ]{1,50}?"
    r"(?:Pol['’]y|Prob\.|Hist\.|Com\.|Law\.|Change|Perspectives|Notes|Q\.))"
    r"|(?P<yv>(?:19|20)\d\d)\s+(?P<j2>[A-Z][A-Za-z.&'’ ]{1,50}?"
    r"(?:Rev\.|Review|L\.\s?J\.|LJ|J\.|L\.|Q\.|Pol['’]y)))"
    r"\s+(?P<pg>\d{1,4})(?:\s*,\s*\d{1,4}(?:\s*[-–]\s*\d{1,4})?){0,4}"
    r"(?:\s*\((?P<yr>(?:1[89]|20)\d\d)\))?")
                                                                                          
                                                                                             
       
                                                                                                    
                                                                                 
                                                                                               
                                          
                                                                                             
                                                                                         
_MOD_FN_BOOK = re.compile(
    r"(?:\[\d{1,4}\]\s+|;\s+|\b(?:[Ss]ee(?:\s+also|\s+generally)?|[Cc]f|[Cc]ompare|quoting|citing)\s+)"
    r"(?P<w>(?:von\s+)?[A-Z][a-z][A-Za-z'’\-]+(?:(?:,\s+|\s+and\s+)(?:von\s+)?[A-Z][a-z][A-Za-z'’\-]+){0,3},\s+"
    r"(?!(?:Ex\s+parte|Re|In\s+re)\b)"
    r"[A-Z][A-Za-z'’\-]*(?:(?:[ :,]{1,2}|\s+[-–]\s+)(?:[A-Za-z0-9'’\-]+|\([A-Z][A-Za-z ,'’]{2,40}\))){0,28}?"
    r"(?:,\s+\d{1,2}(?:st|nd|rd|th)\s+(?:Eng\s+)?ed)?"
    r"\s*\((?:1[5-9]\d\d|20[0-2]\d)\))"
    r"(?=\s*(?:at\s|[.,;)]|$))")
                                                                                                  
                                                     
                                                               
                                                       
                                                                      
                                                                                           
                                                                                        
_MOD_SCC_PAREN = re.compile(
    r"\(\s?(?P<w>[A-Z][A-Za-z'’\-]*(?:[ :,]{1,2}(?:[A-Za-z][A-Za-z'’\-]*|&|\d{1,4})){1,25}?"
    r"\s*\((?:(?:\d{1,2}(?:st|nd|rd|th)\s+ed\.?\s*)?(?:1[5-9]|20)\d\d|loose-?leaf|[^()]{0,25}\(loose-?leaf\))\))"
    r",?\s+at\s+(?:pp?\.|paras?\.|§)")
                                                                                                
                                                              
                                                                    
                                                        
                                                                                               
                                                                                    
_MOD_VOL_TITLE = re.compile(
    r"(?<![\w.,§])(?P<w>\d{1,2}\s+(?:The\s+)?[A-Z][a-z][A-Za-z'’\-]+(?:\s+(?:[A-Z][A-Za-z'’\-]+|of|the|and|on|in|to|for|de)){2,14}"
    r"\s+\d{1,4}(?:\s*[-–]\s*\d{1,4})?\s+\((?:1[5-9]|20)\d\d\))")
_MOD_VOL_NOT = re.compile(r"\b(?:Annals|Cong|Congress|Journals?|Statutes?|Laws|Acts|Debates|Proceedings|Register|Records?|"
                          r"Reports?|Session|Assembly|Parliament|Senate|House|Commons|Lords|Code|Opinions|Attorney)\b")


                                                                                        
                                                                                                
                                                                                          
                                                                                                
                                                                                  
                                                                                           
                                                                            
                                                                                              
                                                                                            
                                                                                                
                                                                                                
ACAD_MOD_V1 = os.environ.get("JR_ACAD_MOD_V1", "1") != "0"
_MOD_V1_TAIL = re.compile(r"\s*,?\s*\d{1,3}(?:[:(]\d{1,3}\)?)?\s+(?P<j>[A-Z][A-Za-z.&'’ ]{1,50}?)\s+\d{1,4}\b")
_MOD_V1_QUOTED = re.compile(r"[“\"][A-Z][^”\"]{9,200}[”\"]\s*,?\s*[\(\[](?:1[89]|20)\d\d(?:\s*[-–]\s*\d{2,4})?[\)\]]")


def _mod_journal_ok(j):
    j = (j or "").strip()
    return bool(j) and (j.upper().replace(".", "").replace(" ", "") in CARDIFF_ACAD_ABBREVS
                        or _names_a_periodical(j))


def _mod_full_article(work, e, t):
    t = str(t or "")
    for rx in (_US_ARTICLE_CITE, _US_ARTICLE_CITE_PIN, _MOD_US_ARTICLE):
        m = rx.match(t.strip())
        if m and m.end() >= len(t.strip()) - 2:
            return True
    q = _MOD_V1_QUOTED.search(t)
    if not q:
        return False
    rest = t[q.end():] + work[e:e + 120]
    m = _MOD_V1_TAIL.match(rest)
    return bool(m and _mod_journal_ok(m.group("j")))


                                                                                          
                                                                                                  
                                                                                                        
                                                                                                  
                                                                
                                                                                                  
                                                                                                      
_MOD_NOT_BOOK = re.compile(
    r"(?i)\b(?:report|rapport|commission|committee|comit[eé]|inquiry|enqu[eê]te|task\s+force|statement|budget|"
    r"department|ministry|minist[eè]re|government|gouvernement|agency|council|bureau|office|board|"
    r"hansard|debates?|proceedings|rules?|regulations?|guidelines?|directive|order)\b")
_MOD_DICT = re.compile(
    r"(?i)dictionar|dictionnaire|lexique|lexicon|\b(?:grand|petit)\s+robert\b|larousse|de\s+la\s+langue|thesaur|glossary|"
    r"\busage\b|word\s+finder")
_MOD_PROSE = re.compile(
    r"^(?:For|See|In|As|Also|Cf|Compare|Contra|E\.?g|Thus|But|And|The\s+court|This)\b|"
    r"\b(?:were|was|is|are|been|imposed|held|example|such\s+as|cited|quoted|which|that)\b")
                                                                                               
                                                                                    
_MOD_MPC = re.compile(r"\b(?:ALI|American\s+Law\s+Institute),\s+Model\s+Penal\s+Code\b")


def _mod_names_only(work, w):
    """`Maddaugh and McCamus` -- capitalised words joined by and/&, each printed elsewhere after
    an initial (`John D. McCamus`): authors, not a title."""
    ws = re.split(r"\s+(?:and|&)\s+|,\s+", w.strip())
    if len(ws) < 2 or not all(re.fullmatch(r"[A-Z][A-Za-z'’\-]+", x) for x in ws):
        return False
                                                                                                    
                                                                                                  
    if re.search(re.escape(w.strip()) + r",\s+at\s+(?:pp?\.|paras?\.|§)", work):
        return True
    return any(re.search(r"\b[A-Z]\.\s*" + re.escape(x) + r"\b", work) for x in ws[1:])


def _mod_book_ok(work, g):
    return not (_MOD_NOT_BOOK.search(g) or _MOD_DICT.search(g) or _mod_names_only(work, re.sub(r"\s*\(.*$", "", g)))


def _mod_matches(work, held):
    """ACAD_MOD's matches (s, e, text, is_b6, is_journal) over `work`, none overlapping `held`."""
    out = []

    def _free(s, e):
        return not any(s < he and hs < e for hs, he in held) and not any(s < oe and os_ < e for os_, oe, *_r in out)

    for m in _MOD_MPC.finditer(work):
        if _free(m.start(), m.end()):
            out.append((m.start(), m.end(), "ALI, Model Penal Code", False, False))

    for m in _MOD_COLON_ISSUE.finditer(work):
        if _free(m.start(), m.end()) and not _MOD_DICT.search(m.group()):
            out.append((m.start(), m.end(), m.group(), False, False))                                   
    for m in _MOD_US_ARTICLE.finditer(work):
        if re.search(r"\sv\.?\s", m.group("t")) or _MOD_DICT.search(m.group()):
            continue
        if m.group("v") and not m.group("yr"):
            continue                                                                                 
        s, e = m.start(), m.end("pg")
        txt = work[s:e] + (" (" + m.group("yr") + ")" if m.group("yr") else "")
        if _free(s, m.end()):
            out.append((s, m.end(), txt, False, False))
    for m in _MOD_FN_BOOK.finditer(work):
        g = m.group("w")
        if re.search(r"\sv\.?\s|\bAct\b|\bCh\b", g) or not _mod_book_ok(work, g) or _MOD_PROSE.search(g):
            continue
        if _free(m.start("w"), m.end("w")):
            out.append((m.start("w"), m.end("w"), g, False, False))
    for m in _MOD_SCC_PAREN.finditer(work):
        g = m.group("w")
        if re.search(r"\sv\.?\s|\bRe\b|\bAct\b|\bCode\b", g) or not _mod_book_ok(work, g) or _MOD_PROSE.search(g):
            continue
        if _free(m.start("w"), m.end("w")):
            out.append((m.start("w"), m.end("w"), g, False, False))
    for m in _MOD_VOL_TITLE.finditer(work):
        g = m.group("w")
        if _MOD_VOL_NOT.search(g) or not _mod_book_ok(work, g):
            continue
        if _free(m.start("w"), m.end("w")):
            out.append((m.start("w"), m.end("w"), g, False, False))
    return out


def academic_works(text, groups=False):
    """With groups=True, each work is returned as the SET OF NAMES it was found
    under -- the counterpart of jr_citations.groups(). Default behaviour is
    unchanged: a flat list of keys, which is what every current caller expects.
    """
                                                                                  

                                                                                             
                                                                                              
                                                                                               
                                                                                              
                                                                                      

                     
                                                                                    
                                                                                 
                                                                 
                                                   
                   
                                                                        
                  
                                                                        
                                                                                
                                                                                      
                                                                                   
                                                                                                 
                                                                                            
                                                                                                 
                                                                     
                                                                                           
                                                                            
       
                                                                                             
                                                                        
                                                                                                 
                                                                                              
                                                          
    text = _SPLIT_JOURNAL_CITE.sub(lambda m: m.group(1) + " ", text or "")
    if ACAD_MOD:                                                                     
        text = _MOD_NBH.sub("-", text)
        if ACAD_MOD_BREAK:
            text = _MOD_MIDBREAK.sub(lambda m: " " * len(m.group()), text)
                                                                                             
                                                                                                  
                                                                                               
                                         
    text = re.sub(r"(?<=[A-Za-z])`(?=s\b)", "'", text)
    text = _ordinal_editions(text)                                                        
    _raw = _normalize_dotted_abbrevs(text)
                                                                             
    work = _fold_diacritics(_raw)
    matches = []                             
    _n_journal = len(_JOURNAL_RE)
    for pi, p in enumerate(list(_JOURNAL_RE) + list(TREATISE_PATTERNS)
                           + list(_EXTRA_WORK_PATTERNS)):
        for m in p.finditer(_raw if pi < _n_journal else work):
            t = m.group()
            if _NUM_WORD_RE.match(t):
                continue
            if pi in _J3_PATTERN_INDICES and not _j3_has_context(work, m.start(), m.end()):
                continue                                                        
            if pi in _US_FORM_JOURNAL_INDICES and _TITLE_YEAR_BEFORE.search(
                    _raw[max(0, m.start() - 28):m.start()]):
                continue                                                               
            matches.append((m.start(), m.end(), t, False, True))                                
                                                                              
                                                                                 
                                                                          
                                                                                        
                                                                             
                                                                                    
                                                                                          
                                                     
                                                                            
                                                                                   
                                                                   
                                                                                    
    for m in _REPORT_AUSPICES.finditer(work):
        matches.append((m.start(), m.end(), m.group(), False, True))

    for m in _ARTICLE_SHORT_TITLE_CITE.finditer(work):
        _abbr = re.sub(r"[^A-Za-z]", "", m.group(4)).upper()
        if _abbr not in CARDIFF_ACAD_ABBREVS:
            continue                                                                         
        matches.append((m.start(), m.end(), m.group(), False, True))

    for m in _ARTICLE_TITLE_CITE.finditer(work):
                                                                             
                                                                                      
                                                             
                                                                                   
                                                                                    
                                                                                      
                                                                                       
                                                                                  
                                                                                         
                                                                                          
                                                                             
        _qh = _QUOTED_HEAD.match(m.group())
        if _qh and not _qh.group(1).isupper():
            continue
                                                                                             
                                                                    
                                                                                              
                                                                                       
                                                                                         
                                                                                           
                                                    
        _lr = _REPORT_PINPOINT_TAIL.search(m.group())
        if _lr and re.sub(r"[^A-Za-z]", "", _lr.group(1)).upper() not in CARDIFF_ACAD_ABBREVS:
            continue
        matches.append((m.start(), m.end(), m.group(), False, True))
                                                                                               
                                                                                                             
                                                                                                          
                                                                                                               
    for m in _ARTICLE_TITLE_CITE_SQ.finditer(work):
        _ser = m.group("ser")
        if not (re.sub(r"[^A-Za-z]", "", _ser).upper() in CARDIFF_ACAD_ABBREVS or _names_a_periodical(_ser)):
            continue
        matches.append((m.start(), m.end(), m.group(), False, True))

                                                                                           
                                                                             
                                                                                            
                                                                                          
                                                   
                                                            
                                                                
                                                    
    for m in _ARTICLE_SCIENCE_CITE.finditer(work):
        matches.append((m.start(), m.end(), m.group(), False, True))

                                                                                           
    for m in _ARTICLE_NOPAGE_CITE.finditer(work):
        matches.append((m.start(), m.end(), m.group(), False, True))

                                                                                      
    for m in _US_ARTICLE_CITE.finditer(work):
        if US_PIN and _US_ARTICLE_CITE_PIN.match(work, m.start()):
            continue                                                                 
        matches.append((m.start(), m.end(), m.group(), False, True))
                                                                                                
                                                                                                   
                                                                                              
                                                                                  
    _us_full = []
    if US_PIN:
        for m in _US_ARTICLE_CITE_PIN.finditer(work):
            matches.append((m.start(), m.end(),
                            work[m.start():m.end("pg")] + " (" + m.group("yr") + ")", False, True))
        _us_full = [(m.start(), m.end()) for _rx in (_US_ARTICLE_CITE, _US_ARTICLE_CITE_PIN)
                    for m in _rx.finditer(work)]

                                                                         
                                                                                              
     
                                                                               
                                                                                       
                                                                                        
                               
                                                                                     
                                        
                                                         
                                                                                
                                                                                           
                                                                                    
                                                                                      
                                                              
    for _rx in (_US_BLUEBOOK_BOOK, _US_EDITED_WORK):
        for m in _rx.finditer(work):
            if _OPINION_HEADER.search(m.group()):
                continue
            matches.append((m.start(), m.end(), m.group(), False, False))

                                                              
    if LOOSELEAF:
        for m in _LOOSELEAF_BOOK.finditer(work):
            matches.append((m.start(), m.end(), m.group(), False, False))

                                                                
    for m in _AUTHOR_OF_TITLE.finditer(work):
        matches.append((m.start(), m.end(), m.group(), False, False))

                                                                                            
                                                                       
    for m in _REFERENCE_WORK.finditer(work):
                                                                                      
                                                                                  
                                                                                        
                                                                                       
                                                                                   
        e = m.end()
        mv = _REF_VOLUME.match(work, e)
        if mv:
            e = mv.end()
        matches.append((m.start(), e, work[m.start():e], False, False))

                                                                                             
     
                                                                                          
                                                                                        
                                                                                      
                                                                                    
                                                                                              
                                                                                           
    for _rx in (_BOOK_EDITION, _POSSESSIVE_EDITION, _BOOK_PUBLISHER):
        for m in _rx.finditer(work):
            if _NOT_SCHOLARSHIP.search(m.group()):
                continue                                                                          
            if (_is_official_report(m.group()) or _GOVERNMENT_GUIDANCE.search(m.group())) \
                    and not (_authored_edition(m.group())
                             or _authored_article(m.group())):
                continue                                                         
            if _REFERENCE_WORK.search(m.group()):
                continue                                                           
            matches.append((m.start(), m.end(), m.group(), False, False))

                                                              
    for m in _TITLE_EDITION.finditer(work):
        g = m.group()
        if _NOT_SCHOLARSHIP.search(g) or _NOT_A_WORK.search(g) or _NAME_ON_CASE.search(g):
            continue
        if _REFERENCE_WORK.search(g):
            continue                                                               
        matches.append((m.start(), m.end(), g, False, False))

                                                          
    for m in _TITLE_PINPOINT.finditer(work):
        matches.append((m.start(), m.end(), m.group(), False, False))

                                                      
    for m in _CLASSICAL_WORK.finditer(work):
                                                                                                   
                                                                          
        if ZERO_FALSE and " " in m.group() and not re.search(r"\s[A-Z]", m.group()):
            continue
                                                                                                   
        if ZF_ROUND2 and re.fullmatch(r"(?i)the\s+federalist\s+papers", m.group()):
            matches.append((m.start(), m.end(), "The Federalist", False, False))
            continue
        matches.append((m.start(), m.end(), m.group(), False, False))

                                                        
    for m in _TITLE_YEAR_PINPOINT.finditer(work):
        g = m.group()
        if _NOT_SCHOLARSHIP.search(g) or _NOT_A_WORK.search(g) or _NAME_ON_CASE.search(g):
            continue
        if _REFERENCE_WORK.search(g):
            continue
        if _is_official_report(g) and not (_authored_edition(g) or _authored_article(g)):
            continue
        matches.append((m.start(), m.end(), g, False, False))

                                                                                 
    for m in _NAMED_KIND_OF_WORK.finditer(work):
        matches.append((m.start("t"), m.end("t"), m.group("t"), False, False))

                                                               
    for m in _CUE_TITLE.finditer(work):
        g = m.group(1).strip()
        if len(g) < 12 or _NOT_SCHOLARSHIP.search(g) or (_is_official_report(m.group())
                and not (_authored_edition(m.group()) or _authored_article(m.group()))):
            continue
        if _CUE_VERB.search(g):
            continue                                                      
        matches.append((m.start(), m.start() + len(g), g, False, False))

                                                                                    
                                                                                      
    for _rx in (_RESEARCH_QUOTED, _RESEARCH_BODY_YEAR):
        for m in _rx.finditer(work):
            g = m.group()
            if _NOT_SCHOLARSHIP.search(g) or _NAME_ON_CASE.search(g):
                continue
            if _is_official_report(g):
                continue                                                               
            matches.append((m.start(), m.end(), g, False, False))

                                                                    
    for m in _INVERTED_PUBLISHER.finditer(work):
        g = m.group()
        if _NOT_SCHOLARSHIP.search(g) or _NOT_A_WORK.search(g) or _NAME_ON_CASE.search(g):
            continue
        if _is_official_report(g) and not (_authored_edition(g) or _authored_article(g)):
            continue
        matches.append((m.start(), m.end(), g, False, False))

                                                             
    for m in _BARE_YEAR_BOOK.finditer(work):
        g = m.group()
        if _NAME_ON_CASE.search(g) or _NOT_SCHOLARSHIP.search(g) or (_is_official_report(g)
                                        and not (_authored_edition(g)
                                                 or _authored_article(g))):
            continue
        matches.append((m.start(), m.end(), g, False, False))

                                                               
    for m in _TITLE_BY_AUTHOR.finditer(work):
        g = m.group()
        if _NOT_SCHOLARSHIP.search(g) or _NOT_A_WORK.search(g) or _NAME_ON_CASE.search(g):
            continue
        if _is_official_report(g) and not (_authored_edition(g) or _authored_article(g)):
            continue
        matches.append((m.start(), m.end(), g, False, False))

                                                                       
    for m in _NAME_ON_SUBJECT.finditer(work):
        g = m.group()
        if _NAME_ON_CASE.search(g) or _NAME_ON_VERB.match(m.group(1)) or _NAME_ON_BODY.match(m.group(1)):
            continue
                                                                                               
                                                                                 
        if not m.group(1)[:1].isupper():
            continue
        if _NAME_ON_PROSE.search(g) or _NOT_SCHOLARSHIP.search(g) or (_is_official_report(g)
                                        and not (_authored_edition(g)
                                                 or _authored_article(g))):
            continue
        matches.append((m.start(), m.end(), g, False, False))

                                                                                        
                                                                                            
                                                                                          
                                                                                        
                                                            
     
                                                                                              
                                                                                             
                                                                                          
                                                                                             
                                                                                           
     
                                                                                        
                                                                                            
                                                                                           
                                                                                            
                                                                  
     
                                                                                            
                                                                                             
                                                                                        
                                                                                           
                                                                                           
     
                                                                                            
                                                                                                
                                                    
     
                                                                                             
                                                                                         
                                                                                              
                                                                                              
                                                                                         
                                                                    

                                                                                         
                                                                            
    if CARDIFF_ACAD_TITLES:
        for _re in (_FULLNAME_CITE, _FULLNAME_CITE_PRE):
            for m in _re.finditer(work):
                if _flat_title(m.group("j")) in CARDIFF_ACAD_TITLES:
                    matches.append((m.start(), m.end(), m.group(), False, True))
    if CARDIFF_ACAD_ABBREVS:
        for cite_re in (_CARDIFF_CITE_RE, _CARDIFF_CITE_NOVOL_RE):
            for m in cite_re.finditer(work):
                                                                                            
                                                                                             
                                                                                
                abbrev = m.group(1).upper().replace('.', '').replace(' ', '')
                                                                                          
                                                                                          
                                                     
                if (abbrev in CARDIFF_ACAD_ABBREVS
                        or _names_a_periodical(m.group(1))):
                                                                                         
                    matches.append((m.start(), m.end(), m.group(1), False, True))                   
                                                                                              
        for m in _UNQUOTED_ARTICLE_CITE.finditer(work):
            _ab = m.group("j").upper().replace(".", "").replace(" ", "")
                                                                                           
                                                                                             
                                                                           
            if (_ab in CARDIFF_ACAD_ABBREVS
                    or _names_a_periodical(m.group("j"))):
                matches.append((m.start(), m.end(), m.group(), False, True))
                                                                                            
        for m in _TITLED_JOURNAL_CITE.finditer(work):
            _ab = m.group("j").upper().replace(".", "").replace(" ", "")
            if (_ab in CARDIFF_ACAD_ABBREVS
                    or _names_a_periodical(m.group("j"))):
                matches.append((m.start(), m.end(), m.group(), False, True))
                                                                               
    _b6_start = len(_ACAD_BOOK_PATTERNS) - 3
    for pi, p in enumerate(_BOOK_RE):
        ib6 = (pi >= _b6_start)
        for m in p.finditer(work):
            _g, _st = m.group(), m.start()
                                                                                                                 
                                                                                                                  
                                                                                                             
                                                                                                                      
            if ("fho1" in p.groupindex and re.match(r"[A-Z][a-z]+,\s", _g)
                    and _FHO_EDITOR_BEFORE.search(work[max(0, _st - 30):_st])):
                _k = _g.index(",") + 1
                _k += len(_g[_k:]) - len(_g[_k:].lstrip())
                _st += _k
                _g = _g[_k:]
                                                                                                  
                                                                                                  
                                                                                    
            if ZERO_FALSE and pi in _LAW_OF_BOOK and not re.search(
                    r"[A-Z][A-Za-z]+(?:'s\s+|,\s+|\s+on\s+(?:the\s+)?)(?:The\s+)?Law\s+of\s+[A-Z]", _g):
                continue
                                                                    
            _cut = _SEE_CUE_CUT.search(_g)
            if _cut and len(_g) - _cut.end() >= 8:
                _st += _cut.end()
                _g = _g[_cut.end():]
                                                                        
            if _OPEN_YEAR_TAIL.search(_g) and _is_case_report_tail(work, m.end()):
                continue
            _en = m.end()
                                                                                                 
                                                                                                 
                                                                                             
                                                                                              
                                                                                    
            if RESTATEMENT_TRIM and _g.startswith("Restatement"):
                _mt = _RESTATEMENT_TITLE.match(work, _st)
                if _mt:
                    _g, _en = _mt.group(), _mt.end()
            matches.append((_st, _en, _g, ib6, False))                    
                                                                     
    for m in _PRACTICE_ANNUAL.finditer(work):
        matches.append((m.start(), m.end(), m.group(), False, False))
                                                                                          
                                                                                          
                                                                                               
                                                                                            
                                                                                                  
    _lc_seen = {}
    _lc_held = [(s_, e_) for s_, e_, _t, _b, _j in matches]
    for m in _LAW_COM_PAPER.finditer(work):
        if m.group("wp") and not _LAW_COM_NEAR.search(work[max(0, m.start() - 200):m.start()]):
            continue
        _bs = m.start("b")
        if any(e_ > _bs - 250 and s_ < m.end() + 40 for s_, e_ in _lc_held):
            continue
        if re.search(r"Law\s+Com(?:mission|\.)?(?:\s+Report)?\s*,?\s+[Nn]o\.?\s*\d{1,3}\s*(?:,|;|and)?\s*$",
                     work[max(0, _bs - 40):_bs]):
            continue
        _k = ("lccp" if m.group("n2") else (m.group("wp") or "report").lower(),
              m.group("n") or m.group("n2") or m.group("n3"))
        _txt = "Law Commission, %s(%s)" % ((m.group("q").strip() + " ") if m.group("q") else "",
                                           re.sub(r"\s+", " ", m.group("b")))
        if _k not in _lc_seen or (m.group("q") and not _lc_seen[_k][1]):
            _lc_seen[_k] = ((m.start(), m.end(), _txt, False, False), bool(m.group("q")))
    matches.extend(v[0] for v in _lc_seen.values())
                                                                                              
     
                                                                                           
                                                                                            
                                                                                              
                                                                                                
                                                                                              
                                                                                               
                                                                                               
                                                        
    _sf_vouched = set()                                                                            
                                                                                                
                                                                                                    
    _lr_vouched = set()
    if B23_LAW_REFORM:
        _lr_seen = set()
        for m in _LAW_REFORM_PAPER.finditer(work):
            _b = m.group("body")
            _bi = _b if _b.isupper() else "".join(w[0] for w in _b.split() if w[:1].isupper())
            _k = (_bi, m.group("kind").split()[-1].lower(), m.group("n"), m.group("y"))
            if _k in _lr_seen:
                continue
            _lr_seen.add(_k)
            matches[:] = [x for x in matches if not (x[0] >= m.start() and x[0] < m.end())]
            matches.append((m.start(), m.end(), m.group(), False, False))
            _sf_vouched.add((m.start(), m.end()))
            _lr_vouched.add((m.start(), m.end()))
                                                                                                                      
                                                                                                         
    if B24_LAW_REFORM_ORD:
        for _s, _e, _lab, _k in _law_reform_ord(work):
            if any(not (_e <= a or _s >= b) for a, b in _lr_vouched):
                continue
            matches[:] = [x for x in matches if not (x[0] >= _s and x[0] < _e)]
            matches.append((_s, _e, _lab, False, False))
            _sf_vouched.add((_s, _e))
            _lr_vouched.add((_s, _e))
    if B20_SHORT_FORM:
        _held = [(s_, e_) for s_, e_, _t, _b, _j in matches]
        _names = " ".join(_t for _s, _e, _t, _b, _j in matches).lower()
        for _s, _e, g, _title in _short_form_treatises(work):
            if _is_official_report(g) and not (_authored_edition(g) or _authored_article(g)
                                               or _title == "\x00full"):
                continue
            if _title == "\x00full":
                _sf_vouched.add((_s, _e))
                _title = "\x00supersede"
            if _title == "\x00supersede":
                                                                                      
                matches[:] = [x for x in matches if not (x[0] >= _s and x[0] < _e)]
                matches.append((_s, _e, g, False, False))
                continue
            if any(_s < e_ and s_ < _e for s_, e_ in _held):
                continue
            if _title:
                if re.sub(r"\s+", " ", _title).lower() in re.sub(r"\s+", " ", _names):
                    continue
            else:
                _sur = _SF_SURNAME.search(g)
                if _sur and re.search(r"\b" + re.escape(_sur.group(1).lower()) + r"\b", _names):
                    continue
            matches.append((_s, _e, g, False, False))
                                                                                               
                                                                       
    if ACAD_MOD:
        matches.extend(_mod_matches(work, [(s_, e_) for s_, e_, _t, _b, _j in matches]))
                                                                                       
                                                                                  
                                                            
    _defined = _defined_abbrevs(_raw)
    matches = [
        (s, e, t, ib6, ij) for s, e, t, ib6, ij in matches
        if not (ij and (
            (_defined and t.upper().replace(".", "").replace(" ", "") in _defined)
            or (_BRACKET_INSTRUMENT.search(_raw[max(0, s - 2):s])
                and _BRACKET_INSTRUMENT_TAIL.match(_raw[e:e + 8]))))
    ]

                                                                                               
                                                                                                          
                                                                                                   
                                                                                            
                                                                                                  
                                                                                                
                                           
    if _us_full:
        matches = [x for x in matches
                   if not (not x[4] and len(str(x[2]).split()) <= 4
                           and any(x[0] < fs < x[1] <= fe for fs, fe in _us_full))]
    matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))
                                                                                 
                                                             
    matches = [
        (s, e, t, ib6, ij) for s, e, t, ib6, ij in matches
        if not _NON_LEGAL_EXCLUDE_RE.search(
            work[max(0, s - 100): min(len(work), e + 100)]
        )
    ]
                                                                                             
                                                                                     
                                                                                       
                                                                                   
                                                                                      
                                                                            
                                                             
                                                                                                
                                                                                                  
                                                                                              
                                                                                                 
    def _r47_left(s_):
        _w = work[max(0, s_ - 24):s_]
                                                                                              
        _c = [m_.end() for m_ in re.finditer(r"(?:[a-z]{4,}[.;][”\"]?|[”\"])\s+(?=[A-Z(\d])", _w)]
        return _w[_c[-1]:] if _c else _w
    if ENCYCLOPAEDIAS_IN:
                                                                                                              
                                                                                                              
                                                                                                                  
                                                                                
        matches = [
            (s, e, t, ib6, ij) for s, e, t, ib6, ij in matches
                                                                                                                       
            if not ((_ENCYC_NAME_RE.search(_r47_left(s).rsplit(";", 1)[-1]) and not _ENCYC_NAME_RE.search(work[s:e]))
                    or _ENCYCLOPAEDIA_BARE_IN.search(str(t)))
        ]
    else:
        matches = [
            (s, e, t, ib6, ij) for s, e, t, ib6, ij in matches
            if not (_ENCYCLOPAEDIA_RE.search(_r47_left(s) + work[s:e])
                    or _ENCYCLOPAEDIA_BARE.search(str(t)))
        ]
                                                                                         
                                                                                      
                                                                                            
                                                          
                                                                              
    used = []
    for s, e, t, ib6, ij in matches:
        if any(s < ue and e > us for us, ue, *_ in used):
            continue
        used.append((s, e, t, ib6, ij))
                                                                                         
                                                                                   
                                                                                              
                                                                                          
                                                                                        
                                                                 
    used = [(s, e, t, ib6, ij) for s, e, t, ib6, ij in used
            if not _GOV_REPORT_RE.search(work[s:e])
            and not _NOT_A_WORK_RE.search(work[s:e])
            and not _US_REPORTER_IN_TITLE.search(work[s:e])
            and not _NEWS_OUTLET.search(work[s:e])]
                                                                                        
                                                                           
                                                                          
                                                                                    
                                                                                  
    _V_ADJ = _V_ADJ_RE
    v_guarded = []
    _zf_cache = {}
    for s, e, t, ib6, ij in used:
                                                                         
        if ZERO_FALSE:
            _zf = _zf_fix(work, s, e, t, ij, (s, e) in _sf_vouched or (s, e) in _lr_vouched, _zf_cache)
            if _zf is None:
                continue
            s, e, t = _zf
        if (not ib6 and len(t) <= 20
                and re.fullmatch(r"[A-Za-z'\-]+", t)
                and ' ' not in t):
            ctx_pre  = work[max(0, s - 4): s]
            ctx_post = work[e: min(len(work), e + 4)]
            if _V_ADJ.search(ctx_pre) or _V_ADJ.search(ctx_post):
                continue                                                            
                                                                                        
                                                                                                  
        if (CASE_TAIL and not ij and not any(c in t for c in "“”\"")
                and _case_cite_follows(work, e, t)):
            continue
                                                                                      
        if (not ib6 and len(t) <= 34 and len(t.split()) <= 4
                and not any(c.isdigit() for c in t)
                and _party_tail_before(work[max(0, s - 45):s])):
            continue
                                                                                     
                                                                                      
                                                                                        
                                                                                    
                                                                                     
                                                                                            
                                                                                            
                                                     
                                                                                            
                                                               
                                                                                              
                                                                                               
                                                    
                                                                                              
                                                                                              
                                       
                                                                                         
                                                                                    
                                                                                          
                              
                                                                              
                                                                             
                                 
                                                                                         
                                                                                     
                                                                                             
                                                                                             
                                                         
                                                                                            
                                                                                            
        lo = max(0, s - 130)
        back = work[lo:s]
        _cuts = list(_LOOKBACK_CUT.finditer(back))
        begin = (lo + _cuts[-1].end()) if _cuts else lo
        for _pj in _PER_JUDGE.finditer(back):
            begin = max(begin, lo + _pj.end())
        for _phrase in ("cited in", "referring to", "citing", "quoted in", "discussed in"):
            _ci = back.lower().rfind(_phrase)
            if _ci >= 0:
                begin = max(begin, lo + _ci + len(_phrase))
                                                                                                     
                                                                                                 
                                                                                                  
                                                                                               
                                                                                           
        _fwd = work[e:min(len(work), e + 40)]
        _fc = re.search(r"[.;]\s+(?=[A-Z\[(“‘\"])", _fwd)
        ctx = work[begin:e + (_fc.start() + 1 if _fc else len(_fwd))]
                                                                                     
                                                                                        
                                                                                             
                                                                                           
                                                                           
                                                                                             
                                                                                            
                                                                                               
                                                                                       
                                                                      
                                                                                          
                                                                                   
                                                                                          
                                                                                           
                                                                                             
                                                                                             
                                                                             
        _v1 = (ACAD_MOD and ACAD_MOD_V1 and not _is_official_report(t) and not _is_not_a_work(t)
               and _mod_full_article(work, e, t))
        if ((_is_official_report(t) or _is_official_report(ctx)) and not _v1
                and not (_authored_edition(t) or _authored_article(t)
                         or _AUTHOR_OF_TITLE.search(t)
                                                                                                    
                                                                                                      
                         or _AUTHORS_COLON_TITLE_ED.fullmatch(t)
                         or (s, e) in _sf_vouched                                                  
                         or t.startswith("Law Commission, ")                              
                         or _person_authored_book(t) or _authored_chapter(t))):
                                                                                       
                                                                                           
                                                                                        
                                                                                        
                                                                                     
                                                                                          
                                                                                           
                                                                                        
                                                                  
            continue
                                                                                       
                                                                                    
                                                                  
                                                                                
                                                                                   
                                      
                                                                                      
                                                                                        
                                                                                      
                                                                                  
                                                  
                                                                                                 
                                                                                                 
                                                           
        if (s, e) in _lr_vouched:
            v_guarded.append((s, e, t, ib6, ij))
            continue
        if _is_not_a_work(t) or (_is_not_a_work(ctx) and not _v1 and not (
                _authored_edition(t) or _authored_article(t) or _authored_book(t)
                or _authored_chapter(t)
                                                                                   
                or _us_bluebook(t)
                                                                                           
                                                                                           
                                                                                     
                or _EDITORIAL_CITE.search(t)
                                                                                   
                                                                               
                                                                                   
                                                                                   
                                                                                     
                                                                                    
                                                                                      
                                                                                       
                                                                              
                or (_publisher_edition(t) and not _NOT_SCHOLARSHIP.search(ctx))
                                                                                              
                                                                                               
                                                                                              
                                                                          
                or (_PUBLISHER_YEAR.search(t) and len(t[:_PUBLISHER_YEAR.search(t).start()].strip()) >= 8
                    and not _NOT_SCHOLARSHIP.search(ctx)))):
            continue
                                                                                       
                                                                                         
                                                                                      
                                                                      
                                                                                          
                                                                                         
                                                                                          
        if not _bare_name_corroborated(work, t, s, e):
            continue
        v_guarded.append((s, e, t, ib6, ij))
    used = v_guarded
                                                                                               
                                                                                                
                                                                                           
                                                                                                      
                                                                    
                                                                                       
                                                                                   
                                                                                    
                                                                                       
                                                                           
                                                                              
                                                                                    
                                                                               
                                                                                       
                                                                                        
    non_b6_ends = [e for s, e, t, ib6, ij in used if not ib6]

    def _same_footnote(prev_end, start):
        return not _FOOTNOTE_MARK.search(work[prev_end:start])

    filtered = [(s, e, t, ij) for s, e, t, ib6, ij in used
                if not (ib6 and any(0 < s - ne <= 350 and _same_footnote(ne, s)
                                    for ne in non_b6_ends))]
                                                                                        
    if PASS_1J and filtered:
        filtered.sort()
        _out1j, _kill1j = [], set()
        for _i, (_s, _e, _t, _j) in enumerate(filtered):
            _sp = None if _j else _imprint_span(work, _s, _e, _t)
            if not _sp:
                continue
            _bs, _be = _sp
            _rs = _run_before(work, _bs)
            if _rs >= _bs:
                continue                                                                      
            if _RUN_ENCYC.search(work[_rs:_bs]):
                _kill1j.add(_i)                                                                                                                      
                continue
            _inside = [_k for _k, _c in enumerate(filtered)
                       if _k != _i and _k not in _kill1j and _c[1] > _rs and _c[0] < _bs]
            if any(len(_skeleton(_norm_key(filtered[_k][2]))) >= 3 for _k in _inside):
                _kill1j.add(_i)                                                     
                continue
            _kill1j.update(_inside)
            _kill1j.add(_i)
            _out1j.append((_rs, _be, work[_rs:_be], False))
        if _kill1j:
            filtered = sorted([_c for _k, _c in enumerate(filtered) if _k not in _kill1j] + _out1j)
                                                                              
                                                                                     
                                                                                   
                                                       
    _alias_of = {}
                                                                                   
                                                                                            
                                                                                             
                                                                                   
                                                                                       
                                                                                           
                                                                                           
                                                                                          
                                            
    _author_alias = {}
    filtered.sort()
    _drop = set()
    _drop_flat = set()
    for _i in range(len(filtered) - 1):
        if _i in _drop:
            continue
        _s1, _e1, _t1, _j1 = filtered[_i]
        _s2, _e2, _t2, _j2 = filtered[_i + 1]
        if _s2 < _e1 or not _same_footnote(_e1, _s2):
            continue
        _sep = work[_e1:_s2]
                                                                                            
                                                                                              
                                                                                               
                                                                                          
                                                                                            
                                                                                               
                                                                                            
                                                                       
                                                                                            
                                                                                                
                             
        if (_ACAD_PARALLEL_SEP.match(_sep) and "," in _sep
                and _BARE_AUTHOR_NAME.match(str(_t1).strip())
                and _BARE_AUTHOR_NAME.match(str(_t2).strip())):
            continue
        if _ACAD_PARALLEL_SEP.match(_sep):
            _drop.add(_i + 1)
            _alias_of.setdefault(_norm_key(_t1), set()).add(_norm_key(_t2))
            if _is_austlii_parallel(_t1, _sep, _t2):
                _drop_flat.add(_i + 1)
            elif _is_author_of_next(_t1, _sep, _t2, work[_e2:_e2 + 40]):
                                                                       
                _drop_flat.add(_i)
                _alias_of.setdefault(_norm_key(_t2), set()).add(_norm_key(_t1))
                _author_alias[_norm_key(_t1)] = _norm_key(_t2)
    filtered = [c for _i, c in enumerate(filtered)
                if _i not in (_drop if groups else _drop_flat)]

                                                                                       
                                                                                                    
                                                                                               
                                                                                               
                                                                                              
                                                                                               
                                                                                                 
                                                                                                
                               
    if len(filtered) > 1:
        filtered.sort()
        _dead = set()
        for _i in range(len(filtered)):
            if _i in _dead:
                continue
            for _k in range(_i + 1, len(filtered)):
                if filtered[_k][0] >= filtered[_i][1]:
                    break
                if _k in _dead:
                    continue
                _a, _b = filtered[_i], filtered[_k]
                _ov = min(_a[1], _b[1]) - _b[0]
                _la, _lb = _a[1] - _a[0], _b[1] - _b[0]
                if _ov < 12 or _ov < 0.5 * min(_la, _lb):
                    continue
                _ka, _kb = _norm_key(_a[2]), _norm_key(_b[2])
                if _ka == _kb or len(set(_skeleton(_ka)) & set(_skeleton(_kb))) < 2:
                    continue
                _lose, _win = ((_k, _i) if _la >= _lb else (_i, _k))
                _dead.add(_lose)
                _alias_of.setdefault(_norm_key(filtered[_win][2]), set()).add(_norm_key(filtered[_lose][2]))
                if _lose == _i:
                    break
        if _dead:
            filtered = [c for _i, c in enumerate(filtered) if _i not in _dead]

                                                                                       
    if ZERO_FALSE and STITCH and len(filtered) > 1:
        filtered.sort()
        _outk = [filtered[0]]
        for _c in filtered[1:]:
            _p = _outk[-1]
            if (_c[0] >= _p[1] and _same_footnote(_p[1], _c[0])
                    and _zf_stitch(_p[2], work[_p[1]:_c[0]], _c[2], _p[3], _c[3])):
                _joined = work[_p[0]:_c[1]]
                _alias_of.setdefault(_norm_key(_joined), set()).update((_norm_key(_p[2]), _norm_key(_c[2])))
                _outk[-1] = (_p[0], _c[1], _joined, False)
            else:
                _outk.append(_c)
        filtered = _outk

                                                                          
                                                                                        
                                                                                              
                                                    
                                                                                                
                                                                                                
                                                                                                 
                                                                                 
    if not groups and len(filtered) > 1:
        filtered.sort()
        _dropi = set()
        for _i in range(len(filtered) - 1):
            _s1, _e1, _t1, _j1 = filtered[_i]
            _s2, _e2, _t2, _j2 = filtered[_i + 1]
            if _j1 or not (0 <= _s2 - _e1 <= 160) or not _JOINT_AUTHORS.match(str(_t1).strip()):
                continue
            _gap = work[_e1:_s2]
            if not _gap.lstrip().startswith(",") or ";" in _gap or re.search(r"\.\s+[A-Z]", _gap):
                continue
            if not _same_footnote(_e1, _s2):
                continue
            _dropi.add(_i)
            _alias_of.setdefault(_norm_key(_t2), set()).add(_norm_key(_t1))
        if _dropi:
            filtered = [c for _i, c in enumerate(filtered) if _i not in _dropi]

                                                                                    
                                                                                                
                           
                                                                                                 
                                                                                               
                                                                                                
                                                                                             
                                                           
    if not groups and len(filtered) > 1:
        filtered.sort()
        _dropg = set()
        for _i in range(len(filtered) - 1):
            _s1, _e1, _t1, _j1 = filtered[_i]
            _s2, _e2, _t2, _j2 = filtered[_i + 1]
            if _j1 or not _j2 or _i in _dropg or not (0 <= _s2 - _e1 <= 40):
                continue
            if not _same_footnote(_e1, _s2) or not _TITLE_THEN_CITE_SEP.match(work[_e1:_s2]):
                continue
            if len(_skeleton(_norm_key(_t1))) < 3:
                continue                                                                       
            _dropg.add(_i + 1)
            _alias_of.setdefault(_norm_key(_t1), set()).add(_norm_key(_t2))
        if _dropg:
            filtered = [c for _i, c in enumerate(filtered) if _i not in _dropg]

                                                                           
    _short_of = {}
    for _s, _e, _t, _j in filtered:
        _dm = (_DEFINED_SHORT.match(work[_e:_e + 60])
               or _DEFINED_SHORT_US.match(work[_e:_e + 110]))
        if not _dm:
            continue
        _sk, _fk = _norm_key(_dm.group(1)), _norm_key(_t)
        if _sk and _fk and _sk != _fk and not _contains_words(_fk, _sk):
            _short_of[_sk] = _fk
    if _short_of:
        _full_keys = {_norm_key(_c[2]) for _c in filtered}
                                                                                        
        _kill = {_k for _k, _v in _short_of.items() if _v in _full_keys}
        if _kill:
            for _k in _kill:
                _alias_of.setdefault(_short_of[_k], set()).add(_k)
            filtered = [_c for _c in filtered if _norm_key(_c[2]) not in _kill]

                                                                                      
                                                                                   
                                                                                     
                                                                        
    seen = set()
    _printed = {}
    count = 0
    for s, e, t, ij in filtered:
                                                                                              
                                                                                               
                                                                                            
                                                                                              
                                                                                              
        if ij and _CRIMLR_CITE.search(work[max(0, s - 60):min(len(work), e + 60)]):
            lo = max(0, s - 160)
            back = work[lo:s]
                                                                                
                                                                                      
                                                                                    
                                                                                
            _masked = _mask_quoted(back)
            cut = max(_masked.rfind(". "), _masked.rfind("; "), _footnote_cut(back))
            ctx = work[(lo + cut + 2) if cut >= 0 else lo:min(len(work), e + 60)]
            if _is_not_a_work(ctx):
                continue
        if _COURT_PAPER.search(t) or _PUBLISHER_ONLY.match(t):
            continue                                                                                       
        k = _norm_key(t)
        if ij:
                                                                                        
                                                                                           
                                                                                       
                                                                                             
                                                                                           
                                                                                           
                                                                 
             
                                                                                            
                                                                                           
                                              
            before = work[max(0, s - 30):s]
                                                                                                           
                                                                                                           
                                                                                                            
                                                        
            before = before[before.rfind("\n") + 1:]
            _years = _YEAR_IN_CTX.findall(before)
            ym = _years[-1] if _years else None
                                                                                            
            post = work[e: min(len(work), e + 25)]
            pm = re.match(r'[ \t,.]+(\d+)', post)
            year = ym or ''                                                        
            page = pm.group(1) if pm else ''
            if year or page:
                k = f"{k}_{year}_{page}"
        seen.add(k)
                                                                                             
                                                                                         
                                                                                             
                                                                                           
                                                                                             
                                                        
        if RAW_KEYS and k not in _printed and work[s:e] == t and _raw[s:e] != t:
            _kb = _norm_key(t)
            _pk = _norm_key(_raw[s:e])
            if _fold_diacritics(_pk) == _kb and k.startswith(_kb):
                _printed[k] = _pk + k[len(_kb):]

                                                              
     
                                                                                           
                                                                                          
                                                                                           
                                       
                                                                            
                                                                                           
                                                                     
                                                   
     
                                                                                            
                                                                                        
                                                                                            
                                                                                              
                                                                                            
                                                                                               
                                                          
                                                                                         
                                                                                               
                                                                                         
                                                                                                
                                                                                                
                                                                                            
                                                                                             
                                                                  
    distinct = []
                                                                               
                                                                                 
                                                                                   
                                                                                 
                                                                                 
                                                                                  
                                                  
    for k in sorted(seen, key=lambda s: (len(_skeleton(s)), len(s), s), reverse=True):
        if any(o != k and _contains_words(o, k) for o in distinct):
            continue
        distinct.append(k)

                                                                               
     
                                                                                            
                                                                                             
                                                                                           
                                                                                           
                                                                                           
                                                                                             
                                                                                           
                                                                                           
                                                                                      
                                                                            
                                                                                     
                                                                                            
                                                                                          
                  
    if len(distinct) > 1:
        _folded = []
        for k in distinct:
            _m = re.match(r'^(.+?)\s*__\d{1,4}$', k)
            _j = _m.group(1).strip() if _m else ''
                                                                                               
                                                                                        
            if _j and not re.search(r"\d", _j) and (_j in _JOURNAL_ABBREV_ALIASES
                       or _j in _JOURNAL_ABBREV_ALIASES.values()
                       or _names_a_periodical(_j)):
                _abbrs = {_j} | {_ab for _ab, _fu in _JOURNAL_ABBREV_ALIASES.items()
                                 if _fu == _j}
                if any(_o != k and any(_contains_words(_o, _ab) for _ab in _abbrs)
                       for _o in distinct):
                    continue
            _folded.append(k)
        if _folded:
            distinct = _folded

                                                                                           
     
                                                                                           
                                                                                            
                                                                                          
                                                                                  
                                                                                    
                                                                                          
                                                                                         
                                                                                         
                                                                                        
              
     
                                                                             
                                                                                      
                                                                                         
     
                                                                                           
    if not groups and _author_alias:
        _surv = set(distinct)
        _kept = [k for k in distinct
                 if _author_alias.get(k) in (None, k) or _author_alias[k] not in _surv]
        if _kept:
            distinct = _kept
                                                                                                   
                                                                                                
                          
                                                                                
                                                                                             
                                                                                              
                                                                                                
                                                                                             
                                                                                      
                                                                                               
                                               
    if not groups and len(distinct) > 1:
        _tok = {k: [re.sub(r"[^a-z0-9]", "", w) for w in k.replace("_", " ").split()] for k in distinct}
        _tok = {k: [w for w in v if w] for k, v in _tok.items()}
        _gone = set()
        for _a in distinct:
            _ta = _tok[_a]
            if len(_ta) < 4 or not re.fullmatch(r"(?:1[6-9]|20)\d\d", _ta[-1]):
                continue
            for _b in distinct:
                if _b == _a or _b in _gone:
                    continue
                _tb = _tok[_b]
                if len(_tb) <= 4:
                    continue
                for _n in range(min(len(_ta), len(_tb) - 1), 3, -1):
                    if _ta[-_n:] == _tb[:_n]:
                        if len([w for w in _ta[-_n:-1] if w not in _JOIN_WORDS and not w.isdigit()]) >= 3:
                            _gone.add(_a)
                        break
                if _a in _gone:
                    break
        if _gone and len(_gone) < len(distinct):
            distinct = [k for k in distinct if k not in _gone]
                                                                                              
    if ZERO_FALSE and SAME_WORK and len(distinct) > 1:
        distinct = _zf_same_work(distinct, _alias_of)
                                                                  
    if ACAD_FP and not groups and len(distinct) > 1:
        distinct = _acad_fp_merge(distinct, work)
                                                                        
    if ACAD_ED and not groups and len(distinct) > 1:
        distinct = _acad_ed_merge(distinct, work)
                                                                                          
    if LS_FAM and not groups and len(distinct) > 1:
        distinct = _ls_fam_merge(distinct, work)
    if LS_SHORT and not groups and len(distinct) > 1:
        distinct = _ls_short_merge(distinct, work)
                                                                                         
                                                                   
    for _sk in _scots_institutional(text):
        if not any(_contains_words(_o, _sk) for _o in distinct):
            distinct.append(_sk)
                                                                
    if ACAD_OLD:
        distinct.extend(_old_short_forms(text, distinct))
    if groups:
        out = []
        for k in distinct:
            names = {k} | _alias_of.get(k, set())
            for surv, al in _alias_of.items():
                if k in al:
                    names |= {surv} | al
            out.append(frozenset(names))
        return _r107_final(_r106_final(_r47_final(out), text, groups=True), text, groups=True)
                                                                                
                                                                                           
                                                                                        
                                                                                      
                                                                                              
                                                                                
                                                                
                                                                                          
                                                                                         
                                                             
                                                                                             
                                                                                    
                                                                                           
                                                                                     
                                                                       
                                                              
                                                                                
                                                                                          
                                                                                           
                                                                
                                                                                             
                                                                                            
                                                                                         
                                                                                         
    if CASE_KEY:
        _nc = [k for k in distinct if not _CASE_KEY_TAIL.search(k)]
        if len(_nc) != len(distinct):
            distinct = _nc
    if _printed:
        _outp = []
        for k in distinct:
            k = _printed.get(k, k)
            if k not in _outp:
                _outp.append(k)
        distinct = _outp
    return _r107_final(_r106_final(_r47_final(distinct), text), text)


                                                                                                                 
                                                                                                                   
                                                                                                            
                                                                                                                 
                                                                                                                
                                                                                                                
                                                                                                                 
                                                                                                       
                                                                                                                 
                                                                                                                
R106_ON = os.environ.get("JR_R106", "1") != "0"
_AP106 = r"[’'`]?\s*s?[’'`]?"
_LEGAL_DICT_RE = re.compile(
    r"\bBlack" + _AP106 + r"\s+Law\s+Dictionary\b"
    r"|\bJowitt" + _AP106 + r"\s+Dictionary\s+of\s+English\s+Law\b"
    r"|\bStroud" + _AP106 + r"\s+Judicial\s+Dictionary\b"
    r"|\bWords\s+(?:and|&)\s+Phrases\s+(?:Legally|Judicially)\s+Defined(?:\s+in\s+Canadian\s+Courts)?\b"
    r"|(?<=\d\s)Words\s+(?:and|&)\s+Phrases\b"
    r"|\bWords\s+(?:and|&)\s+Phrases(?=\s*(?:,\s*Permanent|\(\s*(?:perm|\d)|,?\s*vol))"
    r"|\bBouvier" + _AP106 + r"\s+(?:Law\s+)?Dictionary\b"
    r"|\bWharton" + _AP106 + r"\s+Law\s+Lexicon\b"
    r"|\bOsborn" + _AP106 + r"\s+(?:Concise\s+)?Law\s+Dictionary\b"
    r"|\bBallentine" + _AP106 + r"\s+Law\s+Dictionary\b"
    r"|\bMozley\s+(?:&|and)\s+Whiteley" + _AP106 + r"\s+Law\s+Dictionary\b"
    r"|\bTomlins" + _AP106 + r"\s+Law\s+Dictionary\b"
    r"|\bJacob" + _AP106 + r"\s+(?:New\s+)?Law\s+Dictionary\b"
    r"|\bSweet" + _AP106 + r"\s+Dictionary\s+of\s+English\s+Law\b"
    r"|\bBurrows" + _AP106 + r"\s+Words\s+(?:and|&)\s+Phrases\b"
    r"|\bCowel" + _AP106 + r"\s+(?:Law\s+Dictionary|Interpreter)\b"
    r"|\b(?:Butterworths\s+)?(?:Concise\s+)?Australian\s+Legal\s+Dictionary\b"
    r"|\bEncyclopa?edic\s+Australian\s+Legal\s+Dictionary\b"
    r"|\bAustralian\s+Law\s+Dictionary\b"
    r"|\bOxford\s+Dictionary\s+of\s+Law\b"
    r"|\bDictionary\s+of\s+(?:Modern\s+)?Legal\s+Usage\b"
    r"|\b(?:Dictionary\s+of\s+Canadian\s+Law|Canadian\s+Law\s+Dictionary|New\s+Zealand\s+Law\s+Dictionary)\b"
    r"|\bDictionary\s+of\s+(?:English|Scots|Scottish|Australian|Irish|Roman)\s+Law\b"
    r"|\b[A-Z][a-z]+" + _AP106 + r"\s+(?:Law|Legal)\s+Dictionary\b")
_GEN_ENC_KEY = re.compile(r"(?i)encyclop(?!\w*dist)|wikipedia|britannica|\bworld\s+book\b")
                                                                                                                   
                                                                                                                       
_LEGAL_SUBJ = re.compile(r"(?i)\blaws?\b|legal|juris|\bforms\b|precedent|halsbury|statut|\bstair\b|\bcourts?\b|\btax|comparative|\bpublic\b|procedure|juridi|droit|recht|\bgreen\b|parliament|\bcomp\.?\s+l\b"
                         r"|\bcrim|justice|constitution|conveyanc|pleading|practice|\brights\b|\btreat(?:y|ies)\b")


def _r106_name_out(k, text=None):
    """R106: the key of a general (non-legal) encyclopaedia.
    ⚠ (24 Nov 2026, Master delta) THE KEY CAN STOP SHORT OF THE WORD THAT MAKES IT LEGAL: `encyclopaedia of banking` is
    Cresswell's Encyclopaedia of Banking Law, `sweet maxwell encyclopedia` Sweet & Maxwell's Encyclopedia of
    Employment Law, `encyclopaedia of planning` the Encyclopaedia of Planning Law and Practice -- while Munn's
    Encyclopedia of Banking and Finance is not legal. So before a key goes, the full title is read from the judgment:
    a printed encyclopaedia title that carries the key's own words and a legal word keeps it."""
    k = str(k)
    if not (_GEN_ENC_KEY.search(k) and not _LEGAL_SUBJ.search(k)):
        return False
    if text:
        words = [w for w in re.findall(r"[a-z]{3,}", k.lower())
                 if not w.startswith("encyclop") and w not in ("the", "and", "new", "vol", "eds")]
        for m in re.finditer(r"(?i)encyclop\w*\b[^.;()\[\]\n]{0,60}", text):
            pre = re.split(r"[.;:)\]]\s", text[max(0, m.start() - 30):m.start()])[-1]                                     
            title = (pre + m.group()).lower()
            if _LEGAL_SUBJ.search(m.group()) and words and all(w in title for w in words[:2]):
                return False
    return True


def _r106_norm(t):
    t = re.sub(r"[’'`]|\bs\b|\bbutterworths\s+|\bconcise\s+", "", str(t).lower())
    return re.sub(r"\s+", " ", t).strip()


def _r106_legal_dicts(text):
    seen, out, last = set(), [], -10
    for m in _LEGAL_DICT_RE.finditer(text or ""):
                                                                                               
        if m.start() <= last + 4:
            last = m.end()
            continue
        last = m.end()
        t = re.sub(r"\s+", " ", m.group()).strip()
        k = _r106_norm(t)
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out


def _r106_final(out, text, groups=False):
    if not R106_ON:
        return out
    res = []
    for k in out:
        if isinstance(k, (set, frozenset, list, tuple)):
            names = [n for n in k if not _r106_name_out(n, text)]
            if names:
                res.append(type(k)(names) if not isinstance(k, list) else names)
        elif not _r106_name_out(k, text):
            res.append(k)
    have = _r106_norm(" | ".join(" ".join(map(str, k)) if isinstance(k, (set, frozenset, list, tuple)) else str(k)
                                 for k in res))
    for d in _r106_legal_dicts(text):
        if _r106_norm(d) not in have:
            res.append(frozenset({d}) if groups else d)
    return res

                                                                                                                  
                                                                                                                         
                                                                                                                  
                                                                                                                      
                                                                                                                   
                                                                                                                    
                                                                                                                 
                                                                                                                  
                                                                                                             
                                                                                                                      
                                                                                                            
                            
R107_ON = os.environ.get("JR_R107", "1") != "0"
_PL_BODY = re.compile(
    r"Congressional\s+Research\s+Service|\bCRS\s+Report|House\s+of\s+(?:Commons|Lords)\s+Library|Parliamentary\s+Library"
    r"|Library\s+of\s+Parliament|Parliamentary\s+(?:Information\s+and\s+)?Research\s+(?:Service|Branch)")
_PL_TYPE = re.compile(
    r"(?i)\b(?:Research\s+Paper|Background\s+Paper|Briefing\s+Paper|Research\s+Note|Research\s+Brief|Current\s+Issues\s+Brief"
    r"|Standard\s+Note|CRS\s+Report|Report\s+for\s+Congress|Briefing\s+No|Debate\s+Pack|Research\s+Briefing|Insight|In\s+Focus)\b"
    r"|\b(?:BP|PRB|RP|CIB|SN)[\s-]?\d")
_PL_OUT = re.compile(r"(?i)Legislative\s+Summary|\bBills?\s+Digest|\bAlert\s+Digest|Parliamentary\s+Handbook"
                     r"|\bBill\s+C[\s-]?\d|\bBill\s+\d{4}\b|\bBill\s+No\b")
_PL_ID = re.compile(
    r"(?i)\b(?:Research\s+Paper|Background\s+Paper|Briefing\s+Paper|Research\s+Note|Research\s+Brief|Current\s+Issues\s+Brief"
    r"|Standard\s+Note|CRS\s+Report)\s*(?:No\.?\s*)?([A-Z]{0,3}[\s-]?\d[\w./-]*(?:,?\s+(?:19|20)\d{2}(?:-\d{2})?)?)"
    r"|\b((?:BP|PRB|RP|CIB|SN)[\s-]?\d[\w-]*)|\b(R[LS]?\d{4,5})\b")
_PL_QTITLE = re.compile(r"[“\"]([^”\"]{8,140})[”\"]")


def _r107_papers(text):
    """(key, display) for each parliamentary-library research paper cited."""
    out, seen = [], set()
    for m in _PL_BODY.finditer(text or ""):
        a, b = max(0, m.start() - 260), min(len(text), m.end() + 260)
                                                                                           
        left = text[a:m.start()]
        cut = max(left.rfind("\n\n"), left.rfind(". "), left.rfind("; "), left.rfind("]"))
        if cut >= 0:
            left = left[cut + 1:]
        right = text[m.end():b]
        stop = [i for i in (right.find("\n\n"), right.find("; "), right.find(". See"), right.find(".\n")) if i >= 0]
        if stop:
            right = right[:min(stop)]
        win = left + m.group() + right
        if re.search(r"\bv\.?\s+(?:the\s+)?(?:Library\s+of\s+Parliament|Congressional)", win):
            continue
        if _PL_OUT.search(win) or not _PL_TYPE.search(win):
            continue
        i = _PL_ID.search(win)
        q = _PL_QTITLE.search(win)
        ident = next((g for g in (i.groups() if i else ()) if g), None)
        key = (re.sub(r"[\s.]+", " ", ident).strip().lower() if ident else
               (q.group(1).strip().lower()[:80] if q else re.sub(r"\s+", " ", win).strip().lower()[:80]))
        if key in seen:
            continue
        seen.add(key)
        body = re.sub(r"\s+", " ", m.group())
        label = re.sub(r"\s+", " ", i.group(0)).strip() if i else (q.group(1) if q else "research paper")
        out.append((key, body + ", " + label.strip()))
    return out


def _r107_final(out, text, groups=False):
    if not R107_ON:
        return out
    res = list(out)
    have = " | ".join(" ".join(map(str, k)) if isinstance(k, (set, frozenset, list, tuple)) else str(k) for k in res).lower()
    for key, disp in _r107_papers(text):
        if key[:40] in have:
            continue
        res.append(frozenset({disp}) if groups else disp)
    return res

                                                                                                
                                                                                                  
                                                                                             
                                                                                               
                                                                                                     
                                                                                                                      
                                                                                                       
                                                                                                     
                                                                                                           
_R47_KEY = re.compile((r"(?!x)x" if ENCYCLOPAEDIAS_IN else r"\bhalb?sbury\s*[’']?\s*s?[’']?\s+statutes\b") +
                      r"|^\s*(?:in\s+)?halsbury\b(?!\s*[’']?\s*s?[’']?\s+(?:the\s+)?(?:laws?|statutes)\b)"
                      r"|\bhalsburys\b(?!\s*[’']?\s+(?:the\s+)?laws?\b)"
                      + ("" if R106_ON else                                                  
                      r"|\b(?:black|bouvier|stroud|jowitt|wharton|osborn)\s*[’']?\s*s?\s+(?:law\s+|judicial\s+)?dicti\s?onary\b"),
                      re.I)


                                                                                                                
                                                                                                           
                                                                                                           
                                                                                                                
                                                                                                                  
                                                                                                              
                                                                                                                     
                                                                                            
_NOT_WORK_KEY = re.compile(
    r"\b(?:act|ord(?:inance)?|bill|reg(?:ulation)?|cap)\.?\s+(?:no\.?\s*)?\d+\s*(?:of|/)\s*\d{4}\b"
    r"|\b(?:criminal|civil|district|magistrate s)?\s*(?:case|suit)\s+no\.?\s*\d"
    r"|^(?:the\s+)?(?:new\s+)?(?:california|york|texas|florida|illinois|ohio|pennsylvania|michigan|georgia|massachusetts|"
    r"virginia|washington|arizona|colorado|jersey|carolina|oregon|nevada|utah|maryland|minnesota|wisconsin|missouri|"
    r"tennessee|indiana|louisiana|kentucky|alabama|connecticut|iowa|kansas|oklahoma|delaware|hawaii|alaska)\s+s?\s*"
    r"(?:[a-z]+\s+){0,3}(?:law|act|code)$"
    r"|^(?:the\s+)?(?:chicago|warsaw|montreal|hague|geneva|vienna|new york|brussels)\s+convention$"
    , re.I)
                                                                                                                
                                                                                                                         
                                            
_NEWS_DATE = re.compile(r"\b(?:jan|feb|mar|apr|may|june?|july?|aug|sept?|oct|nov|dec)\.?\s+\d{1,2},?\s+(?:199\d|20[0-4]\d)$", re.I)
_AUTHOR_LEAD = re.compile(r"^(?:\d+\s+)?(?:[a-z]\.\s*){1,3}[a-z]{2,}", re.I)
                                                                                                                 
                                                                                                    
_GOV_KEY = re.compile(
    r"census\s+bureau|white\s+house\s+(?:briefing|fact)|briefing\s+room|press\s+release|minute\s+of\s+board"
    r"|nlrb\s+bulletin|pleads\s+guilty|waitangi\s+tribunal|national\s+planning\s+policy\s+framework"
    r"|civil\s+courts\s+review|strategic\s+framework|developing\s+the\s+framework", re.I)
_GOV_KEEP = re.compile(r"(?i)law\s+(?:reform\s+)?commission|\bjournal\b|\bj\.\s|law\s+rev(?:iew)?\b|\breview\s+\d|quarterly"
                       r"|\bl\.?\s?rev\b")


                                                                                                              
                                                                                                                 
                                                                                                           
_CASE_TRUSTS_KEY = re.compile(r"(?i)^(?:in\s+re\s+)?[a-z'’ .-]{0,40}\b(?:will|settlement|marriage\s+settlement|estate|trust)"
                              r"\s+trusts?(?:__\d+|_\d{4}_)?$")
_BARE_SOLJO_KEY = re.compile(r"(?i)^sol\.?\s*jo\.?$")


def _not_work_key(k):
    s = str(k).strip()
    return bool(_NOT_WORK_KEY.search(k) or (_GOV_KEY.search(k) and not _GOV_KEEP.search(k))
                or (_NEWS_DATE.search(k) and not _AUTHOR_LEAD.match(k) and not _GOV_KEEP.search(k))
                or _CASE_TRUSTS_KEY.match(s) or _BARE_SOLJO_KEY.match(s))


def _r47_final(distinct):
    def _clean(k):
        k = str(k)
        if _not_work_key(k) and "; " not in k:
            return None
        if not _R47_KEY.search(k):
            return k
        rest = [p for p in k.split("; ") if not _R47_KEY.search(p)]
        return "; ".join(rest) if rest and "; " in k else None
    out = []
    for k in distinct:
        if isinstance(k, (set, frozenset, list, tuple)):
            names = [n for n in (_clean(x) for x in k) if n]
            if names:
                out.append(type(k)(names) if not isinstance(k, list) else names)
        else:
            c = _clean(k)
            if c and c not in out:
                out.append(c)
    return out


def count_academic_refs(text):
    """Count academic references (journals + books) using two-pass deduplication.
    Single source of truth — imported by build_master_2.py and validate_cardiff.py.
    The detection layers are documented on academic_works(), of which this is the length."""
    return len(academic_works(text))




                                                                             
                                                                             
                                                      
 
                                                                               
                                                                              
                                                                       
                                                                             


                                                                                              
                                                                                               
                                                                                         
                                                                                            
                      
 
                                                                                     
                                                                                               
                                      
                                                                                     
                                                                                             
                                                                                      
                                                                                             
                   
                                                                       
                                                                                             
                                                                                             
                                                                                              
                                                                
                                                                                            
                                                             
 
                                                                                              
                                                    
_CASE_SENSITIVE_BOOK = {85, 86}
                                                                                            
                                                                                                   
                                                                                                    
                                                                                        
                                                                                               
                                                                                               
_LAW_OF_BOOK = {i for i, p in enumerate(_ACAD_BOOK_PATTERNS)
                if p.startswith(r"(?<! v )(?<! v\.)\b(?!Convention|Protocol|Agreement|Treaty|Regulation|Statute|Code|Ordinance)")}

_JOURNAL_RE = [re.compile(p, re.IGNORECASE) for p in _ACAD_JOURNAL_PATTERNS]
_BOOK_RE = [re.compile(p, 0 if i in _CASE_SENSITIVE_BOOK else re.IGNORECASE)
            for i, p in enumerate(_ACAD_BOOK_PATTERNS)]

                                                             
_V_ADJ_RE = re.compile(r'[\s(]v[.\s]')

                                                          
_NUM_WORD_RE = re.compile(r'^\d+\s+[a-z]+$')

                                                                                      
                                                                                             
                                                                                            
                                                                                       
                                                                                       
                                                                    
                                                                                     
                                                                                      
 
                                                                                           
                                                                                         
 
                                                                                          
                                                                                      
                                                                                      
                                                                                       
                                                                                     
                                                             
                                                             
                                                             
                                                                                           
                                                                                        
                                                                                          
                                                                                         
                                                                                              
                                                                                               
                                                                   
_ORD = r"\d{1,2}\s*(?:st|nd|rd|th)\s+ed(?:n|ition)?\b"

                                                                               
                                                                                           
                                                                             
                                                                                        
                                                                                         
                                                                                          
                                                                       
_POSSESSIVE_EDITION = re.compile(
    r"\b[A-Z][A-Za-z\-]+(?:'s|’s)\s+"                                              
    r"[A-Z][A-Za-z'’:\- ]{3,60}?"                                                            
    r"\s*,?\s*\(?\s*" + _ORD, re.I)                                                   

                                                                                       
                                                                                              
                                                                                     
_PUBLISHER = (r"(?:[A-Z][A-Za-z&.'\-]+\s+){0,4}"
              r"(?:University\s+Press|Press|Publishing|Publishers|Books|"
              r"Sweet\s*&\s*Maxwell|Oxford|Cambridge|Butterworths|LexisNexis|"
              r"Thomson\s+Reuters|Hart|Routledge|Wolters\s+Kluwer|Federation\s+Press|"
              r"Academy\s+Publishing|"
                                                                                     
                                                                                           
                                                                                       
                                                                                            
                                                                                   
              r"Stevens\s*&\s*Sons(?:\s+Limited)?|Maxwell|Callaghan|Little,?\s+Brown)")
                                                                                            
                                                                                            
                                                                               
 
                                                                                             
                                                                                      
                                                                                         
                                                                                             
                                                                                            
                                                                                           
_INVERTED_PUBLISHER = re.compile(
    r"\b([A-Z][A-Za-z'\u2019\-]{2,}\s+[A-Z][A-Za-z'\u2019\-]{1,24}"
    r"(?:\s+(?:of|on|and|the|in|to|for|a|an)\s+[A-Za-z][A-Za-z'\u2019\-]{1,24}"
    r"|\s+[A-Z][A-Za-z'\u2019\-]{1,24}){1,7})"                                                        
    r"\s*,\s*"
    r"(?:[A-Z][A-Za-z'\u2019.\-]+(?:\s+[A-Z][A-Za-z'\u2019.\-]+){0,2}"
    r"(?:\s*,\s*(?:and\s+)?|\s+and\s+)){1,4}"                                          
    r"\(?\s*" + _PUBLISHER + r"[^)\n]{0,40}?,\s*(?:1[89]|20)\d{2}\b")


                                                                                               
                                                                                              
                                                                                               
                                                                                               
                                                                                                
                      
 
                                                                                            
                                                                                              
_NAME_ON_SUBJECT = re.compile(
    r"\b([A-Z][A-Za-z'’\-]{2,})\s+on\s+(?:the\s+)?"
    r"([A-Z][A-Za-z'’\- ]{3,50}?)"
    r"\s*(?:,\s*(?:vol\s*\d|\d{1,2}\s*(?:st|nd|rd|th)\s+ed)"
    r"|\(\s*(?:\d{1,2}\s*(?:st|nd|rd|th)\s+ed[^)]{0,20},\s*)?(?:1[89]|20)\d{2})", re.I)

                                                                                    
                                                                                             
                                                                                           
                                                                                           
                           
 
                                                                                          
                                                                                              
                                                                                       
                                                                                               
                                                                   
_BARE_YEAR_BOOK = re.compile(
    r"\b([A-Z][A-Za-z'’\-]+(?:\s+[A-Z][A-Za-z'’\-]+){0,2}),\s+"
                                                                                       
                                                                                        
                                                                                         
                                                                                             
                                                                                            
                                                      
    r"([A-Z][A-Za-z'’\-]+(?:\s+[A-Za-z'’:\-]+){1,14})\s*,\s*(?:1[89]|20)\d{2}\b")

                                                                                             
                                                                                             
                                                                                             
                                                                                       
                                                                                               
                                          
 
                                                                                               
                                                                                           
                                                                                             
                                                             
_CUE_TITLE = re.compile(
    r"\b((?:[A-Z][A-Za-z'’\-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-z'’\-]+)?,\s+"
    r"(?:(?:The\s+|A\s+|An\s+)?[A-Z][A-Za-z'’\- ]{0,40}?)?"                                
    r"|(?:The\s+|A\s+|An\s+)?[A-Z][A-Za-z'’\- ]{0,40}?)"                            
    r"(?:Annotated|Commentary|Commentaries|Treatise|Institutes|Maxims|Essays|Outlines|"
    r"Elements|Digest|Handbook|Jurisprudence|Studies)"
    r"[A-Za-z'’\- ]{0,45}?)"
    r"\s*,?\s*\(?(?:1[6-9]|20)\d{2}")

                                                                                            
                                                                                               
                                                                                               
                             
_CUE_VERB = re.compile(r"\b(?:was|is|were|are|has|have|had|will|would|held|met|found|"
                       r"decided|reported|published|recommended|organised|organized|"
                       r"attended|chaired)\b", re.I)

_NAME_ON_CASE = re.compile(r"\sv\.?\s", re.I)
_NAME_ON_VERB = re.compile(r"(?i)^\w+(?:ing|ed)$")
                                                                                         
                                                                                        
                                                                                         
                                                                               
_NAME_ON_BODY = re.compile(r"(?i)^(?:committee|commission|council|board|authority|panel|"
                           r"inquiry|guidance|guidelines|practice|protocol|circular)$")
_NAME_ON_PROSE = re.compile(
    r"(?i)\b(?:appeal|application|behalf|record|remand|review|oath|affidavit|instructions|"
    r"condition|terms|circuit|indictment|trial|remittal|point|ground|basis|footing|question|"
    r"issue|matter|assumption)\b")

                                                                             
                                     
 
                                                                                      
                                                                                      
                                                                                     
                                                                    
 
                                                                                      
                                                     
                                                                                         
                                                                                
 
                                                                                         
                                                                                      
                                                                                      
                                                         
                                                                                   
                                                                               
                                                                         
                                                                                    
                                                                          
                                                                                        
                                                                                        
                                                                        
 
                                                                                         
                                                                                           
                                                                                    
                                                                                             
                                               
 
                                                                                          
                                                                                             
                                                                                             
                                                                                           
                                                                             
_RESEARCH_BODY = (
    r"(?:"
    r"(?:[A-Z][A-Za-z'’&.\-]+\s+){1,4}(?:Foundation|Institute|Institution|Academy|Society)"
    r"|Institute\s+(?:for|of)\s+[A-Z][A-Za-z'’\-]+(?:\s+[A-Z][A-Za-z'’\-]+){0,3}"
    r"|(?:[A-Z][A-Za-z'’&.\-]+\s+){0,3}Cent(?:re|er)\s+for\s+"
    r"[A-Z][A-Za-z'’\-]+(?:\s+[A-Z][A-Za-z'’\-]+){0,3}"
    r"|(?:[A-Z][A-Za-z'’&.\-]+\s+){1,3}(?:University|College)"
    r"|University\s+of\s+[A-Z][A-Za-z'’\-]+"
    r")")

                                                                                            
                                                                                             
                                                                                             
                                             
                                                                                   
                                                                                      
                                                                                       
                 
                                                                                            
                                                                                              
                                                                                              
                                      
_RESEARCH_GAP = (
    r"[\s,;:)\]\.]{0,4}"
    r"(?:[\(\[]\d{4}[\)\]][\s,]{0,3})?"
    r"(?:(?:a|an|the)\s+)?"
    r"(?:report|paper|study|lecture|address|briefing|monograph)?\s*"
    r"(?:published\s+)?"
    r"(?:by|for|at|under\s+the\s+auspices\s+of)\s+(?:the\s+)?")

                                                                                     
                                                                                         
                                                                                   
                                                                                        
                                                                                   
_RESEARCH_QUOTED = re.compile(
    r"[“\"](?=[^”\"]*\s)[^”\"]{10,180}[”\"]" + _RESEARCH_GAP + _RESEARCH_BODY)

                                                                                         
                                                                                             
                                                                 
                                                                                          
                                                                                   
                                                                                              
                                                                                           
                      
                                                     
                                                                               
                                
                                                                                              
                                                                                          
                                                                                  
_RESEARCH_UNQUOTED = re.compile(
    r"\b[A-Z][A-Za-z'’\-]+(?:[\s:]+[A-Za-z'’\-]+){1,11}" + _RESEARCH_GAP + _RESEARCH_BODY)

                                                                                         
                                                                                            
                                                                                        
                                                                                            
                                                                 
                                                                                            
                                                                                      
                                                                                   
_RESEARCH_BODY_YEAR = re.compile(
    r"\b[A-Z][A-Za-z'’\-]+(?:[\s:]+[A-Za-z'’\-]+){1,11}\s*,\s*"
    + _RESEARCH_BODY + r"\s*,\s*(?:1[89]|20)\d{2}\b")

                                                                                     
                                                                                      
                                                                           
                                                                                 
                                                                                 
                                                                                       
                                                                                       
                                                                                    
                                                                                   
                                                                      
_PUBLISHER_EDITION = re.compile(
    r"\(\s*[A-Z][A-Za-z&.'’\- ]{3,60},\s*(?:Rev\s+)?" + _ORD + r"[^)]{0,30}\)", re.I)


def _publisher_edition(s):
    """True for '(Stevens & Sons Limited, 5th Ed, 1890)' -- an imprint plus an edition."""
    return bool(_PUBLISHER_EDITION.search(str(s or "")))


_BOOK_PUBLISHER = re.compile(
    r"\b([A-Z][A-Za-z'’\-]+(?:[ :][A-Za-z'’\-,]+){1,12}?)"                             
    r"\s*(?:\([^)]{0,60}\)\s*)?"                                                                  
    r"\(\s*(?:" + _PUBLISHER + r")\s*,\s*(?:" + _ORD + r"\s*,\s*)?(?:1[89]|20)\d{2}\s*\)",
    re.I | re.U)
                                                                                            
                                                                                          
                                                                                                
                                                                                
_PUBLISHER_YEAR = re.compile(
    r"\(\s*(?:" + _PUBLISHER + r")\s*,\s*(?:1[89]|20)\d{2}\s*\)", re.U)

                                                            
                                                                                              
                                                                                           
                                                                                   
                                                                                 
_NOT_SCHOLARSHIP = re.compile(r"(?:dictionar|thesaur|word\s+finder)", re.I)

                                                                    
                                                                                        
                                                                                      
                                                                                        
                                                                       
_BOOK_EDITION = re.compile(
    r"\b(?!(?:LexisNexis|Butterworths|Sweet|Thomson|Wolters|Routledge|Blackstone\s+Press"
    r"|Academy\s+Publishing|Federation\s+Press)\b)"                                                  
    r"((?-i:[A-Z])[A-Za-z'\-]+(?:\s+(?:and|&)\s+(?-i:[A-Z])[A-Za-z'\-]+)?)"                        
    r"\s*[,:–—-]\s+((?-i:[A-Z])[A-Za-z'’:,\- ]{4,70}?)"                                              
                                                                                           
                                                                                         
                                                                                            
                                                                                           
                                                                    
    r"[ \t]{0,4},?[ \t]{0,4}\(?[ \t]{0,4}" + _ORD, re.I)                                  

                                                                                             
                                                                                              
                                                                                             
                                                                                           
 
                                                                                          
                                                                                       
                                    
 
                                                                                        
                                                                                 
                                                                                            
                                                                                             
                                                                                       
                                                                        
                                                                                            
                                                                                            
                                                                                       
                                         
 
                                                                                           
                                                                                           
                                                                      
_REFERENCE_WORK = re.compile(
    r"(?<!Lord\s)\b(?:"
    r"[A-Z][A-Za-z']{2,}(?:'s|’s)?\s+Laws\s+of\s+[A-Z][A-Za-z]{2,}"                                 
                                                                                
                                                                                    
                                                                                  
    r"|[A-Z][A-Za-z']{2,}(?:'s|’s)\s+Laws(?=\s*,?\s*[Vv]ol)"
                                                                           
                                                                                        
                                                                                       
                                                                                   
                                      
    r"|[A-Z][A-Za-z']{2,}(?:'s|’s)\s+Law\s+of\s+[A-Z][A-Za-z]{2,}(?:\s+[A-Z][A-Za-z]{2,}){0,3}"
    r"|Corpus\s+Juris(?:\s+Secundum)?"
                                                                                             
                                                                                           
                                                                                         
                                                                                       
    r"|Encyclopa?edia\s+of\s+[A-Z][A-Za-z]{2,}"
                                                                                            
    r"|Halb?sbury['’`]?s?\s+Statutes(?:\s+of\s+[A-Z][A-Za-z]{2,})?"
                                                                                                                          
                                                                                                              
    r"|Am(?:erican)?\.?\s?Jur(?:isprudence)?\.?(?:\s?(?:2d|3d|Second))?(?=\W)(?!\s*\[\s?\d)(?!\s{2,}\d)"
    r"|(?:The\s+Laws\s+of\s+Scotland\s*[:,]?\s*)?Stair\s+Memorial\s+Encyclop(?:a|æ)?edia"
    r"|Encyclop(?:a|æ)?edia\s+(?:Britannica|Americana)|World\s+Book\s+Encyclop(?:a|æ)?edia"
    r"|Chambers['’]?s?\s+Encyclop(?:a|æ)?edia|Wikipedia(?=\W)"
                                                                                                                     
                                                                                                                                       
                                                                                     
                                                                                        
                                                                                           
                                                                               
    r"|(?:[A-Z][A-Za-z'’]{2,}(?:'s|’s)?\s+)?Annotated\s+Statutes\s+of\s+[A-Z][A-Za-z]{2,}"
    r"|American\s+Jurisprudence(?!\s*\[\s?\d)(?!\s{2,}\d)"
    r"|Restatement\s+\(?(?:Second|Third)\)?\s+of\s+[A-Z][A-Za-z]{2,}"
    r")\b")

                                                                                        
                                                                                          
                                                                                          
                                                                                          
                                                                                         
                                                                                    
 
                                                                                          
                                                                                            
                                                                                             
                    
_TITLE_EDITION = re.compile(
    r"\b(?:The|An|A)\s+[A-Z][A-Za-z'\u2019\-]{2,}"
    r"(?:\s+(?:of|on|and|the|in|to|for|a|an)\s+[A-Za-z][A-Za-z'\u2019\-]{1,24}"
    r"|\s+[A-Z][A-Za-z'\u2019\-]{1,24}){1,8}"
                                                              
    r"[ \t]{0,4}[,:]?[ \t]{0,4}\(?[ \t]{0,4}(?:[a-z]+[ \t]{1,3}){0,4}(?i:" + _ORD + r")")


                                                                                     
                                                                                       
                                                                           
                                                                                     
                                                                                        
                                                                                       
                                                                                 
_TITLE_PINPOINT = re.compile(
    r"\(\s*(?!(?:See|Cf|Ibid|Lord|Lady|Sir|Dame|Mr|Mrs|Ms|Dr|Justice|Chief)\b)"
    r"(?:The\s+|An?\s+)?[A-Z][A-Za-z'’\-]{2,24}"
    r"(?:\s+(?:of|on|and|the|in|to|for)\s+[A-Za-z]{2,24}"
    r"|\s+[A-Z][A-Za-z'’\-]{2,24}){1,7}"
    r"\s+at\s+pp?\s*\d{1,4}")

                                                                                          
                                                                                            
                                           
_TITLE_YEAR_PINPOINT = re.compile(
    r"\b(?:The\s+|An\s+|A\s+)?[A-Z][A-Za-z'\u2019\-]{2,}"
    r"(?:\s+(?:of|on|and|the|in|to|for|a|an|as)\s+[A-Za-z][A-Za-z'\u2019\-]{1,24}"
    r"|\s*:\s*(?:The\s+|An?\s+)?[A-Z][A-Za-z'\u2019\-]{1,24}"
    r"|\s+[A-Z][A-Za-z'\u2019\-]{1,24}){2,8}"
    r"[ \t]{0,4},?[ \t]{0,4}\([ \t]{0,2}(?:[A-Z][A-Za-z'\u2019\- ]{2,28},[ \t]{0,2})?"
    r"(?:1[6-9]|20)\d{2}[ \t]{0,2}\)"
                                                                                            
                                                                                           
                                                                                             
    r"(?=\s*,?\s*(?:at\s+)?(?:pp?|paras?|chs?)\.?\s*\d)")


                                                                                 
                                                                                  
_NAMED_KIND_OF_WORK = re.compile(
    r"\b[A-Z][A-Za-z'’\-]{2,20}(?:\s+[A-Z][A-Za-z'’\-]{1,20}){0,2}"
    r"(?:\s+in\s+(?:his|her|their)|(?:'s|’s))\s+"
    r"(?:(?:1[6-9]|20)\d{2}\s+)?"
    r"(?:book|novel|text|treatise|monograph|essay|study)\s*,?\s+"
                                                                                
                                                                                 
                                                                                     
                                                                                    
                                                                                      
    r"(?P<t>(?:The\s+|An?\s+)?[A-Z][A-Za-z'’\-]{1,24}"
    r"(?:\s+(?:of|on|and|the|in|to|for)\s+[A-Za-z]{2,24}"
    r"|\s+[A-Z][A-Za-z'’\-]{2,24}){1,7})")

                                                                                  
_CLASSICAL_WORK = re.compile(
    r"\b(?:"
    r"Summa\s+Theologi[ac]a"
    r"|De\s+Legibus\s+et\s+Consuetudinibus\s+Angli[ae]e?"
    r"|The\s+Wealth\s+of\s+Nations"
    r"|Leviathan(?=\s*[,(]|\s+ch)"
    r"|The\s+Social\s+Contract"
    r"|The\s+Spirit\s+of\s+the\s+Laws"
    r"|De\s+Officiis|De\s+Republica|De\s+Legibus"
    r"|Nicomachean\s+Ethics"
    r"|The\s+Federalist(?:\s+Papers)?"
    r"|Democracy\s+in\s+America"
    r"|Utilitarianism(?=\s*[,(])"
    r"|The\s+Province\s+of\s+Jurisprudence\s+Determined"
    r"|The\s+Common\s+Law(?=\s*\((?:1[6-9]|20)\d{2}\))"
    r")", re.I)

_REF_VOLUME = re.compile(r"\s*vol(?:ume)?\.?\s*\d{1,3}(?:\(\d{1,2}\))?", re.I)

                                                                                      
                                               
_QUOTED_HEAD = re.compile(r"[\u201c\"]\s{0,2}([A-Za-z])")

_ARTICLE_SCIENCE_CITE = re.compile(
    r"(?<!\bThe )[“\"](?=[^”\"]*\s)[^”\"]{10,180}[”\"]\s*,?\s*"
    r"([A-Z][A-Za-z&’'\.]+(?:\s+(?:of|and|the|for|in)?\s*[A-Za-z&’'\.]+){0,7})"
    r"\s+\d{1,3}\s*\(\d{4}\)\s*\d{1,4}(?:\s*[-–]\s*\d{1,4})?")

                                                                                         
                                                                                            
                                                     
                                                    
                                                                                             
                                                                                            
                                               
 
                                                                                           
                                                                                             
                                                                                       
                                                                                          
                                
 
                                                                                             
                                                                                              
                                                                                              
                                                                                       
                                  
                                                                                      
                                                          
                                                                                             
                              
                                                                                           
                                                                                             
                                                                                            
                                                                                 
 
                                                                                           
                                                                                              
                                                                                          
                                                                                         
                                                                                       
                                                            
_REPORT_AUSPICES = re.compile(
    r"(?:a\s+)?report\s+([A-Z][A-Za-z'’\-]*(?:\s+(?:of|and|the|a|in|for)?\s*"
    r"[A-Z][A-Za-z'’\-]*){0,7})\s*,?\s*"
    r"published\s+(?:under\s+the\s+auspices\s+of|by)\s+"
    r"(?:the\s+)?([A-Z][A-Za-z'’\-]*(?:\s+(?:for|of|and|the)?\s*[A-Z][A-Za-z'’\-]*){0,6})")

_ARTICLE_SHORT_TITLE_CITE = re.compile(
    r"[“\"]([A-Z][A-Za-z\-]{2,14})[”\"]\s*,?\s*"
    r"[\(\[](\d{4})[\)\]]\s*,?\s*(\d{1,3})\s+([A-Z][A-Za-z.& ]{1,24}?)\s+(\d{1,4})\b")

_ARTICLE_TITLE_CITE = re.compile(
                                                                                           
                                                                                       
                                                                                         
                                                       
                                                                                         
                                                                                       
                                                                           
                                                                           
                                                                                         
                                                                                         
                                                                                         
                                                                               
                                                                                             
                                                                               
    r"(?<!\bThe )[“\"](?=[^”\"]*\s)[^”\"]{10,180}[”\"]\s*,?\s*"                   
                                                                                            
                                                                                           
                                                                                
                                                                                            
                                                                                             
                                                                                        
                                                                                          
                                                                                  
                                                                                          
                                                                                          
                                                                           
                                                                                     
                                                               
                                                                      
                                                       
                                                                                       
                                                                            
                                                                                   
                                                                                           
                                                                                            
                                                                                        
                                                                                            
                                                                                       
                                                                                   
                                                                                           
                                                                               
                                                                                            
                                                                                        
                                                                                        
                                                                                          
                                                    
    r"[\(\[](?:\d{1,2}\s+[A-Z][a-z]{2,9}\s+|[A-Z][a-z]{2,9}\s+\d{1,2},?\s+)?"
    r"\d{4}(?:\s*[-–]\s*\d{2,4})?[\)\]]\s*,?\s*(?:\d{1,3}(?:\(\d{1,3}\))?\s+)?"
                                                                                   
                                                                                       
                                                                                 
                                                                                     
                                                                                       
                                                                                     
                                                                                      
                                                                                        
                                                                                      
                                                                                       
                                                                                       
                                                                                          
                                                                                       
                                                                                      
                                                                                           
                                                                                     
                                                                                     
                                                                                          
                                                                                            
                                                                    
    r"[A-Z][A-Za-z.&'’,\- ]{1,80}?\s*(?:\(\d(?:st|nd|rd|th|d)\)\s*)?"
                                                                                      
                                                                                          
                                                                                     
                                           
    r"(?:[A-Z]?\d{1,4}|[ivxlcdmIVXLCDM]{2,10})\b")

                                                                                     
                                                                                           
                                                                                          
                                                                                          
                                                                                            
                                                                                        
                                                                                             
                
 
                                                                                    
                                                                                         
                                                                                        
                                                                                   
                                                                                        
                                                                               
                                                                                  
                                                                                    
                                                                                    
                                                                                   
                                                                                         
                                                                                
                                                                                        
                                                                             
_ARTICLE_NOPAGE_CITE = re.compile(
    r"(?<!\bThe )[“\"](?=[^”\"]*\s)[^”\"]{10,180}[”\"]\s*,?\s*"
    r"[\(\[]\d{4}(?:\s*[-–]\s*\d{2,4})?[\)\]]\s*,?\s*(?:\d{1,3}(?:\(\d{1,3}\))?\s+)?"
    r"[A-Z][A-Za-z.&'’,\- ]{2,60}?"
    r"(?:Journal|Review|Quarterly|Bulletin|Gazette|Reporter)"
    r"[A-Za-z.&'’,\- ]{0,40}?(?=[.;:)\]\n]|\s+at\s|$)")

                                                                                     
                                                                       
                                                                                 
                                                                                  
                                                                                     
                                                                                      
                                                                                       
                                                                    
                                                                                     
                                                                
 
                                                                                      
                                                                                       
                                                                      
 
                                                                                        
                                                                                           
                                                                                       
                                                                                   
                                                              
                                                                                       
                                               
 
                                                                                
                                                                                       
                                                                                        
                                                                                      
                                         
_FULLNAME_CITE = re.compile(
    r"[\(\[]\d{4}(?:[ \t]{0,2}[-–][ \t]{0,2}\d{2,4})?[\)\]][ \t,]{0,4}"
    r"(?:\d{1,3}(?:\(\d{1,3}\))?[ \t]{1,4})?"
    r"(?P<j>[A-Z][A-Za-z.&'’]{0,24}(?:[ ]{1,2}[A-Za-z0-9&][A-Za-z.&'’]{0,24}){1,9})"
    r"[ \t,]{1,4}(?:[A-Z]?\d{1,4})\b")
_FULLNAME_CITE_PRE = re.compile(
    r"(?<![A-Za-z])"
    r"(?P<j>[A-Z][A-Za-z.&'’]{0,24}(?:[ ]{1,2}[A-Za-z0-9&][A-Za-z.&'’]{0,24}){1,9})"
    r"[ \t]{0,2}[\(\[]\d{4}(?:[ \t]{0,2}[-–][ \t]{0,2}\d{2,4})?[\)\]]"
    r"[ \t,]{1,4}(?:[A-Z]?\d{1,4})\b")


def _flat_title(t):
    """The comparison form of a periodical's name: letters and digits, upper case."""
    return re.sub(r"[^A-Z0-9]+", "", str(t or "").upper())


                                                                                         
                                                                                      
                                                                                      
                                                                                       
                                                                                          
                                                                                      
                                                                                          
                       
 
                                                                                     
                                                                                    
                                                                                          
                                                                                 
 
                                                                                        
                                                                                         
                                                                                       
                                                                                       
_TITLED_JOURNAL_CITE = re.compile(
    r"\bin\s+(?:The\s+)?[A-Z][A-Za-z'’]+"
    r"(?:[ ,;:\-–]{1,3}[A-Za-z0-9'’]+){2,20}"
    r"[ \t]{0,2}[\(\[][ \t]{0,2}\d{1,3}[ \t]{1,3}"
    r"(?P<j>[A-Z][A-Za-z.&'’ ]{1,40}?)[ \t]{1,3}\d{1,4}\b")


_CARDIFF_CITE_RE = re.compile(
    r"\(\d{4}\)\s*,?\s+\d{1,3}(?:\(\d{1,3}\))?\s+([A-Z][A-Za-z.&'’,\- ]{1,70}?)\s+\d{1,4}\b")
_CARDIFF_CITE_NOVOL_RE = re.compile(
    r"\(\d{4}\)\s*,?\s+([A-Z][A-Za-z.&'’,\- ]{1,70}?)\s+\d{1,4}\b")


                                                                                       
                                                                                      
                                                                                
                                                                                        
                                                                                      
                                                                                     
                                                                                        
                                                                                           
                                                                                             
                                                     
                                                                                  
                                                                                             
                                                                             
_UNQUOTED_ARTICLE_CITE = re.compile(
    r"(?<![A-Za-z])(?:[A-Z][A-Za-z'\u2019\-]*\.?\s+){0,3}[A-Z][A-Za-z'\u2019\-]{2,}"
    r"(?:\s+(?:and|&)\s+(?:[A-Z][A-Za-z'\u2019\-]*\.?\s+){0,3}[A-Z][A-Za-z'\u2019\-]{2,})?"
    r",\s+"
    r"[A-Z][A-Za-z'\u2019\-]+"
                                                                                                   
                                                                                           
                                                                                        
                                                
                                                                                         
                                                                                         
                                                                                        
                                                                                          
                                                                                          
                                                                                    
                                                   
                                                                                       
                                                                                
                                                 
                                                                                          
                                                                                  
                                    
    r"(?:[ ,;:\-]{1,3}(?:[A-Za-z0-9'\u2019]+|\(\d{1,2}\))){2,25}"
    r"\s*[\(\[](?:1[89]|20)\d{2}(?:\s*[-\u2013]\s*\d{2,4})?[\)\]]\s*,?\s*"
    r"(?:\d{1,3}(?:\(\d{1,3}\))?\s+)?"
    r"(?P<j>[A-Z][A-Za-z.&'’ ]{1,40}?)"
    r"\s+(?:[A-Z]?\d{1,4})\b")


                                                                                       
                                                                                      
                                                                              
                                                                                      
                                                                   
                                                                                      
                                                                                       
                                                                                            
                                                                                            
                                                                                           
                                                              
_US_ARTICLE_CITE = re.compile(
    r"(?<![A-Za-z])[A-Z][A-Za-z'’\-]{2,}"
    r"(?:\s*(?:&|and)\s*[A-Z][A-Za-z'’\-]{2,})?"
                                                                                        
                                                                                           
                                                                                             
                                                                                          
                                                                                      
                                                                                            
                                                                                             
                                                                                            
                                                                                          
                                                       
                                                                                          
                                                                                    
                                                   
    r",\s+[A-Z][A-Za-z'’\-]+(?:[ ,;:\-]{1,3}[A-Za-z0-9'’]+){2,25},\s+"
    r"(\d{1,3}\s+[A-Z][A-Za-z.&'’ ]{2,40}?"
    r"(?:Review|Rev|Journal|Jnl|Quarterly|Psychologist|Psychology|Psychiatry|Science|Sciences|L\.?\s*Rev\.?|L\.?\s*J\.?|J\.?|L\.?|Probs\.?|Stud\.?|Lit\.?|Q\.?|Bull\.?|Ann\.?|Reg\.?|Pol\.?|Aff\.?))"
    r"\s+\d{1,4}(?:\s*,\s*\d{1,4})?\s*\((?:1[89]|20)\d{2}\)")
                                                                                               
                                                                 
                                                                            
                                                                                   
                                                                           
                                                                                                 
                                                                                                
                                                                                   
_US_ARTICLE_CITE_PIN = re.compile(
    r"(?<![A-Za-z])[A-Z][A-Za-z'’\-]{2,}"
    r"(?:\s*(?:&|and)\s*[A-Z][A-Za-z'’\-]{2,})?"
                                                                                                   
    r",\s+[A-Z][A-Za-z'’\-]*(?:[ ,;:\-]{1,3}[A-Za-z0-9'’]+){2,25},\s+"
    r"(\d{1,3}\s+[A-Z][A-Za-z.&'’ ]{2,40}?"
    r"(?:Review|Rev|Journal|Jnl|Quarterly|Psychologist|Psychology|Psychiatry|Science|Sciences|L\.?\s*Rev\.?|L\.?\s*J\.?|J\.?|L\.?|Probs\.?|Stud\.?|Lit\.?|Q\.?|Bull\.?|Ann\.?|Reg\.?|Pol\.?|Aff\.?))"
    r"\s+(?P<pg>\d{1,4})(?:\s*,\s*\d{1,4}(?:\s*[-–]\s*\d{1,4})?){0,4}"
    r"(?:\s*,?\s*(?:and\s+)?n{1,2}\.\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)?"
    r"\s*\((?P<yr>(?:1[89]|20)\d{2})\)")


                                                                             
                                                                                     
                                                                                      
                                                            
 
                                                                                      
                                                                           
                                                                                        
                                                                                             
                                                                                                
                                                                                         
                                                                                     
 
                                                                                        
                                                                                         
                                                                                           
                                                                                           
                                                                                            
                                                                                             
                                                                 
 
                                                                                        
                                                                                          
                                                                                            
                                                                                        
                                                                                          
                                                                         
 
                                                                                            
                                                                                           
                                                                                            
                                                                                          
                                                                                          
                                                    
 
                                                                               
                                                                                       
                                                                                          
                                                                                           
                                                                                         
_B19_YEAR = r"(?:1[5-9]\d{2}|20[0-2]\d)"
_B19_SUR = r"[A-Z][A-Za-z'’\-]{1,20}(?:\s+[A-Z][A-Za-z'’\-]{1,20})?"
_B19_AUTH = r"(?:[A-Z]\.\s*){1,4}" + _B19_SUR
_B19_AUTHORS = (r"%s(?:\s*,\s*(?:&\s*)?%s){0,5}(?:\s*,?\s*(?:&|and)\s*%s)?"
                r"(?:\s*,?\s+et\s+al\.?)?" % (_B19_AUTH, _B19_AUTH, _B19_AUTH))
                                                                                                  
                                                    
                                                                             
                                                                                             
                                                                       
                                                                 
                                                                                                
                                                                                   
                                                                                           
_LL_AUTH = r"(?:(?:[A-Z]\.\s*){1,4}|[A-Z]{1,4}\s+)" + _B19_SUR
_LOOSELEAF_BOOK = re.compile(
    r"(?<![A-Za-z.])" + _LL_AUTH + r"(?:\s*,\s*" + _LL_AUTH + r"){0,3}(?:\s*,?\s*(?:&|and)\s*" + _LL_AUTH + r")?"
    r"(?:,\s+with\s+the\s+assistance\s+of\s+" + _LL_AUTH + r")?,\s+"
    r"[A-Z][A-Za-z'’\-]+:?(?:\s+(?:[A-Z][A-Za-z'’\-]*|of|the|in|and|on|to|for|under|a|an|&|by|with):?){1,12}?"
    r"\s*\(loose-?leaf(?:\s+ed\.?)?\)")
LOOSELEAF = os.environ.get("JR_LOOSELEAF", "1") != "0"
_B19_VOL = r"(?:\d{1,3}[A-Z]?\s+|Vols?\.\s*[\d\-–,\s]{1,8})?"
                                                                                       
                                                                                        
                                                                                       
                                                                                          
                                               
_B19_SEP = r"[ ,:;&/?!\-‐‑‒–—―‘’“”'\"]{1,3}"
_B19_TOK = r"[A-Za-z0-9][A-Za-z0-9.]*"
_B19_TITLE = (r"[‘“'\"]?[A-Z][A-Za-z0-9.]*(?:%s%s){1,30}"
              % (_B19_SEP, _B19_TOK))
                                                                                           
                                                                                            
_B19_PIN = r"(?:[^()A-Z]|\([a-z0-9]{1,4}\)){0,40}"
                                                                                   
                                                                                   
                                             
                                                                  
                                                                                             
                                                                            
                                                                                               
                                                                                          
                                                                                          
                                                      
_B19_PAREN = (r"(?:\((?:[^()]{0,60}?[ .])?%s\)"
              r"|\((?:[^()]{0,40}?\()?loose[-‐-―\s]?leaf[^()]{0,40}\)+)" % _B19_YEAR)

_US_BLUEBOOK_BOOK = re.compile(
    _B19_VOL + _B19_AUTHORS + r",\s+" + _B19_VOL + _B19_TITLE + _B19_PIN + _B19_PAREN)

                                                                                       
                                                                                          
                                    
                                                      
                                                                       
                                                                               
                                                                                        
                                                                           
                                                                                         
                                            
 
                                                                                      
                                                                           
                                                                                     
                                                                                         
                                                                                        
                                 
                                                                                           
                                                                                             
                                                                                            
                                                                                             
                                                 
                                                                                       
                                                                                       
                                                                                           
                                                                        
_B19_TOK_NS = r"[A-Za-z0-9][A-Za-z0-9]*(?:\.(?![ \t]*[A-Z]))?"
_B19_TITLE_NS = (r"[A-Z][A-Za-z0-9]*(?:\.(?![ \t]*[A-Z]))?"
                 r"(?:%s%s){1,20}" % (_B19_SEP, _B19_TOK_NS))
_B19_EDITOR = (r"(?:[A-Z]\.\s*){1,3}[A-Z][A-Za-z'’\-]{1,20}"
               r"(?:\s*(?:&|and|,)\s*(?:[A-Z]\.\s*){1,3}[A-Z][A-Za-z'’\-]{1,20}){0,3}")
_US_EDITED_WORK = re.compile(
    _B19_VOL + _B19_TITLE_NS + _B19_PIN +
    r"\((?:[^()]{0,50}?[ .])?" + _B19_EDITOR +
    r"\s+(?:eds?|trans)\.?\s*" + _B19_YEAR + r"\)")


                                                                                           
                                                                                    
                                                                       
_OPINION_HEADER = re.compile(
    r"(?i)\bJJ?\.\s*,?\s*(?:concurring|dissenting)\b")


def _us_bluebook(s):
    """True where the WHOLE string is the Bluebook 'A. Author, Title <pinpoint> (year)'.

    ⚠️ THIS IS A VOUCHER, AND IT IS ANCHORED FOR THAT REASON. `_is_not_a_work` is applied
    twice over -- once to the match and once to the 130 characters of prose in front of it --
    and the second arm reads the SENTENCE THAT INTRODUCES the citation, which in a judgment
    discussing a commission or a statute contains the very words the veto bans:
        "... on which the Royal Commission drew in reaching its conclusions and making its
         recommendations (see, e.g., B. Slattery, 'First Nations and the Constitution: A
         Question of Trust' (1992), 71 Can. Bar Rev. 261 ...)"                [2024] SCC 10
    Slattery's article was discarded on the strength of a Royal Commission belonging to the
    sentence, not to him. The module already carries exactly this exemption for
    `_authored_edition`, `_authored_article` and `_authored_book`, whose comment says the
    match's own credentials outrank anything in the surrounding sentence; B19's shape is the
    same kind of credential and `_AUTHORED_BOOK` cannot see it, because it demands a CAPITAL
    immediately after the author comma and a quoted title opens with a quotation mark.
    `match`, not `search`, so a citation merely mentioned inside a longer span of prose
    vouches for nothing.
    """
    return bool(_US_BLUEBOOK_BOOK.match(str(s or "").strip()))


                                                                                          
                                                                                            
                                                                                      
                                                                                
                                                                                       
                                                                                   
                                                                                           
                                                                                         
                                                                                      
_LOOKBACK_CUT = re.compile(r"[.;\]]\s")


                                                                                         
                                                                           
                                                                                         
                                                                                     
                                                                                            
                                                                                    
_AUTHOR_OF_TITLE = re.compile(
    r"\bauthor\s+of\s+((?:The|A|An)\s+)?[A-Z][A-Za-z'’\-]+"
    r"(?:[ :,][A-Za-z'’\-]+){1,12}\s*,?\s*\(\s*(?:1[89]|20)\d{2}\s*\)")


                                                                             
                                                  
 
                                                                                           
                                                                                    
                            
 
                                                                                            
                                                                                            
                                                                                            
                                                                        
                                                                                           
 
                                                                                            
                                                                                           
                     
 
                                                                                         
                                                                                     
                                                                                            
                                                                                         
                                                                                           
                                                                                             
                                                                                 
                                                
 
                                                                                       
                                                                                     
                                                                                        
 
                                                                                           
                                                                                          
                                                                                             
                                                                                        
                                                                                   
_PERIODICAL_WORD = re.compile(
    r"(?i)(?:^|[\s,])(?:Journal|Jnl|Review|Rev|Revue|Rivista|Zeitschrift|Annales|Annuaire|"
    r"Bulletin|Yearbook|Quarterly|Studies|Problems|Psychology|Psychiatry|Criminology|"
    r"Sociology|Economics|Medicine|Science|Sciences|Biology|Digest|Forum)\b")

_NOT_A_PERIODICAL = re.compile(
    r"(?i)\b(?:Official\s+Journal|Law\s+Reports?|Weekly\s+Law|Government\s+Gazette|"
    r"Hansard|Official\s+Bulletin|Court\s+Bulletin|Parliamentary\s+Debates)\b")

_PERIODICAL_NAME_WORD = re.compile(r"[A-Za-z][A-Za-z'’&.\-]*")


def _names_a_periodical(name):
    """True where the journal name, read on its own, says it is a scholarly periodical.

    Two or more words, one of them a periodical word, and none of the gazettes. The
    two-word floor matters: "(1998) Review 12" is a pinpoint into something else, and a
    single bare periodical word is never a journal's whole name.
    """
    n = " ".join(str(name or "").split())
    if len(_PERIODICAL_NAME_WORD.findall(n)) < 2:
        return False
    if _NOT_A_PERIODICAL.search(n):
        return False
    return bool(_PERIODICAL_WORD.search(n))


def set_cardiff_acronyms(acronyms):
    """Install the 3,075-entry journal acronym list. Optional."""
    global CARDIFF_ACAD_ABBREVS
    CARDIFF_ACAD_ABBREVS = set(acronyms or ())


def set_cardiff_titles(titles):
    """Install the 2,113-entry FULL TITLE list -- the counterpart of the acronyms.

    `_FULLNAME_CITE` uses it as its positive anchor exactly as the abbreviation layer
    uses `CARDIFF_ACAD_ABBREVS`.
    """
    global CARDIFF_ACAD_TITLES
    CARDIFF_ACAD_TITLES = {_flat_title(t) for t in (titles or ()) if _flat_title(t)}

                                                                             
                                                                                
                                                                           
 
                                                                                        
                                                                                       
                                                                                         
                                                                                          
                                                                                           
 
                                                                                     
                                                                                 
                                                       
                                                                             
TREATISE_PATTERNS = []

                                                                             
                                                                                     
                                                                                             
                                                                                          
                                                                                          
                   
                                                                                       
                                                                           
                                                                                       
                                                              
 
                                                                                             
                                                                                             
                                                                    
                                                                      
                                                      
                                                                                         
                  
 
                                                                                           
                                                                                           
                                                                                         
_CHAPTER_WORK = re.compile(
    "(?:“(?P<c1>[A-Z‘'“][^”]{8,180})”"
    "|\"(?P<c2>[A-Z‘'][^\"]{8,180})\")"
    ",?\\s+in\\s+"
    "[A-Z][A-Za-z\'’\\-]+(?:[ ][A-Za-z\'’&\\-]+){0,8}"
    "\\s*\\(eds?\\b[^()]{0,120}?\\)")

                                                                                           
                                                                                            
                                                                              

                                                                             
                                                                                            
                                                                                         
                                                                                        

                                                                                                
                                                                                            
                                                                                        
                                         
_EDITORIAL_WORK = re.compile(
    r"(?i)\b(?:the\s+)?(?:editorial|case\s+note|note|comment(?:ary)?)\s*,\s*"
    r"[A-Z][^,;.]{10,120}?\s*,?\s+in\s+"
    r"[\(\[]\d{4}[\)\]]\s*[A-Za-z][A-Za-z .]{2,40}\s*\d{1,4}")

                                                                                            
                                                                            
                                                         
_PAPER_NO_WORK = re.compile(
    r"[A-Z][A-Za-z'’:,\- ]{10,120}?\s*,\s*"
    r"(?:[A-Z][a-z]+\s+)?\d{4}\s*,\s*"
    r"(?:The\s+)?[A-Z][A-Za-z ]{5,60}?\bPaper\s+No\s*\d{1,4}")

                                                                                              
                                                                                  
                                                                            
                                                                                            
                                                                         
_TITLE_BY_WORK = re.compile(
    r"\b(?:[Tt]he|[Aa]n?)\s+(?:[a-z]+\s+)?"
    r"[A-Z][A-Za-z'’\-]{3,60}"
    r"\s*\(\s*(?:1[6-9]|20)\d{2}\s*\)\s*by\s+"
    r"(?:Sir\s+|Dr\s+|Professor\s+|Prof\s+|Lord\s+){0,2}"
    r"[A-Z][A-Za-z'’.\-]*(?:[ ][A-Z][A-Za-z'’.\-]*){1,4}")

                                                                               
                                                                                           
                                                                                           
                                                                      
                                                                                            
                                                                                             
                                                                                      
                                                                                            
                                                                                         
                                                                           
 
                                                                                
                                                                                           
                                                          
                                                          
                                                          
                                                                                            
                                                                                        
                                                                                            
                                    
_REJECTED_WORK_PATTERNS = (_EDITORIAL_WORK, _PAPER_NO_WORK, _TITLE_BY_WORK)

                                                                             
                                                                                  
 
                                                                                         
                                                                                           
                                                                                          
                                                            
                                          
                                       
                                                                        
                                                                                   
                                                                                        
                                                                              
                                                                                  
 
                                                                                            
                                                                                             
                                 
 
                                                                                  
                                                                                             
                                                                                         
                                                   

                                                                                         
_TITLE_TOK = r"(?:[A-Z][A-Za-z'’\-]*:?|and|of|the|to|for|on|or|a|an)"

                                                           
                                                                            
                                                                                           
                                                                                    
                                                                                            
                                   
_TITLE_BY_TRIM = re.compile(
    r"(?<=\s)[A-Z][A-Za-z'’\-]{3,60}\s*\(\s*(?:1[6-9]|20)\d{2}\s*\)"
    r"(?=\s*by\s+(?:Sir\s+|Dr\s+|Professor\s+|Prof\s+|Lord\s+){1,3}"
    r"[A-Z][A-Za-z'’.\-]*(?:\s[A-Z][A-Za-z'’.\-]*){1,4})")

                                                                                          
                           
                                                                                    
                                                                       
                                                                                    
                                                                                  
                                                                                      
_PAPER_NO_TRIM = re.compile(
    r"[A-Z][A-Za-z'’\-]*:?"
    r"(?:\s+" + _TITLE_TOK + r"){2,14}"
    r"(?=\s*,\s*(?:[A-Z][a-z]+\s+)?(?:1[6-9]|20)\d{2}\s*,\s*"
    r"(?:The\s+)?[A-Z][A-Za-z ]{5,60}?\bPaper\s+No\.?\s*\d{1,4})")

                                                                                             
                                                                                        
                                                         
                                                                                              
                                                                                          
                                                                                              
                             
_AUTHOR_TITLE_AT = re.compile(
    r"(?<=\]\s)"
    r"[A-Z][A-Za-z'’\-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-z'’\-]+)?,\s+"
    r"(?:The|An?)\s+[A-Z][A-Za-z'’\-]*"
    r"(?:\s+" + _TITLE_TOK + r"){1,10}"
    r"(?=\s*,\s*at\s+\d)")

                                                                                           
                                                                                           
                                                                                        
                                         
                                                                                        
                                                                                           
                                                                                         
                                                                                           
                                                                                           
                                                                                           
                                                          
_EDITORIAL_CITE = re.compile(
    r"\b(?:[Ee]ditorial|[Cc]ase\s+note|[Cc]ommentary)\s*,\s*"
    r"[A-Z][^,;.]{10,120}?\s*,?\s+in\s+"
    r"[\(\[](?:1[6-9]|20)\d{2}[\)\]]\s*[A-Za-z][A-Za-z .]{2,40}?\s*\d{1,4}\b")

                                                                  
                                                                                      
                                                                    
                                                                                    
                                                                                         
                                                                                        
                                           
                                                                                           
                                                                                            
                                                                             
 
                                                                                               
                                                                                     
                                                                                        
                                                                                            
                                                                                    
_INIT_AUTHOR_IN_TITLE = re.compile(
    r"(?:[A-Z]\.?\s+){2,3}[A-Z][A-Za-z'’\-]{2,}"
    r"(?:\s+(?:and|&)\s+(?:[A-Z]\.?\s+){2,3}[A-Z][A-Za-z'’\-]{2,})?"
    r"\s+in\s+[A-Z][A-Za-z'’\-]{2,}"
    r"(?:\s+" + _TITLE_TOK + r"){1,8}"
    r"(?=\s+(?:treated|said|says|wrote|writes|stated|states|observed|observes|noted|notes|"
    r"argued|argues|suggested|suggests|explained|explains|described|describes|expressed|"
    r"expresses|concluded|concludes|commented|comments)\b)")

                                                                             
                                                             
 
                                                                                       
                                                                                          
                                                                        
                                                               
                                                               
                                                                                            
                                                                                            
                                                                        
 
                                                                                          
                                                                                            
                                                                        
                                                                                          
                                                                                    
                                                                                          
                                                                                        
                                                                                     
                                                                                    

                                                                                      
                                                                                   
_TITLE_TOK_WIDE = r"(?:[A-Z][A-Za-z'’\-]*:?|and|of|the|to|for|on|or|a|an|at|in)"
                                                                                             
_TITLE_TOK_JOIN = (r"(?:[A-Z][A-Za-z'’\-]*:?|and|of|the|to|for|on|or|a|an|at|in"
                   r"|but|not|with|from|by)")

                                                                                  
                                                                                       
                                                                                          
                                         
                                                                                          
                                                                                       
                                                                                   
                                                                                           
                                                                   
_SLT_NEWS = re.compile(
    r"(?<![A-Za-z])[A-Z][A-Za-z'’\-]*"
    r"(?:\s+" + _TITLE_TOK_JOIN + r"|\s*[-–]\s*" + _TITLE_TOK_JOIN + r"){1,14}"
    r"\s*,\s*(?:1[89]|20)\d{2}\s+SLT\s*\(\s*News\s*\)\s*\d{1,4}")

                                                                 
                                                                                    
                                                                                   
                                                                                       
                                                                                       
                                                                                 
                                                                                  
                                                                         
                                            
_UNPUBLISHED_WORK = re.compile(
    r"(?<![A-Za-z])[A-Z][A-Za-z'’\-]{2,}"
    r"(?:\s+" + _TITLE_TOK_WIDE + r"){2,12}"
    r"(?=\s*\(\s*unpublished\s*\))")

                                                                         
                                                                                     
                                                                                  
                                                                                        
                                                                                      
                                                                                        
                                                                                          
                                                                                           
                                                                          
                                            
_QUOTED_VOL_YEAR = re.compile(
    "(?:“(?P<q1>[A-Z][^”]{6,120})”"
    "|\"(?P<q2>[A-Z][^\"]{6,120})\")"
    r"\s*,?\s*(?=Vol(?:ume)?\.?\s*\d{1,3}\s*,?\s*\(\s*(?:1[6-9]|20)\d{2}\s*\))")

                                                                   
                                                                                    
                                                                                          
                                                                                         
                                                                                      
                                               
                                                                                        
                                                                                         
                                                                                        
                                                                                         
                                                                                           
                                                                                       
                                                                                      
                                     
_REVISER_EDITION = re.compile(
    r"(?<![A-Za-z])(?:The[ \t]+|An?[ \t]+)?[A-Z][A-Za-z'’\-]{2,}"
    r"(?:[ \t]+" + _TITLE_TOK_WIDE + r"){1,10}"
    r"[ \t]{0,4},?[ \t]{0,4}(?:\r?\n[ \t]{0,4}){0,2}"
    r"\([ \t]{0,2}[A-Z][A-Za-z'’\-]{2,24}"
    r"[ \t]{1,3}rev(?:ised)?\.?[ \t]{0,2},[ \t]{0,2}"
    r"(?:1[6-9]|20)\d{2}[ \t]{0,2}\)")

                                                           
                                                                                         
                                                                                   
                                                                                   
                                                                                         
                                                    
                                                                                          
                                                                                     
                                                                                           
                                                                                
                                                                                     
                                                   
                                                                                           
                                                                                          
                                                                                       
                            
                                     
_EDITION_OF_TITLE_BY = re.compile(
    r"\b\d{1,2}\s*(?:st|nd|rd|th)\s+ed(?:n|ition)?\.?\s*"
    r"\(\s*(?:1[6-9]|20)\d{2}\s*\)\s+of\s+(?:the\s+|an?\s+)?"
    r"[A-Z][A-Za-z'’\-]{2,}(?:\s+" + _TITLE_TOK_WIDE + r"){1,10}"
    r"\s+by\s+(?:Sir\s+|Dr\s+|Professor\s+|Prof\s+|Lord\s+|Mr\s+){0,2}"
    r"[A-Z][A-Za-z'’.\-]*(?:\s+[A-Z][A-Za-z'’.\-]*){1,4}")

                                                                                          
                                           
                                                                                      
                                                                                     
                                                                                       
                                                                                        
                                                                
 
                                                                                        
                                                                                    
                                                                                         
                                                                                            
                                                                             
                                                                                          
                                
 
                                                                                          
                                                                                           
                                                                                        
                                                                                         
                                                                                          
                                                                                            
                                                                              
_ARTICLE_ON_SUBJECT = re.compile(
    r"(?i)\b(?:an?|his|her|their|the|this)\s+(?:\w+\s+){0,2}"
    r"(?:article|essay|case\s+note|note|comment(?:ary)?)\s+(?:in|at)\s+"
    r"[\(\[](?:1[6-9]|20)\d{2}[\)\]]\s*(?:\d{1,3}\s+)?"
    r"[A-Za-z][A-Za-z.]{1,14}(?:[ ][A-Za-z][A-Za-z.]{1,14}){0,4}\s+\d{1,4}"
    r"\s+on\s+(?:the\s+)?(?-i:[A-Z][A-Za-z'’\-]+(?:\s+" + _TITLE_TOK_WIDE
    + r"|\s+No\.?\s*\d{1,4}){1,10})")

                                                                                 
                                                                          
                                                                                        
                                                                                          
                                                                                      
                                                                                          
                                                                 
                                                                                      
                                                                                     
                                                        
                                                                                           
                                                                         
                                                                               
                                                                                         
                                                          
                                                                                    
                                                                               
                                                                          
                                                                                         
                                                                                           
                                                                                        
                                                                                     
                                                                                           
        
                                                                                             
                                                                                
                                                                                           
                                                                                         
                                                                                          
                                           
                                                                                        
                                                        
                                                     
 
                                                                                            
                                                                                            
                                                                              
                                                            
 
                                                                           
                                                                                        
                                                                         
                                                                                        
                                                                               
                                                                                        
                                                                               
                                                                                        
 
                                                                              
 
                                                                                        
                                                                                         
                                                                                        
                                                                                         
                                                                                         
_B21_QT = ("(?:“[A-Z‘'“][^”]{8,200}”|\"[A-Z‘'][^\"]{8,200}\""
           "|‘[A-Z“'][^’]{8,200}’)")
_B21_TITLE = (r"(?:The\s+|An?\s+|La\s+|Le\s+|Les\s+)?[A-Z][A-Za-z0-9'’.]*"
              r"(?:[ ,:;&\-]{1,3}[A-Za-z0-9][A-Za-z0-9'’.]*){1,18}")
_CHAPTER_EDS = re.compile(
    _B21_QT + r",?\s+in\s+"
    r"(?:(?:[A-Z][A-Za-z'’.\-]*|and|&|et|von|van|de|du|der)\s+){1,10}eds?\.?,\s+"
    + _B21_TITLE)
_CHAPTER_YEAR = re.compile(
    _B21_QT + r",?\s+in\s+" + _B21_TITLE +
    r"[,;]?\s*\((?:1[5-9]|20)\d{2}\)")

                                                                                                  
                                                                                                     
                                                                                 
                                                     
                                                                                                        
_QUOTED_TITLE_EDITION = re.compile(
    r"[“\"][A-Z][^”\"\n]{8,150}[”\"]\s*,?\s*\(?\s*\d{1,2}(?:st|nd|rd|th)\s+[Ee]d(?:ition|n)?\b\.?")
                                                              
                                                                                
_AUTHOR_WORK_QUOTED = re.compile(
    r"\b[A-Z][a-z]{2,}(?:’s|'s)\s+(?:work|book|textbook|text|treatise|monograph|article)\s*,?\s*"
    r"[“\"‘][A-Z][^”\"’\n]{8,150}[”\"’]")
                               
                                                                                                       
_AUTHORS_COLON_TITLE_ED = re.compile(
    r"\b(?:[A-Z][a-z]+\s+){0,2}[A-Z][a-z]{2,}(?:\s+(?:and|&)\s+(?:[A-Z][a-z]+\s+){0,2}[A-Z][a-z]{2,})?\s*:\s+"
    r"[A-Z][A-Za-z'’,\- ]{10,150}?\s*\(\s*\d{1,2}(?:st|nd|rd|th)\s+[Ee]d(?:ition|n)?\.?(?:\s*,?\s*(?:1[89]|20)\d{2})?\s*\)")
                                                                                                      
                                                
_ARCHBOLD_EDITION = re.compile(
    r"\bArchbold(?:['’]s)?\s+(?:Hong\s+Kong|Criminal\s+Pleading[A-Za-z,& ]{0,40}?)\s*,?\s*"
    r"(?:\(?(?:19|20)\d{2}\)?|\d{1,2}(?:st|nd|rd|th)\s+[Ee]d)")
                                                                                        
_TW = r"(?:[A-Z][A-Za-z'’\-]+|of|and|the|in|on|for|to|a|its|their)"                        
_TITLE = r"[A-Z][A-Za-z'’\-]+(?:\s+" + _TW + r"){1,10}"                                                 
_ED = r"\d{1,2}(?:st|nd|rd|th)\s+[Ee]d(?:ition|n)?\.?"
_HON = r"(?:(?:Professor|Prof\.?|Sir|Dame|Dr\.?|Lord|Lady|Hon\.?|Mr\.?|Ms\.?)\s+)?"
_PERSON = _HON + r"(?:[A-Z][a-z]*\.?\s+){1,3}[A-Z][A-Za-z'’\-]+(?:\s+(?:QC|SC|KC))?"
                                                                      
                                                                                           
_TITLE_ED_AUTHOR_PUB = re.compile(r"\b" + _TITLE + r"\s*\(\s*" + _ED + r"\s*\)\s*,?\s*" + _PERSON
                                  + r"\s*\([^()\n]{0,50}(?:19|20)\d{2}\s*\)")
                                                                                                   
_TITLE_ED_PUB = re.compile(r"\b" + _TITLE + r",?\s+" + _ED + r",?\s*\([A-Z][A-Za-z&.,'’ ]{2,40}?,?\s*(?:19|20)\d{2}\)")
                                                                                                           
_TITLE_ED_BY = re.compile(r"\b" + _TITLE + r",?\s+" + _ED + r",?\s+by\s+" + _PERSON)
                                                                                                                     
_TWO_AUTHORS_TITLE_ED = re.compile(r"\b[A-Z][a-z]{2,}\s+(?:and|&)\s+[A-Z][a-z]{2,},?\s+" + _TITLE + r"\s*\(\s*" + _ED + r"\s*\)")
                                                                                                                                 
_HIS_BOOK = re.compile(r"\b(?:his|her|their)\s+(?:(?:influential|leading|well-known|seminal|classic|standard|celebrated)\s+)?"
                       r"(?:book|treatise|monograph|textbook)\s*,?\s*[“\"]?[A-Z][A-Za-z'’\-]+"
                       r"(?:(?:\s*[-–:]\s*|\s+)" + _TW + r"){2,12}")
                                                                                                                        
_TITLE_BY_AUTHOR_ED = re.compile(r"\b" + _TITLE + r"\s+by\s+" + _PERSON + r",?\s+" + _ED)
                                                                                                                      
                                                   
                                                                                       
                                                                       
_TITLE_ED_BARE = re.compile(
                                                                                                                    
                                                                                                                    
    r"(?<![A-Za-z'’])(?<![:–—\-]\s)(?<![:–—\-])"
    r"(?!(?:Article|Section|Cap|Chapter|Schedule|Rule|Order|Part|Regulation|Report|Annual|Volume|Vol|"
    r"Practice\s+Direction|Practice\s+Note|Basic\s+Law|The\s+Gazette|Gazette)\b)(?![^,\n]{0,40}\bLaws\s+of\b)"
    r"[A-Z][A-Za-z'’\-]+(?:\s+(?:of|and|the|in|on|for|to)){0,2}\s+[A-Z][A-Za-z'’\-]+(?:\s+" + _TW + r"){0,9}"
    r",?\s+" + _ED + r"(?=\s*(?:,|\(|at\b|paras?\b|pp?\b|vol\b|§|\[|\d))")
                                                                                      
_POSS_TREATISE = re.compile(
    r"(?<!the\s)(?<!The\s)\b(?!Kong|Court|Board|Council|Government|Department|Company|Bank|Commission|Parliament|State)"
                                                                                                            
                                                                                                                          
                                                                                      
    r"[A-Z][a-z]{2,}['’]s\s+(?:(?:[A-Z][a-z]+\s+){0,3}(?:Equity|Evidence)|(?:[A-Z][a-z]+\s+){1,3}(?:Law|Practice|Procedure|Contracts?|Torts?|Trusts?))\b"
    r"(?<!Basic Law)(?!\s*[\[(](?:1[6-9]|20)\d{2}[\])])(?=\s*(?:,|at\b|paras?\b|vol\b|§|\(|\[|\d))")
                                                                                 
_HK_PRACTICE = re.compile(r"\bHong\s+Kong\s+(?:Civil\s+(?:Court\s+Practice|Procedure)|Criminal\s+(?:Practice|Procedure)|Court\s+Forms)\b"
                          r"(?!\s+(?:Rules|Ordinance|Regulations))")
                                                                                                            
                                                                                                 
                                                                                                                       
                                                                                                       
                                                                                              
                                                                                                                   
                                                                                                                 
                                                                                     
_NZ_AUTH = r"(?:[A-Z][A-Za-z'’\-]*\.?\s+){1,3}[A-Z][A-Za-z'’\-]{2,}"
_NZ_BOOK = re.compile(
    r"\b" + _NZ_AUTH + r"(?:\s*(?:,|and|&)\s+" + _NZ_AUTH + r"){0,3}(?:\s+\((?:eds?\.?)\))?\s+"
    r"[A-Z][A-Za-z'’\-]*(?:(?:\s*[:,–—\-]\s*|\s+)(?:[A-Z][A-Za-z'’\-]*|of|and|the|in|on|for|to|a|an|its|their|under|after|before|(?:19|20)\d{2})){1,26}"
                                                                                                              
                                                                           
    r"\s*\((?!Nos?\.?\s|[A-Z]{2,5}\s*(?:Nos?\.?\s*)?\d|[^()\n]{0,80}(?:\bCourt\b|\bDivision\b|\bBench\b|\bTribunal\b|"
    r"\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\b))"
    r"(?:\d{1,2}(?:st|nd|rd|th)\s+(?:[A-Z][a-z]+\s+)?ed|(?:online\s+)?looseleaf\s+ed|[A-Z][A-Za-z&.'’]+)"
    r"[^()\n]{0,90}?(?:\((?:[A-Z]{2,4}|[A-Za-z ]{2,20})\)[^()\n]{0,40}?)?(?:(?:19|20)\d{2}|LexisNexis|Thomson\s+Reuters|Brookers)\)")
                                                                                                                    
_ORD_UNITS = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
_ORD_WORD = {w: i + 1 for i, w in enumerate(_ORD_UNITS)}
_ORD_WORD.update({"tenth": 10, "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14, "fifteenth": 15,
                  "sixteenth": 16, "seventeenth": 17, "eighteenth": 18, "nineteenth": 19, "twentieth": 20,
                  "thirtieth": 30, "fortieth": 40})
_ORD_TENS = {"twenty": 20, "thirty": 30, "forty": 40}
_ORD_EDITION = re.compile(r"\b(?:(?P<tens>Twenty|Thirty|Forty)[\s\-]+)?(?P<unit>" + "|".join(sorted(_ORD_WORD, key=len, reverse=True))
                          + r")\s+(?P<ed>[Ee]dition|[Ee]dn\b|[Ee]d\.)", re.IGNORECASE)


def _ordinal_editions(text):
    def rep(m):
        n = _ORD_WORD[m.group("unit").lower()] + (_ORD_TENS[m.group("tens").lower()] if m.group("tens") else 0)
        suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return "%d%s %s" % (n, suf, m.group("ed"))
    return _ORD_EDITION.sub(rep, text)


                                                                                                    
_ARTICLE_TITLE_CITE_SQ = re.compile(
    r"(?<!\bThe )‘(?=[^’]*\s)[A-Z][^’\n]{10,180}’\s*,?\s*[\[(](?:1[6-9]|20)\d{2}[\])]\s*"
    r"(?:\d{1,3}\s+)?(?P<ser>[A-Z][A-Za-z.&' ]{1,30}?)\s+\d{1,5}\b")

_EXTRA_WORK_PATTERNS = (_CHAPTER_WORK, _TITLE_BY_TRIM, _PAPER_NO_TRIM, _AUTHOR_TITLE_AT,
                        _EDITORIAL_CITE, _INIT_AUTHOR_IN_TITLE,
                        _SLT_NEWS, _UNPUBLISHED_WORK, _QUOTED_VOL_YEAR,
                        _REVISER_EDITION, _EDITION_OF_TITLE_BY, _ARTICLE_ON_SUBJECT,
                        _CHAPTER_EDS, _CHAPTER_YEAR,
                        _QUOTED_TITLE_EDITION, _AUTHOR_WORK_QUOTED, _AUTHORS_COLON_TITLE_ED, _ARCHBOLD_EDITION,
                        _TITLE_ED_AUTHOR_PUB, _TITLE_ED_PUB, _TITLE_ED_BY, _TWO_AUTHORS_TITLE_ED, _HIS_BOOK,
                        _TITLE_BY_AUTHOR_ED, _TITLE_ED_BARE, _POSS_TREATISE, _HK_PRACTICE, _NZ_BOOK)


                                                                                            
                                                                                               
                                                                                                                    
                                                                               
                                                                                            
                                                                                        
                                                                                               
                                                                                                
_TREATISE_NOT_A_WORK = frozenset("""
Aerospace Transportation and General Workers Union of Canada|Armstrong Carol Ann|Bench Family Division|
Business Innovation and Employment|Case Its Merits|Child Youth and Family|Children and Youths Sexual Offences Against Children|
Children's Law|Christopher's Law|Commissioners Uniform State Laws|Comment People|Commons Parliamentary Debates|
Composers Authors and Music Publishers of Canada|Conclusion Issue|Conclusion Jurisdiction|Conclusion Pith and Substance|
Conclusion Reasonable Expectation of Privacy|Conclusion Statutory Interpretation|Conference Labor|
Conference Private International Law|Corruption Drug Trafficking and Other Serious Crimes|Courts Trial|Decision Jurisdiction|
Duties Deceased Persons|Duties Imports|Elizabeth New Jersey|Health Safety and Compensation Commission|Hearings Amendments|
Imposed States Parties|Insolvency Restructuring and Dissolution|Interest Investments|Interest Loans|Interest Money Claims|
Interest Money Claims Act|Interest Mortgages|Issues Standard of Review|Justice Northern Ireland|
Liens Crops and Wool and Stock Mortgages|Limits Service|Lords Parliamentary Debates|Martial United States|
Mining Private Lands Act|Mining Private Lands Acts|Mining Private Property Act|Newfoundland Trial Division|
Ontario Official Report of Debates|Panel Multidistrict Litigation|Panel Take|Rates Foreign Legations and High Commissioners|
Reader's Digest|Responsibility Ministers|Ruling Voir Dire|Sabah Sarawak and Singapore|
Secretary Department of Community Services and Health|Statutes Regulations and Agreements|Subcommittee Administrative Practice and Procedure|
Subcommittee Antitrust and Monopoly|Subcommittee Constitutional Rights|Subcommittee Improvements|Subcommittee Institutions|
Subcommittee Investigations|Subcommittee Labor|Subcommittee Patents|Subcommittee Study of Monopoly Power|
Subcommittee Surface Transportation|Taxes Income|Tolls Privately Constructed Road Traffic|Trading Import and Export|War Land|
What's Law|Zealand United States|Lloyd's Law|
Halsbury Laws of England|Halsbury's Laws|Halsbury's Laws of England|Halsbury's Law of England|Halsbury's Laws of Australia|
Halsbury's Laws of Canada|Halsbury's Laws of Singapore|
Black's Law|Bouvier's Law|Wharton's Law|Tomlin's Law|Stroud Judicial Dictionary|Dukelow The Dictionary of Canadian Law|
Dictionary Historical Principles""".replace("\n", "").split("|"))


def _treatise_key_norm(key):
    return re.sub(r"[’�]", "'", str(key)).strip()


def set_treatise_dict(entries):
    """Compile 'Author Title' keys into patterns tolerant of how they are actually cited.

    One key covers 'Hogg on Constitutional Law of Canada', 'Hogg, Constitutional Law of
    Canada' and "Hogg's Constitutional Law of Canada", because the separator between the
    author and the title varies with the citing judge, not with the work.
    """
    global TREATISE_PATTERNS
    pats = []
    for key in entries or ():
        if _treatise_key_norm(key) in _TREATISE_NOT_A_WORK:
            continue
        toks = str(key).split()
        if len(toks) < 2:
            continue
        author, title = toks[0], toks[1:]
        body = r"\s+".join(re.escape(w) for w in title)
        pats.append(re.compile(
            re.escape(author) + r"(?:[’']s)?\s*(?:,\s*|\s+on\s+|\s+)(?:the\s+)?" + body
                                                                                    
                                                                                  
                                                                                  
                                                                               
                                                                                          
            + r"(?=.{0,45}(?:\d{1,2}(?:st|nd|rd|th)\s+[Ee]d|\b[Ee]d(?:ition)?\b|\((?:1[89]\d{2}|20[0-2]\d)\)))",
            re.IGNORECASE))
    TREATISE_PATTERNS = pats
    return len(pats)

                                                                             
                                                                                  
                                                                                     
                                                                                      
_TREATISE_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "data", "treatise_dict.json")


def load_treatise_dict(path=None):
    """Load the shipped treatise dictionary. Returns the number of patterns compiled."""
    p = path or _TREATISE_JSON
    try:
        with open(p, encoding="utf-8") as fh:
            return set_treatise_dict(json.load(fh).keys())
    except (OSError, ValueError):
        return 0


load_treatise_dict()


                                                                             
                               
 
                                                                                         
                                                                          
 
                                                                            
                                                                             
                                                                                  
                                                       
 
                                                                                        
                                                                                     
                                                                                         
                                                                                     
                                                                                      
 
                                                                                     
                                                                                 
                                                                             

                                                                               
                                                                                          
                                                                                          
                                                                                         
                                                                          
_AGENCY_REPORT = re.compile(
    r"\b((?:[A-Z][A-Za-z&'\-]+\s+){1,6}"
    r"(?:Annual\s+|Country\s+of\s+Origin\s+Information\s+|Human\s+Rights\s+|Progress\s+|Country\s+)?"
    r"Report)\s*(?:of|on|for|dated|\()\s*(?:\d{1,2}\s+)?(?:[A-Z][a-z]+\s+)?(?:1[89]|20)\d{2}")


_REPORT_TITLE = [
                                                                                         
                                                                                    
                                                                                         
                                                                                         
                                                                                     
                                                                                        
              
                                                          
    re.compile(r"\b(?:[A-Z][A-Za-z]+\s+){1,6}(?:Report|Reports),?\s*\((?:[^()]|\([^()]{0,20}\)){0,60}?(?:1[89]|20)\d{2}"),
                                                                                             
    re.compile(r"\bReports?\s+(?:of|by|to)\s+the\s+(?:(?:[A-Z][A-Za-z-]+|of|on|and|for|to|the)\s+){1,9}"
               r"(?:\([^)]{0,40}\)\s*)?\((?:[^()]|\([^()]{0,20}\)){0,60}?(?:1[89]|20)\d{2}"),
                                                                                  
                                                                 
    re.compile(r"\b(?:(?:Australian|Ontario|English|Scottish|New\s+Zealand|Singapore)\s+)?"
               r"Law\s+(?:Reform\s+)?Commission[^.;\n]{0,80}\((?:[^()]|\([^()]{0,20}\)){0,60}?(?:1[89]|20)\d{2}"),
    re.compile(r"\b(?:World\s+Health\s+Organi[sz]ation|Family\s+Law\s+Council|"
               r"American\s+Law\s+Institute|Royal\s+Commission|Law\s+Council)"
               r"[^.;\n]{0,90}\((?:[^()]|\([^()]{0,20}\)){0,60}?(?:1[89]|20)\d{2}"),
                                                                                  
                                                                                        
                                                                                        
                                                                                      
                                                                                      
                                                                                         
    re.compile(r"(?i)\breports?\s+(?:by|of|from)\s+the\s+(?:[A-Z][A-Za-z-]+\s+){1,6}"
               r"(?:Committee|Commission|Council|Board|Authority|Tribunal|Institute|"
               r"Organi[sz]ation|Bureau|Inquiry)\b"),
                                                                                        
                                                                                       
                                                                                        
                                                                                
    _AGENCY_REPORT,
                                                                                               
                                                                                                
                                                                                               
                                         
     
                                                                                          
                                                                                              
                                                                                                
                                                                                            
                                                                                              
    re.compile(r"(?i)\breports?\s+(?:by|of|from)\s+the\s+"
               r"(?:Committee|Commission|Council|Board|Authority|Tribunal|Institute|"
               r"Organi[sz]ation|Bureau|Inquiry|Agency|Department|Ministry|Panel)\s+"
               r"(?:for|on|of|into|to)\s+(?:the\s+)?(?:[A-Z][A-Za-z-]+\s*){1,6}"),
                                                                                     
                                                                                
    re.compile(r"\bYear\s?Book\s+[A-Z][A-Za-z]+\s+(?:1[89]|20)\d{2}"),

                                                                                              
                                                                                        
                                                                                                
     
                                                                                         
                                                                              
                                                                      
                                                                                
     
                                                                                         
                                                                                              
                                                                                          
    re.compile(r"\b(?:Scot(?:tish)?\s+|Northern\s+Ireland\s+|NI\s+|Irish\s+)?"
               r"Law\s+Com(?:mission)?\s+No\.?\s*\d{1,4}"),
    re.compile(r"\bCm(?:nd|d)?\.?\s*\d{3,5}\b"),
    re.compile(r"\b(?:Consultation|Discussion|Working|Issues|Green|White)\s+Paper"
               r"(?:\s+No\.?\s*\d{1,4})?"),
    re.compile(r"\bReports?\s+No\.?\s*\d{1,4}"),
                                                                                             
                                                                
    re.compile(r"\b(?:House\s+of\s+(?:Commons|Lords)|Senate|Joint)\s+"
               r"(?:Select\s+|Standing\s+)?Committee\s+on\s+(?:[A-Z][A-Za-z]+\s*){1,5}"),

                                                                                           
                                                                                    
]


def count_reports(text):
    """Distinct reports cited -- law reform, committee, parliamentary and agency.

    Deduplicated the same way the academic counter is: a report cited five times counts
    once, and a short form is merged into the long form that contains it.
    """
    work = _normalize_dotted_abbrevs(text or "")
    keys = set()
    for rx in _REPORT_TITLE:
        for m in rx.finditer(work):
            if _NOT_A_REPORT.search(m.group()):
                continue
            k = _norm_key(m.group())
            if k:
                keys.add(_fold_command_paper(k))
    out = []
                                                                                                  
                                                                                               
                                  
    for k in sorted(keys, key=lambda x: (-len(x), x)):
                                                                                       
                                                                                        
                                                                                 
                                                                                        
                                                                                           
                                                                                              
                                                                                            
                                                                                              
                                                                                               
                                                                                               
                                                         
        _ki = set(_NZLC_NO.findall(k))
        if any(k != o and _contains_words(o, k)
               and not (_ki and _NZLC_NO.findall(o) and not (_ki & set(_NZLC_NO.findall(o))))
               for o in out):
            continue
        out.append(k)
    return len(out)


_NZLC_NO = re.compile(r"\bnzlc\s*((?:r|ip|pp|sp|mp|cp)\s*\d{1,3})\b")
                                                                                                  
                                                                                                   
                                                                                          


                                                                                            
                                                                                              
                                                                                              
                                                                    
                                                                                           
                                                                                                
                                                                                             
                                                                                  
_NOT_A_REPORT = re.compile(
    r"(?i)\bofficial\s+reports?\b|\bparliamentary\s+debates\b|\bhansard\b"
    r"|\b(?:medical|psychiatric|psychological|expert|valuation|surveyor'?s|police)\s+report\b")


def _fold_command_paper(k):
    """'cmd 6902' and 'cmnd 6902' are the same paper cited two ways -- fold the series word."""
    return re.sub(r"^cm(?:nd|d)?\.?\s*(\d{3,5})$", r"cmd \1", k.strip())


def report_titles(text):
    """The reports themselves, for checking a count against the judgment."""
    work = _normalize_dotted_abbrevs(text or "")
    seen, out = set(), []
    for rx in _REPORT_TITLE:
        for m in rx.finditer(work):
            s = " ".join(m.group().split())
            k = _norm_key(s)
            if k and k not in seen:
                seen.add(k)
                out.append(s)
    return out
