#!/usr/bin/env python3
"""
Test Performance Optimization for Revolutionary System
"""

import requests
import json
import time

def test_performance_optimization():
    """Test the performance optimizations"""
    print("🚀 TESTING PERFORMANCE OPTIMIZATIONS")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "🔄 Medical Negligence (Previously Slow)",
            "case_id": "PERF-MED-001",
            "case_context": "Medical malpractice case involving negligent surgery leading to patient complications. Hospital failed to follow proper protocols.",
            "expected_time": 60  # Should be under 60 seconds now
        },
        {
            "name": "🚫 Drug Crime (Fast Case)",
            "case_id": "PERF-DRUG-001", 
            "case_context": "Accused was found selling illegal substances including charas and ganja near a school.",
            "expected_time": 30  # Should be under 30 seconds
        },
        {
            "name": "💻 Cyber Crime (Medium Case)",
            "case_id": "PERF-CYBER-001",
            "case_context": "Online fraud through fake banking website where accused stole credit card details.",
            "expected_time": 45  # Should be under 45 seconds
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*20} TEST {i}/{len(test_cases)} {'='*20}")
        print(f"🧪 {test_case['name']}")
        print(f"⏱️ Expected Time: Under {test_case['expected_time']}s")
        print("=" * 60)
        
        payload = {
            "case_id": test_case["case_id"],
            "case_context": test_case["case_context"]
        }
        
        try:
            print("🔄 Sending request to optimized system...")
            start_time = time.time()
            
            response = requests.post(
                "http://localhost:8001/dashboard/populate-optimized",
                json=payload,
                timeout=300
            )
            
            end_time = time.time()
            actual_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Response received in {actual_time:.2f}s")
                
                # Performance analysis
                expected_time = test_case["expected_time"]
                performance_ratio = actual_time / expected_time
                
                if actual_time <= expected_time:
                    performance_status = "🚀 EXCELLENT"
                elif actual_time <= expected_time * 1.5:
                    performance_status = "✅ GOOD"
                elif actual_time <= expected_time * 2:
                    performance_status = "⚠️ ACCEPTABLE"
                else:
                    performance_status = "❌ NEEDS OPTIMIZATION"
                
                print(f"📊 Performance: {performance_status}")
                print(f"   Expected: {expected_time}s")
                print(f"   Actual: {actual_time:.2f}s")
                print(f"   Ratio: {performance_ratio:.2f}x")
                
                # Check for max iterations errors
                legal_compliance = data.get('legal_compliance', '')
                bns_laws = data.get('bns_laws', '')
                
                max_iterations_error = False
                if "Max iterations" in legal_compliance or "Max iterations" in bns_laws:
                    max_iterations_error = True
                    print("❌ Max iterations error detected!")
                else:
                    print("✅ No max iterations errors")
                
                # Check success metrics
                success_metrics = data.get('success_metrics', {})
                overall_success = success_metrics.get('overall', False)
                ai_confidence = data.get('ai_confidence', 0)
                
                print(f"📈 Success Metrics:")
                print(f"   Overall Success: {'✅' if overall_success else '❌'}")
                print(f"   AI Confidence: {ai_confidence:.1%}")
                print(f"   Legal Analysis: {'✅' if success_metrics.get('legal_analysis', False) else '❌'}")
                print(f"   Live Cases: {'✅' if success_metrics.get('live_cases', False) else '❌'}")
                
                results.append({
                    "test": test_case["name"],
                    "expected_time": expected_time,
                    "actual_time": actual_time,
                    "performance_ratio": performance_ratio,
                    "performance_status": performance_status,
                    "max_iterations_error": max_iterations_error,
                    "overall_success": overall_success,
                    "ai_confidence": ai_confidence
                })
                
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                results.append({
                    "test": test_case["name"],
                    "expected_time": expected_time,
                    "actual_time": 999,
                    "performance_ratio": 999,
                    "performance_status": "❌ FAILED",
                    "max_iterations_error": True,
                    "overall_success": False,
                    "ai_confidence": 0
                })
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append({
                "test": test_case["name"],
                "expected_time": expected_time,
                "actual_time": 999,
                "performance_ratio": 999,
                "performance_status": "❌ ERROR",
                "max_iterations_error": True,
                "overall_success": False,
                "ai_confidence": 0
            })
        
        # Wait between tests
        if i < len(test_cases):
            print("\n⏳ Waiting 3 seconds before next test...")
            time.sleep(3)
    
    # Final performance summary
    print("\n" + "="*80)
    print("📊 PERFORMANCE OPTIMIZATION RESULTS")
    print("="*80)
    
    excellent_count = sum(1 for r in results if "EXCELLENT" in r["performance_status"])
    good_count = sum(1 for r in results if "GOOD" in r["performance_status"])
    acceptable_count = sum(1 for r in results if "ACCEPTABLE" in r["performance_status"])
    needs_work_count = sum(1 for r in results if "NEEDS OPTIMIZATION" in r["performance_status"] or "FAILED" in r["performance_status"] or "ERROR" in r["performance_status"])
    
    max_iterations_errors = sum(1 for r in results if r["max_iterations_error"])
    successful_tests = sum(1 for r in results if r["overall_success"])
    avg_confidence = sum(r["ai_confidence"] for r in results) / len(results)
    avg_performance_ratio = sum(r["performance_ratio"] for r in results if r["performance_ratio"] < 10) / len([r for r in results if r["performance_ratio"] < 10])
    
    for result in results:
        print(f"   {result['performance_status']}: {result['test']}")
        print(f"      ⏱️ Time: {result['actual_time']:.2f}s (Expected: {result['expected_time']}s)")
        print(f"      📊 Ratio: {result['performance_ratio']:.2f}x")
        print(f"      🧠 AI Confidence: {result['ai_confidence']:.1%}")
        print(f"      🔄 Max Iterations Error: {'Yes' if result['max_iterations_error'] else 'No'}")
    
    print(f"\n🎯 OVERALL PERFORMANCE:")
    print(f"   🚀 Excellent: {excellent_count}/{len(results)}")
    print(f"   ✅ Good: {good_count}/{len(results)}")
    print(f"   ⚠️ Acceptable: {acceptable_count}/{len(results)}")
    print(f"   ❌ Needs Work: {needs_work_count}/{len(results)}")
    
    print(f"\n📈 OPTIMIZATION METRICS:")
    print(f"   Max Iterations Errors: {max_iterations_errors}/{len(results)}")
    print(f"   Successful Tests: {successful_tests}/{len(results)}")
    print(f"   Average AI Confidence: {avg_confidence:.1%}")
    print(f"   Average Performance Ratio: {avg_performance_ratio:.2f}x")
    
    if max_iterations_errors == 0:
        print(f"\n🎉 OPTIMIZATION SUCCESS: No max iterations errors!")
    elif max_iterations_errors < len(results):
        print(f"\n✅ OPTIMIZATION IMPROVED: Reduced max iterations errors!")
    else:
        print(f"\n⚠️ OPTIMIZATION NEEDED: Still experiencing max iterations errors")
    
    if avg_performance_ratio <= 1.5:
        print(f"🚀 PERFORMANCE EXCELLENT: Average {avg_performance_ratio:.2f}x expected time")
    elif avg_performance_ratio <= 2.0:
        print(f"✅ PERFORMANCE GOOD: Average {avg_performance_ratio:.2f}x expected time")
    else:
        print(f"⚠️ PERFORMANCE NEEDS WORK: Average {avg_performance_ratio:.2f}x expected time")
    
    return results

if __name__ == "__main__":
    print("🔍 Checking server connection...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Optimized server is running!")
            test_performance_optimization()
        else:
            print("❌ Server not responding properly")
    except:
        print("❌ Cannot connect to server")
        print("💡 Make sure optimized server is running on port 8001")
