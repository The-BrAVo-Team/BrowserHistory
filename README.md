# Web Automation and Crawling Project

## Overview

This project consists of three main Python scripts designed for different tasks involving web automation and data retrieval:
1. **`accessHistory.py`**: Retrieves browser history from a SQLite database.
2. **`googleAutomate.py`**: Automates Google searches using Selenium WebDriver and scrapes links from search results.
3. **`webcrawler.py`**: Crawls websites to extract valid links using requests and BeautifulSoup.

## Project Files

### `accessHistory.py`

This script connects to a SQLite database containing browser history and retrieves URLs in order of their last visit time.

#### Usage

1. Ensure you have the required SQLite database file (e.g., `History` file from a Chrome browser profile).
2. Update the script with the correct path to the `History` file.
3. Run the script to fetch and print the URLs.

```python
import sqlite3

con = sqlite3.connect("path_to_history_file")
cur = con.cursor()
res = cur.execute("SELECT url FROM urls ORDER BY last_visit_time")
print(res.fetchall())
```

### `googleAutomate.py`

This script automates Google searches using Selenium WebDriver, reads search engines and keywords from files, and retrieves links from search results pages. It also integrates the `web_crawler` function from `webcrawler.py` to further crawl the retrieved links.

#### Prerequisites

- Install Selenium and Chrome WebDriver:
  ```bash
  pip install selenium webdriver-manager
  ```

- Create `search_engines.txt` and `keywords.txt` files containing search engine URLs and search keywords, respectively.

#### Usage

1. Update the `path` variable to the folder where Chrome user data will be stored.
2. Run the script to perform searches and print the retrieved links.

```python
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
path = "path_to_chrome_user_data"
chrome_options.add_argument("--user-data-dir=" + path)
chrome_options.add_argument("--profile-directory=Default")
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

search_engines = read_keywords_from_file("search_engines.txt")
query_list = read_keywords_from_file("keywords.txt")
links = []

rnd.shuffle(query_list)

for query in query_list:
    query = query.replace(' ', '+')
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
```

### `webcrawler.py`

This script contains a function `web_crawler` that takes a URL, sends a GET request, and extracts valid links from the webpage using BeautifulSoup.

#### Prerequisites

- Install BeautifulSoup and requests:
  ```bash
  pip install beautifulsoup4 requests
  ```

#### Usage

1. Import the `web_crawler` function in your script.
2. Call `web_crawler(url)` to crawl the given URL and retrieve valid links.

```python
import requests
from bs4 import BeautifulSoup

def web_crawler(url):
    reject_list = ["facebook.com", "linkedin.com", "instagram.com"]
    link_list = []

    try:
        response = requests.get(url, timeout=10, allow_redirects=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href and "https://www." in href and not any(x in href for x in reject_list):
                    link_list.append(href)
            return set(link_list) if link_list else {'https://www.google.com'}
        else:
            return {'https://www.yahoo.com'}
    except Exception as e:
        print(f"Error occurred while crawling {url}: {e}")
        return {'https://www.chess.com'}

def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file {file_path}: {e}")
        return []

if __name__ == '__main__':
    file_path = 'search_engines.txt'
    urls = read_urls_from_file(file_path)
    link_list = []

    if urls:
        for url in urls:
            link_list.extend(web_crawler(url))
        for link in set(link_list):
            print(link)
    else:
        print("No URLs to process.")
```

## Requirements

- Python 3.x
- `sqlite3` (built-in with Python)
- `requests` library
- `beautifulsoup4` library
- `selenium` library
- `webdriver-manager` library

Install the necessary packages using:
```bash
pip install requests beautifulsoup4 selenium webdriver-manager
```

## Running the Scripts

1. Ensure all required files (`search_engines.txt`, `keywords.txt`, and the Chrome `History` file) are in place.
2. Execute each script individually based on the described usage.

## License

This project is licensed under the MIT License.

## Authors

The BraVo Team! 