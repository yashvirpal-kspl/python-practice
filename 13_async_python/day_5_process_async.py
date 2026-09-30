import asyncio
import time 
from concurrent.futures import ProcessPoolExecutor

def encrypt(data):
    return f"{data[::-1]}"   #data return nothing -1

async def main():
    loop = asyncio.get_running_loop()   
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool,encrypt,"Credit Card 1234")
        print(result)

if __name__=="__main__":
            
    asyncio.run(main())        