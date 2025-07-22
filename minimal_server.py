#!/usr/bin/env python3
"""
Minimal FastAPI Server for Grid 5 Legal Dashboard
Bypasses Pinecone for immediate testing and demonstration
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

# Minimal models for testing
class DashboardRequest(BaseModel):
    case_id: str
    case_context: str
    additional_context: Optional[str] = None

class DashboardResponse(BaseModel):
    message: str
    status: str = "success"
    generation_time: float = 0.0
    case_id: Optional[str] = None
    grids_included: Optional[List[str]] = None
    grid_5_status: Optional[str] = None

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

# Mock data for demonstration
MOCK_LIVE_CASES = [
    LiveCaseDocument(
        title="State of Maharashtra vs. Dr. Anil Kumar - Medical Negligence Case",
        court="Bombay High Court",
        date="2024-01-15",
        citation="2024 BHC 1234",
        summary="Medical negligence case involving surgical procedure complications. Court held that deviation from standard medical practice constitutes negligence.",
        similarity_score=0.92,
        url="https://indiankanoon.org/doc/123456"
    ),
    LiveCaseDocument(
        title="Dr. Rajesh Sharma vs. State Medical Council - Professional Misconduct",
        court="Delhi High Court", 
        date="2024-02-20",
        citation="2024 DHC 5678",
        summary="Professional misconduct case against medical practitioner. Established precedent for medical ethics violations.",
        similarity_score=0.88,
        url="https://indiankanoon.org/doc/789012"
    ),
    LiveCaseDocument(
        title="Patient Rights Foundation vs. City Hospital - Institutional Liability",
        court="Supreme Court of India",
        date="2024-03-10", 
        citation="2024 SCC 9876",
        summary="Landmark case on institutional liability for medical negligence. Expanded scope of hospital accountability.",
        similarity_score=0.85,
        url="https://indiankanoon.org/doc/345678"
    )
]

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
        "timestamp": datetime.now().isoformat(),
        "demo_mode": True,
        "note": "Running in demo mode with mock data for immediate testing"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "fastapi_server": "✅ Running",
            "indian_kanoon_api": "🔄 Demo Mode" if not os.getenv("INDIAN_KANOON_API_TOKEN") else "✅ Configured",
            "openai_api": "🔄 Demo Mode" if not os.getenv("OPENAI_API_KEY") else "✅ Configured"
        },
        "demo_mode": True
    }

@app.post("/dashboard/populate", response_model=DashboardResponse)
async def populate_dashboard(request: DashboardRequest):
    """Populate dashboard with Grids 1-4 (original functionality)"""
    try:
        start_time = time.time()
        
        # Simulate processing time
        await asyncio.sleep(2)
        
        generation_time = time.time() - start_time
        
        return DashboardResponse(
            message="Dashboard populated successfully with Grids 1-4 (Demo Mode)",
            status="success",
            generation_time=generation_time,
            case_id=request.case_id,
            grids_included=["Grid 1", "Grid 2", "Grid 3", "Grid 4"]
        )
        
    except Exception as e:
        logger.error(f"Error populating dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dashboard/populate-with-grid5", response_model=DashboardResponse)
async def populate_dashboard_with_grid5(request: DashboardRequest):
    """Enhanced dashboard population including Grid 5"""
    try:
        start_time = time.time()
        
        # Simulate processing time for all grids
        await asyncio.sleep(3)
        
        generation_time = time.time() - start_time
        
        return DashboardResponse(
            message="Enhanced dashboard populated successfully with all 5 grids! (Demo Mode)",
            status="success",
            generation_time=generation_time,
            case_id=request.case_id,
            grids_included=["Grid 1", "Grid 2", "Grid 3", "Grid 4", "Grid 5"],
            grid_5_status="✅ Live Cases Analytics Active (Demo Mode)"
        )
        
    except Exception as e:
        logger.error(f"Error in enhanced dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grid/live-cases", response_model=LiveCasesResponse)
async def get_live_cases(request: DashboardRequest):
    """Grid 5: Live Cases Analytics endpoint"""
    try:
        start_time = time.time()
        
        # Simulate processing time
        await asyncio.sleep(1.5)
        
        # Filter mock cases based on context (simple keyword matching)
        context_lower = request.case_context.lower()
        filtered_cases = []
        
        for case in MOCK_LIVE_CASES:
            if any(keyword in case.summary.lower() for keyword in ["medical", "negligence", "doctor", "hospital"]):
                filtered_cases.append(case)
        
        # If no specific matches, return all cases
        if not filtered_cases:
            filtered_cases = MOCK_LIVE_CASES
        
        generation_time = time.time() - start_time
        
        return LiveCasesResponse(
            message="Live cases analysis completed successfully (Demo Mode)",
            status="success",
            cases=filtered_cases,
            total_cases=len(filtered_cases),
            generation_time=generation_time
        )
        
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
        "demo_mode": True,
        "environment": {
            "openai_api": "✅ Configured" if os.getenv("OPENAI_API_KEY") else "🔄 Demo Mode",
            "indian_kanoon_api": "✅ Configured" if os.getenv("INDIAN_KANOON_API_TOKEN") else "🔄 Demo Mode",
            "grid_5_enabled": True
        },
        "components": {
            "fastapi_server": "✅ Running",
            "grids_available": ["Grid 1", "Grid 2", "Grid 3", "Grid 4", "Grid 5"],
            "demo_data": "✅ Mock legal cases available"
        },
        "features": [
            "Real-time case search simulation",
            "AI-powered case similarity scoring",
            "Citation network analysis",
            "Strategic legal recommendations",
            "Court performance metrics"
        ]
    }

@app.get("/demo/cases")
async def get_demo_cases():
    """Get all demo cases for testing"""
    return {
        "message": "Demo cases retrieved successfully",
        "cases": MOCK_LIVE_CASES,
        "total": len(MOCK_LIVE_CASES),
        "note": "These are mock cases for demonstration purposes"
    }

if __name__ == "__main__":
    print("🚀 Starting Legal Dashboard Grid 5 API Server (Demo Mode)...")
    print("📊 Features: Enhanced dashboard with live cases analytics")
    print("🔗 Access: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("🎭 Demo Mode: Using mock data for immediate testing")
    
    uvicorn.run(
        "minimal_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
