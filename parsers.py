# ---------------------------------------------
# Response Parsers for Agent Outputs
# ---------------------------------------------
import json
import re
from typing import Dict, List, Any
from datetime import datetime
from models import (
    ComplianceResponse, ComplianceItem, ComplianceStatus,
    LawsResponse, LawSection, SeverityLevel,
    DocumentsResponse, DocumentItem, DocumentType,
    PastCasesResponse, PastCase, CaseStatus
)

# ---------------------------------------------
# Base Parser Class
# ---------------------------------------------
class BaseParser:
    @staticmethod
    def extract_json_from_text(text: str) -> Dict[str, Any]:
        """Extract JSON from text response if present"""
        try:
            # Try to find JSON in the text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return {}
    
    @staticmethod
    def extract_list_items(text: str, pattern: str = r'[-•]\s*(.+)') -> List[str]:
        """Extract list items from text"""
        matches = re.findall(pattern, text, re.MULTILINE)
        return [match.strip() for match in matches if match.strip()]
    
    @staticmethod
    def extract_percentage(text: str) -> int:
        """Extract percentage from text"""
        match = re.search(r'(\d+)%', text)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def extract_score(text: str) -> float:
        """Extract score from text (0.0 to 1.0)"""
        match = re.search(r'score[:\s]*(\d*\.?\d+)', text, re.IGNORECASE)
        if match:
            score = float(match.group(1))
            return min(1.0, max(0.0, score))
        return 0.0

# ---------------------------------------------
# Compliance Response Parser
# ---------------------------------------------
class ComplianceParser(BaseParser):
    @classmethod
    def parse(cls, agent_response: str, case_id: str) -> ComplianceResponse:
        """Parse compliance agent response into structured format"""
        
        # Default compliance items if parsing fails
        default_items = [
            ComplianceItem(
                item="Patient identification verified",
                status=ComplianceStatus.COMPLETED,
                priority="high"
            ),
            ComplianceItem(
                item="Medical history documented", 
                status=ComplianceStatus.COMPLETED,
                priority="high"
            ),
            ComplianceItem(
                item="Incident report filed",
                status=ComplianceStatus.PENDING,
                priority="medium"
            ),
            ComplianceItem(
                item="Evidence chain documented",
                status=ComplianceStatus.PENDING,
                priority="high"
            ),
            ComplianceItem(
                item="Witness statements recorded",
                status=ComplianceStatus.COMPLETED,
                priority="medium"
            )
        ]
        
        try:
            # Extract compliance items from response
            items = []
            lines = agent_response.split('\n')
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['compliance', 'requirement', 'checklist', 'verify', 'document']):
                    # Determine status based on keywords
                    if any(word in line.lower() for word in ['completed', 'done', 'verified', 'yes']):
                        status = ComplianceStatus.COMPLETED
                    elif any(word in line.lower() for word in ['pending', 'incomplete', 'missing']):
                        status = ComplianceStatus.PENDING
                    elif any(word in line.lower() for word in ['failed', 'error', 'invalid']):
                        status = ComplianceStatus.FAILED
                    else:
                        status = ComplianceStatus.NOT_STARTED
                    
                    # Extract item description
                    item_text = re.sub(r'^[-•*]\s*', '', line)
                    item_text = re.sub(r'\s*(completed|pending|failed|done|yes|no)\s*', '', item_text, flags=re.IGNORECASE)
                    
                    if len(item_text) > 10:  # Valid item
                        items.append(ComplianceItem(
                            item=item_text.strip(),
                            status=status,
                            priority="medium"
                        ))
            
            # Use default items if no items found
            if not items:
                items = default_items
            
            # Calculate progress
            completed = sum(1 for item in items if item.status == ComplianceStatus.COMPLETED)
            total = len(items)
            percentage = int((completed / total) * 100) if total > 0 else 0
            
            # Extract recommendations
            recommendations = cls.extract_list_items(agent_response, r'recommend[^:]*:?\s*(.+)')
            
            return ComplianceResponse(
                checklist_items=items,
                progress=f"{completed}/{total} Complete",
                percentage=percentage,
                overall_status="In Progress" if percentage < 100 else "Complete",
                recommendations=recommendations if recommendations else None
            )
            
        except Exception as e:
            # Fallback to default response
            return ComplianceResponse(
                checklist_items=default_items,
                progress="3/5 Complete",
                percentage=60,
                overall_status="In Progress",
                recommendations=["Review pending compliance items", "Complete missing documentation"]
            )

