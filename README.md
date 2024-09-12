This project implements a Retrieval-Augmented Generation (RAG) model, designed to provide intelligent responses based on both uploaded documents and external knowledge sources like Wikipedia and arXiv. RAG combines the strengths of document retrieval and generation models, ensuring that the chatbot can answer questions based on relevant documents, even if they are not part of its pre-training. By embedding the uploaded documents and using these embeddings to retrieve the most relevant information, RAG enhances the accuracy and relevance of the model’s responses.

Folder Structure

![image](https://github.com/user-attachments/assets/920c03c8-1b75-40c8-8a39-561dc8d2da36)


This project consists of a FastAPI server and a Streamlit client interface. Users can upload documents (PDF or TXT) via the client, which will then be split into smaller chunks and embedded for question answering. The embedded vectors are stored and processed using a vector store (powered by FAISS), allowing for efficient retrieval. When users ask questions, the model leverages these embeddings to answer accurately based on the uploaded documents.

If no document is uploaded, the model switches to using external tools like Wikipedia and arXiv to generate responses.

Key Features:

- RAG model to combine retrieval with generation.
- Document upload functionality with automated chunking and embedding.
- Streamlit UI for easy interaction.
- Integration with Wikipedia and arXiv as fallback knowledge sources.
