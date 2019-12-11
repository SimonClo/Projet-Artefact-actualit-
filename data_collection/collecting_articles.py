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
    """Search for matching newspaper on the gallica website and return infos about the found newspaper
    
    Arguments:
        title {string} -- search string the newspaper should match
    
    Keyword Arguments:
        match_nums {int} -- number of results to be returned (default: {1})
    
    Returns:
        dict -- a dictionnary giving the title, the reference, the ocr quality and the number of issues
    """
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
    """find the references of all issues of a newspaper with a given name in a given time period
    
    Arguments:
        title {string} -- the name of the newspaper to search issues for
        yearStart {int} -- the beginning of the period to search issues for
        yearEnd {int} -- the end of the period to search issues for
    
    Keyword Arguments:
        ocrQuality {float} -- minimal ocr quality accepted (default: {0.6})
    
    Returns:
        list -- a list of all the references of the issues from the given newspaper
    """
    cqlQuery = f"dc.title any '{title}' and dc.type any fascicule"
    r = requests.get(f"http://gallica.bnf.fr/SRU?version=1.2&maximumRecords=1&operation=searchRetrieve&query={cqlQuery}")
    strContent = r.content.decode("utf-8")
    xmlContent = ElementTree.fromstring(strContent)
    newspaper_ref = xmlContent.find("srw:records/srw:record/srw:recordData/oai_dc:dc/dc:identifier",ns).text.split("/")[5]
    return get_issues_reference_by_newspaper_ref(newspaper_ref,yearStart,yearEnd,ocrQuality)

def get_issues_reference_by_newspaper_ref(ref,yearStart,yearEnd,ocrQuality=0.6):
    """find the references of all issues of a newspaper with a given reference in a given time period
    
    Arguments:
        ref {string} -- ark reference (official gallica reference) of the newspaper
        yearStart {int} -- beginning of the time period to search issues for
        yearEnd {int} -- end of the time period to search issues for
    
    Keyword Arguments:
        ocrQuality {float} -- the minimal ocr quality accepted (default: {0.6})
    
    Returns:
        list -- a list of all the references of the issues from the given newspaper
    """
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
    """retrieve the content of an issue given its reference
    
    Arguments:
        ref {string} -- ark reference of an the issue
    
    Returns:
        dict -- an issue dictionnary
        dict-keys :
            newspaper {string}: name of the newspaper the issue comes from
            date {string}: date of the issue
            raw_text {list of strings}: all text within the issue
            url {string}: the url the issue can be found at

    """
    r = requests.get(f"https://gallica.bnf.fr/ark:/12148/{ref}.texteBrut")
    soup = BeautifulSoup(r.content,features="html.parser")
    issue = {}
    infos = soup.select("p > strong")
    issue["newspaper"] = list(filter(lambda tag: tag.text=="Titre : ",infos))[0].parent.text[8:]
    issue["date"] = list(filter(lambda tag: tag.text=="Date d'édition : ",infos))[0].parent.text[17:]
    text_begining = soup.find("hr")
    issue["raw_text"] = [elt.text for elt in text_begining.find_next_siblings("p")]
    issue["url"] = f"https://gallica.bnf.fr/arl:/12148/{ref}"
    return issue
