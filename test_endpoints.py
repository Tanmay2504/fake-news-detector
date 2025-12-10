"""
Test script for Fake News Detection API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test /health endpoint"""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_predict():
    """Test /predict endpoint"""
    print("\n" + "=" * 60)
    print("TEST 2: Fake News Prediction")
    print("=" * 60)
    
    payload = {
        "text": "BREAKING!!! SHOCKING discovery about vaccines that THEY don't want you to know!!!",
        "clean": True,
        "mode": "ensemble"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Text: {payload['text'][:50]}...")
        print(f"Prediction: {data.get('prediction', 'N/A').upper()}")
        print(f"Confidence: {data.get('confidence', 0):.2%}")
        print(f"Models used: {data.get('models_used', [])}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_predict_real():
    """Test /predict endpoint with real news"""
    print("\n" + "=" * 60)
    print("TEST 3: Real News Prediction")
    print("=" * 60)
    
    payload = {
        "text": "The Senate passed the infrastructure bill with bipartisan support today according to Reuters.",
        "clean": True,
        "mode": "ensemble"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Text: {payload['text']}")
        print(f"Prediction: {data.get('prediction', 'N/A').upper()}")
        print(f"Confidence: {data.get('confidence', 0):.2%}")
        print(f"Models used: {data.get('models_used', [])}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_explain():
    """Test /explain endpoint"""
    print("\n" + "=" * 60)
    print("TEST 4: LIME Explanation")
    print("=" * 60)
    
    payload = {
        "text": "Senate passes infrastructure bill",
        "num_features": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/explain", json=payload)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Model: {data.get('model', 'N/A')}")
        print(f"Prediction: {data.get('prediction', 'N/A').upper()}")
        print(f"Top influential words:")
        for word, weight in data.get('top_features', [])[:5]:
            print(f"  {word}: {weight:.4f}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 Starting API Tests...\n")
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Fake News Prediction", test_predict()))
    results.append(("Real News Prediction", test_predict_real()))
    results.append(("LIME Explanation", test_explain()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your API is working perfectly!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check the errors above.")
