from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webcrawler import web_crawler
import random as rnd
import os, shutil;

class GoogleAutomation:
    def __init__(self, path, keywordList, searchEngineList, overwrite=False, ):
        self.path = path
        self.overwrite = overwrite
        self.keywordList = self.read_keywords_from_file(keywordList)
        self.searchEngineList = self.read_keywords_from_file(searchEngineList)
        self.countLinks = 0
        self.links = []
        
    
    def read_keywords_from_file(self, file_path):
        with open(file_path, 'r') as file:
            keywords = [line.strip() for line in file.readlines()]
        return keywords
    
    def run(self):
        chrome_options = webdriver.ChromeOptions()
        # Path to any folder where webdriver chrome data will go
        # WILL OVERWRITE PATH/Default
        # Removes the Default folder which contains the history files to start from a clean slate.
        if os.path.exists(self.path + "\\Default"):
            shutil.rmtree(self.path + "\\Default")
        chrome_options.add_argument("--user-data-dir=" + self.path)
        # Name of user folder which will conatin History file

        chrome_options.add_argument("--profile-directory=Default")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        rnd.shuffle(self.keywordList)

        for query in self.keywordList:
            query = query.replace(' ', '+')  
            # Specify number of pages on google search, each page contains 10 links
            n_pages = 3
            for page in range(1, n_pages):
                url = rnd.choice(self.searchEngineList) + query + "&start=" + str(page)
                self.links.append(url)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
        """
                Doing Extra work that does not get added to the History File. May want to rework this.
                search = soup.find_all('div', class_="yuRUbf")
                for h in search:
                self.links.append(h.a.get('href'))
                self.links.extend(web_crawler(rnd.choice(self.links)))
        
        """
                
                
        links = set(self.links)
        print(links, len(links))
        driver.quit()


if __name__ == '__main__':      
    ga = GoogleAutomation( "C:\\Users\\keoca\\Desktop\\TWP3\\TestUser", "keywords.txt", "search_engines.txt")
    ga.run()
    quit()