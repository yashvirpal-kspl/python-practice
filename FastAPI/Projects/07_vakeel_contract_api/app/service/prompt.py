CONTRACT_ANALYSIS_PROMPT="""
    You are an expert legal analyst specialization in Indian contract law.
    Analyze the following contract text and provide a structred analysis

    CONTRACT_TEXT:
    {contract_text}
    
    Provide your structred analysis as JSON object with exactly this structer:
    {{
        "summery": "A 2-3 sentence summary of what this is about",
        "contract_type":"The type of contract (e.g. NDA,Service agreement,Employment Contract)",
        "key_clauses":[
            {{
                "clause_title":"Name of the clause",
                "clause_text":"The relevant text from the contract",
                "explanation":"What this clause means in simple terms",
                "is_standard":True or False,
            }}
        ],
        "risk_flags":[
            "risk_title":"Short title of the risk",
            "description":"What the risk is",
            "risk_level":"low or medium or high or critical",
            "recommendation":"What to do about it",
            "clause_reference":"Which clause this refers to"
        ],
        "overall_risk_level":"low or medium or high or critical",
        "recommendations":[
            "Recommendation 1",
            "Recommendation 2",
        ]
    }}
    Rules:
    - Identify at least 3-5 key clauses
    - Flag any unusual, missing or one-sided clauses as risks
    - Be specific with clause references
    - Keep Explanations simple and clear 
    - Return only the JSOn object, no othe rtext 
"""

CLAUSE_EXTRACTION_PROMPT=""" 
    Extract all distinct clauses from this contract text.
    for each clause, provide the title an dfull text
    
    
    CONTRACT_TEXT:
    {contract_text}
    
    
    Return as a JSON Array:
    
    [
        {{
            "clause_title":"Title",
            "clause"text":"Full text of the clause"
        }}
    ]
    
    Return only the JSON array, no other text

"""


RISK_ASSESSMENT_PROMPT="""

    You are a leagal risk assessor. Review these contract clauses and flag any risks.

    CONTRACT_TEXT:
    {contract_text}
    
    FOr each risk found, provide:
    {{
        "risk_title":"Short Title",
        "description": "What make this risky",
        "risk_level":"low or medium or high or critical",
        "recommmendation":"What to do",
        "clause_reference":"Which CLause"
    }}
    
    Return as a JSON array. Return only the JSON array, no other text.
    
"""

SUMMERY_PROMPT="""
    Summerize this contract in 3- sentences for non-lawyer.
    Include: What it's about, who the parties are, key obligations, and duration
    

    CONTRACT_TEXT:
    {contract_text}
    
    Return only the summary text, no JSON 

"""