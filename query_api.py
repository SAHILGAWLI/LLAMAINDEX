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
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
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

# --- Shared LLM and Chat Engine Setup ---
llm = OpenAI(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

context_prompt = (
    "You are a chatbot, able to have normal interactions, as well as talk "
    "about documents stored in the Pinecone index.\n"
    "Here are the relevant documents for the context:\n"
    "{context_str}\n"
    "Instruction: Use the previous chat history, or the context above, to interact and help the user. "
    "If the answer cannot be found in the above context, say 'I don't know based on the provided documents.'"
)

# --- Memory management for multi-user chat ---
from typing import Dict
from threading import Lock

# session_id -> ChatMemoryBuffer
chat_memories: Dict[str, ChatMemoryBuffer] = {}
chat_memories_lock = Lock()

def get_citizen_chat_engine(session_id: str):
    with chat_memories_lock:
        if session_id not in chat_memories:
            chat_memories[session_id] = ChatMemoryBuffer.from_defaults(token_limit=3900)
        memory = chat_memories[session_id]
    return index.as_chat_engine(
        chat_mode="condense_question",
        memory=memory,
        llm=llm,
        context_prompt=context_prompt,
        verbose=False,
    )

def get_chat_engine(session_id: str):
    with chat_memories_lock:
        if session_id not in chat_memories:
            chat_memories[session_id] = ChatMemoryBuffer.from_defaults(token_limit=3900)
        memory = chat_memories[session_id]
    return index.as_chat_engine(
        chat_mode="condense_plus_context",
        memory=memory,
        llm=llm,
        context_prompt=context_prompt,
        verbose=False,
    )

query_engine = index.as_query_engine()

# ---------------------------------------------
# FastAPI App
# ---------------------------------------------
app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

class CitizenChatRequest(BaseModel):
    session_id: str
    message: str

class CitizenChatResponse(BaseModel):
    answer: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    try:
        response = query_engine.query(request.question)
        return QueryResponse(answer=str(response))
    except Exception as e:
        logging.error(f"Error during query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        chat_engine = get_chat_engine(request.session_id)
        response = chat_engine.chat(request.message)
        return ChatResponse(answer=str(response))
    except Exception as e:
        logging.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import StreamingResponse

@app.post("/citizen_chat", response_model=CitizenChatResponse)
def citizen_chat_endpoint(request: CitizenChatRequest):
    try:
        chat_engine = get_citizen_chat_engine(request.session_id)
        response = chat_engine.chat(request.message)
        return CitizenChatResponse(answer=str(response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Streaming endpoint for citizen chat
# Usage: POST /citizen_chat_stream with JSON {"session_id": ..., "message": ...}
# Returns a streaming text/plain response with tokens as they are generated.
@app.post("/citizen_chat_stream")
def citizen_chat_stream_endpoint(request: CitizenChatRequest):
    try:
        chat_engine = get_citizen_chat_engine(request.session_id)
        response = chat_engine.stream_chat(request.message)
        def token_stream():
            for token in response.response_gen:
                yield token
        return StreamingResponse(token_stream(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "LlamaIndex Pinecone Query API is running."}
