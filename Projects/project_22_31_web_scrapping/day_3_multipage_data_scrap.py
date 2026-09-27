import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
START_PAGE = "catalogue/page-1.html"
OUTPUT_PAGE = "books_data.json"
TARGET_COUNT = 70

def scrape_page(url):
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()

    except requests.RequestException as e:
        print("Failed to fetch url",e)
        return [], None
    
    soup = BeautifulSoup(response.text,"html.parser")
    books = []
    
    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 > a")
        title = title_tag.get("title")
        price = article.select_one("p.price_color").text.strip()
        #print(f"{title} {price}")
        
        books.append({"title":title,"price":price})
    #print(books) 
    
    next_link = soup.select_one("li.next > a")
    #next_url = next_link.get("href")
    next_url = urljoin(url,next_link.get("href")) if next_link else None
    
    return books,next_url

def main():
    collected = []
    current_url = urljoin(BASE_URL,START_PAGE) 

    while len(collected) < TARGET_COUNT and current_url:
        print(f"Scrapping: {current_url}")
        
        books,next_url = scrape_page(current_url)
        collected.extend(books)
        current_url = next_url
        
    collected = collected[:TARGET_COUNT]
    print(f"scrapped {len(collected)} books")
    
    with open(OUTPUT_PAGE,"w",encoding="utf-8") as f:
        json.dump(collected,f,indent=2)
        
    print(f"Data save to {OUTPUT_PAGE}")
    
if __name__ == "__main__":
    main()         