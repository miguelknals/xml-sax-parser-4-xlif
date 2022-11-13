# shttps://www.youtube.com/watch?v=x79MHadgpjQ
# martina conda environment
# based on:
# -Ejercio ChistesXML: Parser SAX en Python de SARO and SAT subjects (Universidad Rey Juan Carlos)
# -https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
# -https://cloud.ibm.com/docs/language-translator



import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

# pandas to export to excel
import pandas as pd
import xlsxwriter

# API imports and json to analyze json response
import requests
import json
# data need it to call IBM Watson 
# 
# api_key and api_url MUST be provided from your IBM Clour IBM Watson Language Translator 
#
api_key= "your_api_key" 
api_url= "your_api_url" 
url="{}/v3/identify".format(api_url)
headers =  {'Content-Type': 'text/plain;charset=utf-8'}

params ={'version': '2018-05-01'}

class class_WatsonConnectionInfo():
    def __init__(self, api_key,api_url,url, headers, params):
        self.api_key= api_key
        self.api_url= api_url
        self.url=url
        self.headers= headers
        self.params=params

WatsonConnectionInfo= class_WatsonConnectionInfo(api_key,api_url,url , headers, params )
   


class CounterHandler(ContentHandler):

    def __init__(self):
        self.inContent=False
        self.theContent=""
        self.inSegment=False
        self.segnum=0
        self.source=""
        self.target=""
        self.TranslationContent=[]
        
    def returnTranslationContent(self):
        return self.TranslationContent
            
    def startElement(self, name, attrs):
        if name == "segment":
            self.segnum+=1
            #print ("Seg # {}".format(self.segnum))
            self.inSegment=True
        elif name== "source":
            self.inContent=True
        elif name== "target":
            self.inContent=True
            
    def endElement(self, name):
        if name== "segment":
            if self.inSegment:
                self.inSegment=False
                self.TranslationContent.append([self.segnum, [self.source,self.target]])
            #print("---------------------------------------------")
        elif name=="source":
            self.source=self.theContent
            #print ("source:" + self.source )
        elif name ==  "target":
            self.target =self.theContent
            #print ("target:" + self.target ) 
            
        if self.inContent:
            self.inContent=False
            self.theContent=""
                       
    def characters(self, content):
        if self.inContent:
            self.theContent += content
        

def num_there(s):  # function that detects if word has numbers 
        # based on https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    return any(i.isdigit() for i in s) 

def func_clean_sentence(s,cutlenght): # removes comas, dots and words with numbers
    clean_s=""
    word_list= s.split()
    counter=0
    for word in word_list:
        word=word.replace(".", "")
        word=word.replace(",", "")
        if num_there(word) == False:
            clean_s +=" " + word    
            counter+=1
        if counter==cutlenght:
            break
    if clean_s=="": 
        clean_s=s
    return clean_s


