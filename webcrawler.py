import requests
from bs4 import BeautifulSoup

# List of terms to reject from the results
reject_list = ["careers", "policies", "source", "Source", "privacy", "accessibility", "audio", "about", "terms", "=", "#", "@"]

def web_crawler(url):
    """
    Crawls a given URL to extract valid links.
    """
    link_list = []
    try:
        # Send a GET request to the URL with a timeout of 10 seconds
        response = requests.get(url, timeout=10, allow_redirects=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all anchor tags
            links = soup.find_all('a')

            # Filter and collect valid links
            for link in links:
                href = link.get('href')
                if href and "https://www." in href and not any(x in href for x in reject_list):
                    link_list.append(href)

            # Return a set of unique valid links
            return set(link_list) if link_list else {'https://www.google.com'}
        else:
            # Return a default URL if the request was not successful
            return {'https://www.yahoo.com'}
    except Exception as e:
        # Handle exceptions and return a fallback URL
        print(f"Error occurred while crawling {url}: {e}")
        return {'https://www.chess.com'}

def read_urls_from_file(file_path):
    """
    Reads URLs from a given file.
    """
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
    file_path = 'search_engines.txt'  # Replace 
    urls = read_urls_from_file(file_path)
    link_list = []

    if urls:  # Proceed only if URLs were successfully read
        for url in urls:
            link_list.extend(web_crawler(url))
        
        for link in set(link_list):
            print(link)
    else:
        print("No URLs to process.")
