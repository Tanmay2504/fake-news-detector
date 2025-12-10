# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check

**GET** `/health`

Check system health and model status.

**Response:**
```json
{
  "ok": true,
  "ensemble_loaded": true,
  "models_available": ["random_forest", "lightgbm", "xgboost"],
  "model_dir": "models",
  "cache_stats": {
    "size": 42,
    "max_size": 1000,
    "hits": 156,
    "misses": 89,
    "hit_rate": 0.637,
    "ttl": 3600
  }
}
```

---

### 2. Single Prediction

**POST** `/predict`

Classify a single news article as fake or real.

**Request Body:**
```json
{
  "text": "BREAKING: Shocking discovery reveals hidden truth!",
  "clean": true,
  "mode": "ensemble"
}
```

**Parameters:**
- `text` (string, required): News article text to classify
- `clean` (boolean, optional): Clean text before prediction (default: true)
- `mode` (string, optional): Prediction mode - "ensemble" or specific model name (default: "ensemble")

**Response:**
```json
{
  "prediction": "fake",
  "confidence": 0.87,
  "probability_fake": 0.87,
  "probability_real": 0.13,
  "proba": [0.87, 0.13],
  "individual_predictions": {
    "random_forest": {
      "prediction": "fake",
      "probability_fake": 0.92,
      "probability_real": 0.08,
      "confidence": 0.92
    },
    "lightgbm": {
      "prediction": "fake",
      "probability_fake": 0.85,
      "probability_real": 0.15,
      "confidence": 0.85
    },
    "xgboost": {
      "prediction": "fake",
      "probability_fake": 0.78,
      "probability_real": 0.22,
      "confidence": 0.78
    }
  },
  "models_used": ["random_forest", "lightgbm", "xgboost"],
  "rule_based_analysis": {
    "prediction": "fake",
    "confidence": 0.75,
    "fake_score": 8,
    "real_score": 2,
    "fake_indicators_found": 5,
    "real_indicators_found": 1
  },
  "cached": false
}
```

**Example (curl):**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "BREAKING: Shocking discovery reveals hidden truth!",
    "clean": true
  }'
```

**Example (Python):**
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "text": "BREAKING: Shocking discovery reveals hidden truth!",
        "clean": True
    }
)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

### 3. Batch Prediction

**POST** `/batch`

Classify multiple news articles at once (max 100 per request).

**Request Body:**
```json
{
  "texts": [
    "SHOCKING: You won't believe this!",
    "According to official sources, the meeting concluded on Tuesday."
  ],
  "clean": true
}
```

**Parameters:**
- `texts` (array of strings, required): List of news articles
- `clean` (boolean, optional): Clean text before prediction (default: true)

**Response:**
```json
{
  "predictions": ["fake", "real"],
  "confidences": [0.89, 0.82],
  "probas": [
    [0.89, 0.11],
    [0.18, 0.82]
  ]
}
```

**Example (Python):**
```python
import requests

response = requests.post(
    "http://localhost:8000/batch",
    json={
        "texts": [
            "SHOCKING: You won't believe this!",
            "According to official sources, the meeting concluded on Tuesday."
        ],
        "clean": True
    }
)

result = response.json()
for i, (pred, conf) in enumerate(zip(result['predictions'], result['confidences'])):
    print(f"Article {i+1}: {pred} ({conf:.2%} confidence)")
```

---

### 4. Explain Prediction

**POST** `/explain`

Get LIME-based word-level explanations for predictions.

**Request Body:**
```json
{
  "text": "BREAKING: Shocking discovery reveals hidden truth!",
  "num_features": 10,
  "model_name": null
}
```

**Parameters:**
- `text` (string, required): News article to explain
- `num_features` (integer, optional): Number of top features to show (1-50, default: 10)
- `model_name` (string, optional): Specific model to explain (null = ensemble)

**Response:**
```json
{
  "prediction": "fake",
  "confidence": 0.87,
  "weights": [
    ["shocking", 0.2485],
    ["breaking", 0.1823],
    ["hidden", 0.1567],
    ["reveals", 0.1234],
    ["truth", -0.0892],
    ["discovery", 0.0678]
  ],
  "explanation_text": "Words suggesting FAKE: 'shocking', 'breaking', 'hidden' | Words suggesting REAL: 'truth'",
  "individual_explanations": {
    "random_forest": {
      "prediction": "fake",
      "confidence": 0.92,
      "weights": [["shocking", 0.28], ["breaking", 0.21]]
    }
  }
}
```

**Example (Python):**
```python
import requests

