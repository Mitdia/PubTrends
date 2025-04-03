from typing import Dict
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE


def text_to_vector(text_dict: Dict[str, str]):
    texts = list(text_dict.values())
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(texts)
    return feature_matrix


def embed_in_2d(matrix : csr_matrix, perplexity : int = 30) -> np.ndarray:
    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        init='random', 
    )
    return tsne.fit_transform(matrix)

