from fastapi import APIRouter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI


router = APIRouter(
    prefix="/query",
    tags=["query"]
)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="sample_collection",   
    url="http://localhost:6333"
    )

@router.post("/")
async def query(question: str):
    """
    This function takes a question as input and returns the answer.
    """
    #return {"question": question, "answer": "This is a test answer."}
    search_result = vector_db.similarity_search(query=question)
   # print(f"Search result for '{question}' : {search_result}")
    
    context = " ".join([
        f"[Page{doc.metadata.get('page', 'Unknown')}]: {doc.page_content}"  
        for doc in search_result
        ])
    
    SYSTEM_PROMPT = f"""You are a helpful assistant that answers questions based on the context provided.
If the answer is not contained within the context, you should respond with "I don't know."

Also include the page number of the context in your answer. The context is below.
Context: {context}

"""
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        #temperature=0.2,
        #max_tokens=200
    )
    #return {"question": question, "answer": search_result}
    return {"question": question, "answer": response.choices[0].message.content}