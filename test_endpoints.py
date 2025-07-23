#!/usr/bin/env python3
"""
🧪 API Endpoint Testing Script
Test both old (hierarchical) and new (optimized) dashboard endpoints
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
OLD_ENDPOINT = f"{BASE_URL}/dashboard/populate-hierarchical"
NEW_ENDPOINT = f"{BASE_URL}/dashboard/populate-optimized"

# Test case context
TEST_CASE = {
    "case_context": "Medical malpractice case involving surgical complications and patient safety violations during emergency surgery at City Hospital. Patient experienced unexpected complications due to procedural errors and inadequate monitoring."
}

def test_endpoint(endpoint_url, endpoint_name):
    """Test a specific endpoint and return results"""
    print(f"\n🧪 Testing {endpoint_name}")
    print(f"📡 URL: {endpoint_url}")
    print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            endpoint_url,
            json=TEST_CASE,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minute timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Basic info
            print(f"✅ Success: {data.get('success', False)}")
            print(f"🆔 Case ID: {data.get('case_id', 'N/A')}")
            print(f"⏰ Server Time: {data.get('total_time', 'N/A')}s")
            
            # Grid analysis
            grids = data.get('grids', {})
            print(f"📊 Grids Found: {len(grids)}")
            
            for grid_name, grid_data in grids.items():
                if grid_data:
                    print(f"   └─ {grid_name}: ✅ Has data")
                else:
                    print(f"   └─ {grid_name}: ❌ Empty")
            
            # Success metrics (new endpoint only)
            if 'success_metrics' in data:
                metrics = data['success_metrics']
                print(f"📈 Success Metrics:")
                print(f"   └─ Compliance: {'✅' if metrics.get('compliance_success') else '❌'}")
                print(f"   └─ Laws: {'✅' if metrics.get('laws_success') else '❌'}")
                print(f"   └─ Live Cases: {'✅' if metrics.get('live_cases_success') else '❌'}")
                print(f"   └─ Overall: {'✅' if metrics.get('overall_success') else '❌'}")
            
            # AI Confidence (new endpoint only)
            if 'ai_confidence' in data:
                confidence = data['ai_confidence']
                print(f"🤖 AI Confidence: {confidence:.2f}")
            
            return {
                'success': True,
                'duration': duration,
                'status_code': response.status_code,
                'data': data
            }
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return {
                'success': False,
                'duration': duration,
                'status_code': response.status_code,
                'error': response.text
            }
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout after 5 minutes")
        return {
            'success': False,
            'duration': 300,
            'error': 'Timeout'
        }
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {
            'success': False,
            'duration': time.time() - start_time,
            'error': str(e)
        }

def compare_responses(old_result, new_result):
    """Compare the results from both endpoints"""
    print(f"\n📊 COMPARISON SUMMARY")
    print(f"{'='*50}")
    
    # Performance comparison
    print(f"⏱️  PERFORMANCE:")
    if old_result['success'] and new_result['success']:
        old_time = old_result['duration']
        new_time = new_result['duration']
        improvement = (old_time - new_time) / old_time * 100
        print(f"   Old Endpoint: {old_time:.2f}s")
        print(f"   New Endpoint: {new_time:.2f}s")
        print(f"   Improvement: {improvement:.1f}% faster")
    else:
        print(f"   Old Endpoint: {'✅' if old_result['success'] else '❌'} ({old_result['duration']:.2f}s)")
        print(f"   New Endpoint: {'✅' if new_result['success'] else '❌'} ({new_result['duration']:.2f}s)")
    
    # Grid comparison
    if old_result['success'] and new_result['success']:
        old_grids = len(old_result['data'].get('grids', {}))
        new_grids = len(new_result['data'].get('grids', {}))
        print(f"\n📊 GRIDS:")
        print(f"   Old Endpoint: {old_grids} grids")
        print(f"   New Endpoint: {new_grids} grids")
        print(f"   Reduction: {old_grids - new_grids} grids removed")
    
    # Success rate
    print(f"\n✅ SUCCESS RATE:")
    print(f"   Old Endpoint: {'✅ Success' if old_result['success'] else '❌ Failed'}")
    print(f"   New Endpoint: {'✅ Success' if new_result['success'] else '❌ Failed'}")
    
    # Recommendations
    print(f"\n🎯 RECOMMENDATION:")
    if new_result['success'] and (not old_result['success'] or new_result['duration'] < old_result['duration']):
        print(f"   ✅ Use NEW optimized endpoint")
        print(f"   📈 Better performance and reliability")
    elif old_result['success'] and not new_result['success']:
        print(f"   ⚠️  NEW endpoint has issues - investigate")
    else:
        print(f"   🔄 Both endpoints working - migrate when ready")

def save_results(old_result, new_result):
    """Save test results to JSON file"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'test_case': TEST_CASE,
        'old_endpoint': {
            'url': OLD_ENDPOINT,
            'result': old_result
        },
        'new_endpoint': {
            'url': NEW_ENDPOINT,
            'result': new_result
        }
    }
    
    filename = f"endpoint_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {filename}")

def main():
    """Main testing function"""
    print(f"🚀 API Endpoint Comparison Test")
    print(f"{'='*50}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Test Case: Medical malpractice scenario")
    
    # Test old endpoint
    old_result = test_endpoint(OLD_ENDPOINT, "OLD (Hierarchical) Endpoint")
    
    # Wait a moment between tests
    print(f"\n⏳ Waiting 5 seconds before next test...")
    time.sleep(5)
    
    # Test new endpoint
    new_result = test_endpoint(NEW_ENDPOINT, "NEW (Optimized) Endpoint")
    
    # Compare results
    compare_responses(old_result, new_result)
    
    # Save results
    save_results(old_result, new_result)
    
    print(f"\n🎉 Testing completed!")

if __name__ == "__main__":
    main()
