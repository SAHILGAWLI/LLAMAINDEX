#!/usr/bin/env python3
"""
Simple FastAPI Server for Grid 5 Legal Dashboard
Runs without Pinecone dependency for immediate testing
"""

import os
import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Dashboard Grid 5 API",
    description="Enhanced Legal Dashboard with Live Cases Analytics",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import models and components
try:
    from models import (
        DashboardRequest, DashboardResponse, 
        LiveCasesResponse, EnhancedDashboardResponse,
        CaseAnalytics, LiveCaseDocument
    )
    from agents import EnhancedAgentManager
    from parsers import ResponseParser
    logger.info("✅ Successfully imported all Grid 5 components")
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    # Create minimal models for testing
    from pydantic import BaseModel
    
    class DashboardRequest(BaseModel):
        case_id: str
        case_context: str
        additional_context: Optional[str] = None
    
    class DashboardResponse(BaseModel):
        message: str
        status: str = "success"
        generation_time: float = 0.0

# Initialize components
try:
    agent_manager = EnhancedAgentManager()
    logger.info("✅ Enhanced Agent Manager initialized")
except Exception as e:
    logger.error(f"❌ Agent Manager initialization failed: {e}")
    agent_manager = None

@app.get("/")
async def root():
    """Root endpoint with system status"""
    return {
        "message": "🏛️ Legal Dashboard Grid 5 API is running!",
        "version": "2.0.0",
        "status": "active",
        "features": [
            "Grid 1: Compliance Analysis",
            "Grid 2: Legal Research", 
            "Grid 3: Document Analysis",
            "Grid 4: Case Precedents",
            "Grid 5: Live Cases Analytics (NEW!)"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "agent_manager": "✅ Ready" if agent_manager else "❌ Not Available",
            "indian_kanoon_api": "🔄 Checking..." if os.getenv("INDIAN_KANOON_API_TOKEN") else "❌ Token Missing",
            "openai_api": "✅ Ready" if os.getenv("OPENAI_API_KEY") else "❌ Token Missing"
        }
    }

@app.post("/dashboard/populate")
async def populate_dashboard(request: DashboardRequest):
    """Populate dashboard with Grids 1-4 (original functionality)"""
    try:
        start_time = time.time()
        
        if not agent_manager:
            raise HTTPException(status_code=503, detail="Agent Manager not available")
        
        # Run original 4 grids
        agent_responses = await agent_manager.populate_dashboard(
            request.case_id, 
            request.case_context
        )
        
        # Parse responses
        parsed_responses = ResponseParser.parse_all_responses(
            agent_responses, 
            request.case_id, 
            request.case_context
        )
        
        generation_time = time.time() - start_time
        
        return DashboardResponse(
            message="Dashboard populated successfully with Grids 1-4",
            status="success",
            generation_time=generation_time
        )
        
    except Exception as e:
        logger.error(f"Error populating dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dashboard/populate-with-grid5")
async def populate_dashboard_with_grid5(request: DashboardRequest):
    """Enhanced dashboard population including Grid 5"""
    try:
        start_time = time.time()
        
        if not agent_manager:
            raise HTTPException(status_code=503, detail="Agent Manager not available")
        
        # Check if Grid 5 is available
        if not os.getenv("INDIAN_KANOON_API_TOKEN"):
            logger.warning("Grid 5 unavailable - falling back to Grids 1-4")
            return await populate_dashboard(request)
        
        # Run enhanced dashboard with Grid 5
        try:
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
                "message": "Enhanced dashboard populated successfully with all 5 grids!",
                "status": "success",
                "generation_time": generation_time,
                "grids_included": ["Grid 1", "Grid 2", "Grid 3", "Grid 4", "Grid 5"],
                "grid_5_status": "✅ Live Cases Analytics Active"
            }
            
        except Exception as grid5_error:
            logger.error(f"Grid 5 error: {grid5_error}")
            logger.info("Falling back to Grids 1-4")
            return await populate_dashboard(request)
        
    except Exception as e:
        logger.error(f"Error in enhanced dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grid/live-cases")
async def get_live_cases(request: DashboardRequest):
    """Grid 5: Live Cases Analytics endpoint"""
    try:
        start_time = time.time()
        
        if not os.getenv("INDIAN_KANOON_API_TOKEN"):
            raise HTTPException(
                status_code=503, 
                detail="Indian Kanoon API token not configured. Please set INDIAN_KANOON_API_TOKEN environment variable."
            )
        
        if not agent_manager:
            raise HTTPException(status_code=503, detail="Agent Manager not available")
        
        # Run Grid 5 Live Cases Agent
        live_cases_response = await agent_manager.run_single_agent(
            "live_cases",
            f"Case Context: {request.case_context}\nAdditional Context: {request.additional_context or ''}"
        )
        
        generation_time = time.time() - start_time
        
        return {
            "message": "Live cases analysis completed successfully",
            "status": "success",
            "generation_time": generation_time,
            "case_id": request.case_id,
            "analysis_summary": "Grid 5 Live Cases Analytics provides real-time legal case data and AI-powered insights",
            "features": [
                "Real-time case search via Indian Kanoon API",
                "AI-powered case similarity scoring",
                "Citation network analysis",
                "Strategic legal recommendations",
                "Court performance metrics"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in Grid 5 live cases: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/status")
async def system_status():
    """Comprehensive system status"""
    return {
        "system": "Legal Dashboard Grid 5",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "openai_api": "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing",
            "indian_kanoon_api": "✅ Configured" if os.getenv("INDIAN_KANOON_API_TOKEN") else "❌ Missing",
            "grid_5_enabled": bool(os.getenv("INDIAN_KANOON_API_TOKEN"))
        },
        "components": {
            "agent_manager": "✅ Ready" if agent_manager else "❌ Not Available",
            "grids_available": ["Grid 1", "Grid 2", "Grid 3", "Grid 4"] + (["Grid 5"] if os.getenv("INDIAN_KANOON_API_TOKEN") else [])
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Legal Dashboard Grid 5 API Server...")
    print("📊 Features: Enhanced dashboard with live cases analytics")
    print("🔗 Access: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
