from fastapi import APIRouter, HTTPException
from config import GEMINI_API_KEY
from models import Contract,AnalysisResult
from database import contracts_collection
from bson import ObjectId
from service.gemini_analyze_contract import analyze_contract


router = APIRouter(
    prefix="/analysis",
    tags=["analysis"]
)



@router.post("/analyse/{contract_id}")
async def analyse_contract(contract_id:str):
    """
    Analyse a contract using AI and return insight 
    
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500,detail="GOOGLE AI API key not cofigured")
    
    if not contract_id:
        raise HTTPException(status_code=400,detail="Contract ID is required")
    
    contract = contracts_collection.find_one({"_id":ObjectId(contract_id)})  
    if not contract:
        raise HTTPException(status_code=404,detail="Contract not found")
    
    if not contract.get("text_content"):
        raise HTTPException(status_code=400,detail="Contract has no text content to analyze")
    
    contracts_collection.update_one({"_id":ObjectId(contract_id)},{"$set":{"analysis_status":"in_progress"}})
    
    result = await analyze_contract(contract_id,contract["text_content"])
    
    doc = result.model_dump()
    insert_result = analyses_collection.insert_one(doc)
    
    result.id = str[insert_result.inserted_id]
    
    contracts_collection.update_one({"_id":ObjectId(contract_id)},{"$set":{"analysis_status":"completed"}})
    
    return {
        "message":"Contract analyzed successfully",
        "analysis":result.model.dump(),
        "id":result.id
    }
    
    
@router.get("/{analysis_id}")
def get_analysis(analysis_id:str):
    """
    Retrieve the resul tof specific analsis by ID
    """    
    
    analysis = analysis_collection.find_one({"_id":ObjectId(analysis_id)})
    
    if not analysis:
        raise HTTPException(status_code=404,detail="Analysis not found")
    
    return {
        "analysis":analysis
    }
    
@router.get("/")
def list_analysis():
    """
    List all analysis performed
    """    
    
    analyses = []
    
    for doc in analysis_collection.find({}):
        dce["id"] = str(doc['_id'])
        analyses.append(doc)
        
    return {"analyses":analyses}    
   
@router.get("/contract/{contract_id}")
async def get_analysis_for_contract(contract_id:str):
    """
    Get all analysis for a specific contract
    """  
    analyses = []
    cursor = analysis_collecton.find({"contract_id":contract_id}) 
    
    for doc in cursor:
        doc["id"]=str(doc.pop("_id"))
        analyses.append(doc)
        
    return {"analyses":analyses,"total":len(analyses)}    