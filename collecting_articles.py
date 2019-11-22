import requests
from xml.etree import ElementTree

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
    for record in xmlContent.find("srw:records",ns) :
        results.append({
            "title" : record.findall("srw:recordData/oai_dc:dc/dc:title",ns)[0].text,
            "reference" : record.findall("srw:recordData/oai_dc:dc/dc:identifier",ns)[0].text.split("/")[5],
            "mean_ocr" : record.find("srw:extraRecordData/nqamoyen",ns).text
        })
    return results