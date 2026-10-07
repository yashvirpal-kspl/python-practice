from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class RiskLevel(str,Enum):
    LOW="low"
    MEDIUM="medium"
    HIGH="haigh"
    CRITICAL="critical"


class Contract(BaseModel):
    id: Optional[str] = None
    filename:str
    original_name:str
    upload_date:str =""
    text_content:str = ""
    page_count:int = 0
    word_count:int = 0
    status:str = "uploaded"  # Default status is "uploaded" and  analising,analyzed,error
    
    def model_post_init(self,_context):
        if not self.upload_date:
            self.upload_date = datetime.utcnow().isoformat()
            

class ClauseAnalysis(BaseModel):
    clause_title:str            
    clause_text:str            
    explaination:str            
    is_standard:bool
    
class RiskFlag(BaseModel):                
    flag_title:str            
    description:str 
    risk_level:RiskLevel           
    explaination:str            
    is_critical:bool
    
class AnalysisResult(BaseModel):
    id: Optional[str] = None 
    contract_id:str
    analysis_date:str =""
    summary:str=""       
    contract_type:str=""       
    key_clauses:list[ClauseAnalysis]=[]       
    risk_flags:list[RiskFlag]=[]       
    overall_risk_level:RiskLevel=RiskLevel.LOW      
    recommendations:list[str]=[]      
    
    def model_post_init(self,_context):
        if not self.analysis_date:
            self.analysis_date = datetime.now().isoformat() 