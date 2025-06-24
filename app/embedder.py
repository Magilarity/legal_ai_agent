from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, cast

vectorizer = TfidfVectorizer()

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    # toarray().tolist() returns List[List[float]]
    return cast(List[List[float]], vectorizer.fit_transform(chunks).toarray().tolist())