from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.tools.retriever import create_retriever_tool

embeddings = OllamaEmbeddings()

# Store the tools globally
tools = []

def add_file_to_vector_store(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_text(text)
    vectordb = FAISS.from_texts(documents, OllamaEmbeddings())
    retriever = vectordb.as_retriever()
    
    # Add retriever to tools list
    retriever_tool = create_retriever_tool(retriever, "Uploaded File Search", "Search information from the uploaded file")
    tools.append(retriever_tool)
    print(tools)
    return "file content extracted successfully."
