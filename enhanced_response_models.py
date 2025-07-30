# ---------------------------------------------
# Enhanced Response Models for Revolutionary System
# ---------------------------------------------
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

# ---------------------------------------------
# Enhanced Compliance Models
# ---------------------------------------------
class ComplianceStatus(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"
    NOT_STARTED = "not_started"

class ComplianceItem(BaseModel):
    item: str = Field(..., description="Compliance requirement description")
    status: ComplianceStatus = Field(..., description="Current compliance status")
    priority: str = Field(..., description="Priority level (high/medium/low)")
    suggestion: Optional[str] = Field(None, description="AI-generated suggestion")
    required: bool = Field(True, description="Whether this item is required")
    crime_specific: bool = Field(False, description="Whether this is crime-specific requirement")

class EnhancedComplianceResponse(BaseModel):
    checklist_items: List[ComplianceItem]
    progress: str = Field(..., description="Progress summary (e.g., '3/5 Complete')")
    percentage: int = Field(..., description="Completion percentage")
    overall_status: str = Field(..., description="Overall compliance status")
    recommendations: Optional[List[str]] = Field(None, description="AI-generated recommendations")
    crime_type: Optional[str] = Field(None, description="Detected crime type")
    specialized_requirements: Optional[List[str]] = Field(None, description="Crime-specific requirements")
    legal_framework: Optional[str] = Field(None, description="Applicable legal framework (BNS/BNSS/BSA)")

# ---------------------------------------------
# Enhanced Laws Models
# ---------------------------------------------
class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LawSection(BaseModel):
    section: str = Field(..., description="Section number")
    title: str = Field(..., description="Section title")
    act: str = Field("BNS", description="Act name (BNS, NDPS, POCSO, IT Act, etc.)")
    severity: SeverityLevel = Field(..., description="Severity classification")
    relevance_score: float = Field(..., description="AI-calculated relevance score (0-1)")
    description: Optional[str] = Field(None, description="Brief description")
    penalties: Optional[str] = Field(None, description="Associated penalties")
    punishment: Optional[str] = Field(None, description="Punishment details")
    application: Optional[str] = Field(None, description="How it applies to the case")

class EnhancedLawsResponse(BaseModel):
    laws: List[LawSection]
    total_found: int = Field(..., description="Total number of relevant laws found")
    context_summary: str = Field(..., description="AI-generated context summary")
    legal_analysis: Optional[str] = Field(None, description="AI legal analysis")
    crime_type: Optional[str] = Field(None, description="Detected crime type")
    primary_act: str = Field("BNS", description="Primary applicable act")
    case_complexity: str = Field("Medium", description="Case complexity assessment")
    investigation_priority: str = Field("Medium", description="Investigation priority level")

# ---------------------------------------------
# Enhanced Live Cases Models
# ---------------------------------------------
class LiveCaseDocument(BaseModel):
    title: str = Field(..., description="Case title")
    court: str = Field(..., description="Court name")
    date: Optional[str] = Field(None, description="Case date")
    citation: Optional[str] = Field(None, description="Case citation")
    summary: str = Field("", description="Case summary")
    similarity_score: float = Field(0.0, description="Similarity to current case")
    url: str = Field("", description="Indian Kanoon URL")
    crime_type: Optional[str] = Field(None, description="Crime type classification")
    confidence: float = Field(0.5, description="Classification confidence")

class EnhancedLiveCasesResponse(BaseModel):
    message: str = Field(..., description="Response message")
    status: str = Field("success", description="Response status")
    cases: List[LiveCaseDocument] = Field(default_factory=list, description="List of relevant cases")
    total_cases: int = Field(0, description="Total number of cases found")
    generation_time: float = Field(0.0, description="Time taken to generate response")
    api_mode: str = Field("enhanced_live", description="API mode used")
    crime_type: Optional[str] = Field(None, description="Detected crime type")
    search_optimization: str = Field("standard", description="Search optimization method")
    similarity_range: Optional[Dict[str, float]] = Field(None, description="Min/max similarity scores")

# ---------------------------------------------
# Enhanced FIR Intelligence Models
# ---------------------------------------------
class FIRCompleteness(BaseModel):
    field: str = Field(..., description="Field name")
    field_key: str = Field(..., description="Field key")
    status: str = Field(..., description="Completion status")
    priority: str = Field(..., description="Priority level")
    suggestion: str = Field(..., description="Completion suggestion")
    required: bool = Field(..., description="Whether field is required")

class EnhancedFIRIntelligenceResponse(BaseModel):
    fir_text: str = Field(..., description="Generated FIR text")
    grid_1_sections: List[str] = Field(default_factory=list, description="Legal sections")
    grid_2_completeness: List[FIRCompleteness] = Field(default_factory=list, description="Completeness analysis")
    grid_3_best_practices: List[str] = Field(default_factory=list, description="Best practices")
    generation_time: float = Field(0.0, description="Generation time")
    ai_confidence: float = Field(0.0, description="AI confidence score")
    crime_type: Optional[str] = Field(None, description="Detected crime type")
    specialized_sections: Optional[List[str]] = Field(None, description="Crime-specific sections")
    compliance_score: Optional[str] = Field(None, description="Overall compliance score")

# ---------------------------------------------
# Revolutionary Dashboard Response
# ---------------------------------------------
class RevolutionaryDashboardResponse(BaseModel):
    # Core grids with enhanced structure
    grid_1_compliance: EnhancedComplianceResponse = Field(..., description="Legal compliance analysis")
    grid_2_laws: EnhancedLawsResponse = Field(..., description="BNS laws and legal framework")
    grid_3_live_cases: EnhancedLiveCasesResponse = Field(..., description="Live cases analytics")
    grid_4_fir_intelligence: EnhancedFIRIntelligenceResponse = Field(..., description="FIR intelligence")
    
    # Revolutionary metadata
    generation_time: float = Field(..., description="Total generation time")
    grid_count: int = Field(4, description="Number of grids generated")
    optimization_enabled: bool = Field(True, description="Whether optimization is enabled")
    performance_improvement: str = Field("", description="Performance improvement description")
    cost_reduction: str = Field("", description="Cost reduction achieved")
    ai_confidence: float = Field(0.0, description="Overall AI confidence")
    
    # Success metrics
    success_metrics: Dict[str, bool] = Field(default_factory=dict, description="Success metrics for each component")
    
    # Revolutionary features
    prompt_system: str = Field("revolutionary_knowledge_aware", description="Prompt system used")
    knowledge_base_utilization: str = Field("comprehensive_modern_legal_framework", description="Knowledge base utilization")
    crime_type_detection: Optional[Dict[str, Any]] = Field(None, description="Crime type detection results")
    specialized_analysis: Optional[Dict[str, Any]] = Field(None, description="Specialized analysis results")

# ---------------------------------------------
# Response Parser for Revolutionary System
# ---------------------------------------------
class RevolutionaryResponseParser:
    @staticmethod
    def parse_compliance_response(raw_text: str, crime_type: str = None) -> EnhancedComplianceResponse:
        """Parse raw compliance text into structured response"""
        # Implementation would parse the raw text and extract structured data
        # This is a simplified version - full implementation would use regex and NLP
        
        items = []
        lines = raw_text.split('\n')
        completed_count = 0
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['compliance', 'requirement', 'status']):
                status = ComplianceStatus.PENDING
                if 'complete' in line.lower():
                    status = ComplianceStatus.COMPLETED
                    completed_count += 1
                
                items.append(ComplianceItem(
                    item=line.strip(),
                    status=status,
                    priority="medium",
                    required=True,
                    crime_specific=crime_type is not None
                ))
        
        if not items:  # Default items if parsing fails
            items = [
                ComplianceItem(
                    item="BNS 2023 sections applied",
                    status=ComplianceStatus.COMPLETED,
                    priority="high",
                    required=True
                ),
                ComplianceItem(
                    item="Investigation procedures initiated",
                    status=ComplianceStatus.PENDING,
                    priority="high",
                    required=True
                )
            ]
            completed_count = 1
        
        total_items = len(items)
        percentage = int((completed_count / total_items) * 100) if total_items > 0 else 0
        
        return EnhancedComplianceResponse(
            checklist_items=items,
            progress=f"{completed_count}/{total_items} Complete",
            percentage=percentage,
            overall_status="In Progress" if percentage < 100 else "Complete",
            crime_type=crime_type,
            legal_framework="BNS 2023, BNSS 2023, BSA 2023"
        )
    
    @staticmethod
    def parse_laws_response(raw_text: str, crime_type: str = None) -> EnhancedLawsResponse:
        """Parse raw laws text into structured response"""
        import re
        
        laws = []
        lines = raw_text.split('\n')
        
        for line in lines:
            # Look for section patterns
            section_match = re.search(r'section\s*(\d+[a-z]*)', line, re.IGNORECASE)
            if section_match:
                section_num = section_match.group(1)
                
                # Extract title and details
                title = line.split('-', 1)[-1].strip() if '-' in line else line.strip()
                
                # Determine severity
                severity = SeverityLevel.MEDIUM
                if any(word in line.lower() for word in ['death', 'murder', 'life']):
                    severity = SeverityLevel.HIGH
                elif any(word in line.lower() for word in ['fine', 'minor']):
                    severity = SeverityLevel.LOW
                
                # Determine act
                act = "BNS"
                if 'ndps' in line.lower():
                    act = "NDPS"
                elif 'pocso' in line.lower():
                    act = "POCSO"
                elif 'it act' in line.lower():
                    act = "IT Act"
                
                laws.append(LawSection(
                    section=section_num,
                    title=title,
                    act=act,
                    severity=severity,
                    relevance_score=0.8,
                    description=f"{act} Section {section_num}"
                ))
        
        return EnhancedLawsResponse(
            laws=laws,
            total_found=len(laws),
            context_summary=f"Found {len(laws)} relevant legal sections",
            legal_analysis=raw_text[:200] + "..." if len(raw_text) > 200 else raw_text,
            crime_type=crime_type,
            primary_act="BNS"
        )
    
    @staticmethod
    def convert_current_to_structured(current_response: Dict[str, Any]) -> RevolutionaryDashboardResponse:
        """Convert current unstructured response to structured format"""
        
        # Parse compliance
        compliance_text = current_response.get('legal_compliance', '')
        crime_type = current_response.get('crime_type')
        grid_1 = RevolutionaryResponseParser.parse_compliance_response(compliance_text, crime_type)
        
        # Parse laws
        laws_text = current_response.get('bns_laws', '')
        grid_2 = RevolutionaryResponseParser.parse_laws_response(laws_text, crime_type)
        
        # Parse live cases (already structured)
        live_cases_data = current_response.get('live_cases', {})
        grid_3 = EnhancedLiveCasesResponse(**live_cases_data) if live_cases_data else EnhancedLiveCasesResponse()
        
        # Parse FIR intelligence (already structured)
        fir_data = current_response.get('grid_4_fir_intelligence', {})
        grid_4 = EnhancedFIRIntelligenceResponse(**fir_data) if fir_data else EnhancedFIRIntelligenceResponse(fir_text="")
        
        return RevolutionaryDashboardResponse(
            grid_1_compliance=grid_1,
            grid_2_laws=grid_2,
            grid_3_live_cases=grid_3,
            grid_4_fir_intelligence=grid_4,
            generation_time=current_response.get('generation_time', 0.0),
            ai_confidence=current_response.get('ai_confidence', 0.0),
            success_metrics=current_response.get('success_metrics', {}),
            performance_improvement=current_response.get('performance_improvement', ''),
            cost_reduction=current_response.get('cost_reduction', ''),
            crime_type_detection={
                'detected_type': crime_type,
                'confidence': current_response.get('ai_confidence', 0.0)
            } if crime_type else None
        )
