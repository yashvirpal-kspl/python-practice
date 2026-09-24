import time

while True:
    try:
        seconds=int(input("⏰inter the time in second: "))
        if seconds <1:
            print("Please enter  a number greater than 0")
            continue
        break
    except ValueError:
        print("Invalid input, please enter a whole number")
        
print("\n 🔔 Timer Started...")
for remining in range(seconds,0,-1) :
    min,secs=divmod(remining,60)   
    time_format=f"{min:02}:{secs:02}" 
    print(f"\n⏰ Time left: {time_format}",end="\r")
    time.sleep(1)
    
    
print("\nTimes up! take a break")  
print("\a")  #optional: make beep sound