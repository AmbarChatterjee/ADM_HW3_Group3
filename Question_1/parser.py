import os
import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm


def extract_course_info(html_folder, output_folder,  urls_file):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Read the URLs from the URLs file
    with open(urls_file, 'r', encoding='utf-8') as urls_file:
        urls = urls_file.read().splitlines()
    # Define column names
    column_names = [
        "courseName",
        "universityName",
        "facultyName",
        "isItFullTime",
        "description",
        "startDate",
        "fees",
        "modality",
        "duration",
        "city",
        "country",
        "administration",
        "url"
    ]
    # Create a header row in the TSV file
    header_row = "\t".join(column_names)

    # Iterate through each HTML file
    for i,url in enumerate(urls, start=1):
        html_filename = os.path.join(html_folder, f'Html-{i}.txt')
        output_filename = os.path.join(output_folder, f'course_{i}.tsv')

        # Initialize variables to store extracted data
        courseName = ""
        universityName = ""
        facultyName = ""
        isItFullTime = ""
        description = ""
        startDate = ""
        fees = ""
        modality = ""
        duration = ""
        city = ""
        country = ""
        administration = ""


        with open(html_filename, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the courseName
            courseName_element = soup.find('h1', class_='text-white course-header__course-title')
            if courseName_element:
                courseName = courseName_element.get_text(strip=True)

            # Extract the universityName and facultyName
            inst_dept_element = soup.find('h3', class_='h5 course-header__inst-dept')
            if inst_dept_element:
                institution_element = inst_dept_element.find('a', class_='course-header__institution')
                department_element = inst_dept_element.find('a', class_='course-header__department')

                if institution_element:
                    universityName = institution_element.get_text(strip=True)
                if department_element:
                    facultyName = department_element.get_text(strip=True)

            # Extract additional information
            key_info_elements = soup.find('div', class_='key-info__outer')
            if key_info_elements:
              fulltime_element=key_info_elements.find('span',class_='key-info__study-type')
              startdate_element=key_info_elements.find('span',class_='key-info__start-date')
              modality_element=key_info_elements.find('span',class_='key-info__qualification')
              duration_element=key_info_elements.find('span',class_='key-info__duration')
              if fulltime_element:
                isItFullTime=soup.find('span', class_='key-info__study-type').get_text(strip=True)
              if startdate_element:
                startDate=soup.find('span', class_='key-info__start-date').get_text(strip=True)
              if modality_element:
                modality=soup.find('span', class_='key-info__qualification').get_text(strip=True)
              if duration_element:
                duration=soup.find('span', class_='key-info__duration').get_text(strip=True)


            #Extract the geographical information
            course_data_element=soup.find('div',class_='course-data__container col-24 ml-md-n1 p-0 pb-3')
            if course_data_element:
                city_element=course_data_element.find('a',class_='course-data__city')
                country_element=course_data_element.find('a',class_='course-data__country')
                admin_element=course_data_element.find('a',class_='course-data__on-campus')
                if city_element:
                  city=city_element.get_text(strip=True)
                if country_element:
                  country=country_element.get_text(strip=True)
                if admin_element:
                  administration=admin_element.get_text(strip=True)

            # Extract fees information
            fees_element = soup.find('div', class_='course-sections__fees')
            if fees_element:
                fees_paragraph = fees_element.find('p')
                if fees_paragraph:
                    fees_text = fees_paragraph.get_text(strip=True)
                    if "Please see the university website for further information on fees for this course." not in fees_text:
                        fees = fees_text
            # Extract description information
            description_element = soup.find('div', class_='course-sections__description')
            if description_element:
                description_paragraph = description_element.find('p')
                if description_paragraph:
                    description_text = description_paragraph.get_text(strip=True)
                    description = description_text
        # Write the extracted data to a TSV file
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(header_row + "\n")  # Write the header row
            data_row = "\t".join([
                courseName,
                universityName,
                facultyName,
                isItFullTime,
                description,
                startDate,
                fees,
                modality,
                duration,
                city,
                country,
                administration,
                url
            ])
            output_file.write(data_row)