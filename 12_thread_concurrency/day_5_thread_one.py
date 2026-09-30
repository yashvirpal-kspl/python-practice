import threading
import time

def boil_milk():
    print(f"Milk Boiling....")
    time.sleep(2)
    print(f"Milk Boiled....")
    
def toast_bun():
    print(f"Bun Toasting....")
    time.sleep(2)
    print(f"Bun Toasted....") 
    
thread1 = threading.Thread(target=boil_milk)    
thread2 = threading.Thread(target=toast_bun)    

start = time.time()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
end = time.time()

print(f"Breakfast is ready in: {end-start:.2f} seconds")     