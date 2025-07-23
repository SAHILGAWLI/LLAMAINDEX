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
from fastapi.middleware.cors import CORSMiddleware

# Additional imports for live cases functionality
import asyncio
import time
import requests
import urllib.parse
import http.client
import json
import re
from typing import Dict, List, Optional

# ---------------------------------------------
# Environment Variables and Logging
# ---------------------------------------------
load_dotenv()  # Load .env file

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
logger = logging.getLogger(__name__)

# ---------------------------------------------
# API Keys Setup
# ---------------------------------------------
api_key = os.environ["PINECONE_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

# ---------------------------------------------
# Pinecone and LlamaIndex Setup
# ---------------------------------------------
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("zhoop")
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

# Add CORS middleware for browser access (Next.js compatible)
# Environment-driven CORS configuration for production safety
allowed_origins = os.getenv("CORS_ORIGINS", 
    "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,https://zhoop.onrender.com"
).split(",")

# Add wildcard for development (remove CORS_ALLOW_ALL in production)
if os.getenv("CORS_ALLOW_ALL", "true").lower() == "true":
    allowed_origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization", 
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
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

# Live Cases Models (matching live_api_server.py exactly)
# Note: Using unified DashboardRequest from models.py

# Live Cases Models moved to models.py

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
    LiveCaseDocument, LiveCasesResponse,
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
    Advanced endpoint that populates all 5 grids using hierarchical execution.
    
    Execution Flow:
    1. Laws Agent (Most Independent) - Establishes legal framework
    2. Compliance Agent - Enhanced with legal context
    3. Documents Agent - Enhanced with legal + compliance context  
    4. Cases Agent - Enhanced with all previous context
    5. Live Cases Agent - Enhanced with ALL previous context
    
    This approach yields superior results by leveraging inter-agent dependencies.
    """
    try:
        start_time = time.time()
        
        # Run agents in hierarchical order with context passing
        logger.info(f"🚀 Starting hierarchical execution for case {request.case_id}")
        start_agents_time = time.time()
        
        agent_responses = await agent_manager.populate_dashboard_hierarchical(
            request.case_id, 
            request.case_context
        )
        
        agents_time = time.time() - start_agents_time
        logger.info(f"⚡ Agents completed in {agents_time:.2f}s")
        
        # Parse responses into structured format
        parsed_responses = ResponseParser.parse_all_responses(
            agent_responses, 
            request.case_id, 
            request.case_context
        )
        
        # TIER 5: Execute Live Cases with enhanced context from all previous agents
        live_cases_response = None
        try:
            logger.info(f"🔍 Starting TIER 5: Live Cases with enhanced context")
            tier5_start = time.time()
            
            # Build enhanced context from all previous agents
            enhanced_context = f"""
            LEGAL FRAMEWORK: {agent_responses.get('legal', '')[:300]}...
            COMPLIANCE REQUIREMENTS: {agent_responses.get('compliance', '')[:200]}...
            DOCUMENT INSIGHTS: {agent_responses.get('documents', '')[:200]}...
            SIMILAR PAST CASES: {agent_responses.get('cases', '')[:200]}...
            """
            
            # Create enhanced request for live cases
            live_request = DashboardRequest(
                case_id=request.case_id,
                case_context=request.case_context,
                additional_context=enhanced_context,
                user_role=request.user_role,
                jurisdiction=request.jurisdiction
            )
            
            # Execute live cases with enhanced context
            live_cases_response = await get_live_cases(live_request)
            
            tier5_time = time.time() - tier5_start
            logger.info(f"✅ Grid 5 (Live Cases) completed in {tier5_time:.2f}s with enhanced context")
            
        except Exception as e:
            logger.warning(f"⚠️ Grid 5 (Live Cases) failed: {e} - Continuing with 4-grid response")
        
        generation_time = time.time() - start_time
        
        return DashboardResponse(
            grid_1_compliance=parsed_responses["compliance"],
            grid_2_laws=parsed_responses["legal"],
            grid_3_documents=parsed_responses["documents"],
            grid_4_cases=parsed_responses["cases"],
            grid_5_live_cases=live_cases_response,
            generation_time=generation_time,
            ai_confidence=0.95 if live_cases_response else 0.92  # Higher confidence with Grid 5
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

# ---------------------------------------------
# Live Cases Utility Functions
# ---------------------------------------------

def build_optimized_search_query(case_context: str, additional_context: str = None) -> str:
    """Build optimized search query for Indian Kanoon API"""
    import re
    
    # Extract key legal terms from case context
    legal_keywords = {
        'medical', 'negligence', 'malpractice', 'surgical', 'doctor', 'hospital',
        'criminal', 'murder', 'theft', 'assault', 'fraud', 'corruption', 'bribery',
        'civil', 'constitutional', 'rights', 'discrimination', 'harassment',
        'contract', 'breach', 'agreement', 'commercial', 'property', 'land',
        'divorce', 'custody', 'marriage', 'employment', 'labor', 'worker'
    }
    
    # Extract keywords from case context
    context_words = set(re.findall(r'\b\w+\b', case_context.lower()))
    relevant_keywords = context_words.intersection(legal_keywords)
    
    # If we have relevant keywords, use them
    if relevant_keywords:
        query_parts = list(relevant_keywords)[:3]  # Limit to 3 most relevant
    else:
        # Fallback: extract first few meaningful words
        words = re.findall(r'\b[a-zA-Z]{4,}\b', case_context)
        query_parts = words[:3] if words else ['legal', 'case']
    
    # Build simple query
    search_query = ' '.join(query_parts)
    
    logger.info(f"🔍 Optimized search query: '{search_query}' (from: '{case_context[:100]}...')")
    return search_query

def get_api_mode():
    """Check if we're in live or demo mode"""
    return "live" if os.getenv("INDIAN_KANOON_API_TOKEN") else "demo"

async def search_indian_kanoon_api(query: str, max_results: int = 10):
    """Search using real Indian Kanoon API"""
    api_token = os.getenv("INDIAN_KANOON_API_TOKEN")
    if not api_token:
        raise HTTPException(status_code=503, detail="Indian Kanoon API token not configured")
    
    base_url = os.getenv("INDIAN_KANOON_BASE_URL", "https://api.indiankanoon.org")
    
    # Indian Kanoon API endpoint (based on ikapi.py)
    encoded_query = urllib.parse.quote_plus(query)
    url = f"/search/?formInput={encoded_query}&pagenum=1&maxpages=1"
    
    headers = {
        "Authorization": f"Token {api_token}",
        "Accept": "application/json"
    }
    
    try:
        logging.info(f"🔍 Searching Indian Kanoon API with query: {query}")
        
        # Make API request using http.client like ikapi.py
        connection = http.client.HTTPSConnection("api.indiankanoon.org")
        connection.request('POST', url, headers=headers)
        response = connection.getresponse()
        results = response.read()
        
        if isinstance(results, bytes):
            results = results.decode('utf8')
        
        if response.status == 200:
            try:
                data = json.loads(results) if results else {}
                logging.info(f"✅ Indian Kanoon API returned data: {str(data)[:500]}...")
                logging.info(f"🔍 Data type: {type(data)}, Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                # Indian Kanoon JSON has 'docs' key with list of case dicts
                if isinstance(data, dict):
                    return data.get('docs', [])
                return []
            except json.JSONDecodeError:
                logging.error(f"❌ Invalid JSON response: {results[:200]}...")
                return []
        else:
            logging.error(f"❌ Indian Kanoon API error: {response.status} - {results}")
            raise HTTPException(status_code=response.status, detail=f"Indian Kanoon API error: {results}")
            
    except Exception as e:
        logging.error(f"❌ Network error calling Indian Kanoon API: {e}")
        raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

def calculate_similarity_score(query: str, case_title: str, case_headline: str = "", case_citation: str = "", case_court: str = "") -> float:
    """Advanced legal similarity scoring with domain-specific intelligence"""
    try:
        # Normalize text
        query_lower = query.lower()
        title_lower = case_title.lower()
        headline_lower = case_headline.lower() if case_headline else ""
        citation_lower = case_citation.lower() if case_citation else ""
        court_lower = case_court.lower() if case_court else ""
        
        # Legal domain stop words (more comprehensive)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
            'case', 'involving', 'vs', 'v', 'versus', 'state', 'union', 'government', 'court', 'high', 'supreme'
        }
        
        # Legal priority keywords (higher weight)
        legal_priority_terms = {
            'negligence': 3.0, 'medical': 2.5, 'surgical': 2.5, 'malpractice': 3.0,
            'criminal': 2.0, 'civil': 2.0, 'constitutional': 2.5, 'contract': 2.0,
            'tort': 2.5, 'damages': 2.0, 'compensation': 2.0, 'liability': 2.5,
            'fraud': 2.5, 'breach': 2.0, 'defamation': 2.5, 'harassment': 2.5,
            'assault': 2.5, 'theft': 2.0, 'corruption': 3.0, 'bribery': 3.0
        }
        
        # Extract keywords from query
        query_words = set(re.findall(r'\b\w+\b', query_lower)) - stop_words
        
        # Calculate weighted matches
        def calculate_weighted_matches(text: str, words: set) -> float:
            matches = 0.0
            for word in words:
                if word in text:
                    weight = legal_priority_terms.get(word, 1.0)
                    matches += weight
            return matches
        
        # Multi-field scoring with different weights
        title_matches = calculate_weighted_matches(title_lower, query_words)
        headline_matches = calculate_weighted_matches(headline_lower, query_words)
        citation_matches = calculate_weighted_matches(citation_lower, query_words)
        
        # Court hierarchy bonus (Supreme Court > High Court > District Court)
        court_bonus = 0.0
        if 'supreme' in court_lower:
            court_bonus = 0.15
        elif 'high' in court_lower or 'hc' in court_lower:
            court_bonus = 0.10
        elif 'district' in court_lower or 'sessions' in court_lower:
            court_bonus = 0.05
        
        # Calculate total possible score
        total_query_weight = sum(legal_priority_terms.get(word, 1.0) for word in query_words)
        if total_query_weight == 0:
            return 0.5  # Default score
        
        # Weighted scoring
        title_score = (title_matches / total_query_weight) * 0.6
        headline_score = (headline_matches / total_query_weight) * 0.25
        citation_score = (citation_matches / total_query_weight) * 0.15
        
        base_score = title_score + headline_score + citation_score
        final_score = min(base_score + court_bonus, 1.0)
        
        return max(final_score, 0.1)  # Minimum 10% score
        
    except Exception as e:
        logging.error(f"Error calculating similarity: {e}")
        return 0.5

def add_case_intelligence(cases: List[LiveCaseDocument], query: str) -> List[LiveCaseDocument]:
    """Add intelligent case categorization and priority scoring for officers"""
    
    # Case type detection patterns
    case_patterns = {
        'Medical Negligence': ['medical', 'negligence', 'doctor', 'hospital', 'surgical', 'malpractice', 'treatment'],
        'Criminal': ['criminal', 'murder', 'theft', 'assault', 'fraud', 'bribery', 'corruption'],
        'Civil Rights': ['constitutional', 'fundamental', 'rights', 'discrimination', 'harassment'],
        'Contract Dispute': ['contract', 'breach', 'agreement', 'commercial', 'business'],
        'Property': ['property', 'land', 'real estate', 'possession', 'ownership'],
        'Family Law': ['divorce', 'custody', 'marriage', 'maintenance', 'adoption'],
        'Labor Law': ['employment', 'labor', 'worker', 'salary', 'termination']
    }
    
    # Priority levels for officers
    priority_mapping = {
        'Criminal': 'HIGH',
        'Medical Negligence': 'HIGH', 
        'Civil Rights': 'MEDIUM',
        'Contract Dispute': 'MEDIUM',
        'Property': 'LOW',
        'Family Law': 'LOW',
        'Labor Law': 'MEDIUM'
    }
    
    query_lower = query.lower()
    
    for case in cases:
        # Detect case type
        case_text = f"{case.title} {case.summary}".lower()
        detected_type = 'General'
        max_matches = 0
        
        for case_type, keywords in case_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in case_text or keyword in query_lower)
            if matches > max_matches:
                max_matches = matches
                detected_type = case_type
        
        # Add metadata to summary
        priority = priority_mapping.get(detected_type, 'MEDIUM')
        case.summary = f"[{detected_type} | {priority} Priority] {case.summary}"
        
        # Boost similarity for high-priority cases
        if priority == 'HIGH':
            case.similarity_score = min(case.similarity_score * 1.2, 1.0)
        elif priority == 'MEDIUM':
            case.similarity_score = min(case.similarity_score * 1.1, 1.0)
    
    return cases

