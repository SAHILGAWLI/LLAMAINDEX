#!/usr/bin/env python3
"""
Live API Server for Grid 5 Legal Dashboard
Uses REAL Indian Kanoon API when token is provided
"""

import os
import asyncio
import logging
import time
import requests
import urllib.parse
import http.client
import json
import re
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

# Models
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
    api_mode: str = "demo"

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
        logger.info(f"🔍 Searching Indian Kanoon API with query: {query}")
        
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
                logger.info(f"✅ Indian Kanoon API returned data: {str(data)[:500]}...")
                logger.info(f"🔍 Data type: {type(data)}, Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                # Indian Kanoon JSON has 'docs' key with list of case dicts
                if isinstance(data, dict):
                    return data.get('docs', [])
                return []
            except json.JSONDecodeError:
                logger.error(f"❌ Invalid JSON response: {results[:200]}...")
                return []
        else:
            logger.error(f"❌ Indian Kanoon API error: {response.status} - {results}")
            raise HTTPException(status_code=response.status, detail=f"Indian Kanoon API error: {results}")
            
    except Exception as e:
        logger.error(f"❌ Network error calling Indian Kanoon API: {e}")
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
        logger.error(f"Error calculating similarity: {e}")
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

@app.get("/")
async def root():
    """Root endpoint with system status"""
    api_mode = get_api_mode()
    return {
        "message": f"🏛️ Legal Dashboard Grid 5 API - {api_mode.upper()} MODE!",
        "version": "2.0.0-LIVE",
        "status": "active",
        "api_mode": api_mode,
        "features": [
            "Grid 1: Compliance Analysis",
            "Grid 2: Legal Research", 
            "Grid 3: Document Analysis",
            "Grid 4: Case Precedents",
            f"Grid 5: Live Cases Analytics - {'REAL INDIAN KANOON API' if api_mode == 'live' else 'DEMO MODE'}"
        ],
        "timestamp": datetime.now().isoformat(),
        "note": "Add INDIAN_KANOON_API_TOKEN environment variable for live mode"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    api_mode = get_api_mode()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_mode": api_mode,
        "components": {
            "indian_kanoon_api": "✅ Ready" if api_mode == "live" else "❌ Token Missing - Demo Mode",
            "openai_api": "✅ Ready" if os.getenv("OPENAI_API_KEY") else "❌ Token Missing",
            "server": "✅ Running"
        }
    }

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
                # Build search query
                search_query = f"{request.case_context} {request.additional_context or ''}".strip()
                
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

@app.get("/system/status")
async def system_status():
    """Comprehensive system status"""
    api_mode = get_api_mode()
    
    return {
        "system": f"Legal Dashboard Grid 5 - {api_mode.upper()} MODE",
        "version": "2.0.0-LIVE",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "api_mode": api_mode,
        "environment": {
            "openai_api": "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing",
            "indian_kanoon_api": "✅ Configured" if os.getenv("INDIAN_KANOON_API_TOKEN") else "❌ Missing",
            "grid_5_enabled": True,
            "live_mode": api_mode == "live"
        },
        "api_endpoints": {
            "/grid/live-cases": f"🟢 {api_mode.upper()} MODE",
            "/system/status": "🟢 Available"
        }
    }

@app.get("/test/indian-kanoon")
async def test_indian_kanoon():
    """Test Indian Kanoon API connection"""
    api_mode = get_api_mode()
    
    if api_mode == "demo":
        raise HTTPException(status_code=503, detail="Indian Kanoon API token not configured")
    
    try:
        # Test simple search
        test_results = await search_indian_kanoon_api("medical negligence", max_results=3)
        
        return {
            "message": "✅ Indian Kanoon API connection successful",
            "test_query": "medical negligence",
            "results_found": len(test_results),
            "sample_results": test_results[:2] if test_results else [],
            "timestamp": datetime.now().isoformat(),
            "api_mode": "live"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indian Kanoon API test failed: {str(e)}")

if __name__ == "__main__":
    api_mode = get_api_mode()
    print(f"🚀 Starting Legal Dashboard Grid 5 API Server - {api_mode.upper()} MODE...")
    print("🏛️ Features: Indian Kanoon API integration")
    print("🔗 Access: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    
    if api_mode == "demo":
        print("⚠️  DEMO MODE: Add INDIAN_KANOON_API_TOKEN environment variable for live data")
    else:
        print("✅ LIVE MODE: Using real Indian Kanoon API")
    
    uvicorn.run(
        "live_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
