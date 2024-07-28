import streamlit as st
from Document_Upload import process_pdf, perform_similarity_search
from General_Query import get_chain
import os
import requests

st.set_page_config(
    page_title="Knowledge Management System", layout="wide"
)

def get_ollama_response(input_text):
    response = requests.post(
        "http://localhost:8000/query",
        json={'question': input_text}  # Ensure 'question' is correctly named
    )
    
    # Print the API response for debugging
    print("API Response:", response.json())
    
    if response.status_code == 200:
        return response.json().get('response', "No response found.")
    else:
        return f"Error: {response.status_code} - {response.text}"

st.title("Welcome to the Knowledge Management System")


tab1, tab2 = st.tabs(["Answers for uploaded documents", "Answer for any Topics"])


with tab1:
    st.header("Answers for uploaded documents")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        
        st.subheader("Processing PDF file...")
        pages = process_pdf("temp.pdf")
        
        if pages is not None:
            st.success("File processed successfully!")
            
          
            query = st.text_input("Enter your query:")
            
           
            if st.button("Search"):
                st.subheader("Searching for answers...")
                perform_similarity_search(pages, query)
        
        else:
            st.error("Failed to process the PDF file. Please check the file format and try again.")
        
       
        os.remove("temp.pdf")


with tab2:
    st.header("Ask General Question")
    input_text = st.text_input("Enter your question:")
    
    if st.button("Submit"):
        if input_text:
            try:
                response = get_ollama_response(input_text)
                st.success(f"Response: {response}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")
