import base64
import json
from google import genai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

CROP_ANALYSIS_PROMPT = """
    You are an expert agricultural scientist specializing in crop disease detection.
Analyze this image of a crop/plant and provide a detailed disease assessment.

Provide your analysis as a JSON object with exactly this structure:

{
"crop_detected": "Name of the crop or plant visible in the image",
"severity": "healthy" or "mild" or "moderate" or "severe" or "critical",
"diseases": [
        {
            "name": "Disease name",
            "confidence": 0.0 to 1.0,
            "description": "Brief description of the disease and visible symptoms"
        }
    ],
"treatments": [
        {
            "treatment_name": "Name of treatment",
            "treatment_type": "organic" or "chemical" or "preventive",
            "instructions": "Step by step treatment instructions",
            "urgency": "immediate" or "within_week" or "seasonal"
        }
    ],
    "overall_health": "One sentence summary of plant health",
    "additional_notes": "Any other observations or recommendations"
}
"""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def analyse_image(image_path: str, content_type: str):
    """
    Analyse the image content using Google GenAI for disease detection.
    """

    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="gpt-5.5",
        input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": CROP_ANALYSIS_PROMPT },
                {
                    "type": "input_image",
                    "image_url": f"data:{content_type};base64,{base64_image}",
                },
            ],
        }
    ],
    )

    print(f"Raw response from GenAI: {response.output_text}")
    return json.loads(response.output_text)

   
    
   
    