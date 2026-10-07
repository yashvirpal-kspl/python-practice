from fastapi import FastAPI
from database import init_db
from routes.contracts import router as contracts_router
from routes.analysis import router as analysis_router

app = FastAPI(
    title="Vakeel Contract API",
    description="API Powered contracts analysis using generative AI(Gemini).",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    init_db()  # Initialize the database and create indexes

@app.get("/")
async def root():
    return {
        "message": "Welcome to Vakeel Contract API!",
        "app":" Vakeel Contract API",
        "version": "1.0.0",
        "endpoints": {
            "/": "Root endpoint",
            "POST /contracts/upload": "Upload a PDF or TXT contract for analysis",
            "GET /contracts/":"Retrieve all uploaded contracts",
            "GET /contracts/{contract_id}":"Retrieve details of specific contracts",
            "POST /analysis/analyse/{contract_id}":"Analyze a contract using AI and return insight",
            "GET /analysis/{analysis_id}":"Retrieve the result of a specific analysis by ID",
            "GET /analysis/contract/{contract_id}":"Retrieve the list of all analyse performed for specific contract",
            
            
        }
        }
    
    
app.include_router(contracts_router)
app.include_router(analysis_router)    