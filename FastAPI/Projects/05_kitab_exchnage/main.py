from fastapi import FastAPI
from database import create_tables

from routes import books, users
 

app = FastAPI(
    title="Kitab Exchange API",
    description="Book exchange API for Kitab Exchange",
    lifespan=lifespan
    
)


@app.on_event("startup") 
def on_startup():
    create_tables()

app.include_router(books.router)
app.include_router(users.router)

@app.get("/")
def health_check():
    return {"message":"Kitab Exchange API is running"}