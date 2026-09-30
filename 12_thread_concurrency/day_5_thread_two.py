import threading
import time

def prepare_chai(type_,wait_time):
    print(f"{type_ } Chai Brewing....")
    time.sleep(wait_time)
    print(f"{type_ } Chai ready")
    

    
thread1 = threading.Thread(target=prepare_chai,args=("Masala",2))    
thread2 = threading.Thread(target=prepare_chai,args=("Ginger",3))   

start = time.time()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
end = time.time()

print(f"Breakfast is ready in: {end-start:.2f} seconds")     