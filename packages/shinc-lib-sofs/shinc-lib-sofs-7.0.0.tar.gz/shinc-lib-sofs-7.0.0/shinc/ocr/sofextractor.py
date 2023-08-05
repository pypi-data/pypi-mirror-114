try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import subprocess
import os
import time
import PyPDF2
import csv
import re
import pdfplumber
import datetime
from datetime import timezone
from dateparser_data.settings import default_parsers
from dateparser.search import search_dates
from datetime import timezone
from rdflib import Namespace,URIRef, BNode, Literal,Graph, plugin
from dateutil.parser import parse
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from uuid import uuid4
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from json import dumps
from bson.objectid import ObjectId 


SHC = Namespace("http://data.shinc.co.uk/")
NS = { 'foaf': FOAF, 'rdfs' : RDFS, "owl" : OWL, 'xsd' : XSD, 'rdf' : RDF, 'shc' : SHC}

class SOFImageExtractor:

    def __init__(self, image, tmppath='/tmp'):
        self.tmppath = tmppath
        self.image = image


    def ocr(self, image):
        fn = self.tmppath + "/" + str(ObjectId())
        cp = subprocess.run(["tesseract", "{}".format(image), "{}".format(fn)], check=True)
        if cp.returncode != 0:
            del environ[response_key]
            raise SOFException("Error running ocr " + image + " " + fn)
        else:
            time_to_wait = 5
            time_counter = 0
            while not os.path.exists(fn + ".txt"):
                time.sleep(1)
                time_counter += 1
                if time_counter > time_to_wait:break
            if os.path.exists(fn + ".txt"):
                result_file = open(fn + ".txt", 'r')
                result = result_file.read()
                result_file.close()
                os.remove(fn + ".txt")
            else:
                raise SOFException("Error writing OCR " + image + " " + fn + ".txt")
        return result

    def processOcrLine(self, n):
        return n.strip()

    def extract(self):
        #return list(map(self.processOcrLine, self.ocr(self.image).split("\n")))
        return self.ocr(self.image)



