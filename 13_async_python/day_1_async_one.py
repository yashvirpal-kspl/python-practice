import asyncio

async def brew_chai():
    print("Brewing chai....")
    await asyncio.sleep(2)    #Not block main thread
    print("Chai is ready")
    
asyncio.run(brew_chai())    