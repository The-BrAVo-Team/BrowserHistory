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
                if "https://www." in href:
                    print(href)
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch URL: {url}")


def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


file_path = 'normalurls.txt'  # Replace the string with the path to your text file containing URLs
urls = read_urls_from_file(file_path)

for url in urls:
    simple_web_crawler(url)
