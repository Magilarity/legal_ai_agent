from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()


def embed_chunks(chunks):
    return vectorizer.fit_transform(chunks).toarray().tolist()
