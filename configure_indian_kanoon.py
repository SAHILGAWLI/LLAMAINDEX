#!/usr/bin/env python3
"""
Indian Kanoon API Configuration Helper

This script helps configure the Indian Kanoon API token for the LAAMAINDEX platform.
Demo mode has been completely removed to ensure real data integrity.
"""

import os
import sys
import requests
from typing import Dict, Any

def test_api_token(token: str) -> Dict[str, Any]:
    """
    Test the provided Indian Kanoon API token
    """
    try:
        test_url = "https://api.indiankanoon.org/search/?formInput=test&pagenum=0"
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
        
        print(f"🔍 Testing API token: {token[:10]}...")
        response = requests.post(test_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            docs_count = len(data.get("docs", []))
            return {
                "status": "success",
                "message": f"✅ API token is valid! Found {docs_count} test results.",
                "valid": True,
                "response_code": response.status_code
            }
        else:
            return {
                "status": "error",
                "message": f"❌ API token test failed: HTTP {response.status_code}",
                "valid": False,
                "response_code": response.status_code,
                "response_text": response.text[:200]
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ API connectivity test failed: {str(e)}",
            "valid": False,
            "error": str(e)
        }

def configure_environment():
    """
    Interactive configuration of Indian Kanoon API token
    """
    print("🚀 LAAMAINDEX - Indian Kanoon API Configuration")
    print("=" * 50)
    print()
    print("Demo mode has been completely removed from the system.")
    print("You MUST configure a valid Indian Kanoon API token to use live cases.")
    print()
    
    # Check current configuration
    current_token = os.getenv("INDIAN_KANOON_API_TOKEN")
    if current_token:
        print(f"📋 Current token found: {current_token[:10]}...")
        test_current = input("🔍 Test current token? (y/n): ").lower().strip()
        if test_current == 'y':
            result = test_api_token(current_token)
            print(f"   {result['message']}")
            if result['valid']:
                print("✅ Current configuration is working!")
                return
    else:
        print("⚠️ No INDIAN_KANOON_API_TOKEN found in environment")
    
    print()
    print("📝 To get an Indian Kanoon API token:")
    print("   1. Visit: https://api.indiankanoon.org/")
    print("   2. Register for an API account")
    print("   3. Generate your API token")
    print()
    
    # Get new token
    new_token = input("🔑 Enter your Indian Kanoon API token: ").strip()
    if not new_token:
        print("❌ No token provided. Exiting.")
        return
    
    # Test new token
    print()
    result = test_api_token(new_token)
    print(f"   {result['message']}")
    
    if result['valid']:
        # Save to environment (for current session)
        os.environ["INDIAN_KANOON_API_TOKEN"] = new_token
        
        # Provide instructions for permanent configuration
        print()
        print("✅ Token validated successfully!")
        print()
        print("📋 To make this permanent, add to your environment:")
        print(f"   export INDIAN_KANOON_API_TOKEN='{new_token}'")
        print()
        print("🐳 For Docker deployment, add to your docker-compose.yml:")
        print("   environment:")
        print(f"     - INDIAN_KANOON_API_TOKEN={new_token}")
        print()
        print("🚀 You can now use the /dashboard/populate-optimized endpoint with real data!")
    else:
        print("❌ Token validation failed. Please check your token and try again.")

def check_system_status():
    """
    Check the current system status
    """
    print("🔍 LAAMAINDEX System Status Check")
    print("=" * 40)
    
    # Check API token
    token = os.getenv("INDIAN_KANOON_API_TOKEN")
    if token:
        print(f"✅ API Token: Configured ({token[:10]}...)")
        result = test_api_token(token)
        if result['valid']:
            print("✅ API Connectivity: Working")
        else:
            print(f"❌ API Connectivity: Failed - {result['message']}")
    else:
        print("❌ API Token: Not configured")
        print("❌ API Connectivity: Cannot test without token")
    
    # Check demo mode status
    print("✅ Demo Mode: Completely disabled (Real data only)")
    print("✅ Live Cases: Enabled (requires valid API token)")
    
    print()
    if token and test_api_token(token)['valid']:
        print("🚀 System Status: READY FOR PRODUCTION")
    else:
        print("⚠️ System Status: CONFIGURATION REQUIRED")
        print("   Run: python configure_indian_kanoon.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        check_system_status()
    else:
        configure_environment()
