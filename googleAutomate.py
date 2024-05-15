from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webcrawler import web_crawler
import random as rnd
import sys


def read_keywords_from_file(file_path):
    with open(file_path, 'r') as file:
        keywords = [line.strip() for line in file.readlines()]
    return keywords

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

ChromeDriverManager().install()
driver = webdriver.Chrome()

query_list = read_keywords_from_file("keywords.txt")

links = []

for query in query_list:
    query = query.replace(' ', '+')  
    # Specify number of pages on google search, each page contains 10 links
    n_pages = 3
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + query + "&start=" + str(page)
        links.append(url)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            links.append(h.a.get('href'))

driver.quit()
            

if __name__ == '__main__': 
    
    for i in range(15):
        links.extend(web_crawler(rnd.choice(links)))
        print("...")
        
    print(links)
    
    quit()
    
    