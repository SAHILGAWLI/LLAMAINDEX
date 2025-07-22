# ---------------------------------------------
# FastAPI Server for LlamaIndex Pinecone Query
# ---------------------------------------------
import os
import sys
import logging
from dotenv import load_dotenv
import openai
import os
from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
from datetime import datetime

# ---------------------------------------------
# Environment Variables and Logging
# ---------------------------------------------
load_dotenv()  # Load .env file

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ---------------------------------------------
# API Keys Setup
# ---------------------------------------------
api_key = os.environ.get("PINECONE_API_KEY")
if not api_key:
    raise RuntimeError("PINECONE_API_KEY environment variable is not set.")
openai.api_key = os.environ["OPENAI_API_KEY"]

# ---------------------------------------------
# Pinecone and LlamaIndex Setup
# ---------------------------------------------
# Use new Pinecone client
pc = Pinecone(api_key=api_key)

index_name = "zhoop"
# Check if index exists, if not, create it (adjust dimension as needed)
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Make sure this matches your embedding size
        metric="cosine",
        spec=ServerlessSpec(cloud="gcp", region="us-central1")
    )
pinecone_index = pc.Index(index_name)
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
app = FastAPI()

# Add CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------------------------------

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
import asyncio
import time
from datetime import datetime

# Import new agent system
from models import (
    DashboardRequest, DashboardResponse, GridRequest,
    ComplianceResponse, LawsResponse, DocumentsResponse, PastCasesResponse,
    ErrorResponse
)
from agents import agent_manager
from parsers import ResponseParser

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

# ---------------------------------------------
# New ReAct Agent Endpoints for Grid Population
# ---------------------------------------------

@app.post("/dashboard/populate", response_model=DashboardResponse)
async def populate_dashboard(request: DashboardRequest):
    """
    Master endpoint that populates all 4 grids using ReAct agents
    """
    try:
        start_time = time.time()
        
        # Run all agents in parallel
        agent_responses = await agent_manager.populate_dashboard(
            request.case_id, 
            request.case_context
        )
        
        # Parse responses into structured format
        parsed_responses = ResponseParser.parse_all_responses(
            agent_responses, 
            request.case_id, 
            request.case_context
        )
        
        generation_time = time.time() - start_time
        
        return DashboardResponse(
            grid_1_compliance=parsed_responses["compliance"],
            grid_2_laws=parsed_responses["legal"],
            grid_3_documents=parsed_responses["documents"],
            grid_4_cases=parsed_responses["cases"],
            generation_time=generation_time,
            ai_confidence=0.85  # Default confidence score
        )
        
    except Exception as e:
        logging.error(f"Error populating dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dashboard/populate-hierarchical", response_model=DashboardResponse)
async def populate_dashboard_hierarchical(request: DashboardRequest):
    """
    Populate dashboard using hierarchical agent execution for enhanced results.
    
    Execution Flow:
    1. Laws Agent (Most Independent) - Establishes legal framework
    2. Compliance Agent - Enhanced with legal context
    3. Documents Agent - Enhanced with legal + compliance context  
    4. Cases Agent - Enhanced with all previous context
    
    This approach yields superior results by leveraging inter-agent dependencies.
    """
    try:
        start_time = time.time()
        
        # Run agents in hierarchical order with context passing
        agent_responses = await agent_manager.populate_dashboard_hierarchical(
            request.case_id, 
            request.case_context
        )
        
        # Parse responses into structured format
        parsed_responses = ResponseParser.parse_all_responses(
            agent_responses, 
            request.case_id, 
            request.case_context
        )
        
        generation_time = time.time() - start_time
        
        return DashboardResponse(
            grid_1_compliance=parsed_responses["compliance"],
            grid_2_laws=parsed_responses["legal"],
            grid_3_documents=parsed_responses["documents"],
            grid_4_cases=parsed_responses["cases"],
            generation_time=generation_time,
            ai_confidence=0.92  # Higher confidence due to enhanced context
        )
        
    except Exception as e:
        logging.error(f"Error in hierarchical dashboard population: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grid/compliance", response_model=ComplianceResponse)
async def get_compliance_grid(request: GridRequest):
    """
    Get compliance checklist for Grid 1
    """
    try:
        query = f"Generate FHIR compliance checklist for case {request.case_id}"
        if request.context:
            query += f" with context: {request.context}"
        
        response = await agent_manager.run_single_agent("compliance", query)
        
        from parsers import ComplianceParser
        return ComplianceParser.parse(response, request.case_id)
        
    except Exception as e:
        logging.error(f"Error getting compliance grid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grid/laws", response_model=LawsResponse)
async def get_laws_grid(request: GridRequest):
    """
    Get relevant BNS laws for Grid 2
    """
    try:
        query = f"Find relevant BNS law sections for case {request.case_id}"
        if request.context:
            query += f" with context: {request.context}"
        
        response = await agent_manager.run_single_agent("legal", query)
        
        from parsers import LegalParser
        return LegalParser.parse(response, request.context or "")
        
    except Exception as e:
        logging.error(f"Error getting laws grid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grid/documents", response_model=DocumentsResponse)
async def get_documents_grid(request: GridRequest):
    """
    Get document analysis for Grid 3
    """
    try:
        query = f"Analyze and prioritize documents for case {request.case_id}"
        if request.context:
            query += f" with context: {request.context}"
        
        response = await agent_manager.run_single_agent("documents", query)
        
        from parsers import DocumentParser
        return DocumentParser.parse(response, request.case_id)
        
    except Exception as e:
        logging.error(f"Error getting documents grid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grid/cases", response_model=PastCasesResponse)
