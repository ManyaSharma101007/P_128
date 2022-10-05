rom selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("/Users/manyasharma/Downloads/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

new_stars_data = []

def scrape_more_data(hyperlink):
    try : 
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html_parser")
        temp_list = [] 

        for tr_tag in soup.find_all("tr",attrs = {"class" : "fact_row"}):
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags :
                try : 
                    temp_list.append(td_tag.find_all("div",attrs = {"class" : "value"})[0].contents[0])
                
                except :
                    temp_list.append("")
        
        new_stars_data.append(temp_list)

    except :
        time.sleep(1)
        scrape_more_data(hyperlink)
    
star_df_1 = pd.read_csv("new_scraped_data.csv")

for index,row in star_df_1.iterrows():
    print(row["hyperlink"])
    scrape_more_data(row["hyperlink"])
    print(f"Data Scraping at hyperlink {index+1} is completed")

scrape_data = []

for row in new_stars_data :
    replaced = []

    for el in row :
        el = el.replace("\n","")
        replaced.append(el)

    scrape_data.append(replaced)

print(scrape_data)

# Define Header
headers = ["Constellation", "Radius", "Mass", "Discovery_date", "Orbital_period"]

# Define pandas DataFrame   
star_df_1 = pd.DataFrame(scrape_data,columns = headers) 

# Convert to CSV
star_df_1.to_csv("new_scrapped_data.csv",index = True,index_label = 'id')
    