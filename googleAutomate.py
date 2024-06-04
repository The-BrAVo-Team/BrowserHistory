from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webcrawler import web_crawler
import random as rnd

def read_keywords_from_file(file_path):
    with open(file_path, 'r') as file:
        keywords = [line.strip() for line in file.readlines()]
    return keywords

chrome_options = webdriver.ChromeOptions()
# Path to any folder where webdriver chrome data will go
path = "C:\\Users\\keoca\\Desktop\\TWP3\\TestUser"
chrome_options.add_argument("--user-data-dir=" + path)
# Name of user folder which will conatin History file
chrome_options.add_argument("--profile-directory=Default")
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

search_engines = read_keywords_from_file("search_engines.txt")

query_list = read_keywords_from_file("keywords.txt")

links = []

rnd.shuffle(query_list)

for query in query_list:
    query = query.replace(' ', '+')  
    # Specify number of pages on google search, each page contains 10 links
    n_pages = 3
    for page in range(1, n_pages):
        url = rnd.choice(search_engines) + query + "&start=" + str(page)
        links.append(url)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            links.append(h.a.get('href'))
        links.extend(web_crawler(rnd.choice(links)))
        
links = set(links)
driver.quit()
            

if __name__ == '__main__':      
    print(links)
    quit()