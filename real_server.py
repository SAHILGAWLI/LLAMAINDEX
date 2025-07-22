#!/usr/bin/env python3
"""
Real FastAPI Server for Grid 5 Legal Dashboard
Uses actual Indian Kanoon API for live legal case data
"""

import os
import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Dashboard Grid 5 API - LIVE",
    description="Enhanced Legal Dashboard with REAL Indian Kanoon API Integration",
    version="2.0.0-LIVE"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import the real components
try:
    from indian_kanoon_client import IndianKanoonClient
    from query_builder import SmartQueryBuilder
    from agents import EnhancedAgentManager
    from parsers import ResponseParser
    from models import (
        DashboardRequest, DashboardResponse, 
        LiveCasesResponse, EnhancedDashboardResponse,
        CaseAnalytics, LiveCaseDocument
    )
    logger.info("✅ Successfully imported all Grid 5 LIVE components")
    LIVE_MODE = True
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    LIVE_MODE = False
    
    # Fallback models
    from pydantic import BaseModel
    
    class DashboardRequest(BaseModel):
        case_id: str
        case_context: str
        additional_context: Optional[str] = None
    
    class LiveCaseDocument(BaseModel):
        title: str
        court: str
        date: str
        citation: str
        summary: str
        similarity_score: float
        url: str
    
    class LiveCasesResponse(BaseModel):
        message: str
        status: str = "success"
        cases: List[LiveCaseDocument] = []
        total_cases: int = 0
        generation_time: float = 0.0

# Initialize components if in live mode
if LIVE_MODE:
    try:
        # Initialize Indian Kanoon client
        indian_kanoon_client = IndianKanoonClient()
        query_builder = SmartQueryBuilder()
        agent_manager = EnhancedAgentManager()
        logger.info("✅ LIVE components initialized successfully")
    except Exception as e:
        logger.error(f"❌ LIVE component initialization failed: {e}")
        LIVE_MODE = False

@app.get("/")
async def root():
    """Root endpoint with system status"""
    return {
        "message": "🏛️ Legal Dashboard Grid 5 API - LIVE MODE!",
        "version": "2.0.0-LIVE",
        "status": "active",
        "live_mode": LIVE_MODE,
        "features": [
            "Grid 1: Compliance Analysis",
            "Grid 2: Legal Research", 
            "Grid 3: Document Analysis",
            "Grid 4: Case Precedents",
            "Grid 5: Live Cases Analytics - REAL INDIAN KANOON API"
        ],
        "timestamp": datetime.now().isoformat(),
        "api_status": "🟢 LIVE" if LIVE_MODE else "🟡 FALLBACK"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    indian_kanoon_status = "✅ Ready" if os.getenv("INDIAN_KANOON_API_TOKEN") and LIVE_MODE else "❌ Token Missing or Components Failed"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "live_mode": LIVE_MODE,
        "components": {
            "indian_kanoon_api": indian_kanoon_status,
            "openai_api": "✅ Ready" if os.getenv("OPENAI_API_KEY") else "❌ Token Missing",
            "agent_manager": "✅ Ready" if LIVE_MODE else "❌ Not Available",
            "query_builder": "✅ Ready" if LIVE_MODE else "❌ Not Available"
        }
    }