def process_indian_kanoon_results(results: List[Dict], query: str = "") -> List[LiveCaseDocument]:
    """Process Indian Kanoon API results into our format"""
    processed_cases = []
    logger.info(f"🔍 Processing {len(results)} results from Indian Kanoon API")
    if results:
        try:
            logger.info(f"🔑 First doc keys: {list(results[0].keys())}")
            logger.info(f"📄 First doc sample: {json.dumps(results[0])[:800]}...")
        except Exception as _:
            pass
    
    for i, result in enumerate(results):
        logger.info(f"📋 Result {i+1}: {str(result)[:200]}...")
        try:
            # Extract information from Indian Kanoon result
            # Adjust field names based on actual API response structure
            case_doc = LiveCaseDocument(
                title=result.get('title') or result.get('doc_title') or result.get('case_name') or f'Case {i+1}',
                court=result.get('docsource') or result.get('court') or 'Unknown Court',
                date=result.get('publishdate') or 'Unknown Date',
                citation=result.get('citation') or 'No Citation',
                summary=(result.get('headline') or '')[:500] or 'No summary available',
                similarity_score=calculate_similarity_score(
                    query, 
                    result.get('title', ''), 
                    result.get('headline', ''),
                    result.get('citation', ''),
                    result.get('docsource', '')
                ),
                url=f"https://indiankanoon.org/doc/{result.get('tid')}/"
            )
            processed_cases.append(case_doc)
        except Exception as e:
            logger.error(f"❌ Error processing result {i}: {e}")
            continue
    
    return processed_cases

