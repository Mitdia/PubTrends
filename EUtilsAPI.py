from typing import List
import requests
import xml.etree.ElementTree as ET


def get_relevant_geo_ids(pmids_list : List[str] = None) -> List[str]:
    pmids_query = ",".join(pmids_list)
    default_api_link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi" 
    params = {
        "dbfrom": "pubmed",
        "db": "gds",
        "id": pmids_query
    }
    response = requests.get(default_api_link, params=params)
    root = ET.fromstring(response.text)
    geo_ids = []
    for link in root.findall(".//LinkSetDb/Link"):
        geo_id = link.find("Id").text
        geo_ids.append(geo_id)
    return geo_ids
