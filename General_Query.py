import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


load_dotenv()

api_key = os.getenv("LANGCHAIN_API_KEY")
if api_key is None:
    raise ValueError("The LANGCHAIN_API_KEY environment variable is not set. Please configure it.")
os.environ["LANGCHAIN_API_KEY"] = api_key

# prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "rajan intelligent query system."),
    ("user", "{question}")
])


llm = Ollama(model="llama2")
output_parser = StrOutputParser()


index = faiss.IndexFlatL2(384)  
model = SentenceTransformer('all-MiniLM-L6-v2')
stored_responses = {}

def add_to_index(question, response):
    question_vector = model.encode([question])
    index.add(question_vector)
    stored_responses[index.ntotal - 1] = response

def get_similar_response(question):
    question_vector = model.encode([question])
    D, I = index.search(question_vector, k=1)
    if D[0][0] < 0.4:  
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
        add_to_index(normalized_question, response)
        return response
    else:
        # For long responses
        long_prompt = prompt.format(question=question)
        chain = prompt | llm | output_parser
        response = chain.invoke({'question': long_prompt})
        add_to_index(normalized_question, response)
        return response

