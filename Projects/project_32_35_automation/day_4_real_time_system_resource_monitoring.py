import psutil
import time
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  #nt for window os 
    
def show_stats():
    print("🔥" * 30)    
    print("⭐ System Resource Monitor ⭐")
    
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    print(f"CPU Usage: {cpu}")
    # print(f"RAM Usage: {ram.percent}%")
    # print(f"DISK Usage: {disk.percent}%")
    #print(f"RAM Usage: {ram.used}")
    #print(f"DISK Usage: {disk.used}")
    
    print(f"RAM Usage: {ram.percent}% ({round(ram.used / 1e9,2 )} GB used of {round(ram.total / 1e9,2)} GB)")     #convert byte to gb 1e9 e9= 9 time 0
    print(f"DISK Usage: {disk.percent}% ({round(disk.used / 1e9,2 )} GB used of {round(disk.total / 1e9,2)} GB)")     #convert byte to gb 1e9 e9= 9 time 0
    
    print("🔥" * 30)  
    
if __name__=="__main__":
    try:
        while True:
            clear_screen()
            show_stats()
            time.sleep(3)
    except KeyboardInterrupt:
        print("Monitoring Stopped......")           
        
        
        
                                                            
        