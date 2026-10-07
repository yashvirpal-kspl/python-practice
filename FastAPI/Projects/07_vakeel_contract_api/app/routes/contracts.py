from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
import os
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB,UPLOAD_DIR
import uuid
from service.document_parser import extract_text
from models import Contract
from database import contracts_collection

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_contract(
    file: UploadFile = File(...),
):
    """
    Endpoint to upload a PDF or TXT contract for analysis.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and TXT files are allowed."
        )
    content = await file.read()
    
    size_mb = len(content) / (1024 * 1024)      
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB."
        )
        
    os.makedirs(UPLOAD_DIR, exist_ok=True)    
    unique_name = f"{uuid.uuid4().hex}{ext}"
    
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    
    with open(file_path, "wb") as f:
        f.write(content)
        
    parsed = extract_text(file_path)
    
    contract_data = Contract(
        filename = unique_name,
        original_name = file.filename,
        text_content = parsed["text"] if isinstance(parsed,dict) else parsed,
        page_count = len(parsed["page_count"]) if isinstance(parsed,dict) else len(parsed.splitlines()),
        word_count = len(parsed["word_count"]) if isinstance(parsed,dict) else len(parsed.split()),
    )    
    
    doc = contract_data.model_dump()
    result = contracts_collection.insert_one(doc)
    contract_data.id = str(result.inserted_id)
    return {
        "message":"File uploaded and processed successfully",
        "contract":contract_data.model_dump(),
        "id":contract_data.id
    }
    
@router.get("/")
async def list_contracts():
    """
    List all uploaded contracts
    """    
    
    contracts = []
    
    for doc in contracts_collection.find({},{"text_content":0}):
        contract = Contract(**doc)
        contract.id = str(doc["_id"])
        contracts.append(contract.model_dump())
        
    return {"contracts":contracts}  


@router.get("/{contract_id}") 
async def get_contract(contract_id:str):
    """
    Retrieve a specific contract by ID.
    """ 
    from bson import ObjectId
    doc = contracts_collection.find_one({"_id":ObjectId(contract_id)})
    if not doc:
        raise HTTPException(status_code=404,detail="Contract not found")
    
    contract = Contract(**doc)
    contract.id = str(doc["_id"])
    
    return {"contract":contract.model_dump()}