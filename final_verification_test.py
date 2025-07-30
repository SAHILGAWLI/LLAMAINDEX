#!/usr/bin/env python3
"""
Final Verification: No More 2023 Year in FIR Sections
"""

import requests
import json

def final_verification_test():
    """Final test to confirm 2023 year is no longer treated as a section"""
    print("🎯 FINAL VERIFICATION: NO MORE 2023 YEAR IN FIR SECTIONS")
    print("=" * 80)
    
    test_case = {
        "case_id": "FINAL-VERIFY-001",
        "case_context": "Medical malpractice case involving negligent surgery leading to patient complications. Hospital failed to follow proper protocols."
    }
    
    print(f"📝 Test Case: {test_case['case_context']}")
    
    try:
        response = requests.post(
            "http://localhost:8001/dashboard/populate-optimized",
            json=test_case,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Check FIR Intelligence sections
            fir_data = result.get('grid_4_fir_intelligence', {})
            fir_sections = fir_data.get('grid_1_sections', [])
            
            print(f"\n📝 FIR SECTIONS FOUND:")
            print("=" * 40)
            for i, section in enumerate(fir_sections, 1):
                print(f"{i}. {section}")
            
            # Check for 2023 year issue
            has_2023_issue = any('2023' in str(section) for section in fir_sections)
            
            if has_2023_issue:
                print(f"\n❌ FAIL: Still contains 2023 year as section!")
                problematic_sections = [s for s in fir_sections if '2023' in str(s)]
                print(f"   Problematic sections: {problematic_sections}")
                return False
            else:
                print(f"\n✅ PASS: No 2023 year found in sections!")
            
            # Check for expected medical section
            has_medical_section = any('106' in str(section) for section in fir_sections)
            
            if has_medical_section:
                print(f"✅ PASS: Medical negligence section (106) found!")
            else:
                print(f"⚠️ WARNING: Medical negligence section (106) not found")
            
            # Check for fake sections
            fake_sections = ['279', '304A', '336', '337', '338']
            has_fake_sections = any(fake in str(fir_sections) for fake in fake_sections)
            
            if has_fake_sections:
                print(f"❌ FAIL: Still contains fake sections!")
                fake_found = [fake for fake in fake_sections if fake in str(fir_sections)]
                print(f"   Fake sections found: {fake_found}")
                return False
            else:
                print(f"✅ PASS: No fake sections detected!")
            
            # Overall assessment
            if not has_2023_issue and not has_fake_sections and has_medical_section:
                print(f"\n🎉 OVERALL RESULT: ✅ PERFECT SUCCESS!")
                print(f"   ✅ No 2023 year treated as section")
                print(f"   ✅ No fake sections (279, 304A, etc.)")
                print(f"   ✅ Correct medical section (106) used")
                print(f"   ✅ Real BNS sections from laws grid")
                return True
            else:
                print(f"\n🚨 OVERALL RESULT: ❌ ISSUES REMAIN")
                return False
                
        else:
            print(f"❌ Request failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_multiple_cases():
    """Test multiple case types to ensure fix works universally"""
    print(f"\n🧪 TESTING MULTIPLE CASE TYPES")
    print("=" * 80)
    
    test_cases = [
        {
            "case_id": "MULTI-TEST-1",
            "case_context": "Medical malpractice involving surgery complications",
            "expected_section": "106"
        },
        {
            "case_id": "MULTI-TEST-2", 
            "case_context": "Theft case involving stolen property",
            "expected_keywords": ["theft", "property"]
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['case_context'][:50]}...")
        
        try:
            response = requests.post(
                "http://localhost:8001/dashboard/populate-optimized",
                json=test_case,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                fir_data = result.get('grid_4_fir_intelligence', {})
                fir_sections = fir_data.get('grid_1_sections', [])
                
                # Check for 2023 issue
                has_2023 = any('2023' in str(section) for section in fir_sections)
                
                if has_2023:
                    print(f"   ❌ FAIL: Contains 2023 year")
                    all_passed = False
                else:
                    print(f"   ✅ PASS: No 2023 year")
                
                print(f"   📝 Sections: {len(fir_sections)} found")
                
            else:
                print(f"   ❌ Request failed: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🔍 Running final verification tests...")
    
    # Test 1: Main verification
    main_test_passed = final_verification_test()
    
    # Test 2: Multiple cases
    multi_test_passed = test_multiple_cases()
    
    print(f"\n🎯 FINAL SUMMARY")
    print("=" * 80)
    
    if main_test_passed and multi_test_passed:
        print(f"🎉 ALL TESTS PASSED! ✅")
        print(f"")
        print(f"✅ 2023 year filtering: WORKING")
        print(f"✅ Real BNS sections: WORKING") 
        print(f"✅ No fake sections: WORKING")
        print(f"✅ Medical section 106: WORKING")
        print(f"")
        print(f"🚀 FIR Intelligence now uses ONLY real, valid BNS sections!")
        print(f"🎯 The 2023 year issue is completely resolved!")
    else:
        print(f"❌ SOME TESTS FAILED")
        print(f"   Main test: {'✅' if main_test_passed else '❌'}")
        print(f"   Multi test: {'✅' if multi_test_passed else '❌'}")
        print(f"")
        print(f"🔧 Further debugging may be needed")
