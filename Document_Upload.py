from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
import openai

from dotenv import load_dotenv

# Load environment variables from .env file (optional if you use a .env file)
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')




def process_pdf(file_path):
    
    try:
        
        loader = PyPDFLoader(file_path)
        
        # Load and split the PDF into pages
        pages = loader.load_and_split()
        
        return pages
    
    except Exception as e:
       
        print(f"Error processing PDF file {e}")
        return None

def perform_similarity_search(pages, query, k=2):
   
    try:
        
        faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
        
        docs = faiss_index.similarity_search(query, k=k)
        
        for doc in docs:
            print(f"Page {doc.metadata['page']}: {doc.page_content[:300]}")
    
    except Exception as e:
        print(f"Error performing similarity search {e}")
