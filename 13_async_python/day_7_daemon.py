import threading
import time 

def montor_tea_thread():
    while True:
        print(f"Monitoring tea temerature...")
        time.sleep(2)
        
        
t = threading.Thread(target=montor_tea_thread,daemon=True).start()        
print("Main Program Done ")