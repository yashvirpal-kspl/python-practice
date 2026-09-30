import asyncio
import threading
import time


def background_wordker():
    while True:
        time.sleep(1)
        print(f"Logging the system health ")
        
        
async def fetch_orders():
    await asyncio.sleep(3)        
    print("Order Fetched")
    
    
threading.Thread(target=background_wordker,daemon=True).start()    
asyncio.run(fetch_orders())