import requests
from bs4 import BeautifulSoup

def simple_web_crawler(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find and extract relevant information from the page
        # For example, let's extract all the links on the page
        links = soup.find_all('a')

        # Print the extracted links
        for link in links:
            href = link.get('href')
            if href:
                print(href)
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch URL: {url}")


url = 'https://www.usatoday.com/news/nation/' # Replace this URL with the one you want to crawl
simple_web_crawler(url)