# Demo data fallback
DEMO_CASES = [
    {
        "title": "Demo Mode - Add Indian Kanoon API Token for Live Data",
        "court": "Demo Court",
        "date": "2024-01-01",
        "citation": "DEMO 2024",
        "summary": "This is demo data. Add your Indian Kanoon API token in the configuration to get real legal cases.",
        "similarity_score": 0.0,
        "url": "https://example.com"
    }
]

# ---------------------------------------------
# Live Cases Endpoint
# ---------------------------------------------

@app.post("/grid/live-cases", response_model=LiveCasesResponse)
async def get_live_cases(request: DashboardRequest):
    """Grid 5: Live Cases Analytics endpoint - REAL or DEMO"""
    try:
        start_time = time.time()
        api_mode = get_api_mode()
        
        logger.info(f"🔍 Processing case search in {api_mode} mode for: {request.case_context}")
        
        if api_mode == "live":
            # Use REAL Indian Kanoon API
            try:
                # Build optimized search query for Indian Kanoon API
                search_query = build_optimized_search_query(request.case_context, request.additional_context)
                
                # Search Indian Kanoon API
                api_results = await search_indian_kanoon_api(search_query, max_results=10)
                
                # Process results with similarity calculation
                processed_cases = process_indian_kanoon_results(api_results, search_query)
                
                # Add case categorization and priority scoring
                processed_cases = add_case_intelligence(processed_cases, search_query)
                
                # Sort by similarity score (highest first)
                processed_cases.sort(key=lambda x: x.similarity_score, reverse=True)
                
                generation_time = time.time() - start_time
                
                return LiveCasesResponse(
                    message=f"✅ LIVE cases analysis completed - Found {len(processed_cases)} relevant cases from Indian Kanoon API",
                    status="success",
                    cases=processed_cases,
                    total_cases=len(processed_cases),
                    generation_time=generation_time,
                    api_mode="live"
                )
                
            except Exception as e:
                logger.error(f"❌ Live API error: {e}")
                raise HTTPException(status_code=500, detail=f"Live API error: {str(e)}")
        
        else:
            # Demo mode fallback
            await asyncio.sleep(1)  # Simulate processing time
            
            demo_cases = [LiveCaseDocument(**case) for case in DEMO_CASES]
            generation_time = time.time() - start_time
            
            return LiveCasesResponse(
                message="⚠️ DEMO MODE - Add Indian Kanoon API token for live data",
                status="demo",
                cases=demo_cases,
                total_cases=len(demo_cases),
                generation_time=generation_time,
                api_mode="demo"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in Grid 5 live cases: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {
        "message": "LlamaIndex Pinecone Query API with ReAct Agents is running.",
        "version": "2.0.0",
        "features": [
            "Multi-agent RAG system",
            "Intelligent grid population", 
            "Real-time streaming",
            "Legal compliance analysis",
            "Live Indian Kanoon API integration",
            "Advanced legal case similarity scoring"
        ],
        "endpoints": {
            "dashboard": "/dashboard/populate",
            "grids": ["/grid/compliance", "/grid/laws", "/grid/documents", "/grid/cases", "/grid/live-cases"],
            "streaming": "/dashboard/stream",
            "health": "/health"
        }
    }