response = requests.post(
    "http://localhost:8000/explain",
    json={
        "text": "BREAKING: Shocking discovery reveals hidden truth!",
        "num_features": 10
    }
)

result = response.json()
print(f"Prediction: {result['prediction']} ({result['confidence']:.2%})")
print("\nTop contributing words:")
for word, weight in result['weights'][:5]:
    direction = "FAKE" if weight > 0 else "REAL"
    print(f"  {word:20s} {weight:+.4f} → {direction}")
```

---

### 5. Visual Fake News Detection

**POST** `/detect-visual`

Detect fake images using AI generation detection, manipulation analysis, and reverse image search.

**Request (multipart/form-data):**
- `image` (file, required): Image file to analyze
- `event` (string, optional): Event context
- `location` (string, optional): Location context
- `date` (string, optional): Date context

**Response:**
```json
{
  "verdict": "FAKE",
  "fake_score": 0.87,
  "confidence": 0.92,
  "is_fake": true,
  "reasons": [
    "AI-generated detected with 89% confidence",
    "No credible sources found",
    "Manipulation detected (65% probability)"
  ],
  "manipulation_check": {
    "manipulation_probability": 0.65,
    "ela_heatmap": "base64_encoded_image_data..."
  },
  "ai_generation_check": {
    "is_ai_generated": true,
    "confidence": 0.89,
    "model_type": "stable_diffusion"
  },
  "content_analysis": {
    "description": "A photo of a political event",
    "labels": ["people", "indoor", "event", "formal"],
    "objects_detected": 12
  },
  "source_verification": {
    "sources_found": 0,
    "credible_sources": 0,
    "first_seen": null
  }
}
```

**Example (curl):**
```bash
curl -X POST "http://localhost:8000/detect-visual" \
  -F "image=@suspicious_image.jpg" \
  -F "event=Presidential debate" \
  -F "location=Washington DC" \
  -F "date=2024-01-15"
```

**Example (Python):**
```python
import requests

with open('suspicious_image.jpg', 'rb') as f:
    response = requests.post(
        "http://localhost:8000/detect-visual",
        files={'image': f},
        data={
            'event': 'Presidential debate',
            'location': 'Washington DC',
            'date': '2024-01-15'
        }
    )

result = response.json()
print(f"Verdict: {result['verdict']}")
print(f"Fake Score: {result['fake_score']:.2%}")
print(f"Reasons: {', '.join(result['reasons'])}")
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Text too short (minimum 10 characters)"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Prediction failed: Model not loaded"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Visual detection not available: Module not found"
}
```

---

## Rate Limits

Currently no rate limits enforced. For production deployment, consider:
- 100 requests/minute per IP
- 1000 requests/hour per IP
- Batch endpoint: 10 requests/minute

---

## Best Practices

1. **Text Cleaning**: Always use `clean: true` unless you have pre-cleaned text
2. **Batch Processing**: Use `/batch` for multiple articles (much faster)
3. **Caching**: Identical requests are cached for 1 hour (80% faster)
4. **Error Handling**: Always check response status codes
5. **Visual Detection**: Requires Google Cloud Vision API credentials

---

## Performance

- **Single prediction**: ~50-200ms (cached: ~5ms)
- **Batch prediction**: ~30ms per article
- **LIME explanation**: ~2-5 seconds
- **Visual detection**: ~3-10 seconds

---

## Model Information

### Ensemble Weights
- Random Forest: 60%
- LightGBM: 20%
- XGBoost: 20%

### Pipeline Structure
Each model is a scikit-learn Pipeline:
```python
Pipeline([
    ('tfidf', TfidfVectorizer(...)),
    ('clf', Classifier(...))
])
```

### Input/Output
- Input: Raw text string
- Output: Probabilities [fake_prob, real_prob]

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with:
- Try-it-out functionality
- Request/response schemas
- Example values
- Authentication (if enabled)

Alternative: `http://localhost:8000/redoc` for a different documentation style.
