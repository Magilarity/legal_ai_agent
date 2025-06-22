import faiss
import numpy as np

def create_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index

def search_index(index, query_vector, top_k=3):
    D, I = index.search(np.array([query_vector]).astype('float32'), top_k)
    return I[0]
