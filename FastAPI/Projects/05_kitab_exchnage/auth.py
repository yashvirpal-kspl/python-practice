from fastapi import Header, HTTPException

# in prodction, you add this in .env 
API_KEY = "mysecretapikey"

def verify_api_key(x_api_key: str = Header(...)):
    """Verify the API key provided in the request header. """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key