def fucn_analyze_sentence(sentence, WatsonConnectionInfo  ):
    # connection info
    api_key=WatsonConnectionInfo.api_key
    api_url=WatsonConnectionInfo.api_url
    url=WatsonConnectionInfo.url
    headers=WatsonConnectionInfo.headers
    params=WatsonConnectionInfo.params
    if (sentence==""):
        sentence ="ERROR EMPTY SEGMENT"
    # clean sentence        
    #data = 'Language Translator translates text from one language to another'
    cutlengh=10 # 14 words max more than enought
    data = func_clean_sentence(sentence,cutlengh)   
    data=data.encode('utf-8') # otherwise non latin-1 chars will raise errors
        
    response = requests.post(url, headers=headers, params=params, data=data, auth=('apikey', api_key))
    # example of a json response 
    #response_json='{\n  "languages" : [ {\n    "language" : "en",\n    "confidence" : 0.9999978789709277\n  }, {\n    "language" : "nb",\n    "confidence" : 8.776130316639525E-7\n  }, {\n    "language" : "nn",\n    "confidence" : 3.7834233243501815E-7\n  }, {\n    "language" : "da",\n    "confidence" : 2.751659846395185E-7\n  }, {\n    "language" : "de",\n    "confidence" : 2.01589316950686E-7\n  }, {\n    "language" : "pt",\n    "confidence" : 1.4214510847576583E-7\n  }, {\n    "language" : "sq",\n    "confidence" : 5.3559399284835265E-8\n  }, {\n    "language" : "sk",\n    "confidence" : 3.589235615484988E-8\n  }, {\n    "language" : "sv",\n    "confidence" : 1.9196330119853727E-8\n  }, {\n    "language" : "tl",\n    "confidence" : 1.6809069086273966E-8\n  }, {\n    "language" : "af",\n    "confidence" : 1.3107716736051866E-8\n  }, {\n    "language" : "ro",\n    "confidence" : 1.231821600605283E-8\n  }, {\n    "language" : "hr",\n    "confidence" : 1.1175421894105305E-8\n  }, {\n    "language" : "et",\n    "confidence" : 1.0569025942605405E-8\n  }, {\n    "language" : "ca",\n    "confidence" : 1.0434435132123522E-8\n  }, {\n    "language" : "nl",\n    "confidence" : 9.941611302149668E-9\n  }, {\n    "language" : "eo",\n    "confidence" : 7.747794429815364E-9\n  }, {\n    "language" : "fr",\n    "confidence" : 7.68708796856969E-9\n  }, {\n    "language" : "ht",\n    "confidence" : 6.0698158760857485E-9\n  }, {\n    "language" : "ga",\n    "confidence" : 5.272395290998695E-9\n  }, {\n    "language" : "sl",\n    "confidence" : 4.17065806742737E-9\n  }, {\n    "language" : "is",\n    "confidence" : 3.427062594736478E-9\n  }, {\n    "language" : "hu",\n    "confidence" : 2.998168048233462E-9\n  }, {\n    "language" : "ku",\n    "confidence" : 2.729449533017453E-9\n  }, {\n    "language" : "eu",\n    "confidence" : 2.2993642088744596E-9\n  }, {\n    "language" : "pl",\n    "confidence" : 1.7557974791104756E-9\n  }, {\n    "language" : "cs",\n    "confidence" : 1.7510303394304716E-9\n  }, {\n    "language" : "vi",\n    "confidence" : 1.6662962091016883E-9\n  }, {\n    "language" : "es",\n    "confidence" : 1.626227987950868E-9\n  }, {\n    "language" : "cy",\n    "confidence" : 9.168835171354951E-10\n  }, {\n    "language" : "ms",\n    "confidence" : 7.88929352198843E-10\n  }, {\n    "language" : "fi",\n    "confidence" : 7.766626531382921E-10\n  }, {\n    "language" : "lv",\n    "confidence" : 4.3424741905439164E-10\n  }, {\n    "language" : "tr",\n    "confidence" : 3.547057060757583E-10\n  }, {\n    "language" : "az",\n    "confidence" : 2.2650246861664663E-10\n  }, {\n    "language" : "lt",\n    "confidence" : 1.6326582097024252E-10\n  }, {\n    "language" : "ja",\n    "confidence" : 7.57021517748543E-11\n  }, {\n    "language" : "it",\n    "confidence" : 5.877906001376456E-11\n  }, {\n    "language" : "mt",\n    "confidence" : 4.340297681418019E-11\n  }, {\n    "language" : "zh",\n    "confidence" : 4.244432769459518E-11\n  }, {\n    "language" : "zh-TW",\n    "confidence" : 3.547482471497031E-11\n  }, {\n    "language" : "so",\n    "confidence" : 1.7163675434559707E-11\n  }, {\n    "language" : "ko",\n    "confidence" : 1.6552878535011022E-11\n  }, {\n    "language" : "th",\n    "confidence" : 6.574844889217098E-12\n  }, {\n    "language" : "el",\n    "confidence" : 3.84526253008517E-12\n  }, {\n    "language" : "hi",\n    "confidence" : 2.76436936785491E-12\n  }, {\n    "language" : "ur",\n    "confidence" : 9.15021791778457E-13\n  }, {\n    "language" : "sr",\n    "confidence" : 5.612957784781863E-13\n  }, {\n    "language" : "my",\n    "confidence" : 5.563487814647191E-13\n  }, {\n    "language" : "mn",\n    "confidence" : 4.428480933988095E-13\n  }, {\n    "language" : "ar",\n    "confidence" : 3.1586830951321164E-13\n  }, {\n    "language" : "mr",\n    "confidence" : 2.2591166327971796E-13\n  }, {\n    "language" : "km",\n    "confidence" : 1.7216882235990302E-13\n  }, {\n    "language" : "ru",\n    "confidence" : 1.592494545295131E-13\n  }, {\n    "language" : "he",\n    "confidence" : 1.3060551412296534E-13\n  }, {\n    "language" : "lo",\n    "confidence" : 1.17010904044292E-13\n  }, {\n    "language" : "pa",\n    "confidence" : 1.1565127939893657E-13\n  }, {\n    "language" : "bn",\n    "confidence" : 1.1365064080855687E-13\n  }, {\n    "language" : "ky",\n    "confidence" : 1.068962102941264E-13\n  }, {\n    "language" : "ka",\n    "confidence" : 9.853131890277647E-14\n  }, {\n    "language" : "bg",\n    "confidence" : 6.736181548210492E-14\n  }, {\n    "language" : "ta",\n    "confidence" : 6.532126993242809E-14\n  }, {\n    "language" : "uk",\n    "confidence" : 6.051047523488232E-14\n  }, {\n    "language" : "ne",\n    "confidence" : 5.490750070157076E-14\n  }, {\n    "language" : "ml",\n    "confidence" : 5.088408042972086E-14\n  }, {\n    "language" : "kk",\n    "confidence" : 4.9783478466147074E-14\n  }, {\n    "language" : "te",\n    "confidence" : 4.240729887118598E-14\n  }, {\n    "language" : "be",\n    "confidence" : 4.2329215049496696E-14\n  }, {\n    "language" : "hy",\n    "confidence" : 4.2320853745362926E-14\n  }, {\n    "language" : "ps",\n    "confidence" : 4.1164287273958824E-14\n  }, {\n    "language" : "fa",\n    "confidence" : 3.8775428391060435E-14\n  }, {\n    "language" : "ba",\n    "confidence" : 2.0067059693804077E-14\n  }, {\n    "language" : "cv",\n    "confidence" : 1.750222498973511E-14\n  }, {\n    "language" : "pa-PK",\n    "confidence" : 1.7261392358828477E-14\n  }, {\n    "language" : "gu",\n    "confidence" : 1.654944739498609E-14\n  }, {\n    "language" : "si",\n    "confidence" : 9.045262200034714E-15\n  } ]\n}'
    response_json =response.text
     
    LangConfidenceMainDic = json.loads(response_json) # {'languages': [{...}, {...}, {...}, {...}, {...}, {...}, {...}, {...}, {...}, ...]}
    LangConfidenceMainDic = LangConfidenceMainDic['languages'] # [{'language': 'en', 'confidence': 0.9999978789709277}, {'language': 'nb', 'confide
    
    maxconfidence=0; confidence_es=0; confidence_pt=0
    maxlanguage=""
    have_es=False; have_pt=False    
    for langinfo in LangConfidenceMainDic:
        language=langinfo['language']
        confidence=langinfo['confidence']
        if confidence > maxconfidence:
            maxconfidence=confidence
            maxlanguage= language
        if language=="es":
            confidence_es=confidence
            have_es=True
        elif language=="pt":
            confidence_pt=confidence
            have_pt=True
        if have_pt and have_es:
            break # have both no need to search nothing else
    
    print (sentence)
    print ("max_lang {} max conf {}  es {} pt {}".format(maxlanguage, 
            maxconfidence, confidence_es, confidence_pt))
    
    
    return maxlanguage, maxconfidence, confidence_es, confidence_pt
    