class SOFTextExtractor:

    DATEPATTERNS = [

        {
            "name": 'dd-mmmm-yyyy',
            "mask": "%d/%m/%Y",
            "regex": '((31(?!\-(feb(ruary)?|apr(il)?|june?|(sep(?=\b|t)t?|nov)(ember)?)))|((30|29)(?!\-feb(ruary)?))|(29(?=\-feb(ruary)?\-(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\-(jan(uary)?|feb(ruary)?|ma(r(ch)?|y)|apr(il)?|ju((ly?)|(ne?))|aug(ust)?|oct(ober)?|(sep(?=\b|t)t?|nov|dec)(ember)?)\-((1[6-9]|[2-9]\d)\d{2})',
            "delimiter": '-',
            "function":"date_parse",
            "type" : "dmy"
        },

        {
            "name": 'dd/mmmm/yyyy',
            "mask": "%d/%m/%Y",
            "regex": '((31(?!\/(feb(ruary)?|apr(il)?|june?|(sep(?=\b|t)t?|nov)(ember)?)))|((30|29)(?!\/feb(ruary)?))|(29(?=\/feb(ruary)?\/(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\/(jan(uary)?|feb(ruary)?|ma(r(ch)?|y)|apr(il)?|ju((ly?)|(ne?))|aug(ust)?|oct(ober)?|(sep(?=\b|t)t?|nov|dec)(ember)?)\/((1[6-9]|[2-9]\d)\d{2})',
            "delimiter": '/',
            "function":"date_parse",
            "type" : "dmy"
        },


        {
            "name": 'dd mmmm yyyy',
            "mask": "%d/%m/%Y",
            "regex": '((31(?!\ (feb(ruary)?|apr(il)?|june?|(sep(?=\b|t)t?|nov)(ember)?)))|((30|29)(?!\ feb(ruary)?))|(29(?=\ feb(ruary)?\ (((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\ (jan(uary)?|feb(ruary)?|ma(r(ch)?|y)|apr(il)?|ju((ly?)|(ne?))|aug(ust)?|oct(ober)?|(sep(?=\b|t)t?|nov|dec)(ember)?)\ ((1[6-9]|[2-9]\d)\d{2})',
            "delimiter": ' ',
            "function":"date_parse",
            "type" : "dmy"
        },

        {

            "name": 'mmmm dd yyyy',
            "mask": "%m/%d/%Y",
            "regex" : "(jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)[^A-Za-z0-9]+([1-9]|[1-3][0-9])[^A-Za-z0-9]+\d{4}",
            "delimiter" : "[^A-Za-z0-9]+",
            "function":"date_parse",
            "type":"mdy"    
        },

        {

            "name": 'dd?mm?yyyy',
            "mask": "%d/%m/%Y",
            "regex" : "(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]\d{4}",
            "delimiter" : "[\/\-\.]",
            "function":"num_date_parse",
            "type":"dmy"    
        },

        {

            "name": 'mm?dd?yyyy',
            "mask": "%d/%m/%Y",
            "regex" : "(0?[1-9]|1[012])[\.](0?[1-9]|[12][0-9]|3[01])[\.]\d{4}",
            "delimiter" : "[\/\-\.]",
            "function":"num_date_parse",
            "type":"mdy"    
        }

    ]

    TIMEPATTERNS = [

        {
            "name": 'hh:mm',
            "regex": "([01]\d|2[0-3]):([0-5]\d)",
            "delimiter": ':'
        },  

        {
            "name": 'hh.mm',
            "regex": "([01]\d|2[0-3])[.]([0-5]\d)",
            "delimiter": '.'
        },  

        {
            "name": 'hhmm',
            "regex": "([01]\d|2[0-3])([0-5]\d)",
            "delimiter": ''
        }  ,  

        {
            "name": 'hh mm',
            "regex": "([01]\d|2[0-3])[ ]([0-5]\d)",
            "delimiter": ' '
        },

        {
            "name": 'hh,mm',
            "regex": "([01]\d|2[0-3])[,]([0-5]\d)",
            "delimiter": ','
        }    

    ]
        

    def __init__(self, soflist, timepatterns=None, datepatterns=None):
        self.soflist = soflist
        if timepatterns:
            self.timepatterns = timepatterns
        else:
            self.timepatterns = SOFTextExtractor.TIMEPATTERNS
        if datepatterns:
            self.datepatterns = datepatterns
        else:
            self.datepatterns = SOFTextExtractor.DATEPATTERNS
        pass

    def extract(self, text, starttext=None, endtext=None, startdate=None, enddate=None, dateorder=None, timemask="hh:mm", tz=timezone.utc):
        sofs = SOF(id = str(ObjectId()))
        full_sofs = []
        summary_sofs = []
        date_count = startdate
        lines = text.splitlines()
        if starttext:
            started = False
        else:
            started = True
        for line in lines:
            text = line.lower()
            if started and self.textContainsSof(text):
                sof= self.extractLine(text, date_count, dateorder, timemask, tz)
                if sof.dateTimeFrom:
                    date_count = sof.dateTimeFrom
                full_sofs.append(sof) if sof not in full_sofs else sofs
                if next((x for x in self.soflist.softypes if x.id == sof.id and x.summary), None):
                    summary_sofs.append(sof) if sof not in summary_sofs else summary_sofs
            elif started and self.extractDate(text,dateorder):
                date_count = self.extractDate(text,dateorder)[0]['fulldate']
            else:
                if starttext and starttext.lower() in text:
                    print("started reading")
                    started = True
        sofs.sofs = full_sofs
        sofs.summary_sofs = summary_sofs
        return sofs
                    

                

    def extractLine(self, text, date_count, dateorder, timemask, tz=timezone.utc):
        text = text.lower()
        restext = text
        softype = self.textContainsSof(text)
        id = str(ObjectId())
        sof = SOFEvent(id, softype.id, softype.description)
        if softype.summary:
            sof.summary = True
        
        time_from = None
        time_to = None
        date_from = None
        date_to = None

        timetext = text

        dates = self.extractDate(text, dateorder)
        if dates:
            date_from = dates[0]['fulldate']
            date_to = None
            if len(dates) > 1:

                timetext = timetext.replace(dates[1]['datestring'], "")
                date_to = dates[1]['fulldate']
        else:
            date_from = date_count
            date_to = None



        times = self.extractTime(timetext, timemask)
        if times:
            time_from = times[0]
            time_to = None
            if softype.bounded and len(times) > 1:

                time_to = times[1]        

        if (times and not dates) and (softype.bounded and time_to) and (time_to < time_from):
            date_to = date_count + datetime.timedelta(days=1)
        if not time_from:
            time_from = date_from
        if date_from and time_from:
            sof.dateTimeFrom = self.generateDatetime(date_from, time_from,tz)
        if softype.bounded and time_to:
            if not date_to:
                date_to = date_from
            sof.dateTimeTo = self.generateDatetime(date_to, time_to,tz)
        return sof

    def textContainsSof(self, text):
        res = False
        for sof in self.soflist.softypes:
            if sof.name.lower() in text:
                return sof
        return res

    def extractTime(self, text, timemask=None):
        res = None
        if timemask:
            timepattern = next((x for x in self.timepatterns if x['name'] == timemask), None)
        else:
            timepattern = containsTime(text)
        if timepattern:
            res = []
            times = re.findall(timepattern['regex'], text)
            if times and len(times):
                res.append(datetime.time(int(times[0][0]), int(times[0][1])))
                if len(times) > 1:
                    res.append(datetime.time(int(times[1][0]), int(times[1][1])))    

        return res

    def containsTime(self, text):
        for mask in self.timepatterns:
            if re.findall(mask['regex'], text):
                return mask
        return None

    def parseTime(self, timestring, delimiter):
        return time(int(timestring.split(delimiter)[0]), int(timestring.split(delimiter)[1]),0)

    def parseDate(self, datestring, delimiter):
        return date(int(datestring.split(delimiter)[2]), int(datestring.split(delimiter)[1]), int(datestring.split(delimiter)[0]))

    
    def extSearch(self, text, regex):
        resultset=None
        while re.search(regex, text):
            if not resultset:
                resultset = []
            res = re.search(regex, text,re.IGNORECASE).group(0)
            resultset.append(res)
            text = text.replace(res, "", 1)
        return resultset


    def extractDate(self, text, dateorder):
        res = None
        text = text.lower()
        if dateorder:
            dates =  search_dates(text, settings={'DATE_ORDER': dateorder, 'RELATIVE_BASE': datetime.datetime(1925, 1, 1)})
        else:
            dates =  search_dates(text, settings={'RELATIVE_BASE': datetime.datetime(1925, 1, 1)})
        if dates and len(dates) > 0:
            for adate in dates:
               
                delimiters = list(filter(self.checkDelim, re.split("[a-zA-Z0-9]+", adate[0])))

                if  adate[1].year > 1970 and not (self.containsTime(adate[0])) and len(delimiters) == 2 and (delimiters[0] == delimiters[1]):
                    
                    if not res:
                        res = []
                    res.append({'datestring': adate[0], 'fulldate':adate[1]})   

        if not res:
            for datepattern in self.datepatterns:
                patternres = self.extSearch(text, datepattern['regex'])
                if patternres:
                    if not res:
                        res = []
                    mth = getattr(self, datepattern['function'])
                    for pattern in patternres:
                        if pattern and len(re.split('[^a-zA-Z0-9]+', pattern)) > 2:
                            res.append({'datestring':pattern, 'fulldate':mth(pattern,datepattern)})
                    return res

        return res

    def checkDelim(self, delim):
        return delim != ""

    def generateDatetime(self, dateobj, timeobj, tz):
        return datetime.datetime(year=dateobj.year, month=dateobj.month, day=dateobj.day,hour=timeobj.hour,minute=timeobj.minute, tzinfo=tz)


    def monthToNum(self, textMonth):
        return {
                'jan' : 1,
                'feb' : 2,
                'mar' : 3,
                'apr' : 4,
                'jun' : 6,
                'jul' : 7,
                'aug' : 8,
                'sep' : 9, 
                'oct' : 10,
                'nov' : 11,
                'dec' : 12,
                'january' : 1,
                'february' : 2,
                'march' : 3,
                'april' : 4,
                'may' : 5,
                'june' : 6,
                'july' : 7,
                'august' : 8,
                'september' : 9, 
                'october' : 10,
                'november' : 11,
                'december' : 12
        }[textMonth.lower()]



    def date_parse(self, datestring, datepattern):
        dateparts = re.split('[^a-zA-Z0-9]+', datestring)
        thirddate = int(dateparts[2])
        if datepattern['type'].lower() == 'dmy':
            firstdate = int(dateparts[0])
            seconddate = self.monthToNum(dateparts[1])
        else:
            firstdate = int(dateparts[1])
            seconddate = self.monthToNum(dateparts[0])
        return datetime.datetime(day=firstdate, month=seconddate, year=thirddate)

    def num_date_parse(self, datestring, datepattern):
        dateparts = re.split('[^a-zA-Z0-9]+', datestring)
        thirddate = int(dateparts[2])
        if datepattern['type'].lower() == 'dmy':
            firstdate = int(dateparts[0])
            seconddate = int(dateparts[1])
        else:
            firstdate = int(dateparts[1])
            seconddate = int(dateparts[0])
        return datetime.datetime(day=firstdate, month=seconddate, year=thirddate)


    def dd_mmmm_yyyy(self, result, delimiter):
        if len(delimiter) == 2:
            firstdate = result.split(delimiter[0])[0]
            remaingdate = result.replace(firstdate + delimiter[0],"",1)
            seconddate = remainingdate.split(delimiter[1])[0]
            thirddate = remainingdate.split(delimter[1])[1]
            return datetime.datetime(day=int(firstdate), month=self.monthToNum(seconddate), year=int(thirddate)) 
        else:
            fulldate = result.split(delimiter)
            return datetime.datetime(day=int(fulldate[0]), month=self.monthToNum(fulldate[1]), year=int(fulldate[2]))

    def mmmm_dd_yyyy(self, result, delimiter):
        string = re.sub("")
        if len(delimiter) == 2:
            seconddate = result.split(delimiter[0])[0]
            remaingdate = result.replace(firstdate + delimiter[0],"",1)
            firstdate = remainingdate.split(delimiter[1])[0]
            thirddate = remainingdate.split(delimter[1])[1]
            return datetime.datetime(day=int(firstdate), month=self.monthToNum(seconddate), year=int(thirddate)) 
        else:
            fulldate = result.split(delimiter)
            return datetime.datetime(day=int(fulldate[0]), month=self.monthToNum(fulldate[1]), year=int(fulldate[2])) 



