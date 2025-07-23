# ---------------------------------------------
# Data Models for Legal Platform API
# ---------------------------------------------
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import logging

# ---------------------------------------------
# Enums
# ---------------------------------------------
class SeverityLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium" 
    LOW = "Low"

class ComplianceStatus(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    NOT_STARTED = "not_started"
    FAILED = "failed"

class CaseStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    UNDER_REVIEW = "Under Review"
    PENDING = "Pending"

class DocumentType(str, Enum):
    MEDICAL_EVIDENCE = "medical_evidence"
    LEGAL_DOCUMENT = "legal_document"
    WITNESS_STATEMENT = "witness_statement"
    EXPERT_REPORT = "expert_report"
    COMPLIANCE_REPORT = "compliance_report"

# ---------------------------------------------
# Request Models
# ---------------------------------------------
class DashboardRequest(BaseModel):
    case_id: str = Field(..., description="Unique case identifier")
    case_context: str = Field(..., description="Brief description of the case context")
    user_role: Optional[str] = Field("analyst", description="User role for permission-based filtering")
    jurisdiction: Optional[str] = Field("Maharashtra", description="Legal jurisdiction")
    additional_context: Optional[str] = Field(None, description="Additional context for enhanced analysis (used by live cases)")

class GridRequest(BaseModel):
    case_id: str
    context: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None

# ---------------------------------------------
# Response Models - Grid 1: Compliance
# ---------------------------------------------
class ComplianceItem(BaseModel):
    item: str = Field(..., description="Compliance requirement description")
    status: ComplianceStatus = Field(..., description="Current compliance status")
    priority: Optional[str] = Field(None, description="Priority level")
    due_date: Optional[str] = Field(None, description="Due date if applicable")
    notes: Optional[str] = Field(None, description="Additional notes")

class ComplianceResponse(BaseModel):
    checklist_items: List[ComplianceItem]
    progress: str = Field(..., description="Progress summary (e.g., '3/5 Complete')")
    percentage: int = Field(..., description="Completion percentage")
    overall_status: str = Field(..., description="Overall compliance status")
    recommendations: Optional[List[str]] = Field(None, description="AI-generated recommendations")

# ---------------------------------------------
# Response Models - Grid 2: BNS Laws
# ---------------------------------------------
class LawSection(BaseModel):
    section: str = Field(..., description="Law section number")
    title: str = Field(..., description="Law section title")
    severity: SeverityLevel = Field(..., description="Severity classification")
    relevance_score: float = Field(..., description="AI-calculated relevance score (0-1)")
    description: Optional[str] = Field(None, description="Brief description")
    penalties: Optional[str] = Field(None, description="Associated penalties")

class LawsResponse(BaseModel):
    laws: List[LawSection]
    total_found: int = Field(..., description="Total number of relevant laws found")
    context_summary: str = Field(..., description="AI-generated context summary")
    legal_analysis: Optional[str] = Field(None, description="AI legal analysis")

# ---------------------------------------------
# Response Models - Grid 3: Documents
# ---------------------------------------------
class DocumentItem(BaseModel):
    id: str = Field(..., description="Document unique identifier")
    name: str = Field(..., description="Document name")
    type: DocumentType = Field(..., description="Document type classification")
    priority: str = Field(..., description="Priority level (high/medium/low)")
    summary: str = Field(..., description="AI-generated document summary")
    upload_date: Optional[str] = Field(None, description="Upload date")
    file_size: Optional[str] = Field(None, description="File size")
    status: Optional[str] = Field(None, description="Processing status")

class DocumentsResponse(BaseModel):
    documents: List[DocumentItem]
    total_documents: int = Field(..., description="Total number of documents")
    categories: Dict[str, int] = Field(..., description="Document count by category")
    ai_insights: Optional[str] = Field(None, description="AI-generated insights about documents")

# ---------------------------------------------
# Response Models - Grid 4: Past Cases
# ---------------------------------------------
class PastCase(BaseModel):
    case_id: str = Field(..., description="Case identifier")
    title: str = Field(..., description="Case title")
    status: CaseStatus = Field(..., description="Case status")
    outcome: Optional[str] = Field(None, description="Case outcome")
    similarity_score: float = Field(..., description="Similarity score to current case (0-1)")
    date: str = Field(..., description="Case date")
    jurisdiction: Optional[str] = Field(None, description="Case jurisdiction")
    key_facts: Optional[List[str]] = Field(None, description="Key facts from the case")

class PastCasesResponse(BaseModel):
    cases: List[PastCase]
    total_similar: int = Field(..., description="Total similar cases found")
    pattern_analysis: Optional[str] = Field(None, description="AI-generated pattern analysis")
    success_rate: Optional[float] = Field(None, description="Success rate for similar cases")

# ---------------------------------------------
# Master Dashboard Response
# ---------------------------------------------
class DashboardResponse(BaseModel):
    grid_1_compliance: ComplianceResponse
    grid_2_laws: LawsResponse
    grid_3_documents: DocumentsResponse
    grid_4_cases: PastCasesResponse
    grid_5_live_cases: Optional['LiveCasesResponse'] = Field(None, description="Live cases analytics from Indian Kanoon API")
    generation_time: float = Field(..., description="Time taken to generate response")
    ai_confidence: float = Field(..., description="Overall AI confidence score")

# ---------------------------------------------
# Streaming Models
# ---------------------------------------------
class StreamUpdate(BaseModel):
    grid_id: str = Field(..., description="Grid identifier (1-4)")
    update_type: str = Field(..., description="Type of update")
    data: Dict[str, Any] = Field(..., description="Update data")
    timestamp: str = Field(..., description="Update timestamp")
    progress: Optional[float] = Field(None, description="Progress percentage")

# ---------------------------------------------
# Response Models - Grid 5: Live Cases Analytics
# ---------------------------------------------
class LiveCaseDocument(BaseModel):
    title: str
    court: str
    date: str
    citation: str
    summary: str
    similarity_score: float
    url: str

class CitationData(BaseModel):
    cites: List[str] = Field(default_factory=list, description="Cases this case cites")
    cited_by: List[str] = Field(default_factory=list, description="Cases that cite this case")
    citation_count: int = Field(0, description="Total citation count")
    authority_score: float = Field(0.0, description="Citation authority score (0-10)")

class CaseAnalytics(BaseModel):
    conviction_rate: Optional[float] = Field(None, description="Conviction rate in similar cases")
    average_sentence: Optional[str] = Field(None, description="Average sentence for similar cases")
    legal_trends: Optional[str] = Field(None, description="Legal trends analysis")
    success_patterns: List[str] = Field(default_factory=list, description="Success patterns identified")
    risk_factors: List[str] = Field(default_factory=list, description="Risk factors identified")
    strategic_recommendations: Optional[List[str]] = Field(None, description="Strategic recommendations")
    court_performance: Optional[Dict[str, Any]] = Field(None, description="Court performance metrics")
    legal_trend_summary: Optional[str] = Field(None, description="Summary of legal trends")

class LiveCasesResponse(BaseModel):
    message: str
    status: str = "success"
    cases: List[LiveCaseDocument] = []
    total_cases: int = 0
    generation_time: float = 0.0
    api_mode: str = "demo"

# ---------------------------------------------
# Enhanced Dashboard Response with Grid 5
# ---------------------------------------------
class EnhancedDashboardResponse(BaseModel):
    grid_1_compliance: ComplianceResponse
    grid_2_laws: LawsResponse
    grid_3_documents: DocumentsResponse
    grid_4_cases: PastCasesResponse
    grid_5_live_cases: Optional[LiveCasesResponse] = None
    generation_time: float
    ai_confidence: float
    total_api_calls: Optional[int] = 0
    error_message: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

# ---------------------------------------------
# Error Models
# ---------------------------------------------
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")
