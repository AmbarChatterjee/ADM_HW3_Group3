import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
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