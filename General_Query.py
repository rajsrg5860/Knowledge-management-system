import os
from fastapi import FastAPI
import uvicorn
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

# Load environment variables
load_dotenv()

api_key = os.getenv("LANGCHAIN_API_KEY")
if api_key is None:
    raise ValueError("The LANGCHAIN_API_KEY environment variable is not set. Please configure it.")
os.environ["LANGCHAIN_API_KEY"] = api_key

# Initialize FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="API Server"
)

# Define Pydantic model for request body
class QueryRequest(BaseModel):
    question: str

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Rajan intelligent query system."),
    ("user", "{question}")
])

# Initialize LLM and output parser
llm = Ollama(model="llama2")
output_parser = StrOutputParser()

# Initialize FAISS index and SentenceTransformer model
index = faiss.IndexFlatL2(384)  
model = SentenceTransformer('all-MiniLM-L6-v2')
stored_responses = {}

def add_to_index(question, response):
    question_vector = model.encode([question])
    question_vector = np.array(question_vector, dtype=np.float32)
    index.add(question_vector)
    stored_responses[index.ntotal - 1] = response

def get_similar_response(question):
    question_vector = model.encode([question])
    question_vector = np.array(question_vector, dtype=np.float32)
    D, I = index.search(question_vector, k=1)  # Ensure input is float32
    if D[0][0] < 0.4:  # Threshold for similarity
        return stored_responses[I[0][0]]
    return None

def get_chain(question):
    normalized_question = question.lower()  
    cached_response = get_similar_response(normalized_question)
    
    if cached_response:
        return cached_response
    
    if ("capital" in normalized_question or 
        "who" in normalized_question or 
        "what" in normalized_question or 
        "when" in normalized_question):
        # For short responses
        short_prompt = prompt.format(question=question) + " Please answer in one sentence."
        chain = prompt | llm | output_parser
        response = chain.invoke({'question': short_prompt})
    else:
        # For long responses
        long_prompt = prompt.format(question=question)
        chain = prompt | llm | output_parser
        response = chain.invoke({'question': long_prompt})

    add_to_index(normalized_question, response)
    return response

# Add routes using the specified method
def add_routes(app, chain, path):
    @app.post(path)
    async def query(request: QueryRequest):  # Use the Pydantic model here
        response = chain(request.question)
        return {"response": response}

# Add the routes
add_routes(app, get_chain, path="/query")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
