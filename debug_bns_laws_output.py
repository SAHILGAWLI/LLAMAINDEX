#!/usr/bin/env python3
"""
Debug BNS Laws Output to understand the format
"""

import requests
import json

def debug_bns_laws_output():
    """Debug what the BNS laws grid actually outputs"""
    print("🔍 DEBUGGING BNS LAWS OUTPUT")
    print("=" * 60)
    
    test_case = {
        "case_id": "DEBUG-BNS-001",
        "case_context": "Medical malpractice case involving negligent surgery leading to patient complications. Hospital failed to follow proper protocols."
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/dashboard/populate-optimized",
            json=test_case,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("📋 BNS LAWS OUTPUT:")
            print("=" * 40)
            bns_laws = result.get('bns_laws', '')
            print(bns_laws)
            print("\n" + "=" * 40)
            
            print("\n🔍 LEGAL COMPLIANCE OUTPUT:")
            print("=" * 40)
            legal_compliance = result.get('legal_compliance', '')
            print(legal_compliance)
            print("\n" + "=" * 40)
            
            print("\n📝 FIR INTELLIGENCE SECTIONS:")
            print("=" * 40)
            fir_data = result.get('grid_4_fir_intelligence', {})
            sections = fir_data.get('grid_1_sections', [])
            print("Current FIR sections:")
            for i, section in enumerate(sections, 1):
                print(f"{i}. {section}")
            
            print("\n🧪 TESTING SECTION EXTRACTION:")
            print("=" * 40)
            
            # Test the current extraction function
            import re
            
            # Test patterns on actual BNS laws output
            patterns = [
                r"\*\*Section\s+(\d+[A-Z]?)\*\*",  # **Section 304A**
                r"Section\s+(\d+[A-Z]?)",          # Section 289
                r"BNS\s+(\d+[A-Z]?)",              # BNS 338
                r"(\d+[A-Z]?)\s*BNS",              # 304A BNS
                r"Bharatiya\s+Nyaya\s+Sanhita\s+(\d+[A-Z]?)",  # Full name format
            ]
            
            found_sections = set()
            for pattern in patterns:
                matches = re.findall(pattern, bns_laws, re.IGNORECASE)
                if matches:
                    print(f"Pattern '{pattern}' found: {matches}")
                    found_sections.update(matches)
            
            if found_sections:
                print(f"\n✅ EXTRACTED SECTIONS: {sorted(found_sections)}")
            else:
                print(f"\n❌ NO SECTIONS FOUND - This is why fake sections are used!")
                
                # Let's try to find any numbers that might be sections
                all_numbers = re.findall(r'\b(\d+[A-Z]?)\b', bns_laws)
                print(f"All numbers found: {all_numbers}")
                
                # Look for common BNS keywords
                bns_keywords = ['section', 'bns', 'bharatiya', 'nyaya', 'sanhita']
                for keyword in bns_keywords:
                    if keyword.lower() in bns_laws.lower():
                        print(f"Found keyword '{keyword}' in BNS laws output")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_bns_laws_output()