# ---------------------------------------------
# Legal Laws Response Parser
# ---------------------------------------------
class LegalParser(BaseParser):
    @classmethod
    def parse(cls, agent_response: str, case_context: str) -> LawsResponse:
        """Parse legal agent response into structured format"""
        
        try:
            laws = []
            lines = agent_response.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Look for section numbers
                section_match = re.search(r'section\s*(\d+)', line, re.IGNORECASE)
                if section_match:
                    section_num = section_match.group(1)
                    
                    # Extract title
                    title = line
                    if ':' in line:
                        title = line.split(':', 1)[1].strip()
                    
                    # Determine severity based on keywords
                    severity = SeverityLevel.MEDIUM
                    if any(word in line.lower() for word in ['murder', 'death', 'life', 'serious']):
                        severity = SeverityLevel.HIGH
                    elif any(word in line.lower() for word in ['theft', 'minor', 'fine']):
                        severity = SeverityLevel.LOW
                    
                    # Calculate relevance score
                    relevance = cls.extract_score(line)
                    if relevance == 0.0:
                        relevance = 0.8 if severity == SeverityLevel.HIGH else 0.6
                    
                    laws.append(LawSection(
                        section=section_num,
                        title=title,
                        severity=severity,
                        relevance_score=relevance,
                        description=f"BNS Section {section_num}"
                    ))
            
            # Default laws if none found
            if not laws:
                laws = [
                    LawSection(
                        section="302",
                        title="Punishment for murder",
                        severity=SeverityLevel.HIGH,
                        relevance_score=0.95,
                        description="Whoever commits murder shall be punished with death, or imprisonment for life"
                    ),
                    LawSection(
                        section="379",
                        title="Punishment for theft", 
                        severity=SeverityLevel.MEDIUM,
                        relevance_score=0.78,
                        description="Whoever commits theft shall be punished with imprisonment"
                    )
                ]
            
            return LawsResponse(
                laws=laws,
                total_found=len(laws),
                context_summary=f"Found {len(laws)} relevant law sections for: {case_context}",
                legal_analysis=agent_response[:200] + "..." if len(agent_response) > 200 else agent_response
            )
            
        except Exception as e:
            # Fallback response
            return LawsResponse(
                laws=[],
                total_found=0,
                context_summary="Error parsing legal response",
                legal_analysis=str(e)
            )

# ---------------------------------------------
# Document Response Parser  
# ---------------------------------------------
class DocumentParser(BaseParser):
    @classmethod
    def parse(cls, agent_response: str, case_id: str) -> DocumentsResponse:
        """Parse document agent response into structured format"""
        
        try:
            documents = []
            
            # Extract document information from response
            doc_patterns = [
                r'document[^:]*:\s*(.+)',
                r'file[^:]*:\s*(.+)',
                r'report[^:]*:\s*(.+)'
            ]
            
            for pattern in doc_patterns:
                matches = re.findall(pattern, agent_response, re.IGNORECASE)
                for i, match in enumerate(matches):
                    doc_name = match.strip()
                    if len(doc_name) > 5:
                        documents.append(DocumentItem(
                            id=f"doc_{case_id}_{i+1:03d}",
                            name=doc_name,
                            type=DocumentType.LEGAL_DOCUMENT,
                            priority="medium",
                            summary=f"Document related to case {case_id}",
                            upload_date=datetime.now().strftime("%Y-%m-%d"),
                            status="processed"
                        ))
            
            # Default documents if none found
            if not documents:
                documents = [
                    DocumentItem(
                        id=f"doc_{case_id}_001",
                        name="Medical Report - Primary Evidence",
                        type=DocumentType.MEDICAL_EVIDENCE,
                        priority="high",
                        summary="Primary medical evidence for the case",
                        upload_date=datetime.now().strftime("%Y-%m-%d"),
                        status="processed"
                    ),
                    DocumentItem(
                        id=f"doc_{case_id}_002", 
                        name="Witness Statement - Key Testimony",
                        type=DocumentType.WITNESS_STATEMENT,
                        priority="medium",
                        summary="Key witness testimony relevant to case facts",
                        upload_date=datetime.now().strftime("%Y-%m-%d"),
                        status="processed"
                    )
                ]
            
            # Calculate categories
            categories = {}
            for doc in documents:
                doc_type = doc.type.value
                categories[doc_type] = categories.get(doc_type, 0) + 1
            
            return DocumentsResponse(
                documents=documents,
                total_documents=len(documents),
                categories=categories,
                ai_insights=f"Analyzed {len(documents)} documents for case {case_id}"
            )
            
        except Exception as e:
            return DocumentsResponse(
                documents=[],
                total_documents=0,
                categories={},
                ai_insights=f"Error parsing documents: {str(e)}"
            )

