from typing import List, Dict
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


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


def scrape_overall_design_by_gse(gse_id: str) -> str:
    url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try: 
        overall_design = soup.find(string="Overall design").find_next().text
    except AttributeError:
        overall_design = ""
        print(gse_id, "- Fail!")
        print(soup.find(string="Overall design"))
    return overall_design


def summary_to_document(summaries : Dict[str, Dict[str, str]], fields : List[str] = None) -> Dict[str, str]:
    if fields is None:
        fields = ["title", "gdsType", "summary", "taxon"]
    documents = {}
    for geo_id, summary in summaries.items():
        document = ""
        for field_name in fields:
            document += field_name + ": " + summary[field_name] + "\n"
        overall_design = scrape_overall_design_by_gse("GSE" + summary["GSE"])
        document += "Overall design: " + overall_design
        documents[geo_id] = document
    return documents
