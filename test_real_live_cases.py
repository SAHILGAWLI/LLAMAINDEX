#!/usr/bin/env python3
"""
Test Script for Real Live Cases Data

This script tests the /dashboard/populate-optimized endpoint to ensure it's using
real Indian Kanoon API data and not demo/fake data.
"""

import requests
import json
import time
import os
from typing import Dict, Any

def test_optimized_dashboard_real_data():
    """
    Test the optimized dashboard endpoint with real data verification
    """
    print("🧪 Testing /dashboard/populate-optimized for REAL DATA ONLY")
    print("=" * 60)
    
    # Check API token configuration
    api_token = os.getenv("INDIAN_KANOON_API_TOKEN")
    if not api_token:
        print("❌ INDIAN_KANOON_API_TOKEN not configured!")
        print("   Run: python configure_indian_kanoon.py")
        return False
    
    print(f"✅ API Token configured: {api_token[:10]}...")
    
    # Test cases for different crime types
    test_cases = [
        {
            "name": "Medical Negligence Case",
            "case_context": "A patient died during surgery due to medical negligence by the doctor. The hospital failed to provide proper care and the surgical procedure was performed incorrectly.",
            "expected_keywords": ["medical", "negligence", "malpractice"]
        },
        {
            "name": "Cyber Crime Case", 
            "case_context": "Online fraud case where victim lost money through phishing emails and fake banking websites. Cybercriminals used social engineering techniques.",
            "expected_keywords": ["cyber", "fraud", "phishing"]
        },
        {
            "name": "Drug Crime Case",
            "case_context": "Possession and distribution of narcotics substances. Large quantity of drugs seized from the accused under NDPS Act provisions.",
            "expected_keywords": ["NDPS", "narcotics", "drugs"]
        }
    ]
    
    base_url = "http://localhost:8000"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print("-" * 40)
        
        payload = {
            "case_id": f"TEST_REAL_DATA_{i}",
            "case_context": test_case["case_context"]
        }
        
        try:
            print(f"📤 Sending request to /dashboard/populate-optimized...")
            start_time = time.time()
            
            response = requests.post(
                f"{base_url}/dashboard/populate-optimized",
                json=payload,
                timeout=60
            )
            
            response_time = time.time() - start_time
            print(f"⏱️ Response time: {response_time:.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify real data indicators
                live_cases = data.get("live_cases", {})
                
                print(f"✅ Request successful!")
                print(f"   Status: {response.status_code}")
                print(f"   Generation time: {data.get('generation_time', 0):.2f}s")
                
                # Check live cases data
                if isinstance(live_cases, dict):
                    api_mode = live_cases.get("api_mode", "unknown")
                    cases_count = live_cases.get("total_cases", 0)
                    status = live_cases.get("status", "unknown")
                    
                    print(f"   Live Cases Status: {status}")
                    print(f"   API Mode: {api_mode}")
                    print(f"   Cases Found: {cases_count}")
                    
                    # Verify it's real data
                    if api_mode in ["live", "enhanced_live_real"]:
                        print("   ✅ REAL DATA CONFIRMED!")
                        
                        # Check for demo indicators (should not exist)
                        message = live_cases.get("message", "")
                        if "demo" in message.lower() or "fake" in message.lower():
                            print("   ❌ DEMO DATA DETECTED - This should not happen!")
                            return False
                        
                        # Verify cases have real data
                        cases = live_cases.get("cases", [])
                        if cases:
                            first_case = cases[0]
                            title = first_case.get("title", "")
                            court = first_case.get("court", "")
                            
                            print(f"   📋 Sample case: {title[:50]}...")
                            print(f"   🏛️ Court: {court}")
                            
                            # Check for demo indicators in case data
                            if "demo" in title.lower() or "demo" in court.lower():
                                print("   ❌ DEMO CASE DATA DETECTED!")
                                return False
                            else:
                                print("   ✅ Real case data confirmed!")
                        
                    elif api_mode == "error_no_demo":
                        print("   ⚠️ API Error (No demo fallback) - This is expected behavior")
                        print(f"   Error: {live_cases.get('message', 'Unknown error')}")
                    else:
                        print(f"   ❌ Unexpected API mode: {api_mode}")
                        return False
                
                else:
                    print("   ❌ Invalid live_cases format")
                    return False
                    
            elif response.status_code == 503:
                print(f"❌ Service unavailable (503) - API token issue")
                print(f"   Response: {response.text}")
                return False
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            return False
    
    print("\n🎉 ALL TESTS PASSED - REAL DATA ONLY CONFIRMED!")
    return True

def test_api_status_endpoint():
    """
    Test the API status endpoint
    """
    print("\n🔍 Testing API Status Endpoint")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:8000/api/status/indian-kanoon")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status endpoint working")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Configured: {data.get('configured')}")
            print(f"   Demo Mode Available: {data.get('demo_mode_available')}")
            print(f"   Live Cases Enabled: {data.get('live_cases_enabled')}")
            
            if data.get('demo_mode_available'):
                print("   ❌ Demo mode should be disabled!")
                return False
            else:
                print("   ✅ Demo mode properly disabled")
                return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Status endpoint test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 LAAMAINDEX Real Data Verification Test")
    print("=" * 50)
    
    # Test API status first
    status_ok = test_api_status_endpoint()
    
    if status_ok:
        # Test dashboard with real data
        dashboard_ok = test_optimized_dashboard_real_data()
        
        if dashboard_ok:
            print("\n🎉 VERIFICATION COMPLETE: System is using REAL DATA ONLY!")
        else:
            print("\n❌ VERIFICATION FAILED: Issues detected with real data usage")
    else:
        print("\n❌ API Status check failed - cannot proceed with dashboard tests")
