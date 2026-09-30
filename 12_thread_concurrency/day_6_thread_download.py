import threading
import requests
import time

def download(url):
    print(f"Starting download from {url}")
    response = requests.get(url)
    print(f"Finished downloading from {url}, size: {len(response.content)} bytes:")\
        
URLs = [
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/svg",
]        
    

start = time.time()   
theads = []

for url in URLs: 
    t = threading.Thread(target=download,args=(url,))   

    t.start()
    theads.append(t)

for t in theads:
    t.join()   
    
    

end = time.time()

print(f"All Download done in : {end-start:.2f} seconds")      