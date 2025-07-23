#!/usr/bin/env python3
"""
Test script to verify live cases endpoint fix
"""

import json
import requests
import time

def test_live_cases_endpoint():
    """Test the live cases endpoint with correct request format"""
    
    # Test data matching DashboardRequest model
    test_request = {
        "case_id": "TEST_001",
        "case_context": "Medical negligence case involving surgical complications",
        "user_role": "analyst",
        "jurisdiction": "Maharashtra"
    }
    
    url = "http://localhost:8000/grid/live-cases"
    
    try:
        print("🧪 Testing live cases endpoint...")
        print(f"📤 Request: {json.dumps(test_request, indent=2)}")
        
        response = requests.post(url, json=test_request, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Live cases endpoint working correctly")
            print(f"📈 API Mode: {result.get('api_mode', 'unknown')}")
            print(f"📋 Cases Found: {result.get('total_cases', 0)}")
            print(f"⏱️ Generation Time: {result.get('generation_time', 0):.2f}s")
            print(f"💬 Message: {result.get('message', 'No message')}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"📝 Error Details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"📝 Raw Response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_live_cases_endpoint()
