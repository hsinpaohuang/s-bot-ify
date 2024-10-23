from numpy import float64
from numpy.typing import NDArray
from scipy.spatial.distance import cosine
from typing import cast

def find_max_similarity(doc_term_matrix: NDArray[float64], query_vector: NDArray[float64]):
    max_similarity = 0
    max_index = 0

    for i, doc in enumerate(doc_term_matrix):
        similarity = 1 - cosine(
            query_vector,
            cast(NDArray[float64], doc.toarray().flatten()),
        )

        if similarity > max_similarity:
            max_similarity = similarity
            max_index = i

    return max_index, float(max_similarity)
