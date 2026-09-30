import threading
import requests
import time

counter = 0
lock = threading.Lock()

def increament():
    global counter
    
    for i in range(1000000):
       # counter += 1   # can be issue in race condiotion if use this 
        
        #### OR  Prefer this #############
        with lock:
            counter += 1
            
threads = [threading.Thread(target=increament) for _ in range(10)]
         
    

start = time.time()   

[t.start() for t in threads]
[t.join() for t in threads]


    

end = time.time()

print(f"Final Counter: {counter}")      