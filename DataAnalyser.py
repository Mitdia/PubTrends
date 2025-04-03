from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer


def text_to_vector(text_dict: Dict[str, str]):
    texts = list(text_dict.values())
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(texts)
    return feature_matrix



