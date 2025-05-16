import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from openpyxl import Workbook
import time

# Base URL of the website
BASE_URL = 'https://www.policesacco.com.com'

# Initialize a session
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# Function to fetch and parse a webpage
def fetch_page(url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract all internal links from a page
def get_internal_links(soup, base_url):
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Construct full URL
        full_url = urljoin(base_url, href)
        # Ensure the link is within the same domain
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.add(full_url)
    return links

# Function to extract meta title and article content
def extract_content(url):
    soup = fetch_page(url)
    if not soup:
        return None, None
    # Extract meta title
    title_tag = soup.find('title')
    meta_title = title_tag.get_text(strip=True) if title_tag else 'N/A'
    # Extract article content
    article_tag = soup.find('article')
    article_html = str(article_tag) if article_tag else 'N/A'
    return meta_title, article_html

def main():
    # Fetch the homepage
    homepage_soup = fetch_page(BASE_URL)
    if not homepage_soup:
        print("Failed to fetch the homepage.")
        return

    # Get all internal links
    internal_links = get_internal_links(homepage_soup, BASE_URL)
    print(f"Found {len(internal_links)} internal links.")

    # Prepare Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Articles"
    ws.append(['Meta Title', 'Article Content (HTML)'])

    # Process each link
    for idx, link in enumerate(internal_links, start=1):
        print(f"Processing ({idx}/{len(internal_links)}): {link}")
        meta_title, article_html = extract_content(link)
        if meta_title and article_html:
            ws.append([meta_title, article_html])
        time.sleep(1)  # Be polite and avoid overwhelming the server

    # Save the Excel file
    wb.save('policesacco.com_articles.xlsx')
    print("Data extraction complete. Saved to policesacco.com_articles.xlsx.")

if __name__ == "__main__":
    main()
#https://policesacco.com.com/articles