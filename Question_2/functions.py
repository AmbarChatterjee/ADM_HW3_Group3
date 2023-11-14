import pandas as pd
import os
import string
import requests
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from forex_python.converter import CurrencyRates

#function to convert each of the TSV to dataframe
def TSV_to_dataframe(column_names, folder_name, num_files):
    # Create an empty list to store DataFrames
    dfs = []

    # Define the folder path where your TSV files are located
    folder_path = folder_name

    # Loop through each TSV file and append its data to the list of DataFrames
    for i in range(1, num_files + 1):
        file_name = f'course_{i}.tsv'
        file_path = os.path.join(folder_path, file_name)

        # Check if the file exists before trying to load it
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                next(file)  # Skip the first row (header)
                data_row = file.readline()  # Read the second row (data)
                data_list = data_row.strip().split('\t')
                data_dict = {col: value for col, value in zip(column_names, data_list)}
                df = pd.DataFrame(data_dict, index=[0])
                dfs.append(df)

    # Concatenate the list of DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df
#function to perform text pre-processing
def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    
    # Tokenization (split text into words)
    words = text.split()
    
    # Removing punctuation and special characters
    table = str.maketrans('', '', string.punctuation)
    words = [word.translate(table) for word in words]
    
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    
    # Joining the processed words back into a single string
    processed_text = ' '.join(words)
    
    return processed_text
#function to preprocess text
def preprocess_text2(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Remove punctuation and convert to lowercase
    tokens = [word.lower() for word in tokens if word.isalpha()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Stem the words
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    return " ".join(tokens)

# Function to extract the bigger numeric fees value and currency symbol
def extract_fees(row):
    # Handle Euro values
    euro_values = re.findall(r'\d[\d,.]*\s?€', row)
    euro_values = [s.strip() for s in euro_values]
    
    if euro_values:
        for value in euro_values:
            max_fee_euro = float(re.search(r'[\d.]+(?:[.,]\d+)?', value.replace('.', '').replace(',', '.')).group().replace('.', ''))
        return max_fee_euro, '€'
    
    # Handle other currencies
    other_values = re.findall(r'[\d,]+(?:[.,]\d+)?\s?[$£]?', row)
    other_values = [s.strip() for s in other_values]
    
    if not other_values:
        return None, None
    
    fees = []
    max_fee = None
    
    for value in other_values:
        # Extract the numeric part
        fee_value = float(re.search(r'[\d,]+(?:[.,]\d+)?', value.replace(',', '').replace(',', '.')).group().replace(',', ''))
        
        # Extract the currency symbol
        currency_match = re.search(r'[£$]', value)
        
        if currency_match:
            currency = currency_match.group()
        else:
            # Handle the case where £ is not followed by a space
            currency_match = re.search(r'[$£]', row)
            currency = currency_match.group() if currency_match else None
        
        fees.append((fee_value, currency))
    max_fee, currency = max(fees)
    
    return max_fee, currency

#function to get exchange rates using api suggested by ChatGPT
def get__currency_rates_api(from_currency, api_key='ef1ff6e934f5cc8c6b3aebce'):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}'
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates']

#function to convert the currencies
def convert_currency(exchange_rates, amount, from_currency):
    try:
        if from_currency == '£':
            rate= exchange_rates['GBP']
            return "{:.2f}".format(amount/rate)
        elif from_currency == '€':
            rate= exchange_rates['EUR']
            return "{:.2f}".format(amount/rate)
        else:
            return amount
    except Exception as e:
        print("Error: ", str(e))
        return None