async def get_cases_grid(request: GridRequest):
    """
    Get similar past cases for Grid 4
    """
    try:
        query = f"Find similar past cases to case {request.case_id}"
        if request.context:
            query += f" with context: {request.context}"
        
        response = await agent_manager.run_single_agent("cases", query)
        
        from parsers import CaseParser
        return CaseParser.parse(response, request.context or "")
        
    except Exception as e:
        logging.error(f"Error getting cases grid: {e}")
        raise HTTPException(status_code=500, detail=str(e))


        from parsers import ResponseParser
        parsed_responses = ResponseParser.parse_all_responses_with_grid5(
            agent_responses, 
            request.case_id, 
            request.case_context
        )
        
        generation_time = time.time() - start_time
        
        # Build enhanced dashboard response
        from models import EnhancedDashboardResponse
        response = EnhancedDashboardResponse(
            grid_1_compliance=parsed_responses["compliance"],
            grid_2_laws=parsed_responses["legal"],
            grid_3_documents=parsed_responses["documents"],
            grid_4_cases=parsed_responses["cases"],
            grid_5_live_cases=parsed_responses.get("live_cases"),
            generation_time=generation_time,
            ai_confidence=0.95,  # Highest confidence with all grids
            total_api_calls=(
                parsed_responses.get("live_cases").api_calls_made 
                if parsed_responses.get("live_cases") else 0
            )
        )
        
        logging.info(
            f"Enhanced dashboard completed: {generation_time:.2f}s, "
            f"Grid 5: {response.grid_5_live_cases.total_found if response.grid_5_live_cases else 0} cases"
        )
        
        return response
        
    except Exception as e:
        logging.error(f"Error in enhanced dashboard population: {e}")
        # Graceful fallback to Grid 1-4 only
        try:
            return await _fallback_to_grid_1_4(request, start_time, error_message=str(e))
        except Exception as fallback_error:
            logging.error(f"Fallback also failed: {fallback_error}")
            raise HTTPException(
                status_code=500, 
                detail=f"Dashboard population failed: {str(e)}. Fallback also failed: {str(fallback_error)}"
            )

async def _fallback_to_grid_1_4(request: DashboardRequest, start_time: float, error_message: str = None) -> EnhancedDashboardResponse:
    """
    Fallback function to provide Grids 1-4 when Grid 5 is unavailable
    """
    logging.info("Executing fallback to Grids 1-4 only")
    
    fallback_responses = await agent_manager.populate_dashboard_hierarchical(
        request.case_id, request.case_context
    )
    
    from parsers import ResponseParser
    parsed_fallback = ResponseParser.parse_all_responses(
        fallback_responses, request.case_id, request.case_context
    )
    
    from models import EnhancedDashboardResponse
    return EnhancedDashboardResponse(
        grid_1_compliance=parsed_fallback["compliance"],
        grid_2_laws=parsed_fallback["legal"],
        grid_3_documents=parsed_fallback["documents"],
        grid_4_cases=parsed_fallback["cases"],
        grid_5_live_cases=None,
        generation_time=time.time() - start_time,
        ai_confidence=0.85,
        total_api_calls=0,
        error_message=f"Grid 5 unavailable: {error_message}" if error_message else "Grid 5 unavailable"
    )

# ---------------------------------------------
# Streaming Endpoints for Real-time Updates
# ---------------------------------------------

@app.websocket("/dashboard/stream")
async def dashboard_stream(websocket):
    """
    WebSocket endpoint for real-time dashboard updates
    """
    await websocket.accept()
    
    try:
        while True:
            # Wait for client message
            data = await websocket.receive_json()
            
            case_id = data.get("case_id")
            case_context = data.get("case_context", "")
            
            if not case_id:
                await websocket.send_json({
                    "error": "case_id is required"
                })
                continue
            
            # Stream agent responses as they complete
            agents = ["compliance", "legal", "documents", "cases"]
            
            for i, agent_name in enumerate(agents):
                try:
                    # Send progress update
                    await websocket.send_json({
                        "type": "progress",
                        "grid": i + 1,
                        "status": f"Processing {agent_name}...",
                        "progress": (i / len(agents)) * 100
                    })
                    
                    # Run agent
                    query = f"Analyze case {case_id} with context: {case_context}"
                    response = await agent_manager.run_single_agent(agent_name, query)
                    
                    # Send grid update
                    await websocket.send_json({
                        "type": "grid_update",
                        "grid": i + 1,
                        "agent": agent_name,
                        "data": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "grid": i + 1,
                        "error": str(e)
                    })
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "message": "Dashboard population complete"
            })
            
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e)
        })
    finally:
        await websocket.close()

# ---------------------------------------------
# Health Check and Status Endpoints
# ---------------------------------------------

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents_available": list(agent_manager.agents.keys()),
        "version": "2.0.0"
    }

@app.get("/agents/status")
def agents_status():
    """
    Get status of all agents
    """
    return {
        "agents": {
            name: {
                "name": agent.name,
                "status": "ready",
                "tools_count": len(agent.agent.tools)
            }
            for name, agent in agent_manager.agents.items()
        },
        "total_agents": len(agent_manager.agents)
    }

@app.get("/")
def root():
    return {
        "message": "LlamaIndex Pinecone Query API with ReAct Agents is running.",
        "version": "2.0.0",
        "features": [
            "Multi-agent RAG system",
            "Intelligent grid population", 
            "Real-time streaming",
            "Legal compliance analysis"
        ],
        "endpoints": {
            "dashboard": "/dashboard/populate",
            "grids": ["/grid/compliance", "/grid/laws", "/grid/documents", "/grid/cases"],
            "streaming": "/dashboard/stream",
            "health": "/health"
        }
    }