class SOFPDFExtractor:
    def __init__(self, pdf):
        self.pdf = pdf

    def createTextFromPdf(self, pdf):
        content = ""
        with pdfplumber.open(pdf) as pdf:
            for page in pdf.pages:
                content += page.extract_text()
        
        return content

    def extract(self):
        return self.createTextFromPdf(self.pdf)



class SOFEvent:
    def __init__(self, id, type=None, description=None, time_from=None, time_to=None, date_from=None, date_to=None, summary=False):
        self.id = id
        self.eventType = type
        self.dateTimeFrom = date_from
        self.description = description
        self.dateTimeTo = time_to
        self.summary = summary

    def __eq__(self, other):
        if (isinstance(other, SOFEvent)):
            return self.eventType == other.eventType and self.dateTimeFrom == other.dateTimeFrom and self.description == other.description
        return False

class SOF:
    def __init__(self, id, sofs=[], summary_sofs=[]):
        self.id = id
        self.sofs = sofs
        self.summary_sofs = summary_sofs

    def add(self, sof):
        checked = False
        if not (x for x in self.sofs if x == sof):
            self.sofs.append(sof)

    def reorder(self):
        orderedsofs = sorted(self.sofs, key=lambda x: x.dateTimeFrom)
        self.sofs = orderedsofs



