# ADM Homework 3 - Master's Degrees from All Over!

This repository contains code and analysis for ADM Homework 3 on building a search engine for master's degree programs.

## Repository Structure

The repository contains the following key files and folders:

- `main.ipynb`: Jupyter notebook containing the code and analysis for the homework, including data collection, preprocessing, search engine implementation, new scoring function, and map visualization.

- `GeneratedFiles`: Folder containing generated output from `main.ipynb`, including:
  - `courses_data_processed.tsv`: Preprocessed dataset 
  - `folderTSV`: Folder containing parsed TSV files
  - `inverted_index.json`: Inverted index for search engine
  - `tfidf_inverted_index.json`: TF-IDF inverted index
  - `urls.txt`: List of degree webpage URLs
  - `vocabulary.txt`: Vocabulary mapping words to IDs
  - `Map.html`: Interactive map visualization
  - `Description.md`: Metadata markdown file
  - `merged_courses.tsv`: Merged courses data
  
- `CommandLine.sh`: Bash script containing solution for command line question 

- `crawler.py`: Python module containing web scraping functions

- `functions.py`: Python module containing utility functions

- `parser.py`: Python module containing data parsing functions 

- `searchEngine.py`: Python module containing search engine implementation 

- `searchEngineNew.py`: Python module containing new scoring function

## Analysis Summary

The analysis focused on:

- Web scraping degree pages to build a dataset
- Preprocessing text data including stopword removal and stemming 
- Implementing an inverted index search engine for conjunctive queries
- Ranking search results by TF-IDF and cosine similarity
- Defining a custom scoring function to rank results
- Visualizing results on a geographic map colored by cost

The repository contains all code and output to replicate the analysis described in the homework.

## Authors

- Ambar Chatterjee
- Himel Ghosh
- Erika Ioana Zetu
- Alessandra Colaiocco
