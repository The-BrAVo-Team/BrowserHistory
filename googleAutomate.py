from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from webcrawler import web_crawler
import random as rnd
import os, shutil
import time

start_time = time.time()

class GoogleAutomation:
    def __init__(self, path, keywordList, searchEngineList, overwrite=False, ):
        # Name of user folder which will conatin History file
        self.path = path
        # Overwrite T/F
        self.overwrite = overwrite
        # List of Keywords
        self.keywordList = self.read_keywords_from_file(keywordList)
        # List of Search Engines
        self.searchEngineList = self.read_keywords_from_file(searchEngineList)
        self.count = 0

        
    
    def read_keywords_from_file(self, file_path):
        with open(file_path, 'r') as file:
            keywords = [line.strip().split() for line in file.readlines()]
        return keywords
    
    def visit(self,driver, url):
        try:
            print("Visiting: " + url)
            driver.get(url)
        except:
            print("Failed to get page " + url)
        
    
    def run(self):

        # Setup for two drivers: one for google and one to load the pages.

        # First Driver for Google Searches
        gChromeOptions = webdriver.ChromeOptions()
        # Path to any folder where webdriver chrome data will go
        # WILL OVERWRITE PATH/Default
        # Removes the Default folder which contains the history files to start from a clean slate.
        if os.path.exists(self.path + "\\Default") and self.overwrite:
            shutil.rmtree(self.path + "\\Default")  
        gChromeOptions.add_argument("--headless=new") #breaks duckduckgo searches but speeds up google searches
        gChromeOptions.add_argument("--disable-gpu")
        gChromeOptions.add_argument("--no-sandbox")
        gChromeOptions.add_argument("--disable-dev-shm-usage")
        gChromeOptions.add_argument("--user-data-dir=" + self.path)
        gChromeOptions.add_argument("--profile-directory=Default")
        gChromeOptions.add_argument("--mute-audio")
        gChromeOptions.page_load_strategy = 'eager'
        # gChromeOptions.add_experimental_option("prefs", {
        #     #block image loading
        #     "profile.managed_default_content_settings.images": 2,
        # })
        service = ChromeService(ChromeDriverManager().install())
        googleDriver = webdriver.Chrome(service=service, options=gChromeOptions)
        
        rnd.shuffle(self.keywordList)
        links = []
        #while < 1000 links 
        for query in self.keywordList:
            query = "+".join(query)
            # Specify number of pages on google search, each page contains 10 links
            n_pages = 3
            
            for page in range(1, n_pages):
                
                url, divClass = rnd.choice(self.searchEngineList)#Choses a random search engine from the list of engines
                url = url + query + "&start=" + str(page)
                
                print("Visiting page " + str(url))
                googleDriver.get(url)
                self.count += 1
                try:
                    WebDriverWait(googleDriver, timeout=10).until(
                        ec.visibility_of_element_located((By.CLASS_NAME, divClass))
                    )
                except:
                    print("Search Engine timeout")
                soup = BeautifulSoup(googleDriver.page_source, 'html.parser')
                search = soup.find_all('div', class_=divClass)
                print(str(len(search)) + " links found")
                links.extend([h.a.get('href') for h in search])
        googleDriver.quit() 
        gChromeOptions.add_experimental_option("prefs", {
            #block image loading
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.javascript": 2,
        })
        webDriver = webdriver.Chrome(service=service, options=gChromeOptions)
        webDriver.set_page_load_timeout(5)
        if links:
            for url in links:
                self.visit(webDriver,url)
                self.count += 1
        webDriver.quit()
        print(self.count)




if __name__ == '__main__':      
    ga = GoogleAutomation( "C:\\Users\\keoca\\Desktop\\TWP3\\TestUser", "keywords.txt", "search_engines.txt", overwrite=True)
    ga.run()
    print("--- %s seconds ---" % (time.time() - start_time))
    quit()