from pymongo import MongoClient
from config import MONGODB_URL

client = MongoClient(MONGODB_URL)
db = client["mydb"]  #get the default database specified in the connection string

# Collections
contracts_collection = db["contracts"]
analysis_collection = db["analysis"]


def init_db():
    # Create indexes for the collections if they don't exist
    contracts_collection.create_index("filename", unique=True)
    analysis_collection.create_index("analysis_id", unique=True)