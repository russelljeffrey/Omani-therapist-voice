import os
import logging
import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

logging.basicConfig(
    filename="crisis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Suppress ChromaDB telemetry + non-critical logs
logging.getLogger("chromadb").setLevel(logging.ERROR)

KB_PATH = "data/kb/"
CHROMA_PATH = "data/chroma_db"  # Persistent Chroma DB
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

def load_documents():
    """Load and split KB files, with error handling."""
    docs = []
    if not os.path.exists(KB_PATH):
        logging.error(f"Knowledge base directory {KB_PATH} does not exist")
        st.warning(f"Knowledge base directory {KB_PATH} not found. Using fallback document.")
        return [Document(page_content="No knowledge base documents available.", metadata={"source": "fallback"})]
    
    for file in os.listdir(KB_PATH):
        file_path = os.path.join(KB_PATH, file)
        try:
            if not os.path.isfile(file_path):
                logging.warning(f"Skipping {file_path}: Not a file")
                continue
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                file_docs = loader.load()
                docs.extend(file_docs)
                logging.info(f"Loaded PDF: {file_path} with {len(file_docs)} pages")
            elif file.endswith(".txt"):
                loader = TextLoader(file_path)
                file_docs = loader.load()
                docs.extend(file_docs)
                logging.info(f"Loaded text file: {file_path} with {len(file_docs)} chunks")
        except Exception as e:
            logging.error(f"Error loading {file_path}: {str(e)}")
            st.warning(f"Failed to load {file_path}. Skipping.")
    
    if not docs:
        logging.warning("No documents loaded from knowledge base")
        st.warning("No valid documents found in knowledge base. Using fallback document.")
        docs = [Document(page_content="No knowledge base documents available.", metadata={"source": "fallback"})]
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)
    logging.info(f"Split {len(docs)} documents into {len(split_docs)} chunks")
    return split_docs

def setup_vectorstore(force_rebuild=False):
    """Setup or load Chroma vectorstore."""
    try:
        if force_rebuild or not os.path.exists(CHROMA_PATH):
            docs = load_documents()
            if not docs:
                raise ValueError("No documents available for vectorstore creation")
            vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_PATH)
            vectorstore.persist()
            logging.info(f"Created new vectorstore at {CHROMA_PATH} with {len(docs)} documents")
        else:
            vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
            logging.info(f"Loaded existing vectorstore from {CHROMA_PATH}")
        return vectorstore
    except Exception as e:
        logging.error(f"Error setting up vectorstore: {str(e)}")
        st.error(f"Failed to initialize vectorstore: {str(e)}. App may have limited functionality.")
        # Return a dummy vectorstore to prevent app crash
        return Chroma.from_texts(
            texts=["No knowledge base available"], 
            embedding=embeddings, 
            persist_directory=CHROMA_PATH
        )

def retrieve_context(query, k=3):
    """Retrieve relevant chunks from KB."""
    try:
        retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": k})
        docs = retriever.get_relevant_documents(query)
        return docs
    except Exception as e:
        logging.error(f"Error retrieving context: {str(e)}")
        st.warning(f"Failed to retrieve context: {str(e)}. Using fallback response.")
        return [Document(page_content="Unable to retrieve context.", metadata={"source": "error"})]