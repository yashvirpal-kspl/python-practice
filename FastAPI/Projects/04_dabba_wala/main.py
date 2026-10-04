from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables
from routes.reviews import router as review_router



@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("Database table created")
    yield
    #shutdown:cleanup here 
    print("Shutting down the app")

app = FastAPI(
    title="Rangmanch Review API",
    description="Theatre review API for Kanpur Rangmanch",
    lifespan=lifespan
    
)

app.include_router(review_router)

@app.get("/")
def root():
    return {"message":"Welcome to rangmanch review API"}
   