@app.post("/grid/live-cases", response_model=LiveCasesResponse)
async def get_live_cases(request: DashboardRequest):
    """Grid 5: Live Cases Analytics endpoint - REAL API"""
    try:
        start_time = time.time()
        
        if not os.getenv("INDIAN_KANOON_API_TOKEN"):
            raise HTTPException(
                status_code=503, 
                detail="Indian Kanoon API token not configured. Please set INDIAN_KANOON_API_TOKEN environment variable."
            )
        
        if not LIVE_MODE:
            raise HTTPException(
                status_code=503, 
                detail="Live mode components not available. Check imports and configuration."
            )
        
        logger.info(f"🔍 Processing LIVE case search for: {request.case_context}")
        
        # Build intelligent query using SmartQueryBuilder
        query = query_builder.build_query(
            case_context=request.case_context,
            additional_context=request.additional_context or ""
        )
        
        logger.info(f"📝 Generated query: {query}")
        
        # Search using Indian Kanoon API
        search_results = await indian_kanoon_client.search_cases(
            query=query,
            max_results=10
        )
        
        logger.info(f"📊 Found {len(search_results)} cases from Indian Kanoon")
        
        # Process and score results
        processed_cases = []
        for case_data in search_results:
            try:
                # Extract case information
                case_doc = LiveCaseDocument(
                    title=case_data.get('title', 'Unknown Case'),
                    court=case_data.get('court', 'Unknown Court'),
                    date=case_data.get('date', 'Unknown Date'),
                    citation=case_data.get('citation', 'No Citation'),
                    summary=case_data.get('summary', case_data.get('snippet', 'No summary available')),
                    similarity_score=case_data.get('similarity_score', 0.0),
                    url=case_data.get('url', case_data.get('link', ''))
                )
                processed_cases.append(case_doc)
            except Exception as e:
                logger.error(f"❌ Error processing case: {e}")
                continue
        
        generation_time = time.time() - start_time
        
        return LiveCasesResponse(
            message=f"Live cases analysis completed successfully - Found {len(processed_cases)} relevant cases from Indian Kanoon",
            status="success",
            cases=processed_cases,
            total_cases=len(processed_cases),
            generation_time=generation_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in Grid 5 live cases: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/dashboard/populate-with-grid5")
async def populate_dashboard_with_grid5(request: DashboardRequest):
    """Enhanced dashboard population including LIVE Grid 5"""
    try:
        start_time = time.time()
        
        if not LIVE_MODE:
            raise HTTPException(
                status_code=503, 
                detail="Live mode not available. Check configuration and imports."
            )
        
        logger.info(f"🚀 Starting enhanced dashboard population for case: {request.case_id}")
        
        # Run enhanced dashboard with LIVE Grid 5
        agent_responses = await agent_manager.populate_dashboard_with_grid5(
            request.case_id, 
            request.case_context,
            request.additional_context or ""
        )
        
        parsed_responses = ResponseParser.parse_all_responses_with_grid5(
            agent_responses,
            request.case_id,
            request.case_context
        )
        
        generation_time = time.time() - start_time
        
        return {
            "message": "Enhanced dashboard populated successfully with all 5 grids using LIVE data!",
            "status": "success",
            "generation_time": generation_time,
            "case_id": request.case_id,
            "grids_included": ["Grid 1", "Grid 2", "Grid 3", "Grid 4", "Grid 5"],
            "grid_5_status": "✅ Live Cases Analytics Active - REAL INDIAN KANOON DATA",
            "live_mode": True
        }
        
    except Exception as e:
        logger.error(f"❌ Error in enhanced dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/status")
async def system_status():
    """Comprehensive system status"""
    return {
        "system": "Legal Dashboard Grid 5 - LIVE MODE",
        "version": "2.0.0-LIVE",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "live_mode": LIVE_MODE,
        "environment": {
            "openai_api": "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing",
            "indian_kanoon_api": "✅ Configured" if os.getenv("INDIAN_KANOON_API_TOKEN") else "❌ Missing",
            "grid_5_enabled": LIVE_MODE and bool(os.getenv("INDIAN_KANOON_API_TOKEN"))
        },
        "components": {
            "indian_kanoon_client": "✅ Ready" if LIVE_MODE else "❌ Not Available",
            "query_builder": "✅ Ready" if LIVE_MODE else "❌ Not Available",
            "agent_manager": "✅ Ready" if LIVE_MODE else "❌ Not Available",
            "grids_available": ["Grid 1", "Grid 2", "Grid 3", "Grid 4"] + (["Grid 5 - LIVE"] if LIVE_MODE else [])
        },
        "api_endpoints": {
            "/grid/live-cases": "🟢 LIVE Indian Kanoon API" if LIVE_MODE else "🔴 Not Available",
            "/dashboard/populate-with-grid5": "🟢 LIVE Enhanced Dashboard" if LIVE_MODE else "🔴 Not Available"
        }
    }

@app.get("/test/indian-kanoon")
async def test_indian_kanoon():
    """Test Indian Kanoon API connection"""
    if not os.getenv("INDIAN_KANOON_API_TOKEN"):
        raise HTTPException(status_code=503, detail="Indian Kanoon API token not configured")
    
    if not LIVE_MODE:
        raise HTTPException(status_code=503, detail="Live mode components not available")
    
    try:
        # Test simple search
        test_results = await indian_kanoon_client.search_cases(
            query="medical negligence",
            max_results=3
        )
        
        return {
            "message": "✅ Indian Kanoon API connection successful",
            "test_query": "medical negligence",
            "results_found": len(test_results),
            "sample_results": test_results[:2] if test_results else [],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indian Kanoon API test failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Legal Dashboard Grid 5 API Server - LIVE MODE...")
    print("🏛️ Features: REAL Indian Kanoon API integration")
    print("🔗 Access: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    
    if not os.getenv("INDIAN_KANOON_API_TOKEN"):
        print("⚠️  WARNING: INDIAN_KANOON_API_TOKEN not set - Live mode will not work")
    
    uvicorn.run(
        "real_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
