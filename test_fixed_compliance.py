#!/usr/bin/env python3
"""
Test Fixed Compliance Analysis
"""

import requests
import json
import time

def test_fixed_compliance():
    """Test the fixed compliance analysis"""
    print("🔧 TESTING FIXED COMPLIANCE ANALYSIS")
    print("=" * 60)
    
    test_case = {
        "case_id": "FIX-TEST-001",
        "case_context": "Medical malpractice case involving negligent surgery leading to patient complications. Hospital failed to follow proper protocols."
    }
    
    print(f"📝 Test Case: {test_case['case_context']}")
    
    try:
        print("🔄 Sending request to fixed revolutionary dashboard...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8001/dashboard/populate-optimized",
            json=test_case,
            timeout=300
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Response received in {end_time - start_time:.2f}s")
            
            # Check legal compliance
            legal_compliance = data.get('legal_compliance', '')
            print(f"\n🏛️ LEGAL COMPLIANCE ANALYSIS:")
            
            if "Enhanced agent analysis failed" in legal_compliance:
                if "Max iterations" in legal_compliance:
                    print("❌ Still hitting max iterations - needs further optimization")
                else:
                    print("❌ Different error occurred")
                print(f"Error: {legal_compliance[:200]}...")
            else:
                print("✅ Legal compliance analysis successful!")
                print(f"Length: {len(legal_compliance)} characters")
                print(f"Preview: {legal_compliance[:300]}...")
            
            # Check BNS laws
            bns_laws = data.get('bns_laws', '')
            print(f"\n⚖️ BNS LAWS ANALYSIS:")
            if bns_laws and "Enhanced agent analysis failed" not in bns_laws:
                print("✅ BNS laws analysis successful!")
                print(f"Length: {len(bns_laws)} characters")
            else:
                print("❌ BNS laws analysis failed")
            
            # Check live cases
            live_cases = data.get('live_cases', {})
            print(f"\n🏛️ LIVE CASES:")
            if isinstance(live_cases, dict) and live_cases.get('status') == 'success':
                print(f"✅ Live cases successful: {live_cases.get('total_cases', 0)} cases")
            else:
                print("❌ Live cases failed")
            
            # Overall success
            success_metrics = data.get('success_metrics', {})
            overall_success = success_metrics.get('overall', False)
            legal_success = success_metrics.get('legal_analysis', False)
            
            print(f"\n📊 SUCCESS METRICS:")
            print(f"   Legal Analysis: {'✅' if legal_success else '❌'}")
            print(f"   Live Cases: {'✅' if success_metrics.get('live_cases', False) else '❌'}")
            print(f"   Overall: {'✅' if overall_success else '❌'}")
            print(f"   AI Confidence: {data.get('ai_confidence', 0):.1%}")
            
            if legal_success:
                print("\n🎉 COMPLIANCE ANALYSIS FIXED!")
                print("✅ Max iterations issue resolved")
                print("✅ Revolutionary prompts working")
                print("✅ Legal framework integration successful")
            else:
                print("\n⚠️ COMPLIANCE ANALYSIS STILL NEEDS WORK")
                print("🔧 Consider further prompt optimization")
                print("🔧 May need simpler prompt structure")
            
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🔍 Checking server connection...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Fixed server is running!")
            test_fixed_compliance()
        else:
            print("❌ Server not responding properly")
    except:
        print("❌ Cannot connect to server")
        print("💡 Make sure fixed server is running on port 8001")
