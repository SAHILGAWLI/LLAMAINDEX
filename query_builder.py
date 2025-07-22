# ---------------------------------------------
# Smart Query Builder for Indian Kanoon API
# Constructs intelligent search queries from legal context
# ---------------------------------------------

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class QueryContext:
    """Context information for query construction"""
    bns_sections: List[str]
    case_context: str
    legal_keywords: List[str]
    fact_patterns: List[str]
    case_type: Optional[str] = None

class SmartQueryBuilder:
    """
    Intelligent query builder that converts legal context into
    optimized Indian Kanoon search queries
    """
    
    def __init__(self):
        # BNS section mappings to search terms
        self.bns_mappings = {
            '304A': ['negligence', 'medical negligence', 'death by negligence'],
            '302': ['murder', 'culpable homicide', 'intentional killing'],
            '338': ['endangering life', 'rash act', 'negligent act'],
            '323': ['voluntarily causing hurt', 'simple hurt', 'assault'],
            '325': ['grievous hurt', 'voluntarily causing grievous hurt'],
            '420': ['cheating', 'fraud', 'dishonestly inducing'],
            '376': ['rape', 'sexual assault', 'sexual offence'],
            '279': ['rash driving', 'negligent driving', 'motor vehicle'],
            '406': ['criminal breach of trust', 'breach of trust'],
            '498A': ['cruelty', 'domestic violence', 'dowry harassment']
        }
        
        # Legal domain keywords with weights
        self.legal_keywords = {
            'high_priority': ['murder', 'rape', 'fraud', 'negligence', 'assault'],
            'medium_priority': ['theft', 'cheating', 'hurt', 'accident', 'breach'],
            'context_keywords': ['medical', 'surgical', 'hospital', 'doctor', 'patient',
                               'vehicle', 'accident', 'injury', 'death', 'evidence']
        }
        
        # Court hierarchy for filtering
        self.court_hierarchy = {
            'supreme': ['supremecourt'],
            'high': ['delhi', 'bombay', 'kolkata', 'chennai', 'allahabad', 'andhra',
                    'gujarat', 'karnataka', 'kerala', 'madhyapradesh', 'patna',
                    'punjab', 'rajasthan', 'himachal_pradesh', 'jharkhand'],
            'district': ['delhidc'],
            'tribunals': ['itat', 'cerc', 'cci', 'cat', 'consumer']
        }
    
    def extract_bns_sections(self, text: str) -> List[str]:
        """Extract BNS section numbers from text"""
        # Pattern to match BNS sections (e.g., 304A, 302, 376(2))
        pattern = r'\b(?:BNS\s*)?(\d+[A-Z]?(?:\(\d+\))?)\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        # Clean and validate sections
        sections = []
        for match in matches:
            section = match.upper().strip()
            if section in self.bns_mappings or len(section) >= 2:
                sections.append(section)
        
        return list(set(sections))
    
    def extract_legal_keywords(self, text: str) -> List[str]:
        """Extract relevant legal keywords from case context"""
        text_lower = text.lower()
        keywords = []
        
        # High priority keywords
        for keyword in self.legal_keywords['high_priority']:
            if keyword in text_lower:
                keywords.append(keyword)
        
        # Medium priority keywords
        for keyword in self.legal_keywords['medium_priority']:
            if keyword in text_lower:
                keywords.append(keyword)
        
        # Context-specific keywords
        for keyword in self.legal_keywords['context_keywords']:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return list(set(keywords))[:8]  # Limit to top 8 keywords
    
    def extract_fact_patterns(self, text: str) -> List[str]:
        """Extract fact patterns from case context"""
        text_lower = text.lower()
        patterns = []
        
        # Medical negligence patterns
        if any(word in text_lower for word in ['medical', 'doctor', 'hospital', 'surgical']):
            if 'negligence' in text_lower:
                patterns.append('medical negligence')
            if 'malpractice' in text_lower:
                patterns.append('medical malpractice')
            if 'surgical' in text_lower:
                patterns.append('surgical negligence')
        
        # Vehicle accident patterns
        if any(word in text_lower for word in ['vehicle', 'car', 'truck', 'accident']):
            patterns.append('motor vehicle accident')
            if 'rash' in text_lower or 'negligent' in text_lower:
                patterns.append('rash driving')
        
        # Assault patterns
        if any(word in text_lower for word in ['assault', 'attack', 'violence']):
            patterns.append('physical assault')
            if 'domestic' in text_lower:
                patterns.append('domestic violence')
        
        # Fraud patterns
        if any(word in text_lower for word in ['fraud', 'cheating', 'money']):
            patterns.append('financial fraud')
        
        return patterns[:5]  # Limit to top 5 patterns
    
    def build_query_context(self, case_context: str, laws_agent_output: str = "") -> QueryContext:
        """Build comprehensive query context from inputs"""
        combined_text = f"{case_context} {laws_agent_output}"
        
        bns_sections = self.extract_bns_sections(combined_text)
        legal_keywords = self.extract_legal_keywords(combined_text)
        fact_patterns = self.extract_fact_patterns(combined_text)
        
        # Determine case type
        case_type = self.determine_case_type(legal_keywords, fact_patterns)
        
        return QueryContext(
            bns_sections=bns_sections,
            case_context=case_context,
            legal_keywords=legal_keywords,
            fact_patterns=fact_patterns,
            case_type=case_type
        )
    
    def determine_case_type(self, keywords: List[str], patterns: List[str]) -> str:
        """Determine the primary case type"""
        if any('medical' in p for p in patterns):
            return 'medical_negligence'
        elif any('vehicle' in p or 'driving' in p for p in patterns):
            return 'motor_vehicle'
        elif any('assault' in k for k in keywords):
            return 'assault'
        elif any('fraud' in k or 'cheating' in k for k in keywords):
            return 'fraud'
        elif any('murder' in k for k in keywords):
            return 'murder'
        else:
            return 'general'
    
    def construct_indian_kanoon_query(self, context: QueryContext) -> str:
        """Construct optimized Indian Kanoon search query"""
        query_parts = []
        
        # 1. BNS Sections (highest priority)
        if context.bns_sections:
            section_terms = []
            for section in context.bns_sections:
                # Add section number
                section_terms.append(f'"{section}"')
                # Add related terms from mapping
                if section in self.bns_mappings:
                    section_terms.extend([f'"{term}"' for term in self.bns_mappings[section][:2]])
            
            if section_terms:
                bns_query = " ORR ".join(section_terms[:6])  # Limit to avoid too long queries
                query_parts.append(f"({bns_query})")
        
        # 2. High-priority legal keywords
        high_priority_kw = [kw for kw in context.legal_keywords 
                           if kw in self.legal_keywords['high_priority']]
        if high_priority_kw:
            kw_query = " ORR ".join([f'"{kw}"' for kw in high_priority_kw[:3]])
            query_parts.append(f"({kw_query})")
        
        # 3. Fact patterns (for specificity)
        if context.fact_patterns:
            pattern_query = " ORR ".join([f'"{pattern}"' for pattern in context.fact_patterns[:2]])
            query_parts.append(f"({pattern_query})")
        
        # 4. Additional context keywords (lower priority)
        context_kw = [kw for kw in context.legal_keywords 
                     if kw in self.legal_keywords['context_keywords']][:2]
        if context_kw:
            context_query = " ANDD ".join([f'"{kw}"' for kw in context_kw])
            query_parts.append(context_query)
        
        # Combine with AND logic for precision
        final_query = " ANDD ".join(query_parts) if query_parts else ""
        
        # Fallback if no specific terms found
        if not final_query and context.legal_keywords:
            final_query = f'"{context.legal_keywords[0]}"'
        
        return final_query
    
    def get_court_filter(self, case_type: str, priority_level: str = "high") -> str:
        """Get appropriate court filter based on case type and priority"""
        if priority_level == "high":
            # For high-priority cases, include Supreme Court and High Courts
            courts = self.court_hierarchy['supreme'] + self.court_hierarchy['high'][:5]
        elif priority_level == "medium":
            # For medium priority, focus on High Courts
            courts = self.court_hierarchy['high'][:8]
        else:
            # For general cases, include all courts
            courts = (self.court_hierarchy['supreme'] + 
                     self.court_hierarchy['high'][:10] + 
                     self.court_hierarchy['district'])
        
        return ','.join(courts)
    
    def optimize_query_for_relevance(self, query: str, max_length: int = 200) -> str:
        """Optimize query for relevance and length constraints"""
        if len(query) <= max_length:
            return query
        
        # If query is too long, prioritize BNS sections and high-priority terms
        parts = query.split(" ANDD ")
        
        # Keep BNS sections (usually in parentheses)
        priority_parts = [part for part in parts if "(" in part and "ORR" in part]
        
        # Add other parts until we reach length limit
        remaining_parts = [part for part in parts if part not in priority_parts]
        
        optimized_query = " ANDD ".join(priority_parts)
        
        for part in remaining_parts:
            test_query = f"{optimized_query} ANDD {part}" if optimized_query else part
            if len(test_query) <= max_length:
                optimized_query = test_query
            else:
                break
        
        return optimized_query or query[:max_length]
    
    def build_comprehensive_search_strategy(self, case_context: str, 
                                          laws_agent_output: str = "") -> Dict:
        """Build comprehensive search strategy for Indian Kanoon"""
        context = self.build_query_context(case_context, laws_agent_output)
        
        # Primary query (most specific)
        primary_query = self.construct_indian_kanoon_query(context)
        primary_query = self.optimize_query_for_relevance(primary_query)
        
        # Fallback query (broader)
        fallback_context = QueryContext(
            bns_sections=context.bns_sections,
            case_context=context.case_context,
            legal_keywords=context.legal_keywords[:3],  # Fewer keywords
            fact_patterns=context.fact_patterns[:1],    # Fewer patterns
            case_type=context.case_type
        )
        fallback_query = self.construct_indian_kanoon_query(fallback_context)
        
        # Court filters
        primary_courts = self.get_court_filter(context.case_type, "high")
        fallback_courts = self.get_court_filter(context.case_type, "medium")
        
        return {
            'primary_search': {
                'query': primary_query,
                'doctypes': primary_courts,
                'max_cases': 15
            },
            'fallback_search': {
                'query': fallback_query,
                'doctypes': fallback_courts,
                'max_cases': 10
            },
            'context': context,
            'search_metadata': {
                'bns_sections_found': len(context.bns_sections),
                'keywords_extracted': len(context.legal_keywords),
                'patterns_identified': len(context.fact_patterns),
                'case_type': context.case_type,
                'query_complexity': 'high' if len(primary_query) > 100 else 'medium'
            }
        }

# Global query builder instance
_query_builder_instance = None

def get_query_builder() -> SmartQueryBuilder:
    """Get singleton query builder instance"""
    global _query_builder_instance
    if _query_builder_instance is None:
        _query_builder_instance = SmartQueryBuilder()
    return _query_builder_instance