def char_count(s):
    s.replace(" ", "")
    return len(s)
        
    

        

# main
if __name__ == "__main__"    :
    if len (sys.argv) <2:
        print ("Usage: xml-sax-parser-4-xlif.py <document> ")
        print ("")
        print (" <document> Document name to parse")
        quit()

    print ("Creating XLF_Parser and XLF_Handler")
    XLF_Parser = make_parser()
    XLF_Handler = CounterHandler()
    XLF_Parser.setContentHandler(XLF_Handler)
        
    #
    #xmlFile = open (sys.argv[1],"r",encoding="utf-8")
    #filecontents = xmlFile.read()
    #print (filecontents)
    print ("Reading and parsing the file")
    xmlFile = open (sys.argv[1],"r",encoding="utf-8")
    XLF_Parser.parse(xmlFile)
    TranslatedContent= XLF_Handler.returnTranslationContent()  
    # TranslatedContent, contais a list of[.., [seg#, [source, target]]

    print ("Calling the Watson Translator to obtaint lang estimation confidence values")
    ExcelList=[]
    nitems=10 # 0 means untill the end.
    tot_seg=len ( TranslatedContent )
    with open('log.txt', 'a', encoding="utf-8") as file_h:
        for segment_item in TranslatedContent:
            seg_num =segment_item[0]
            print ("Seg num -> {}/{}".format(seg_num, tot_seg))
            translation_info=segment_item[1] # segnum 
            source=translation_info[0] # source eng
            target=translation_info[1] # target nls
            maxlanguage, maxconfidence, confidence_es, confidence_pt = fucn_analyze_sentence(target, WatsonConnectionInfo)
            ESorPT="ES"
            if confidence_pt> confidence_es:
                ESorPT="PT"
            ExcelList.append([ESorPT, confidence_es, confidence_pt, target, source])        
            target=target.replace("\t","")
            source = source.replace("\t","")
            target=target.replace("\n","")
            source = source.replace("\n","")
            file_h.write("{}\t{}\t{}\t{}\t{}\n".format(ESorPT, confidence_es, confidence_pt, target, source))
            nitems-=1
            if nitems==0:
                break
            
   
    
    
    
    # finally write the excel:
    ExcelFile='ES-PT_Confidence_Analysis.xlsx'
    print ("Writing the results in an excel file {}".format (ExcelFile))
    df = pd.DataFrame(ExcelList)
    writer = pd.ExcelWriter(ExcelFile, engine='xlsxwriter')
    columns_names =["ES/PT", "Conf_ES", "Conf_PT","target", "source"]
    df.to_excel(writer, header=columns_names,sheet_name='ES-PT Confidence', index=False)
    writer.save()
        
    
    print ("EOP.")
        
    
    
    
    
    
        