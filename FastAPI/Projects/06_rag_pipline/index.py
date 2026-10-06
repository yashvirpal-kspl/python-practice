from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
#from langchain.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv() # .env file should be in the same directory as this script

pdf_path = Path(__file__).parent / "data" / "sample.pdf"

#PDF Loader
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

#Split the docs into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0
    )
chunks = text_splitter.split_documents(docs)

# Embedding the chunks using OpenAI Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)


# Create a QdrantVectorStore instance
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333"
)

print("Vector store created and documents embedded successfully.")