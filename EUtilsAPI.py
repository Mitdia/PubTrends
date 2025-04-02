from typing import List, Dict
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


def geo_ids_to_summaries(geo_ids_list : List[str]) -> Dict[str, Dict[str, str]]:
    
    geo_query = ",".join(geo_ids_list)
    default_api_summary = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "gds",
        "id": geo_query,
    }
    response = requests.get(default_api_summary, params=params)
    root = ET.fromstring(response.text)
    geo_ids_params = {}
    for geo_id_entry in root.findall(".//DocSum"): 
        geo_id = geo_id_entry.find("Id").text
        geo_id_param = {}
        for child in geo_id_entry.findall(".//Item"):
            geo_id_param[child.attrib["Name"]] = child.text
        geo_ids_params[geo_id] = geo_id_param
    return geo_ids_params