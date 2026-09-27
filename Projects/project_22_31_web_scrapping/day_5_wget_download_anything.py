import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import wget

BASE_URL = "https://books.toscrape.com/"
IMAGE_DIR = "images_wget"

def sanitize_filename(title):
    return re.sub(r'[^\w\-_. ]','',title).replace(" ","_")

def download_image(image_url,filename):
    try:
        response = requests.get(image_url,stream=True,timeout=10)
        response.raise_for_status()
        with open(filename,'wb') as f:
            for chunck in response.iter_content(1024):
                f.write(chunck)
    except Exception as e:
        print(f"Failed to download {filename} - {e}")
        
        
def scrape_download_images():
    
    url = BASE_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")       
    books = soup.select("article.product_pod")[:10] 
    
    # print(books)
    # return
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        
    for book in books:
        title = book.h3.a['title']
        relative_image = book.find('img')['src'] 
        img_url = urljoin(BASE_URL,relative_image)
        print(f" - {img_url}")
        
        filename = sanitize_filename(title + ".jpeg")
        filepath = os.path.join(IMAGE_DIR,filename)
        print(f"Filepath: {filepath}")
        
        print(f"Downloading: {title}")
        #download_image(img_url,filepath)
        wget.download(img_url,filepath,)
    print("All 10 books covers downloaded to images/")    

def main():
    scrape_download_images()
    
if __name__ == "__main__":
    main()      