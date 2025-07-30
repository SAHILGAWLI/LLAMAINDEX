#!/usr/bin/env python3
"""
Monitor Stress Test Progress
"""

import time
import requests

def monitor_server_health():
    """Monitor server health during stress testing"""
    print("🔍 MONITORING SERVER HEALTH DURING STRESS TEST")
    print("=" * 60)
    
    for i in range(10):  # Monitor for 10 iterations
        try:
            start_time = time.time()
            response = requests.get("http://localhost:8001/", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                status = "🟢 HEALTHY"
            else:
                status = f"🟡 WARNING ({response.status_code})"
                
            print(f"Check {i+1}/10: {status} | Response: {response_time:.3f}s")
            
        except Exception as e:
            print(f"Check {i+1}/10: 🔴 ERROR | {e}")
        
        time.sleep(10)  # Check every 10 seconds
    
    print("\n✅ Server health monitoring complete")

def test_simple_endpoint():
    """Test a simple endpoint to verify system responsiveness"""
    print("\n🧪 TESTING SIMPLE ENDPOINT RESPONSIVENESS")
    print("=" * 60)
    
    simple_case = {
        "case_id": "MONITOR-001",
        "case_context": "Simple theft case for monitoring"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8001/dashboard/populate-optimized",
            json=simple_case,
            timeout=60
        )
        actual_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success_metrics', {}).get('overall', False)
            confidence = data.get('ai_confidence', 0)
            
            print(f"✅ Simple test successful:")
            print(f"   Time: {actual_time:.2f}s")
            print(f"   Success: {'✅' if success else '❌'}")
            print(f"   AI Confidence: {confidence:.1%}")
            
            if actual_time <= 30 and success:
                print(f"   🎉 System is responsive and working well!")
            else:
                print(f"   ⚠️ System may be under stress")
        else:
            print(f"❌ Simple test failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Simple test error: {e}")

if __name__ == "__main__":
    print("🔍 STRESS TEST MONITORING STARTED")
    print("=" * 60)
    
    # Test simple endpoint first
    test_simple_endpoint()
    
    # Monitor server health
    monitor_server_health()
    
    print("\n🎉 Monitoring complete!")
