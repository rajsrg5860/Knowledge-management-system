import streamlit as st
from Document_Upload import process_pdf, perform_similarity_search
from General_Query import get_chain
import os

st.set_page_config(
    page_title="Knowledge Management System", layout="wide"
)

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
    
    if st.button("Get Answer"):
        if input_text:
            answer = get_chain(input_text)  # Call the function from Question_answer.py
            st.write(answer)
        else:
            st.error("Please enter a question.")
