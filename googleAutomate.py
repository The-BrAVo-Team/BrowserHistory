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
from accessHistory import modify_timestamps
import time

start_time = time.time()

class GoogleAutomation:
    def __init__(self, scenario, overwrite=False, ):
        # Name of user folder which will conatin History file
        username = os.getlogin()
        
        self.path = f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data'
        
        
        
        scenario_keywords =  {
            "clean": None,
            "ip" : "ip_case.txt",
            "hom" : "hom_case.txt",
            "cc" : "cc_case.txt",
            "drug" : "drug_case.txt"
        }
        
        
        # Overwrite T/F
        self.overwrite = overwrite
        # List of Keywords
        self.keywordList = self.read_keywords_from_file("keywords.txt")
        self.bad_keywords = self.read_keywords_from_file(scenario_keywords[scenario])
        
        print(self.keywordList, self.bad_keywords)
        # List of Search Engines
        self.searchEngineList = self.read_keywords_from_file("search_engines.txt")
        self.count = 0

        
    
    def read_keywords_from_file(self, file_path):
        if file_path == None:
            return [""]
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
        
        # Path to any folder where webdriver chrome data will go
        # WILL OVERWRITE PATH/Default
        # Removes the Default folder which contains the history files to start from a clean slate.
        if os.path.exists(self.path + "\\Default\\History") and self.overwrite:
            os.remove(self.path + "\\Default\\History")
        gChromeOptions = webdriver.ChromeOptions()  
        gChromeOptions.add_argument("--headless=new") #breaks duckduckgo searches but speeds up google searches
        gChromeOptions.add_argument("--disable-gpu")
        gChromeOptions.add_argument("--no-sandbox")
        gChromeOptions.add_argument("--disable-dev-shm-usage")
        gChromeOptions.add_argument("--mute-audio")
        gChromeOptions.page_load_strategy = 'eager'
        
        
        webOptions = webdriver.ChromeOptions()  
        webOptions.add_argument("--headless=new") #breaks duckduckgo searches but speeds up google searches
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
        
        
        
        rnd.shuffle(self.keywordList)
        links = []
        answerKey = []
        detected = False
        
        while self.count < 1000:
            n_pages = 2
            googleDriver = webdriver.Chrome( options=gChromeOptions)
            while not detected:
                
                if rnd.randint(0,10) == 10 and len(self.bad_keywords) > 3:
                    #Suspicious search
                    query = rnd.choice(self.bad_keywords)
                    query = "+".join(query)
                    for page in range(1, n_pages+1):
                    
                        url, divClass = rnd.choice(self.searchEngineList)#Choses a random search engine from the list of engines
                        url = url + query + "&start=" + str(page)
                        print("Visiting page " + str(url))
                        try:
                            googleDriver.get(url)
                            
                            WebDriverWait(googleDriver, timeout=10).until(
                                ec.visibility_of_element_located((By.CLASS_NAME, divClass))
                            )
                            links.append(url)
                            answerKey.append(url)
                            soup = BeautifulSoup(googleDriver.page_source, 'html.parser')
                            search = soup.find_all('div', class_=divClass)
                            print(str(len(search)) + " links found")
                            links.extend([h.a.get('href') for h in search])
                            answerKey.extend([h.a.get('href') for h in search])
                        except:
                            print("Search Engine timeout")
                            detected = True
                            break
                    
                    
                else:
                    query = rnd.choice(self.keywordList)
                    query = "+".join(query)
                    for page in range(1, n_pages+1):
                    
                        url, divClass = rnd.choice(self.searchEngineList)#Choses a random search engine from the list of engines
                        url = url + query + "&start=" + str(page)
                        print("Visiting page " + str(url))
                        googleDriver.get(url)
                        
                        try:
                            WebDriverWait(googleDriver, timeout=10).until(
                                ec.visibility_of_element_located((By.CLASS_NAME, divClass))
                            )
                            links.append(url)
                            soup = BeautifulSoup(googleDriver.page_source, 'html.parser')
                            search = soup.find_all('div', class_=divClass)
                            print(str(len(search)) + " links found")
                            links.extend([h.a.get('href') for h in search])
                        except:
                            print("Search Engine timeout")
                            detected = True
                            break
                    
            googleDriver.quit()
            #Go through all of the links
            webDriver = webdriver.Chrome( options=webOptions)
            webDriver.set_page_load_timeout(5)
            while links and self.count < 1000:
                url = links.pop(0)
                try:
                    self.visit(webDriver,url)
                    self.count += 1
                except:
                    print("failed, unknown error")
            for handle in webDriver.window_handles:
                webDriver.switch_to.window(handle)
                webDriver.close()
            webDriver.quit()
            detected = False
            
        webOptions.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.javascript": 1,
        })
        webDriver = webdriver.Chrome( options=webOptions)
        webDriver.quit()
        print(self.count)
        username = os.getlogin()
        answerfile = open(f'C:\\Users\\{username}\\Desktop\\Answer Key.txt','w')
        answerfile.writelines(line + '\n' for line in answerKey)
        answerfile.close()
        modify_timestamps("2024-1-1", "2024-12-31", "20:00:00", "23:59:59")
        
        
        
        




if __name__ == '__main__':      
    ga = GoogleAutomation( "ip", overwrite=True)
    ga.run()
    print()
    print("--- %s seconds ---" % (time.time() - start_time))
    quit()