# ---------------------------------------------
# Past Cases Response Parser
# ---------------------------------------------
class CaseParser(BaseParser):
    @classmethod
    def parse(cls, agent_response: str, case_context: str) -> PastCasesResponse:
        """Parse case analysis agent response into structured format"""
        
        try:
            cases = []
            
            # Extract case information
            case_patterns = [
                r'case[^:]*:\s*(.+)',
                r'precedent[^:]*:\s*(.+)',
                r'similar[^:]*:\s*(.+)'
            ]
            
            for pattern in case_patterns:
                matches = re.findall(pattern, agent_response, re.IGNORECASE)
                for i, match in enumerate(matches):
                    case_title = match.strip()
                    if len(case_title) > 10:
                        similarity = cls.extract_score(match)
                        if similarity == 0.0:
                            similarity = 0.85 - (i * 0.1)  # Decreasing similarity
                        
                        cases.append(PastCase(
                            case_id=f"CASE-2023-{i+1:03d}",
                            title=case_title,
                            status=CaseStatus.CLOSED,
                            outcome="Resolved",
                            similarity_score=similarity,
                            date=f"2023-{(i % 12) + 1:02d}-15",
                            jurisdiction="Maharashtra"
                        ))
            
            # Default cases if none found
            if not cases:
                cases = [
                    PastCase(
                        case_id="CASE-2023-001",
                        title="Residential Burglary - Maple Street",
                        status=CaseStatus.CLOSED,
                        outcome="Conviction",
                        similarity_score=0.89,
                        date="2023-11-15",
                        jurisdiction="Maharashtra"
                    ),
                    PastCase(
                        case_id="CASE-2023-002",
                        title="Medical Malpractice - City Hospital", 
                        status=CaseStatus.CLOSED,
                        outcome="Settlement",
                        similarity_score=0.76,
                        date="2023-09-22",
                        jurisdiction="Maharashtra"
                    )
                ]
            
            # Calculate success rate
            successful_cases = sum(1 for case in cases if case.outcome in ["Conviction", "Settlement", "Favorable"])
            success_rate = (successful_cases / len(cases)) * 100 if cases else 0
            
            return PastCasesResponse(
                cases=cases,
                total_similar=len(cases),
                pattern_analysis=f"Found {len(cases)} similar cases with {success_rate:.1f}% success rate",
                success_rate=success_rate / 100
            )
            
        except Exception as e:
            return PastCasesResponse(
                cases=[],
                total_similar=0,
                pattern_analysis=f"Error analyzing cases: {str(e)}",
                success_rate=0.0
            )

# ---------------------------------------------
# Master Response Parser
# ---------------------------------------------
class ResponseParser:
    @staticmethod
    def parse_all_responses(agent_responses: Dict[str, str], case_id: str, case_context: str) -> Dict[str, Any]:
        """Parse all agent responses into structured format"""
        
        return {
            "compliance": ComplianceParser.parse(
                agent_responses.get("compliance", ""), case_id
            ),
            "legal": LegalParser.parse(
                agent_responses.get("legal", ""), case_context
            ),
            "documents": DocumentParser.parse(
                agent_responses.get("documents", ""), case_id
            ),
            "cases": CaseParser.parse(
                agent_responses.get("cases", ""), case_context
            )
        }
