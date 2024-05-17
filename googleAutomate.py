from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webcrawler import web_crawler
import random as rnd
import time

def read_keywords_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def fetch_links(driver, url):
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return [h.a.get('href') for h in soup.find_all('div', class_="yuRUbf")]
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def main():
    search_engines = read_keywords_from_file("search_engines.txt")
    query_list = read_keywords_from_file("keywords.txt")

    links = []
    rnd.shuffle(query_list)

    with setup_driver() as driver:
        for query in query_list:
            query = query.replace(' ', '+')
            n_pages = 3
            for page in range(n_pages):
                url = f"{rnd.choice(search_engines)}{query}&start={page*10}"
                links.extend(fetch_links(driver, url))
                time.sleep(rnd.uniform(1, 3))  # Random sleep to avoid detection
                additional_links = web_crawler(rnd.choice(links))
                links.extend(additional_links)

    unique_links = set(links)
    print(unique_links)

if __name__ == '__main__':
    main()
