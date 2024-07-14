It’s a comprehensive system to extract knowledge’s and the management of extracted knowledge, thus I named as Knowledge Management System.

Framework: Langchain and for LLMOps:  Langsmith
Frontend: Streamlet, backend Python
Vector Database: FAISS, Chroma DB

Main functionalities in a pipeline to be developed are as follows:
1. Streamline document management and enhance information retrieval by supporting the upload functionalities of diverse document types

Completion level: 
* At the beginning completed the coding part using only python in the backend
* Later completed coding part, using python in the backend and streamlet in the frontend.
* LLM model used for this module is OpenAI
* Will develop the enhancement code as and when the system matures

2. General Query reply it replies to the question prompt as asked.
Completion level:

Completed the general question answering, implementing the techniques of storing the answer received in FAISS (vector database) maintaining the cache for faster retrieval.
* LLM model used for this module is Ollama
* many enhancement is yet to be done, like answer with real time data, reinforcement learning etc and will keep on working on it.

3. Personal Financial Advice: this module provides smart financial advice to the people based on people earnings; expenses so the people can avoid costly errors mitigate risk. It also offers services and products to the people.

Completion level:
* Started collecting the requirement and data other major part is yet to be implemented.
*Planning to use LLM model Ollama.

Notes:
query_pdf_python.pynb: This file contains the code only of backend and doesnot interact with frontend.
Document_Upload.py: This file contains the code for PDF document uploads and question answer based on PDF.
General_Query.py: This file contains the code of generic question answer.
mains.py: This file contains streamlet code. We can run this file so that the application is up and running.






