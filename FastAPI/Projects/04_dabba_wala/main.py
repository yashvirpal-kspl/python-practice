from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables


from routes.orders import router as order_router
from routes.stats import router as stats_router



@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("Database table created")
    yield
    #shutdown:cleanup here 
    print("Shutting down the app")

app = FastAPI(
    title="Dabba Wala API",
    description="Order management API for Dabba Wala",
    lifespan=lifespan
    
)

app.include_router(order_router)
app.include_router(stats_router)

@app.get("/")
def health_check():
    return {"message":"Dabba Wala API is running"}