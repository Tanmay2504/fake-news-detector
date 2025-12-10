"""
Test script for the Fake News Detection API
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 60)
    print("Testing /health endpoint")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_predict():
    """Test prediction endpoint"""
    print("\n" + "=" * 60)
    print("Testing /predict endpoint")
    print("=" * 60)
    
    test_text = """
    BREAKING NEWS: You won't believe what happens next! 
    This shocking discovery will change everything! 
    Doctors hate this one simple trick!!!
    """
    
    payload = {
        "text": test_text,
        "clean": True,
        "mode": "ensemble"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nPrediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Probability Fake: {result['probability_fake']:.2%}")
        print(f"Probability Real: {result['probability_real']:.2%}")
        print(f"Models Used: {', '.join(result['models_used'])}")
        
        if 'rule_based_analysis' in result:
            print(f"\nRule-based Analysis:")
            print(f"  Fake Score: {result['rule_based_analysis']['fake_score']}")
            print(f"  Real Score: {result['rule_based_analysis']['real_score']}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def test_batch():
    """Test batch prediction endpoint"""
    print("\n" + "=" * 60)
    print("Testing /batch endpoint")
    print("=" * 60)
    
    test_texts = [
        "SHOCKING: You won't believe this amazing discovery!!!",
        "According to the official report, the meeting was held on January 15, 2024."
    ]
    
    payload = {
        "texts": test_texts,
        "clean": True
    }
    
    response = requests.post(f"{BASE_URL}/batch", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        for i, (text, pred, conf) in enumerate(zip(test_texts, result['predictions'], result['confidences'])):
            print(f"\nText {i+1}: {text[:50]}...")
            print(f"  Prediction: {pred}")
            print(f"  Confidence: {conf:.2%}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def test_explain():
    """Test explanation endpoint"""
    print("\n" + "=" * 60)
    print("Testing /explain endpoint")
    print("=" * 60)
    
    test_text = """
    BREAKING NEWS: Shocking discovery reveals hidden truth! 
    You won't believe what they found! This will amaze you!!!
    """
    
    payload = {
        "text": test_text,
        "num_features": 10
    }
    
    response = requests.post(f"{BASE_URL}/explain", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nPrediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"\nTop word contributions:")
        for word, weight in result['weights'][:10]:
            direction = "FAKE" if weight > 0 else "REAL"
            print(f"  {word:20s} {weight:+.4f} → {direction}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def main():
    """Run all tests"""
    print("=" * 60)
    print("Fake News Detection API - Test Suite")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the server is running!")
    
    try:
        # Test health first
        if not test_health():
            print("\n✗ Server not responding. Please start the server first:")
            print("  python main.py")
            return
        
        # Run tests
        results = {
            "health": test_health(),
            "predict": test_predict(),
            "batch": test_batch(),
            "explain": test_explain()
        }
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        for test_name, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{test_name:20s} {status}")
        
        total = len(results)
        passed = sum(results.values())
        print(f"\nPassed: {passed}/{total}")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to server. Please start the server first:")
        print("  python main.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
