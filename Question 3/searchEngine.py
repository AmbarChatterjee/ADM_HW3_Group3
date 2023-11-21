import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def conjunction_search(courses_df, vocabulary, inverted_index, query):
    # Tokenize and preprocess the query using the same pre-processing steps
    query = query.lower()
    query = query.split()
    stemmer = PorterStemmer()
    query = [stemmer.stem(word) for word in query]
    
    # Initialize a list to store document indices matching all query terms
    matching_indices = []
    
    # Initialize a set with the document indices that correspond to the first query term
    first_term_id = vocabulary.get(query[0])
    if first_term_id is not None:
        matching_indices = set(inverted_index.get(str(first_term_id), []))
    
    # For each subsequent term in the query, intersect the indices with the matching indices
    for term in query[1:]:
        term_id = vocabulary.get(term)
        if term_id is not None:
            matching_indices.intersection_update(inverted_index.get(str(term_id), []))

    # Create a new DataFrame with the matching rows
    matching_df = courses_df.iloc[list(matching_indices)]
    return matching_df

def tfidf_conjunction_search_topk(courses_df, vocabulary, inverted_index, query, vectorizer, X, k):
    # Tokenize and preprocess the query using the same pre-processing steps
    query = query.lower()
    query = query.split()
    stemmer = PorterStemmer()
    query = [stemmer.stem(word) for word in query]

    # Initialize a list to store document indices matching all query terms
    matching_indices = []

    # Initialize a set with the document indices that correspond to the first query term
    first_term_id = vocabulary.get(query[0])
    if first_term_id is not None:
        matching_indices = [idx for idx, _ in inverted_index.get(str(first_term_id), [])]

    # For each subsequent term in the query, intersect the indices with the matching indices
    for term in query[1:]:
        term_id = vocabulary.get(term)
        if term_id is not None:
            term_indices = [idx for idx, _ in inverted_index.get(str(term_id), [])]
            matching_indices = list(set(matching_indices) & set(term_indices))

    # Use a heap to maintain the top-k documents based on similarity scores
    heap = []

    # Iterate through the matching indices and update the heap
    for idx in matching_indices:
        # Handle NaN values in the 'description' column
        description = courses_df['description'].iloc[idx]
        if pd.notna(description):
            similarity_score = cosine_similarity(vectorizer.transform([' '.join(query)]), X[idx])[0][0]

            # Push the document with its similarity score onto the heap
            heapq.heappush(heap, (similarity_score, idx))

            # If the heap size exceeds k, pop the smallest element
            if len(heap) > k:
                heapq.heappop(heap)

    # Extract the indices of the top-k documents in reverse order
    topk_indices = [idx for _, idx in sorted(heap, key=lambda x: x[0], reverse=True)]

    # Create a new DataFrame with the top-k matching rows
    topk_matching_df = courses_df.loc[topk_indices].copy()

    # Add a new column for the similarity scores
    topk_matching_df['SimilarityScore'] = [cosine_similarity(vectorizer.transform([' '.join(query)]), X[idx])[0][0] for idx in topk_indices]

    # Select the desired columns
    return topk_matching_df[['courseName', 'universityName', 'description', 'url', 'SimilarityScore']]
