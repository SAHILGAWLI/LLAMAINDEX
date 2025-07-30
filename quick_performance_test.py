#!/usr/bin/env python3
"""
Quick Performance Test - Fast validation of key scenarios
"""

import requests
import time

def quick_test():
    """Quick test of key scenarios"""
    print("⚡ QUICK PERFORMANCE VALIDATION")
    print("=" * 50)
    
    quick_cases = [
        {
            "name": "🚫 Drug Crime (Fast-Track)",
            "case_context": "Drug trafficking case with illegal substances",
            "target": 20
        },
        {
            "name": "💻 Cyber Crime (Medium)",
            "case_context": "Online banking fraud and phishing attack",
            "target": 25
        },
        {
            "name": "🔄 Medical Negligence (Complex)",
            "case_context": "Medical malpractice during surgery with complications",
            "target": 40
        }
    ]
    
    results = []
    
    for i, case in enumerate(quick_cases, 1):
        print(f"\n🧪 Test {i}/3: {case['name']}")
        print(f"🎯 Target: <{case['target']}s")
        
        try:
            start_time = time.time()
            
            response = requests.post(
                "http://localhost:8001/dashboard/populate-optimized",
                json={
                    "case_id": f"QUICK-{i:03d}",
                    "case_context": case["case_context"]
                },
                timeout=120
            )
            
            actual_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success_metrics', {}).get('overall', False)
                confidence = data.get('ai_confidence', 0)
                
                status = "🚀" if actual_time <= case['target'] else "⚠️" if actual_time <= case['target'] * 1.5 else "❌"
                
                print(f"   {status} Time: {actual_time:.2f}s | Success: {'✅' if success else '❌'} | Confidence: {confidence:.1%}")
                
                results.append({
                    "name": case["name"],
                    "time": actual_time,
                    "target": case["target"],
                    "success": success,
                    "confidence": confidence
                })
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Quick summary
    if results:
        avg_time = sum(r["time"] for r in results) / len(results)
        avg_confidence = sum(r["confidence"] for r in results) / len(results)
        success_count = sum(1 for r in results if r["success"])
        
        print(f"\n📊 Quick Summary:")
        print(f"   Average Time: {avg_time:.2f}s")
        print(f"   Success Rate: {success_count}/{len(results)}")
        print(f"   Average Confidence: {avg_confidence:.1%}")
        
        if avg_time <= 30 and success_count == len(results):
            print(f"   🎉 EXCELLENT: System performing optimally!")
        elif avg_time <= 45 and success_count >= len(results) * 0.8:
            print(f"   ✅ GOOD: System performing well!")
        else:
            print(f"   ⚠️ NEEDS ATTENTION: Check performance!")

if __name__ == "__main__":
    quick_test()
