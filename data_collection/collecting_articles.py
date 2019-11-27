import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from xml.etree import ElementTree
import logging

ns = {
    "ns7":"http://gallica.bnf.fr/namespaces/gallica/",
    "oai_dc":"http://www.openarchives.org/OAI/2.0/oai_dc/",
    "onix_dc":"http://bibnum.bnf.fr/NS/onix_dc/",
    "srw":"http://www.loc.gov/zing/srw/",
    "onix":"http://www.editeur.org/onix/2.1/reference/",
    "dc":"http://purl.org/dc/elements/1.1/"
}

def get_newspaper_reference(title,match_nums=1) :
    cqlQuery = f"dc.title any '{title}' and dc.type any fascicule"
    results = []
    r = requests.get(f"http://gallica.bnf.fr/SRU?version=1.2&maximumRecords={match_nums}&operation=searchRetrieve&query={cqlQuery}")
    strContent = r.content.decode("utf-8")
    xmlContent = ElementTree.fromstring(strContent)
    bar = Bar("finding matching newspaper",max=match_nums)
    for record in xmlContent.find("srw:records",ns) :
        periodic = {
            "title" : record.findall("srw:recordData/oai_dc:dc/dc:title",ns)[0].text,
            "reference" : record.findall("srw:recordData/oai_dc:dc/dc:identifier",ns)[0].text.split("/")[5],
            "mean_ocr" : record.find("srw:extraRecordData/nqamoyen",ns).text
        }
        try :
            r = requests.get(f"https://gallica.bnf.fr/services/Issues?ark=ark:/12148/{periodic['reference']}/date")
            strPeriodic = r.content.decode("utf-8")
            xmlPeriodic = ElementTree.fromstring(strPeriodic)
            periodic["issues"] = xmlPeriodic.attrib["total_issues"]
        except :
            periodic["issues"] = "unknown"
        results.append(periodic)
        bar.next()
    bar.finish()
    return results

def get_issues_reference_by_name(title,yearStart,yearEnd,ocrQuality=0.6):
    refs = []
    cqlQuery = f"dc.title adj '{title}' and dc.type adj 'fasicule' and (gallicapublication_date>='{yearStart}/01/01' and gallicapublication_date<='{yearEnd}/12/31') and acces adj 'fayes' and ocrquality>={ocrQuality}"
    r = requests.get(f"http://gallica.bnf.fr/SRU?version=1.2&collapsing=false&maximumRecords=50&operation=searchRetrieve&query={cqlQuery}")
    strContent = r.content.decode("utf-8")
    print(strContent)
    xmlContent = ElementTree.fromstring(strContent)
    for record in xmlContent.find("srw:records",ns) :
        print(record.find("srw:recordData/oai_dc:dc/dc:date",ns).text)

def get_issues_reference_by_newspaper_ref(ref,yearStart,yearEnd,ocrSuality=0.6):
    refs = []
    bar = Bar("fetching issues", max=yearEnd-yearStart+1)
    for year in range(yearStart,yearEnd+1):
        r = requests.get(f"https://gallica.bnf.fr/services/Issues?ark=ark:/12148/{ref}/date&date={year}")
        strIssues = r.content.decode("utf-8")
        try :
            xmlIssues = ElementTree.fromstring(strIssues)
            for issue in xmlIssues:
                refs.append(issue.attrib["ark"])
        except :
            logging.info(f"no issues for year {year}")
        bar.next()
    bar.finish()
    return refs

def get_issue_by_ref(ref):
    r = requests.get(f"https://gallica.bnf.fr/ark:/12148/{ref}.texteBrut")
    soup = BeautifulSoup(r.content)
    article = {}
    infos = soup.select("p > strong")
    article["title"] = list(filter(lambda tag: tag.text=="Titre : ",infos))[0].parent.text[8:]
    article["date"] = list(filter(lambda tag: tag.text=="Date d'édition : ",infos))[0].parent.text[17:]
    text_begining = soup.find("hr")
    article["text"] = "\n".join([elt.text for elt in text_begining.find_next_siblings("p")])
    return article