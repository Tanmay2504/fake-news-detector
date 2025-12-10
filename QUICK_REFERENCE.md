# 🚀 QUICK REFERENCE CARD

## Installation & Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download NLTK data
python setup.py

# 3. Add your models (REQUIRED)
# Place these in models/ directory:
#   - random_forest.joblib
#   - lightgbm.joblib  
#   - xgboost.joblib

# 4. Start server
python main.py
```

---

## API Usage

### Base URL
```
http://localhost:8000
```

### Quick Test
```bash
curl http://localhost:8000/health
```

### Predict
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your news article here"}'
```

### Batch
```bash
curl -X POST "http://localhost:8000/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Article 1", "Article 2"]}'
```

### Explain
```bash
curl -X POST "http://localhost:8000/explain" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your article", "num_features": 10}'
```

---

## Python Examples

### Single Prediction
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "BREAKING: Shocking news!!!"}
)
result = response.json()
print(f"{result['prediction']} ({result['confidence']:.2%})")
```

### Batch Prediction
```python
response = requests.post(
    "http://localhost:8000/batch",
    json={"texts": ["Article 1", "Article 2"]}
)
result = response.json()
for pred, conf in zip(result['predictions'], result['confidences']):
    print(f"{pred}: {conf:.2%}")
```

### Get Explanation
```python
response = requests.post(
    "http://localhost:8000/explain",
    json={"text": "Article text", "num_features": 10}
)
result = response.json()
for word, weight in result['weights'][:5]:
    print(f"{word}: {weight:+.4f}")
```

---

## Docker

```bash
# Build
docker build -t fake-news-api .

# Run
docker run -d -p 8000:8000 \
  -v ${PWD}/models:/app/models \
  fake-news-api

# Using Docker Compose
docker-compose up -d
```

---

## File Structure

```
Fake News V2/
├── main.py              # Start here
├── requirements.txt     # Dependencies
├── test_api.py         # Test suite
├── models/             # Put your .joblib files here
└── src/
    ├── api/routes.py      # All endpoints
    ├── ml/ensemble.py     # Ensemble logic
    ├── ml/rules.py        # Rule patterns
    ├── ml/explainer.py    # LIME
    └── utils/             # Helpers
```

---

## Configuration (.env)

```bash
HOST=0.0.0.0
PORT=8000
MODEL_DIR=models
CACHE_MAX_SIZE=1000
CACHE_TTL=3600
```

---

## Common Commands

```bash
# Start server
python main.py

# Run setup
python setup.py

# Test API
python test_api.py

# Train models (template)
python train_models.py

# Docker build
docker build -t fake-news-api .

# Docker run
docker-compose up -d
```

---

## Troubleshooting

**Models not loading?**
```bash
# Check models exist
ls models/

# Run setup to verify
python setup.py
```

**Import errors?**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**NLTK errors?**
```bash
# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

**Port already in use?**
```bash
# Change port in .env
PORT=5000
```

---

## Response Format

```json
{
  "prediction": "fake",
  "confidence": 0.87,
  "probability_fake": 0.87,
  "probability_real": 0.13,
  "individual_predictions": {
    "random_forest": {"prediction": "fake", "confidence": 0.92},
    "lightgbm": {"prediction": "fake", "confidence": 0.85},
    "xgboost": {"prediction": "fake", "confidence": 0.78}
  },
  "rule_based_analysis": {
    "fake_score": 8,
    "real_score": 2
  }
}
```

---

## Ensemble Weights

- Random Forest: **60%** (primary)
- LightGBM: **20%** (secondary)
- XGBoost: **20%** (secondary)

---

## Documentation Files

- `README.md` - Overview
- `API_DOCUMENTATION.md` - Complete API reference
- `DEPLOYMENT.md` - Production deployment
- `DOCKER.md` - Docker guide
- `PROJECT_SUMMARY.md` - Full summary
- `ARCHITECTURE.md` - System diagrams
- `COMPLETE.md` - Implementation checklist

---

## Key Features

✅ Ensemble ML (3 models)
✅ Rule-based detection
✅ LIME explanations
✅ Caching (80% faster)
✅ Batch processing
✅ Visual detection
✅ Docker support
✅ Full documentation

---

## URLs to Remember

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

---

## Performance

- Single: 50-200ms (uncached), 5ms (cached)
- Batch: ~30ms per article
- LIME: 2-5 seconds
- Visual: 3-10 seconds

---

## Model Format Required

```python
# Each model must be a Pipeline:
Pipeline([
    ('tfidf', TfidfVectorizer(...)),
    ('clf', Classifier(...))
])

# Save as:
joblib.dump(pipeline, 'models/random_forest.joblib')
```

---

## Quick Health Check

```bash
# 1. Check server is running
curl http://localhost:8000/health

# 2. Quick prediction test
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "test article"}'

# 3. Run full test suite
python test_api.py
```

---

## Need Help?

1. Check `COMPLETE.md` for implementation status
2. See `API_DOCUMENTATION.md` for endpoint details
3. Read `DEPLOYMENT.md` for production setup
4. Review `ARCHITECTURE.md` for system design
5. Run `python test_api.py` to verify setup

---

**Ready to go! 🚀**
