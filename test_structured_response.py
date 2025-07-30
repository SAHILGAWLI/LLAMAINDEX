#!/usr/bin/env python3
"""
Test Structured Response Format
"""

import requests
import json
import time

def test_structured_vs_unstructured():
    """Compare structured vs unstructured responses"""
    print("🏗️ TESTING STRUCTURED VS UNSTRUCTURED RESPONSES")
    print("=" * 80)
    
    test_case = {
        "case_id": "STRUCT-TEST-001",
        "case_context": "Medical malpractice case involving negligent surgery leading to patient complications. Hospital failed to follow proper protocols."
    }
    
    print(f"📝 Test Case: {test_case['case_context']}")
    
    # Test unstructured endpoint
    print(f"\n🔄 Testing UNSTRUCTURED endpoint (/dashboard/populate-optimized)...")
    try:
        start_time = time.time()
        response_unstructured = requests.post(
            "http://localhost:8001/dashboard/populate-optimized",
            json=test_case,
            timeout=120
        )
        unstructured_time = time.time() - start_time
        
        if response_unstructured.status_code == 200:
            unstructured_data = response_unstructured.json()
            print(f"✅ Unstructured response: {unstructured_time:.2f}s")
            print(f"   Response type: {type(unstructured_data)}")
            print(f"   Keys: {list(unstructured_data.keys())}")
            
            # Analyze unstructured format
            legal_compliance = unstructured_data.get('legal_compliance', '')
            print(f"   Legal Compliance: {type(legal_compliance)} ({len(str(legal_compliance))} chars)")
            
            bns_laws = unstructured_data.get('bns_laws', '')
            print(f"   BNS Laws: {type(bns_laws)} ({len(str(bns_laws))} chars)")
            
            live_cases = unstructured_data.get('live_cases', {})
            print(f"   Live Cases: {type(live_cases)} ({len(str(live_cases))} chars)")
            
            fir_intelligence = unstructured_data.get('grid_4_fir_intelligence', {})
            print(f"   FIR Intelligence: {type(fir_intelligence)} ({len(str(fir_intelligence))} chars)")
            
        else:
            print(f"❌ Unstructured failed: HTTP {response_unstructured.status_code}")
            unstructured_data = None
            
    except Exception as e:
        print(f"❌ Unstructured error: {e}")
        unstructured_data = None
    
    # Test structured endpoint
    print(f"\n🏗️ Testing STRUCTURED endpoint (/dashboard/populate-structured)...")
    try:
        start_time = time.time()
        response_structured = requests.post(
            "http://localhost:8001/dashboard/populate-structured",
            json=test_case,
            timeout=120
        )
        structured_time = time.time() - start_time
        
        if response_structured.status_code == 200:
            structured_data = response_structured.json()
            print(f"✅ Structured response: {structured_time:.2f}s")
            print(f"   Response type: {type(structured_data)}")
            print(f"   Keys: {list(structured_data.keys())}")
            
            # Analyze structured format
            grid_1 = structured_data.get('grid_1_compliance', {})
            print(f"   Grid 1 Compliance: {type(grid_1)}")
            if isinstance(grid_1, dict):
                print(f"      Progress: {grid_1.get('progress', 'N/A')}")
                print(f"      Percentage: {grid_1.get('percentage', 'N/A')}%")
                print(f"      Items: {len(grid_1.get('checklist_items', []))}")
                print(f"      Crime Type: {grid_1.get('crime_type', 'N/A')}")
            
            grid_2 = structured_data.get('grid_2_laws', {})
            print(f"   Grid 2 Laws: {type(grid_2)}")
            if isinstance(grid_2, dict):
                print(f"      Total Found: {grid_2.get('total_found', 'N/A')}")
                print(f"      Laws: {len(grid_2.get('laws', []))}")
                print(f"      Primary Act: {grid_2.get('primary_act', 'N/A')}")
                print(f"      Crime Type: {grid_2.get('crime_type', 'N/A')}")
            
            grid_3 = structured_data.get('grid_3_live_cases', {})
            print(f"   Grid 3 Live Cases: {type(grid_3)}")
            if isinstance(grid_3, dict):
                print(f"      Status: {grid_3.get('status', 'N/A')}")
                print(f"      Total Cases: {grid_3.get('total_cases', 'N/A')}")
                print(f"      Crime Type: {grid_3.get('crime_type', 'N/A')}")
            
            grid_4 = structured_data.get('grid_4_fir_intelligence', {})
            print(f"   Grid 4 FIR: {type(grid_4)}")
            if isinstance(grid_4, dict):
                print(f"      AI Confidence: {grid_4.get('ai_confidence', 'N/A')}")
                print(f"      Sections: {len(grid_4.get('grid_1_sections', []))}")
                print(f"      Completeness: {len(grid_4.get('grid_2_completeness', []))}")
                print(f"      Best Practices: {len(grid_4.get('grid_3_best_practices', []))}")
            
            # Overall metrics
            print(f"   Overall AI Confidence: {structured_data.get('ai_confidence', 'N/A')}")
            print(f"   Generation Time: {structured_data.get('generation_time', 'N/A')}s")
            print(f"   Prompt System: {structured_data.get('prompt_system', 'N/A')}")
            
        else:
            print(f"❌ Structured failed: HTTP {response_structured.status_code}")
            structured_data = None
            
    except Exception as e:
        print(f"❌ Structured error: {e}")
        structured_data = None
    
    # Comparison analysis
    print(f"\n📊 COMPARISON ANALYSIS")
    print("=" * 80)
    
    if unstructured_data and structured_data:
        print(f"✅ Both endpoints working!")
        
        # Performance comparison
        print(f"\n⏱️ PERFORMANCE:")
        print(f"   Unstructured: {unstructured_time:.2f}s")
        print(f"   Structured: {structured_time:.2f}s")
        print(f"   Difference: {abs(structured_time - unstructured_time):.2f}s")
        
        # Data structure comparison
        print(f"\n🏗️ DATA STRUCTURE:")
        print(f"   Unstructured Format:")
        print(f"      - legal_compliance: Raw text string")
        print(f"      - bns_laws: Raw text string")
        print(f"      - live_cases: Dictionary")
        print(f"      - grid_4_fir_intelligence: Dictionary")
        
        print(f"   Structured Format:")
        print(f"      - grid_1_compliance: Structured object with progress tracking")
        print(f"      - grid_2_laws: Structured object with law details")
        print(f"      - grid_3_live_cases: Enhanced live cases object")
        print(f"      - grid_4_fir_intelligence: Structured FIR object")
        
        # Frontend integration analysis
        print(f"\n💻 FRONTEND INTEGRATION:")
        print(f"   Unstructured:")
        print(f"      ❌ Requires manual text parsing")
        print(f"      ❌ No progress tracking")
        print(f"      ❌ No type safety")
        print(f"      ❌ Inconsistent format")
        
        print(f"   Structured:")
        print(f"      ✅ Ready-to-use objects")
        print(f"      ✅ Progress tracking available")
        print(f"      ✅ Type-safe responses")
        print(f"      ✅ Consistent format")
        print(f"      ✅ Rich metadata")
        
        # AI confidence comparison
        unstructured_confidence = unstructured_data.get('ai_confidence', 0)
        structured_confidence = structured_data.get('ai_confidence', 0)
        
        print(f"\n🧠 AI CONFIDENCE:")
        print(f"   Unstructured: {unstructured_confidence:.1%}")
        print(f"   Structured: {structured_confidence:.1%}")
        print(f"   Difference: {abs(structured_confidence - unstructured_confidence):.1%}")
        
        # Recommendation
        print(f"\n🎯 RECOMMENDATION:")
        if structured_time <= unstructured_time * 1.2:  # Within 20% performance
            print(f"   🏗️ USE STRUCTURED ENDPOINT!")
            print(f"   ✅ Better frontend integration")
            print(f"   ✅ Type safety and validation")
            print(f"   ✅ Progress tracking")
            print(f"   ✅ Rich metadata")
            print(f"   ✅ Comparable performance")
        else:
            print(f"   ⚠️ Consider performance trade-offs")
            print(f"   🏗️ Structured: Better integration, slower")
            print(f"   🔄 Unstructured: Faster, requires parsing")
        
    elif unstructured_data:
        print(f"⚠️ Only unstructured endpoint working")
        print(f"   Check structured endpoint implementation")
        
    elif structured_data:
        print(f"⚠️ Only structured endpoint working")
        print(f"   Check unstructured endpoint implementation")
        
    else:
        print(f"❌ Both endpoints failed")
        print(f"   Check server status and implementation")

if __name__ == "__main__":
    print("🔍 Checking server connection...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
            test_structured_vs_unstructured()
        else:
            print("❌ Server not responding properly")
    except:
        print("❌ Cannot connect to server")
        print("💡 Make sure server is running on port 8001")
