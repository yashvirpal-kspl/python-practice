import asyncio
import time
async def brew(name):
    print(f"Brewing {name} chai....")
    await asyncio.sleep(3)    #Not block main thread
    #time.sleep(3)  # See the diffrence if not use await
    print(f"{name} Chai is ready")

async def main():
    await asyncio.gather(
        brew("Masala Chai"),
        brew("Green Chai"),
        brew("Ginger Chai")
    )

asyncio.run(main())    