import requests
from bs4 import BeautifulSoup

# Add terms to this list that shouldn't appear in results
reject_list = ["careers", "policies", "source", "Source", "privacy", "accessibility", "audio", "about", "terms", "=", "#", "@"]

def web_crawler(url):
    link_list = []
    try:
        # Send a GET request to the URL with a timeout of 10 seconds
        response = requests.get(url, timeout=10, allow_redirects=False)

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
                if href and "https://www." in href and not any(x in href for x in reject_list):
                    link_list.append(href)
            if len(link_list) > 0:
                return set(link_list)
            else:
                return ['https://www.google.com']

        else:
            return ['https://www.yahoo.com']

    except Exception:
        return ['https://www.chess.com']


def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


if __name__ == '__main__':
    file_path = 'goodurls.txt'  # Replace the string with the path to your text file containing URLs
    urls = read_urls_from_file(file_path)
    link_list = []

    for url in urls:
        link_list.extend(web_crawler(url))
    
    for link in link_list:    
        print(link)