class SOFType:
    def __init__(self,id, name, description, bounded=False, notation=False, stoppage=False, display=False, summary=False):
        self.id = id
        self.name = name
        self.description = description
        self.bounded = bounded
        self.notation = notation
        self.stoppage = stoppage
        self.display = display
        self.summary = summary

class SOFList:
    def __init__(self, file):
        self.file = file
        self.sofs = None
        self.softypes = []

    def generate(self):
        return self.createListFromFile(self.file)

    def createListFromFile(self, file):
        self.sofs = Graph()
        f = open(file, "r")
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                name = row[0]
                uri = URIRef(SHC + name.replace(" ","-"))
                softype = SOFType(name.replace(" ","-"), name, name)
                self.sofs.add((uri, RDFS.label, Literal(name, lang="en")))
                self.sofs.add((uri, RDFS.subClassOf, SHC.Event))
                if row[1] == "1":
                    self.sofs.add((uri, RDFS.subClassOf, SHC.BoundedEvent))
                    softype.bounded = True
                if row[4] == "1":
                    self.sofs.add((uri, RDFS.subClassOf, SHC.DisplayableEvent))  
                    softype.notation = True
                if row[5] == "1":
                    self.sofs.add((uri, RDFS.subClassOf, SHC.SummaryEvent))  
                    softype.summary = True
                self.softypes.append(softype)  
        f.close()
        return self.sofs

    def getUriFromDescription(self, text):
        rows = self.sofs.query("SELECT ?type WHERE {?type rdfs:label '" + text + "' } ", initNs=NS)
        return str(rows[0])

    def getSofTypeFromDescription(self, text):
        return next((sof for sof in self.softypes if self.description == text), None)


class SOFException(Exception):
    pass
