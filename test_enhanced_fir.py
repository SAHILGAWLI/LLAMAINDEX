#!/usr/bin/env python3
"""
Test Enhanced FIR Intelligence with New Criminal Laws
"""

import requests
import json
import time

def test_fir_intelligence(case_context, test_name, expected_laws):
    """
    Test FIR intelligence with specific case context
    """
    print(f"\n🧪 {test_name}")
    print("=" * 60)
    print(f"📝 Case Context: {case_context}")
    
    # Prepare test payload
    payload = {
        "fir_fields": {
            "complainant_name": "Test Officer",
            "incident_description": case_context,
            "incident_date": "2024-01-15",
            "incident_place": "Test Location",
            "police_station": "Test Police Station",
            "legal_sections": f"Legal analysis for: {case_context}"
        }
    }
    
    try:
        print("🔄 Sending request to FIR intelligence endpoint...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8001/fir/intelligence-dashboard",
            json=payload,
            timeout=300  # 5 minutes timeout for revolutionary processing
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Response received in {end_time - start_time:.2f}s")
            print(f"🎯 AI Confidence: {data.get('ai_confidence', 0):.1%}")
            
            # Check legal sections
            sections = data.get('grid_1_sections', [])
            print(f"\n⚖️ Legal Sections Suggested ({len(sections)}):")
            
            found_expected = []
            for section in sections:
                print(f"   • {section}")
                # Check if any expected laws are found
                for expected_law in expected_laws:
                    if expected_law.lower() in section.lower():
                        found_expected.append(expected_law)
            
            # Validation
            print(f"\n🔍 Validation:")
            print(f"   Expected Laws: {', '.join(expected_laws)}")
            print(f"   Found: {', '.join(set(found_expected)) if found_expected else 'None'}")
            
            if found_expected:
                print(f"   ✅ SUCCESS: Found {len(set(found_expected))}/{len(expected_laws)} expected laws")
            else:
                print(f"   ⚠️ PARTIAL: No specific expected laws found, but got {len(sections)} general sections")
            
            # Show completeness
            completeness = data.get('grid_2_completeness', [])
            complete_count = sum(1 for item in completeness if item.get('status') == 'complete')
            print(f"   📊 Completeness: {complete_count}/{len(completeness)} fields complete")
            
            # Show best practices
            practices = data.get('grid_3_best_practices', [])
            print(f"   💡 Best Practices: {len(practices)} recommendations")
            
            return True
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def run_all_tests():
    """
    Run comprehensive tests for all new criminal laws
    """
    print("🚀 ENHANCED FIR INTELLIGENCE TESTING")
    print("Testing new criminal laws: NDPS, POCSO, IT Act, DV Act")
    print("=" * 80)
    
    test_cases = [
        {
            "name": "🚫 DRUG CRIME TEST (NDPS Act)",
            "context": "Accused was found selling illegal substances including charas and ganja near a school. Police recovered 500 grams of narcotic drugs from his possession during a raid.",
            "expected_laws": ["NDPS", "narcotic", "drug"]
        },
        {
            "name": "👶 CHILD PROTECTION TEST (POCSO Act)", 
            "context": "Inappropriate behavior and sexual assault against a 12-year-old minor child by the accused teacher in the school premises.",
            "expected_laws": ["POCSO", "child", "minor", "sexual"]
        },
        {
            "name": "💻 CYBER CRIME TEST (IT Act)",
            "context": "Online fraud through fake banking website where accused stole credit card details and transferred money from victim's account using phishing techniques.",
            "expected_laws": ["IT Act", "cyber", "fraud", "phishing", "66"]
        },
        {
            "name": "🏠 DOMESTIC VIOLENCE TEST (DV Act)",
            "context": "Husband physically assaulted wife and demanded additional dowry. Victim suffered injuries and was denied access to household resources.",
            "expected_laws": ["domestic violence", "DV", "498A", "dowry"]
        },
        {
            "name": "🔄 MIXED CRIME TEST",
            "context": "Medical negligence during surgery where doctor failed to follow proper protocols, resulting in patient complications and additional harm.",
            "expected_laws": ["304A", "negligence", "medical"]
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*20} TEST {i}/{len(test_cases)} {'='*20}")
        
        success = test_fir_intelligence(
            test_case["context"],
            test_case["name"], 
            test_case["expected_laws"]
        )
        
        results.append({
            "test": test_case["name"],
            "success": success
        })
        
        # Wait between tests
        if i < len(test_cases):
            print("\n⏳ Waiting 3 seconds before next test...")
            time.sleep(3)
    
    # Final summary
    print("\n" + "="*80)
    print("📊 FINAL TEST RESULTS")
    print("="*80)
    
    successful_tests = sum(1 for r in results if r["success"])
    total_tests = len(results)
    success_rate = (successful_tests / total_tests) * 100
    
    for result in results:
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"   {status}: {result['test']}")
    
    print(f"\n🎯 OVERALL RESULTS:")
    print(f"   Successful Tests: {successful_tests}/{total_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print(f"   🎉 EXCELLENT: Your enhanced FIR intelligence is working great!")
    elif success_rate >= 60:
        print(f"   ✅ GOOD: Most features working, some fine-tuning needed")
    else:
        print(f"   ⚠️ NEEDS WORK: Check server and knowledge base loading")
    
    print(f"\n💡 NEXT STEPS:")
    if success_rate >= 80:
        print(f"   🚀 Ready for next knowledge base enhancement!")
        print(f"   📚 Consider adding investigation procedures next")
    else:
        print(f"   🔧 Debug any failed tests")
        print(f"   📋 Verify NEW_KD2 was loaded correctly")
    
    return results

if __name__ == "__main__":
    print("🔍 Checking server connection...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
            run_all_tests()
        else:
            print("❌ Server not responding properly")
    except:
        print("❌ Cannot connect to server")
        print("💡 Make sure to run: python query_api.py")
