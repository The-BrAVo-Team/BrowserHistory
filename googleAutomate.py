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
    def __init__(self, path, scenario, overwrite=False, log_output=None):
        # Name of user folder which will contain History file
        self.path = path
        
        scenario_keywords = {
            "clean": None,
            "ip": "ip_case.txt",
            "hom": "hom_case.txt",
            "cc": "cc_case.txt",
            "drug": "drug_case.txt"
        }
        
        self.overwrite = overwrite
        self.log_output = log_output  # Output handler

        # List of Keywords
        self.keywordList = self.read_keywords_from_file("keywords.txt") + self.read_keywords_from_file(scenario_keywords[scenario])
        self.log(f"Keywords: {self.keywordList}")
        
        # List of Search Engines
        self.searchEngineList = self.read_keywords_from_file("search_engines.txt")
        self.count = 0

    def log(self, message):
        if self.log_output:
            self.log_output(message)
        else:
            print(message)

    def read_keywords_from_file(self, file_path):
        if file_path is None:
            return [""]
        with open(file_path, 'r') as file:
            keywords = [line.strip().split() for line in file.readlines()]
        return keywords
    
    def visit(self, driver, url):
        try:
            self.log(f"Visiting: {url}")
            driver.get(url)
        except Exception as e:
            self.log(f"Failed to get page {url}: {str(e)}")
        
    def run(self):
        # Setup for two drivers: one for Google and one to load the pages.

        # First Driver for Google Searches
        if os.path.exists(self.path + "\\Default") and self.overwrite:
            shutil.rmtree(self.path + "\\Default")
        gChromeOptions = webdriver.ChromeOptions()
        gChromeOptions.add_argument("--headless=new")
        gChromeOptions.add_argument("--disable-gpu")
        gChromeOptions.add_argument("--no-sandbox")
        gChromeOptions.add_argument("--disable-dev-shm-usage")
        gChromeOptions.add_argument("--mute-audio")
        gChromeOptions.page_load_strategy = 'eager'
        googleDriver = webdriver.Chrome(options=gChromeOptions)
        
        rnd.shuffle(self.keywordList)
        links = []
        
        detected = False
        unsearched_links = []
        for query in self.keywordList:
            query = "+".join(query)
            n_pages = 3
            
            for page in range(1, n_pages):
                url, divClass = rnd.choice(self.searchEngineList)
                url = url + query + "&start=" + str(page)
                if not detected:
                    self.log(f"Visiting page {url}")
                    googleDriver.get(url)
                    
                    try:
                        WebDriverWait(googleDriver, timeout=10).until(
                            ec.visibility_of_element_located((By.CLASS_NAME, divClass))
                        )
                        links.append(url)
                        soup = BeautifulSoup(googleDriver.page_source, 'html.parser')
                        search = soup.find_all('div', class_=divClass)
                        self.log(f"{len(search)} links found")
                        links.extend([h.a.get('href') for h in search])
                    except Exception as e:
                        self.log(f"Search Engine timeout: {str(e)}")
                        detected = True
                        unsearched_links.append(url)
                else:
                    self.log("Search skipped")
                    unsearched_links.append(url)
                
        googleDriver.quit()

        # Second Driver for visiting the collected URLs
        webOptions = webdriver.ChromeOptions()
        webOptions.add_argument("--headless=new")
        webOptions.add_argument("--disable-gpu")
        webOptions.add_argument("--no-sandbox")
        webOptions.add_argument("--disable-dev-shm-usage")
        webOptions.add_argument("--mute-audio")
        webOptions.page_load_strategy = 'eager'
        webOptions.add_argument("--user-data-dir=" + self.path)
        webOptions.add_argument("--profile-directory=Default")
        webOptions.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.javascript": 2,
        })
        webDriver = webdriver.Chrome(options=webOptions)
        webDriver.set_page_load_timeout(5)
        if links:
            for url in links:
                self.visit(webDriver, url)
                self.count += 1
        webDriver.quit()
        
        self.log(f"Total URLs visited: {self.count}")

        # Logging the total execution time
        self.log(f"--- {time.time() - start_time} seconds ---")
