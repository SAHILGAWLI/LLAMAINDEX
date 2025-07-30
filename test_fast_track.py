#!/usr/bin/env python3
"""
Test Fast-Track Optimization
"""

import requests
import json
import time

def test_fast_track():
    """Test the fast-track optimization for simple cases"""
    print("🚀 TESTING FAST-TRACK OPTIMIZATION")
    print("=" * 60)
    
    test_case = {
        "case_id": "FAST-DRUG-001",
        "case_context": "Accused was found selling illegal drugs including charas and ganja near a school. Police recovered 500 grams of narcotic substances."
    }
    
    print(f"📝 Test Case: {test_case['case_context']}")
    print(f"🎯 Expected: Fast-track processing under 30 seconds")
    
    try:
        print("🔄 Sending request to fast-track optimized system...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8001/dashboard/populate-optimized",
            json=test_case,
            timeout=120  # 2 minutes max
        )
        
        end_time = time.time()
        actual_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Response received in {actual_time:.2f}s")
            
            # Performance analysis
            if actual_time <= 30:
                performance_status = "🚀 EXCELLENT - Fast-track working!"
            elif actual_time <= 60:
                performance_status = "✅ GOOD - Significant improvement"
            elif actual_time <= 120:
                performance_status = "⚠️ ACCEPTABLE - Some improvement"
            else:
                performance_status = "❌ NEEDS MORE WORK"
            
            print(f"📊 Performance: {performance_status}")
            print(f"   Actual Time: {actual_time:.2f}s")
            
            # Check for errors
            legal_compliance = data.get('legal_compliance', '')
            bns_laws = data.get('bns_laws', '')
            
            if "Enhanced agent analysis failed" in legal_compliance:
                print("❌ Legal compliance failed")
                print(f"   Error: {legal_compliance[:100]}...")
            else:
                print("✅ Legal compliance successful")
                print(f"   Length: {len(legal_compliance)} chars")
            
            if "Enhanced agent analysis failed" in bns_laws:
                print("❌ BNS laws failed")
                print(f"   Error: {bns_laws[:100]}...")
            else:
                print("✅ BNS laws successful")
                print(f"   Length: {len(bns_laws)} chars")
            
            # Check success metrics
            success_metrics = data.get('success_metrics', {})
            overall_success = success_metrics.get('overall', False)
            ai_confidence = data.get('ai_confidence', 0)
            
            print(f"\n📈 Success Metrics:")
            print(f"   Overall Success: {'✅' if overall_success else '❌'}")
            print(f"   AI Confidence: {ai_confidence:.1%}")
            print(f"   Legal Analysis: {'✅' if success_metrics.get('legal_analysis', False) else '❌'}")
            print(f"   Live Cases: {'✅' if success_metrics.get('live_cases', False) else '❌'}")
            
            # Check live cases
            live_cases = data.get('live_cases', {})
            if isinstance(live_cases, dict) and live_cases.get('status') == 'success':
                print(f"   Live Cases Found: {live_cases.get('total_cases', 0)}")
            
            # Check FIR intelligence
            fir_intelligence = data.get('grid_4_fir_intelligence', {})
            if fir_intelligence:
                print(f"   FIR Intelligence: ✅ Generated")
                fir_confidence = fir_intelligence.get('ai_confidence', 0)
                print(f"   FIR AI Confidence: {fir_confidence:.1%}")
            
            if overall_success and actual_time <= 60:
                print(f"\n🎉 FAST-TRACK OPTIMIZATION SUCCESS!")
                print(f"✅ Drug crime processed in {actual_time:.2f}s")
                print(f"✅ All grids working properly")
                print(f"✅ High AI confidence: {ai_confidence:.1%}")
            elif overall_success:
                print(f"\n✅ OPTIMIZATION WORKING")
                print(f"⚠️ Time could be better: {actual_time:.2f}s")
                print(f"✅ All grids working properly")
            else:
                print(f"\n⚠️ OPTIMIZATION NEEDS MORE WORK")
                print(f"❌ Some grids failing")
                print(f"⏱️ Time: {actual_time:.2f}s")
            
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🔍 Checking server connection...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Fast-track server is running!")
            test_fast_track()
        else:
            print("❌ Server not responding properly")
    except:
        print("❌ Cannot connect to server")
        print("💡 Make sure fast-track server is running on port 8001")
