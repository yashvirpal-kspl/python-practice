import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"

URL = "https://yashvirpal.com/"

def get_h2_headers(url):
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        
    except requests.RequestException as e:
        print(f"Fialed to fetch page: \n{e}")
        return []
    
    soup = BeautifulSoup(response.text,"html.parser")
    h2_tags = soup.find_all("h2")
    print(h2_tags)
    headers = []
    #for tag in h2_tags[:2]:
    for tag in h2_tags:
        header_Text = tag.get_text(strip=True)
        if header_Text and header_Text .lower !="contents":
            headers.append(header_Text)
            
    print(headers)        
    
get_h2_headers(URL)    