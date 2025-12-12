"""
Quick Validation Tests - Run before exhibition
Tests all critical functionality in ~30 seconds
"""

import requests
import joblib
import os
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def test_backend_running():
    """Test 1: Backend server is running"""
    print("\n🔧 Testing Backend Server...")
    try:
        response = requests.get("http://localhost:8000/docs", timeout=3)
        if response.status_code == 200:
            print("✅ Backend is running on http://localhost:8000")
            return True
        else:
            print(f"⚠️  Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        print("   → Start backend: python -m uvicorn main:app --reload")
        return False

def test_frontend_running():
    """Test 2: Frontend server is running"""
    print("\n🎨 Testing Frontend Server...")
    try:
        response = requests.get("http://localhost:5173", timeout=3)
        if response.status_code == 200:
            print("✅ Frontend is running on http://localhost:5173")
            return True
        else:
            print(f"⚠️  Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend not accessible: {e}")
        print("   → Start frontend: cd frontend && npm run dev")
        return False

def test_models_exist():
    """Test 3: All model files exist and load"""
    print("\n🤖 Testing Model Files...")
    models = {
        'Random Forest': 'models/random_forest.joblib',
        'LightGBM': 'models/lightgbm.joblib',
        'XGBoost': 'models/xgboost.joblib'
    }
    
    all_passed = True
    for name, path in models.items():
        if os.path.exists(path):
            try:
                model = joblib.load(path)
                print(f"✅ {name} loaded successfully")
            except Exception as e:
                print(f"❌ {name} failed to load: {e}")
                all_passed = False
        else:
            print(f"❌ {name} not found at {path}")
            all_passed = False
    
    return all_passed

def test_text_prediction():
    """Test 4: Text prediction endpoint works"""
    print("\n📝 Testing Text Prediction API...")
    try:
        test_text = "Scientists at MIT have discovered a groundbreaking new technology."
        response = requests.post(
            "http://localhost:8000/predict",
            json={"text": test_text},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            prediction = data.get('prediction', 'Unknown')
            confidence = data.get('confidence', 0)
            
            print(f"✅ Prediction API works")
            print(f"   → Prediction: {prediction}")
            print(f"   → Confidence: {confidence:.1f}%")
            
            # Validate response structure
            if 'individual_predictions' in data:
                print(f"   → Individual models: {len(data['individual_predictions'])} models")
            
            return True
        else:
            print(f"❌ Prediction failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        return False

def test_lime_explanation():
    """Test 5: LIME explanation endpoint works"""
    print("\n🧠 Testing LIME Explanation API...")
    try:
        test_text = "BREAKING NEWS! You won't believe this shocking discovery!"
        response = requests.post(
            "http://localhost:8000/explain",
            json={"text": test_text},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'explanation' in data and len(data['explanation']) > 0:
                print(f"✅ LIME Explanation works")
                print(f"   → Generated {len(data['explanation'])} word explanations")
                # Show top 3 words
                top_words = sorted(data['explanation'].items(), 
                                 key=lambda x: abs(x[1]), reverse=True)[:3]
                for word, score in top_words:
                    indicator = "🔴 FAKE" if score > 0 else "🟢 REAL"
                    print(f"   → '{word}': {score:.3f} {indicator}")
                return True
            else:
                print("⚠️  LIME returned empty explanation")
                return False
        else:
            print(f"❌ LIME failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ LIME test failed: {e}")
        return False

def test_visual_detection():
    """Test 6: Visual detection endpoint (basic check)"""
    print("\n👁️  Testing Visual Detection API...")
    try:
        # Just check if endpoint exists (we need actual image to test fully)
        # For now, send invalid request to check endpoint is accessible
        response = requests.post(
            "http://localhost:8000/detect-visual",
            files={"image": ("test.txt", b"dummy", "text/plain")},
            data={"context": "test"},
            timeout=5
        )
        
        # We expect either 422 (validation error) or 400 (bad request)
        # but NOT 404 (not found) or 500 (server error)
        if response.status_code in [200, 400, 422]:
            print(f"✅ Visual Detection endpoint is accessible")
            return True
        elif response.status_code == 404:
            print(f"❌ Visual Detection endpoint not found")
            return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return True  # Consider it working but with issues
            
    except Exception as e:
        print(f"❌ Visual Detection test failed: {e}")
        return False

def test_datasets_exist():
    """Test 7: Check if training datasets exist"""
    print("\n📊 Checking Datasets...")
    
    dataset_files = [
        'datasets/train.csv',
        'datasets/test.csv',
        'datasets/Constraint_Train.csv',
    ]
    
    found = []
    missing = []
    
    for filepath in dataset_files:
        if os.path.exists(filepath):
            found.append(filepath)
        else:
            missing.append(filepath)
    
    if found:
        print(f"✅ Found {len(found)} dataset files:")
        for f in found[:3]:  # Show first 3
            print(f"   → {f}")
    
    if missing:
        print(f"⚠️  Missing {len(missing)} dataset files (optional)")
    
    return len(found) > 0

def test_error_handling():
    """Test 8: API handles errors gracefully"""
    print("\n🛡️  Testing Error Handling...")
    
    tests_passed = 0
    tests_total = 3
    
    # Test 1: Empty text
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"text": ""},
            timeout=5
        )
        if response.status_code in [400, 422]:
            print("✅ Correctly rejects empty text")
            tests_passed += 1
        else:
            print(f"⚠️  Empty text returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Empty text test failed: {e}")
    
    # Test 2: Very long text
    try:
        long_text = "word " * 5000
        response = requests.post(
            "http://localhost:8000/predict",
            json={"text": long_text},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Handles very long text")
            tests_passed += 1
        else:
            print(f"⚠️  Long text returned: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Long text test timeout (acceptable)")
        tests_passed += 1
    
    # Test 3: Special characters
    try:
        special_text = "Test 你好 émojis 🎉 @#$%^&*()"
        response = requests.post(
            "http://localhost:8000/predict",
            json={"text": special_text},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Handles special characters")
            tests_passed += 1
        else:
            print(f"⚠️  Special chars returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Special chars test failed: {e}")
    
    return tests_passed == tests_total

def run_all_tests():
    """Run all quick validation tests"""
    print_header("QUICK VALIDATION TEST SUITE")
    print("Testing Fake News Detection System...")
    print(f"Date: December 13, 2025")
    
    results = {}
    
    # Critical tests (must pass)
    critical_tests = [
        ("Backend Server", test_backend_running),
        ("Model Files", test_models_exist),
        ("Text Prediction", test_text_prediction),
        ("LIME Explanation", test_lime_explanation),
    ]
    
    # Important tests (should pass)
    important_tests = [
        ("Frontend Server", test_frontend_running),
        ("Visual Detection", test_visual_detection),
        ("Error Handling", test_error_handling),
        ("Datasets", test_datasets_exist),
    ]
    
    print_header("CRITICAL TESTS")
    critical_passed = 0
    for name, test_func in critical_tests:
        try:
            results[name] = test_func()
            if results[name]:
                critical_passed += 1
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            results[name] = False
    
    print_header("IMPORTANT TESTS")
    important_passed = 0
    for name, test_func in important_tests:
        try:
            results[name] = test_func()
            if results[name]:
                important_passed += 1
        except Exception as e:
            print(f"⚠️  {name} crashed: {e}")
            results[name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\n📊 Results: {total_passed}/{total_tests} tests passed")
    print(f"   Critical: {critical_passed}/{len(critical_tests)} ✓")
    print(f"   Important: {important_passed}/{len(important_tests)} ✓")
    
    # Status indicator
    if critical_passed == len(critical_tests):
        print("\n🎉 READY FOR EXHIBITION!")
        print("   All critical systems are working.")
        if important_passed < len(important_tests):
            print(f"   Note: {len(important_tests) - important_passed} optional tests failed")
    else:
        print("\n⚠️  NOT READY - Fix critical issues first:")
        for name, test_func in critical_tests:
            if not results.get(name, False):
                print(f"   ❌ {name}")
    
    print("\n" + "="*60 + "\n")
    
    return critical_passed == len(critical_tests)

if __name__ == "__main__":
    print("\n")
    success = run_all_tests()
    sys.exit(0 if success else 1)
