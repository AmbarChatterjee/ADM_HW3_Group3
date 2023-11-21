import pandas as pd
import heapq

# Assuming you have the 'courses_df', 'vocabulary', and 'inverted_index' already defined

def calculate_score(document, weights, min_values, max_values, query):
    total_score = 0
    for key, weight in weights.items():
        if key in document and key in min_values and key in max_values:
            value = document[key]
            if key == "fees":
                # Handle fees separately
                if isinstance(value, (int, float)):
                    normalized_value = (value - min_values[key]) / (max_values[key] - min_values[key]) if (max_values[key] - min_values[key]) != 0 else 0
                    if not pd.isna(normalized_value):
                        total_score += normalized_value * weight
            elif isinstance(value, (int, float)):
                # Avoid division by zero and handle NaN values
                denominator = max_values[key] - min_values[key]
                normalized_value = (value - min_values[key]) / denominator if denominator != 0 else 0
                if not pd.isna(normalized_value):
                    total_score += normalized_value * weight
            elif isinstance(value, str):
                # If the value is a string, use a simple binary scoring (presence or absence)
                total_score += int(query.lower() in value.lower()) * weight
            else:
                # If the value is neither numeric nor string, ignore it for scoring
                pass
    return total_score, tuple(document.items())

def top_k_documents(documents, query, weights, k):
    # Create a min heap to store the top-k documents
    min_heap = []

    # Initialize min and max values for normalization
    min_values = {key: float('inf') for key in weights}
    max_values = {key: float('-inf') for key in weights}

    # Calculate scores and update min/max values
    for document in documents:
        score, doc_tuple = calculate_score(document, weights, min_values, max_values, query)
        heapq.heappush(min_heap, (score, doc_tuple))

        # Update min and max values for normalization
        for key in weights:
            if key in document and isinstance(document[key], (int, float)):
                min_values[key] = min(min_values[key], document[key])
                max_values[key] = max(max_values[key], document[key])

    # Get the top-k documents from the heap
    top_k = heapq.nlargest(k, min_heap, key=lambda x: x[0])

    # Convert the top-k documents to DataFrame
    columns = ['courseName', 'universityName', 'facultyName', 'isItFullTime',
       'description', 'startDate', 'fees', 'modality', 'duration', 'city',
       'country', 'administration', 'url', 'ProcessedDescription', 'currency',
       'fees (EUR)']
    result_df = pd.DataFrame([{key: value for key, value in dict(doc_tuple).items() if key in columns} | {"MyScore": score} for score, doc_tuple in top_k])

    return result_df