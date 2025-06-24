import faiss
import numpy as np
from typing import List, cast


def search_index(
    index: faiss.IndexFlatL2, query_vector: List[float], top_k: int = 3
) -> List[int]:
    distances, indices = index.search(np.array([query_vector], dtype=np.float32), top_k)
    # indices[0].tolist() returns List[int]
    return cast(List[int], indices[0].tolist())
