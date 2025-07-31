#!/usr/bin/env python3
"""
Simple test for the role-aware chat system
"""

import requests
import json

def test_basic_citizen_chat():
    """Test basic citizen chat functionality"""
    print("🧪 Testing Basic Citizen Chat")
    
    # Test 1: Simple citizen question
    payload = {
        "session_id": "simple_test_001",
        "message": "What should I do if I'm arrested?",
        "speaker_role": "citizen"
    }
    
    try:
        print("📤 Sending citizen question...")
        response = requests.post(
            "http://localhost:8000/citizen_chat",
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📄 Answer: {result['answer'][:200]}...")
            print(f"🆔 Response ID: {result.get('response_id', 'N/A')}")
            print(f"⚠️ Needs Review: {result.get('requires_officer_review', 'N/A')}")
            print(f"📊 Confidence: {result.get('confidence_score', 'N/A')}")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def test_officer_modification():
    """Test officer modification functionality"""
    print("\n🧪 Testing Officer Modification")
    
    # Test officer modification
    payload = {
        "session_id": "simple_test_001",
        "message": "Please add information about Miranda rights and the right to remain silent",
        "speaker_role": "officer",
        "officer_instruction_type": "modify"
    }
    
    try:
        print("📤 Sending officer modification...")
        response = requests.post(
            "http://localhost:8000/citizen_chat",
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📄 Modified Answer: {result['answer'][:200]}...")
            print(f"🆔 Response ID: {result.get('response_id', 'N/A')}")
            print(f"⚠️ Needs Review: {result.get('requires_officer_review', 'N/A')}")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def main():
    print("🚀 SIMPLE ROLE-AWARE CHAT TEST")
    print("=" * 50)
    
    # Test basic connectivity
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Server is responding: {response.status_code}")
    except:
        print("❌ Cannot connect to server")
        return
    
    # Test citizen chat
    citizen_result = test_basic_citizen_chat()
    
    if citizen_result:
        # Test officer modification
        officer_result = test_officer_modification()
        
        if officer_result:
            print("\n🎉 Both tests passed!")
        else:
            print("\n⚠️ Officer test failed")
    else:
        print("\n❌ Citizen test failed")

if __name__ == "__main__":
    main()
