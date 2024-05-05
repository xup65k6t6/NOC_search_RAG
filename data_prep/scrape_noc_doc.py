import os
import random
import time
import sqlite3
import requests
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag
from tqdm import tqdm

from noc_doc_process import load_table_from_database

def encode_decode(cell):
    if isinstance(cell, str):
        return cell.encode('utf-8').decode('utf-8')
    else:
        return cell

def save_to_database(unit_group, db_path = 'unit_groups.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS unit_groups
                 (url TEXT PRIMARY KEY, 
                 noc TEXT,
                 description TEXT,
                 example_titles TEXT, index_titles TEXT, main_duties TEXT,
                 employment_requirements TEXT, additional_information TEXT, exclusions TEXT,
                 breakdown_summary TEXT )''')

    # Insert data into the table
    c.execute('''INSERT INTO unit_groups VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
               (unit_group['url'],
               unit_group['noc'], 
               unit_group['description'], 
               unit_group['example_titles'], 
               unit_group['index_titles'],
               unit_group['main_duties'], 
               unit_group['employment_requirements'],
               unit_group['additional_information'], 
               unit_group['exclusions'],
               unit_group['breakdown_summary']
               )
               )

    # Commit changes and close connection
    conn.commit()
    conn.close()

def url_exists(url):
    db_path = 'unit_groups.db'
    # Check if the database file exists
    if not os.path.isfile(db_path):
        # print("Database file does not exist.")
        return False
    
    # If the database file exists, perform the query
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM unit_groups WHERE url = ?", (url,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0


def scrape_profile_section(profile_section: Tag) -> dict:
    # Find all panel-default sections
    panel_sections = profile_section.find_all('section', class_="panel panel-default")
    
    # Initialize variables to store data
    example_titles = []
    index_titles = []
    main_duties = ''
    employment_requirements = ''
    additional_information = ''
    exclusions = ''

    # Loop through each panel section and extract data
    for panel_section in panel_sections:
        panel_title = panel_section.find('h4', class_="panel-title").text.strip()
        panel_body = panel_section.find('div', class_="panel-body").text.strip()
        
        # Extract data based on panel title
        if panel_title == "Example titles":
            example_titles = panel_section.find('div', id="ExampleTitles").text.strip()
            index_titles = panel_section.find('div', id="IndexTitles").text.strip()
        elif panel_title == "Main duties":
            main_duties = panel_body
        elif panel_title == "Employment requirements":
            employment_requirements = panel_body
        elif panel_title == "Additional information":
            additional_information = panel_body
        elif panel_title == "Exclusions":
            exclusions = panel_body
    profile_section_dict = {
        "example_titles": example_titles,
        "index_titles": index_titles,
        "main_duties": main_duties,
        "employment_requirements": employment_requirements,
        "additional_information": additional_information,
        "exclusions": exclusions,
    }
    return profile_section_dict

# Function to scrape unit group profile data from a given URL
def scrape_unit_group_profile(url: str) -> dict:
    response = requests.get(url)
    if response.status_code == 200:
        unit_group_dict = {}
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extracting h2 and p tags
        h2_tag = soup.find('h2', style="margin-top:25px;margin-bottom:0;")
        p_tag = soup.find('p', class_="mrgn-tp-md mrgn-bttm-sm")
        unit_group_dict['noc'] = h2_tag.text.strip()
        unit_group_dict['description'] = p_tag.text.strip()
        # if h2_tag:
        #     print("Title:", h2_tag.text.strip())
        # if p_tag:
        #     print("Description:", p_tag.text.strip())
        
        # Extracting profile and breakdown summary
        profile_section = soup.find('div', class_="col-sm-8")
        breakdown_summary_section = soup.find('div', class_="col-sm-4")

        # Extracting profile text
        if profile_section:
            # Extracting profile text
            profile_section_dict = scrape_profile_section(profile_section)
            unit_group_dict = dict(unit_group_dict, **profile_section_dict)
            # print("\nProfile:")
            # print(profile_section_dict)

        if breakdown_summary_section:
            # print("\nBreakdown Summary:")
            # print(breakdown_summary_section.text.strip())
            unit_group_dict['breakdown_summary'] = breakdown_summary_section.text.strip()
        
        return unit_group_dict
    else:
        print("Failed to retrieve unit group profile. Status code:", response.status_code)


# Function to scrape sub-websites for each unit group
def scrape_sub_websites(soup, db_path) -> list[dict]:
    # Find all details tags containing sub-website information
    details_tags = soup.find_all('details', class_='nocLI')
    # Iterate over each details tag
    # sub_website_url_lst = []
    unit_group_lst = []
    with tqdm(total=len(details_tags)) as pbar:
        for details_tag in details_tags:
            # Extract URL from the <a> tag within the details tag
            sub_website_url = "https://noc.esdc.gc.ca" + details_tag.find('a')['href']
            
            if url_exists(sub_website_url):
                print("URL already processed, skipping:", sub_website_url)
                pbar.update(1)
                continue
            # print("Scraping sub-website:", sub_website_url)
            unit_group = scrape_unit_group_profile(sub_website_url)
            unit_group = dict(unit_group, **{"url":sub_website_url})
            # <TODO> save unit_group into db
            # sub_website_url_lst.append(sub_website_url)
            if unit_group:
                unit_group_lst.append(unit_group)
            save_to_database(unit_group, db_path= db_path)
            pbar.update(1)
            time.sleep(random.randint(15, 60))
    return unit_group_lst


if __name__ == "__main__":
    db_path = 'data/unit_groups.db'
    # URL of the website to scrape
    url = "https://noc.esdc.gc.ca/Structure/Hierarchy"

    if os.path.exists(db_path):
        df = load_table_from_database(db_path = db_path, table_name='unit_groups')
    else:
        print("Get data from websites")
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            unit_group_lst = scrape_sub_websites(soup, db_path)
            
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            exit()

        # Create a DataFrame from the unit group data
        df = pd.DataFrame(unit_group_lst)
    noc_detail_cols = [
        # "description",
        # "example_titles",
        # "index_titles",
        "main_duties",
        # "employment_requirements"
        ]
    df = df.map(encode_decode)
    for _ in noc_detail_cols:
        df[_] = df['noc'] + ' \n' + df[_]
    df = df[["url", "noc"] + noc_detail_cols]
    # Save the DataFrame to a CSV file
    df.to_csv('data/unit_group_data.csv', index=False, encoding='utf-8')

    print('Done')
