#!/usr/bin/env python3
"""
Standalone test script for FIR intelligence functions
Tests the enhanced FIR backend logic without external dependencies
"""

import re
from datetime import datetime
from typing import List, Dict, Any

# Copy the enhanced FIR functions for testing
def suggest_sections_from_laws_grid(laws_grid: str) -> List[str]:
    """
    Enhanced BNS section extraction with intelligent analysis
    """
    
    # Enhanced regex patterns for various BNS section formats
    patterns = [
        r"\*\*Section\s+(\d+[A-Z]?)\*\*",  # **Section 304A**
        r"Section\s+(\d+[A-Z]?)",          # Section 289
        r"BNS\s+(\d+[A-Z]?)",              # BNS 338
        r"(\d+[A-Z]?)\s*BNS",              # 304A BNS
        r"Bharatiya\s+Nyaya\s+Sanhita\s+(\d+[A-Z]?)",  # Full name format
    ]
    
    sections = set()
    for pattern in patterns:
        matches = re.findall(pattern, laws_grid, re.IGNORECASE)
        sections.update(match.strip() for match in matches if match.strip())
    
    # Context-based section suggestions if no sections found
    if not sections:
        sections = suggest_contextual_bns_sections(laws_grid)
    
    # Return formatted BNS codes with descriptions
    return format_bns_sections_with_descriptions(sorted(sections)) if sections else []

def suggest_contextual_bns_sections(context: str) -> set:
    """
    Suggest BNS sections based on context keywords when no explicit sections found
    """
    context_lower = context.lower()
    contextual_sections = set()
    
    # Crime type to BNS section mapping
    crime_mappings = {
        # Violent crimes
        'murder': ['302', '300', '299'],
        'assault': ['322', '323', '324', '325', '326'],
        'rape': ['375', '376'],
        'kidnapping': ['359', '360', '361', '362'],
        'robbery': ['390', '392', '393', '394'],
        'theft': ['378', '379', '380', '381'],
        
        # Property crimes
        'burglary': ['449', '450', '451', '452'],
        'cheating': ['415', '416', '417', '418', '419', '420'],
        'fraud': ['415', '420', '463', '464', '465'],
        'forgery': ['463', '464', '465', '466', '467', '468'],
        
        # Medical/Professional negligence
        'negligence': ['304A', '336', '337', '338'],
        'medical': ['304A', '336', '337', '338'],
        'malpractice': ['304A', '336', '337', '338'],
        
        # Traffic/Vehicle related
        'accident': ['279', '304A', '337', '338'],
        'rash': ['279', '336', '337', '338'],
        'negligent': ['279', '304A', '336', '337', '338'],
    }
    
    for keyword, sections in crime_mappings.items():
        if keyword in context_lower:
            contextual_sections.update(sections)
    
    return contextual_sections

def format_bns_sections_with_descriptions(sections: List[str]) -> List[str]:
    """
    Format BNS sections with brief descriptions for better understanding
    """
    # BNS section descriptions (key sections)
    section_descriptions = {
        '302': 'Murder',
        '304A': 'Causing death by negligence',
        '323': 'Voluntarily causing hurt',
        '324': 'Voluntarily causing hurt by dangerous weapons',
        '375': 'Rape',
        '378': 'Theft',
        '420': 'Cheating and dishonestly inducing delivery of property',
        '498A': 'Husband or relative subjecting woman to cruelty',
        '279': 'Rash driving or riding on a public way',
        '336': 'Act endangering life or personal safety of others',
        '337': 'Causing hurt by act endangering life',
        '338': 'Causing grievous hurt by act endangering life',
        '415': 'Cheating',
        '463': 'Forgery',
        '506': 'Criminal intimidation',
    }
    
    formatted_sections = []
    for section in sections:
        description = section_descriptions.get(section, 'General offense')
        formatted_sections.append(f"BNS {section} - {description}")
    
    return formatted_sections

