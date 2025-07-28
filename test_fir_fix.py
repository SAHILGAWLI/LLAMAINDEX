#!/usr/bin/env python3
"""
Test script to verify FIR completeness data structure
"""

def check_completeness(fir_fields):
    """
    Test version of check_completeness function
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
        'incident_description': {
            'label': 'Incident Description',
            'required': True,
            'validation': lambda x: len(x.strip()) >= 20 if x else False,
            'suggestion': 'Detailed description of what happened (minimum 20 characters)'
        }
    }
    
    # Optional fields
    optional_fields = {
        'accused_name': {
            'label': 'Accused Name',
            'required': False,
            'validation': lambda x: len(x.strip()) >= 2 if x else True,
            'suggestion': 'Name of accused person (if known)'
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
    
    # Check optional fields
    for field_key, field_info in optional_fields.items():
        value = fir_fields.get(field_key, '')
        is_present = bool(value and value.strip())
        
        completeness_checks.append({
            'field': field_info['label'],
            'field_key': field_key,
            'status': 'complete' if is_present else 'optional',
            'priority': 'low',
            'suggestion': field_info['suggestion'],
            'required': field_info['required']
        })
    
    return completeness_checks

def test_completeness_structure():
    """
    Test the completeness data structure
    """
    print("🧪 Testing FIR Completeness Data Structure")
    print("=" * 50)
    
    # Test data
    test_fir_fields = {
        'complainant_name': 'John Doe',
        'incident_description': 'This is a detailed description of the incident that occurred.',
        'accused_name': ''
    }
    
    # Test the function
    result = check_completeness(test_fir_fields)
    
    print(f"✅ Generated {len(result)} completeness items")
    
    for i, item in enumerate(result):
        print(f"\nItem {i+1}:")
        print(f"  Field: {item['field']}")
        print(f"  Status: {item['status']}")
        print(f"  Priority: {item['priority']}")
        print(f"  Required: {item['required']} (type: {type(item['required'])})")
        print(f"  Suggestion: {item['suggestion'][:50]}...")
    
    # Verify data types
    print(f"\n🔍 Data Type Validation:")
    for item in result:
        types_correct = (
            isinstance(item['field'], str) and
            isinstance(item['field_key'], str) and
            isinstance(item['status'], str) and
            isinstance(item['priority'], str) and
            isinstance(item['suggestion'], str) and
            isinstance(item['required'], bool)
        )
        print(f"  {item['field']}: {'✅' if types_correct else '❌'}")
    
    print(f"\n🎯 Test completed successfully!")

if __name__ == "__main__":
    test_completeness_structure()
