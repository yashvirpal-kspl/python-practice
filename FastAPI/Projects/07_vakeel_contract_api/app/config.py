from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
ALLOWED_EXTENSIONS = [".pdf", ".txt"]
MAX_FILE_SIZE_MB = 10  # Maximum file size in megabytes
UPLOAD_DIR = "uploads"  # Directory to save uploaded files

GEMINI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")