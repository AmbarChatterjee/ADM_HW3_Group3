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
    #ensuring the text is string by converting to string
    text= str(text)
    # Lowercasing the text
    text = text.lower()
    
    # Tokenization (splitting text into words)
    words = text.split()
    
    # Removing punctuation and special characters
    table = str.maketrans('', '', string.punctuation)
    words = [word.translate(table) for word in words]
    
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Stemming using porter stemmer
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    
    # Joining the processed words back into a single string
    processed_text = ' '.join(words)
    
    return processed_text


# Function to extract the bigger numeric fees value and currency symbol
def extract_fees(row):
    #converting row to string to deal with it using regex
    row = str(row)

    # Regex to Handle all the currencies in the dataframe
    fees_list = re.findall(r'((?:(?:\d[\d,]*)\s?(?:[£$€]|(?:EUR|CHF|ISK|HK\$|RMB|CZK|SEK|HKD|SGD\s\$|JPY|QR)))|(?:(?:[£$€]|(?:EUR|CHF|ISK|HK\$|RMB|CZK|SEK|HKD|SGD\s\$|JPY|QR))\s?(?:\d[\d,.]*)))', row)
    #necessary check when regex is not detecting anything
    if not fees_list:
        return None, None
    #creating empty lists to store data
    values = []
    currencies = []
    for i in fees_list:
        currency_match = re.search(r'(?:[£$€]|(?:EUR|CHF|ISK|HK\$|RMB|CZK|SEK|HKD|SGD\s\$|JPY|QR))', i)
        value_match = re.search(r'(?:\d[\d,]*)', i)

        # Checking if both currency and value are found
        if currency_match and value_match:
            currency = currency_match.group()
            value_str = value_match.group()
            #dealing with the '.' in Euro and ISK currencies as € 15.000 = EUR 15,0000
            if currency=='€' or currency=='ISK':
                value=value_str.replace('.', ',')
                value=value_str.replace(',', '')
                value=float(value)
            # Remove commas and convert to float for all other currencies
            value = float(value_str.replace(',', ''))
            values.append(value)
            currencies.append(currency)
    if values:
        #we consider only the maximum of the fees values in the cell
        max_value = max(values)
        index_of_max = values.index(max_value)
        #if there are various currencies in the same cell, only maximum value currency will be taken.
        max_currency = currencies[index_of_max]
        return max_value, max_currency
    else:
        return None, None


#function to get exchange rates using api suggested by ChatGPT
def get__currency_rates_api(from_currency, api_key='ef1ff6e934f5cc8c6b3aebce'):
    #creating the url using the api key and currency: as per the api documentation
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}'
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates']

#function to convert the currencies: here we are using all the specific currencies found in our dataset
def convert_currency(exchange_rates, amount, from_currency):
    try:
        if from_currency == '£':
            rate= exchange_rates['GBP']
            return "{:.2f}".format(amount/rate)
        elif from_currency == '€' or from_currency == 'EUR':
            rate= exchange_rates['EUR']
            return "{:.2f}".format(amount/rate)
        elif from_currency == '$' or from_currency == 'USD':
            rate= exchange_rates['USD']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'ISK':
            rate= exchange_rates['ISK']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'HK$' or from_currency == 'HKD':
            rate= exchange_rates['HKD']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'RMB':
            rate= exchange_rates['CNY']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'CZK':
            rate= exchange_rates['CZK']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'SEK':
            rate= exchange_rates['SEK']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'JPY':
            rate= exchange_rates['JPY']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'CHF':
            rate= exchange_rates['CHF']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'QR':
            rate= exchange_rates['QAR']
            return "{:.2f}".format(amount/rate)
        elif from_currency == 'SGD $':
            rate= exchange_rates['SGD']
            return "{:.2f}".format(amount/rate)
        else:
            return amount
    except Exception as e:
        print("Error: ", str(e))
        return None