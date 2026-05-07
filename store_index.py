from src.helper import load_pdf, text_split, download_hugging_face_embeddings
#from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
import pinecone
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

# print(PINECONE_API_KEY)
# print(PINECONE_API_ENV)

# =========================
# LOAD DATA
# =========================

extracted_data = load_pdf("data/")

# =========================
# SPLIT INTO CHUNKS
# =========================

text_chunks = text_split(extracted_data)

print(f"Total chunks: {len(text_chunks)}")

# =========================
# LOAD EMBEDDINGS
# =========================

embeddings = download_hugging_face_embeddings()

# =========================
# INITIALIZE PINECONE
# =========================

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "mcq-project"

# Connect existing index
index = pc.Index(index_name)

# =========================
# CREATE VECTOR STORE
# =========================

docsearch = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# =========================
# ADD DOCUMENTS
# =========================

docsearch.add_documents(text_chunks)

print("Documents uploaded successfully!")








# PDFs
#  ↓
# LangChain Community Loaders
#  ↓
# RecursiveCharacterTextSplitter
#  ↓
# MiniLM Embeddings (384-dim)
#  ↓
# Pinecone v7
#  ↓
# Retriever
#  ↓
# Groq Llama 3.1
#  ↓
# LCEL RAG Chain