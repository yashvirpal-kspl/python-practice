import asyncio
import time 
from concurrent.futures import ThreadPoolExecutor

def check_stock(item):
    print(f"Checking {item} in store...")
    time.sleep(3) # Blocking Opration
    return f"{item} stock: 42"

async def main():
    loop = asyncio.get_running_loop()   #this function design for threads
    with ThreadPoolExecutor() as pool:
        results = await loop.run_in_executor(pool,check_stock,"Masala Chai")
        print(results)
        
asyncio.run(main())        