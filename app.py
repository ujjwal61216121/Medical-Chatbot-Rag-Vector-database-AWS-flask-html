


# from flask import Flask, render_template, request

# from dotenv import load_dotenv
# import os
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # =========================
# # LANGCHAIN IMPORTS
# # =========================

# from langchain_pinecone import PineconeVectorStore
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_groq import ChatGroq

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# from pinecone import Pinecone

# # =========================
# # LOCAL IMPORTS
# # =========================

# from src.helper import download_hugging_face_embeddings
# from src.prompt import *

# # =========================
# # FLASK APP
# # =========================

# app = Flask(__name__)

# # =========================
# # LOAD ENV VARIABLES
# # =========================

# load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# # =========================
# # EMBEDDINGS
# # =========================

# embeddings = download_hugging_face_embeddings()

# # =========================
# # PINECONE
# # =========================

# pc = Pinecone(api_key=PINECONE_API_KEY)

# index_name = "mcq-project"

# index = pc.Index(index_name)

# vectorstore = PineconeVectorStore(
#     index=index,
#     embedding=embeddings
# )

# # =========================
# # RETRIEVER
# # =========================

# retriever = vectorstore.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 3}
# )

# # =========================
# # GROQ LLM
# # =========================

# llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0.3
# )

# # =========================
# # PROMPT
# # =========================

# prompt = ChatPromptTemplate.from_template(prompt_template)

# # =========================
# # FORMAT DOCS
# # =========================

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# # =========================
# # LCEL CHAIN
# # =========================

# qa_chain = (
#     {
#         "context": retriever | format_docs,
#         "question": RunnablePassthrough()
#     }
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# # =========================
# # ROUTES
# # =========================

# @app.route("/")
# def index():
#     return render_template("chat.html")


# @app.route("/get", methods=["POST"])
# def chat():

#     msg = request.form["msg"]

#     print("User:", msg)

#     response = qa_chain.invoke(msg)

#     print("Response:", response)

#     return str(response)

# # =========================
# # RUN APP
# # =========================

# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",
#         port=8080,
#         debug=True
#     )

from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# =========================
# LOAD ENV
# =========================
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not PINECONE_API_KEY or not GROQ_API_KEY:
    raise ValueError("Missing API keys in .env file")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# =========================
# LANGCHAIN IMPORTS
# =========================
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from pinecone import Pinecone


# =========================
# LOCAL IMPORTS
# =========================
from src.helper import download_hugging_face_embeddings
from src.prompt import prompt_template


# =========================
# FLASK APP
# =========================
app = Flask(__name__)


# =========================
# EMBEDDINGS
# =========================
embeddings = download_hugging_face_embeddings()


# =========================
# PINECONE SETUP
# =========================
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "mcq-project"
index = pc.Index(index_name)

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


# =========================
# LLM (GROQ)
# =========================
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)


# =========================
# PROMPT
# =========================
prompt = ChatPromptTemplate.from_template(prompt_template)


# =========================
# FORMAT DOCS
# =========================
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# =========================
# CHAIN (RAG PIPELINE)
# =========================
qa_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]

    print("User:", msg)

    response = qa_chain.invoke(msg)

    print("Response:", response)

    return str(response)


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )