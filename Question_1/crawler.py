#importing necessary libraries
import os
import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlsplit

def scrape_urls(url, pages, urlfilename):
    # Part 1: Scrape URLs
    master_urls = [] #we create an empty list to which we will append the urls we get
    for i in tqdm(range(1, pages+1)):
        #We change along the first 400 pages and request via their urls
        base_url = f"{urlsplit(url).scheme}://{urlsplit(url).netloc}"
        url = url+'?page='+str(i)
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')

        try:
            # Find and extract the URLs of master's degree courses
            course_links = soup.find_all('a', class_='courseLink text-dark')
            for link in course_links:
                course_url = link.get('href')
                master_urls.append(base_url+course_url)

            #To conclude, we save it in a .txt file with all the urls of the courses
            with open(urlfilename, 'w') as file:
                for url in master_urls:
                    file.write(url + '\n')
        except:
            pass
        # This will leave a second between each iteration so we do not get banned from the website
        time.sleep(1)
    print(f'\nThe URLs are now saved in the file {urlfilename}')

def scrape_htmls(urlfilename,htmlfolderName):
    # Part 2: Scrape HTML
    #We first read the lines of the file with the urls
    archive = open(urlfilename)
    urls = archive.readlines()
    output_folder = htmlfolderName
    # Create an output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    #We do this so we only need to acces the webpage once to get all the data and not enter it 15*400=6000 times
    for i in tqdm(range(len(urls))):
        #We only need the urls, not the '\n'
        link = urls[i].strip()
        #we get the html within the same session
        html = requests.get(link)
        #and write it in differents files
        # Create the output file path in the output folder
        output_file = os.path.join(output_folder, f'Html-{i + 1}.txt')
        with open(output_file, 'a') as doc:
            doc.write(html.text)
        time.sleep(1)