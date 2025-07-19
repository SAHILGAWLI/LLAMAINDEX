# ---------------------------------------------
# FastAPI Server for LlamaIndex Pinecone Query
# ---------------------------------------------
import os
import sys
import logging
from dotenv import load_dotenv
import openai
import pinecone
from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---------------------------------------------
# Environment Variables and Logging
# ---------------------------------------------
load_dotenv()  # Load .env file

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ---------------------------------------------
# API Keys Setup
# ---------------------------------------------
api_key = os.environ["PINECONE_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

# ---------------------------------------------
# Pinecone and LlamaIndex Setup
# ---------------------------------------------
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("quickstart")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()

# ---------------------------------------------
# FastAPI App
# ---------------------------------------------
app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    try:
        response = query_engine.query(request.question)
        return QueryResponse(answer=str(response))
    except Exception as e:
        logging.error(f"Error during query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "LlamaIndex Pinecone Query API is running."}
