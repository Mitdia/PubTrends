from typing import Dict, List
import numpy as np
from scipy.sparse import csr_matrix

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

from EUtilsAPI import get_relevant_geo_ids, geo_ids_to_summaries, summary_to_document


def text_to_vector(text_dict: Dict[str, str]):
    texts = list(text_dict.values())
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(texts)
    return feature_matrix


def embed_in_2d(matrix : csr_matrix, perplexity : int = 30) -> np.ndarray:
    tsne = TSNE(
        n_components=2,
        perplexity=min(perplexity, matrix.shape[0] - 1),
        init='random', 
    )
    return tsne.fit_transform(matrix)


def cluster(features : csr_matrix, k : int = 5) -> List[int]:
    clusterizator = KMeans(k)
    labels = clusterizator.fit_predict(features)
    return labels


def process_pmids(pmids : List[str], k : int) -> tuple[List[str], List[int], np.ndarray, Dict[str, List[str]]]:
    geo_ids = {}
    for pmid in pmids:
        geo_ids_list = get_relevant_geo_ids([pmid])
        for geo_id in geo_ids_list:
            if geo_id in geo_ids.keys():
                geo_ids[geo_id].append(pmid)
            else:
                geo_ids[geo_id] = [pmid]
    summaries = geo_ids_to_summaries(geo_ids.keys())
    documents = summary_to_document(summaries)
    feature_matrix = text_to_vector(documents)
    labels = documents.keys()
    clusters = cluster(feature_matrix, k)
    embedded_features = embed_in_2d(feature_matrix)
    return labels, clusters, embedded_features, geo_ids