from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routes.query import router as query_router



app = FastAPI(
    title="RAG Pipeline API",
    description="This is a simple API for the RAG pipeline.",
    version="0.1.0",
)

app.include_router(query_router)