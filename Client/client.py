import streamlit as st
from PyPDF2 import PdfReader 
import requests
import tempfile

# API URL
API_URL = "http://localhost:8000"  

st.title('RAG with LLaMA 3.1 - Client Interface')

# File Upload Section
uploaded_file = st.file_uploader("Upload a PDF or TXT file (Optional)", type=['pdf', 'txt'])

if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())  # Write the uploaded file content to temp file
        temp_file_path = temp_file.name  # Get the temp file path

    # Determine the file type
    file_type = uploaded_file.name.split('.')[-1]
    
    # Extract text from the file based on its type
    text = ""
    if file_type == 'pdf':
        # Extract text from PDF
        try:
            with open(temp_file_path, 'rb') as f:
                pdf = PdfReader(f)
                text = ''.join([page.extract_text() for page in pdf.pages])
            st.write("PDF content loaded successfully, waiting for llama to extract it....")
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
    elif file_type == 'txt':
        # Extract text from TXT
        try:
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            st.write("Text file content loaded successfully, waiting for llama to extract it....")
        except UnicodeDecodeError:
            st.error("Error: Unsupported encoding. Could not read the text file.")
        except Exception as e:
            st.error(f"Error reading text file: {e}")
    else:
        st.error("Unsupported file format.")

    # Send the extracted text to FastAPI server
    if text:
        response = requests.post(f"{API_URL}/uploadfile", json={"text": text})

        # Check the server's response for file processing
        if response.status_code == 200:
            result = response.json()
            if "message" in result:
                st.success(result["message"])
            elif "error" in result:
                st.error(result["error"])
            else:
                st.write(result)
        else:
            st.error(f"Text upload failed with status code {response.status_code}")


# Chat Section
query = st.text_input("Enter your question or start chatting:")

if query:
    # Send query to FastAPI server
    response = requests.post(f"{API_URL}/query", json={"query": query})

    if response.status_code == 200:
        result = response.json()
        if "result" in result:
            st.write(result['result'])
        else:
            st.error(result.get('error', 'An error occurred.'))
    else:
        st.error("Query failed.")
