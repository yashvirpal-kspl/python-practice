
import json

from config import GEMINI_API_KEY
from service.prompt import CONTRACT_ANALYSIS_PROMPT
from models import ClauseAnalysis, AnalysisResult, RiskFlag

from google import genai


GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
client = genai.Client(
    api_key=GEMINI_API_KEY
)

async def analyze_contract(contract_id:str,text_content:str):
    prompt = CONTRACT_ANALYSIS_PROMPT.format(contract_text=text_content)
    
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )
       
    data = json.loads(interaction.output_text)
    
    print("Raw Response from GEMINI API, Need to parse it",data)
    
    # raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    # raw_text = raw_text.strip()
    
    # if raw_text.startswith("```json"):
    #     raw_text = raw_text[7:]
    # if raw_text.startswith("```"):
    #     raw_text = raw_text[3:]
    # if raw_text.endswith("```"):
    #     raw_text = raw_text[:-3]    
        
    # raw_text = raw_text.strip()
    
    # analyse_data = json.loads(raw_text)   
    
    # key_clauses = [
    #     CLauseAnalysis(**clause)
    #     for clause in analyse_data.get("key_clauses",[])    
    # ] 
    
    # risk_flags = [
    #     RiskFlag(**flag)
    #     for risk in analyse_data.get("risk_flags",[])    
    # ] 
    # result = AnalysisResult(
    #     contract_id=contract_id,
    #     summary= analyse_data.get("summary",""),
    #     contract_type= analyse_data.get("contract_type","Unknown"),
    #     key_clauses=key_clauses,
    #     risk_flags=risk_flags,
    #     overall_risk_level=analyse_data.get("overall_risk_level","low"),
    #     recommendations=analyse_data.get("recommendations",[]),
    # )
    # return result