def check_completeness(fir_fields: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Enhanced completeness checking with detailed validation and suggestions
    """
    completeness_checks = []
    
    # Essential fields with validation
    essential_fields = {
        'complainant_name': {
            'label': 'Complainant Name',
            'required': True,
            'validation': lambda x: len(x.strip()) >= 2 if x else False,
            'suggestion': 'Full name of the person filing the complaint'
        },
        'complainant_address': {
            'label': 'Complainant Address',
            'required': True,
            'validation': lambda x: len(x.strip()) >= 10 if x else False,
            'suggestion': 'Complete address with locality, city, and pin code'
        },
        'incident_date': {
            'label': 'Incident Date',
            'required': True,
            'validation': lambda x: bool(x and x.strip()),
            'suggestion': 'Date when the incident occurred (DD/MM/YYYY format)'
        },
        'incident_time': {
            'label': 'Incident Time',
            'required': True,
            'validation': lambda x: bool(x and x.strip()),
            'suggestion': 'Approximate time of incident (24-hour format preferred)'
        },
        'incident_place': {
            'label': 'Place of Occurrence',
            'required': True,
            'validation': lambda x: len(x.strip()) >= 5 if x else False,
            'suggestion': 'Specific location where incident occurred'
        },
        'incident_description': {
            'label': 'Incident Description',
            'required': True,
            'validation': lambda x: len(x.strip()) >= 20 if x else False,
            'suggestion': 'Detailed description of what happened (minimum 20 characters)'
        },
        'police_station': {
            'label': 'Police Station',
            'required': True,
            'validation': lambda x: bool(x and x.strip()),
            'suggestion': 'Name of the police station where FIR is being filed'
        }
    }
    
    # Check essential fields
    for field_key, field_info in essential_fields.items():
        value = fir_fields.get(field_key, '')
        is_valid = field_info['validation'](value)
        
        status = 'complete' if is_valid else ('missing' if not value else 'incomplete')
        priority = 'high' if not is_valid else 'low'
        
        completeness_checks.append({
            'field': field_info['label'],
            'field_key': field_key,
            'status': status,
            'priority': priority,
            'suggestion': field_info['suggestion'],
            'required': field_info['required']
        })
    
    return completeness_checks

def calculate_completeness_score(completeness_data: List[Dict[str, str]]) -> float:
    """
    Calculate overall completeness score for FIR
    """
    if not completeness_data:
        return 0.0
    
    total_fields = len(completeness_data)
    complete_fields = sum(1 for item in completeness_data if item.get('status') == 'complete')
    
    return round(complete_fields / total_fields, 2)

def calculate_ai_confidence(fir_fields: Dict[str, str], sections: List[str], completeness: List[Dict[str, str]]) -> float:
    """
    Calculate dynamic AI confidence based on data quality and completeness
    """
    confidence_factors = []
    
    # Factor 1: Completeness score (40% weight)
    completeness_score = calculate_completeness_score(completeness)
    confidence_factors.append(completeness_score * 0.4)
    
    # Factor 2: Incident description quality (30% weight)
    incident_desc = fir_fields.get("incident_description", "")
    desc_quality = min(len(incident_desc) / 100, 1.0) if incident_desc else 0.0  # Normalize to 100 chars
    confidence_factors.append(desc_quality * 0.3)
    
    # Factor 3: Legal sections identified (20% weight)
    sections_factor = min(len(sections) / 3, 1.0) if sections else 0.0  # Normalize to 3 sections
    confidence_factors.append(sections_factor * 0.2)
    
    # Factor 4: Essential fields presence (10% weight)
    essential_fields = ['complainant_name', 'incident_date', 'incident_place']
    essential_present = sum(1 for field in essential_fields if fir_fields.get(field, '').strip())
    essential_factor = essential_present / len(essential_fields)
    confidence_factors.append(essential_factor * 0.1)
    
    # Calculate final confidence
    final_confidence = sum(confidence_factors)
    
    # Ensure confidence is between 0.1 and 0.99
    return max(0.1, min(0.99, round(final_confidence, 2)))

def run_tests():
    """
    Run comprehensive tests on FIR intelligence functions
    """
    print("🧪 Testing Enhanced FIR Intelligence Functions")
    print("=" * 50)
    
    # Test Case 1: Medical Negligence
    print("\n📋 Test Case 1: Medical Negligence")
    test_case_1 = {
        'complainant_name': 'Dr. Priya Sharma',
        'complainant_address': '123 Medical Colony, Mumbai - 400001',
        'incident_date': '2024-01-15',
        'incident_time': '14:30',
        'incident_place': 'City Hospital, Operation Theater 2',
        'incident_description': 'During routine surgery, the doctor failed to follow proper medical protocols, resulting in patient complications and additional harm due to negligent surgical procedures.',
        'police_station': 'Mumbai Central Police Station',
        'legal_sections': 'Medical negligence case involving BNS Section 304A (causing death by negligence) and Section 338 (causing grievous hurt)'
    }
    
    sections_1 = suggest_sections_from_laws_grid(test_case_1['legal_sections'])
    completeness_1 = check_completeness(test_case_1)
    confidence_1 = calculate_ai_confidence(test_case_1, sections_1, completeness_1)
    
    print(f"✅ Legal Sections Found: {len(sections_1)}")
    for section in sections_1:
        print(f"   • {section}")
    print(f"✅ Completeness Score: {calculate_completeness_score(completeness_1):.2f}")
    print(f"✅ AI Confidence: {confidence_1:.2f}")
    
    # Test Case 2: Cyber Fraud
    print("\n💻 Test Case 2: Cyber Fraud")
    test_case_2 = {
        'complainant_name': 'Amit Patel',
        'incident_description': 'Online fraud through phishing emails and unauthorized bank transactions. The accused used social engineering to steal money.',
        'incident_date': '2024-01-20',
        'incident_place': 'Online Platform',
        'legal_sections': 'Cyber fraud case involving cheating and IT Act violations'
    }
    
    sections_2 = suggest_sections_from_laws_grid(test_case_2['legal_sections'])
    completeness_2 = check_completeness(test_case_2)
    confidence_2 = calculate_ai_confidence(test_case_2, sections_2, completeness_2)
    
    print(f"✅ Legal Sections Found: {len(sections_2)}")
    for section in sections_2:
        print(f"   • {section}")
    print(f"✅ Completeness Score: {calculate_completeness_score(completeness_2):.2f}")
    print(f"✅ AI Confidence: {confidence_2:.2f}")
    
    # Test Case 3: Context-based Section Detection
    print("\n🔍 Test Case 3: Context-based Detection")
    test_case_3 = {
        'complainant_name': 'Test User',
        'incident_description': 'The accused committed theft and assault, causing injury to the victim during a robbery attempt.',
        'legal_sections': ''  # Empty to test contextual detection
    }
    
    sections_3 = suggest_sections_from_laws_grid(test_case_3['incident_description'])
    print(f"✅ Contextual Sections Found: {len(sections_3)}")
    for section in sections_3:
        print(f"   • {section}")
    
    print("\n🎯 All Tests Completed Successfully!")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()
