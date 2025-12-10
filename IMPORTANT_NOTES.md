# ⚠️ IMPORTANT NOTES

## Visual Detection Module

The API includes integration for visual fake news detection via the `/detect-visual` endpoint.

### Expected Module Structure

The code expects this module to exist (you mentioned you already have it):

```
src/enhancements/
├── visual_detector.py           # Main visual detection class
├── image_context_classifier.py  # CNN classifier
├── image_processor.py           # Image preprocessing
├── web_search_verifier.py       # Reverse image search
└── source_verifier.py           # Source checking
```

### VisualFakeNewsDetector Class

The API expects this class signature:

```python
class VisualFakeNewsDetector:
    def __init__(self, google_credentials_path: str):
        """Initialize with Google Cloud credentials"""
        pass
    
    def detect(self, image_path: str, context: dict = None) -> dict:
        """
        Detect fake images
        
        Args:
            image_path: Path to image file
            context: Optional context (event, location, date)
            
        Returns:
            {
                "verdict": "FAKE" | "REAL" | "UNCERTAIN",
                "fake_score": 0.87,
                "confidence": 0.92,
                "is_fake": True,
                "reasons": [...],
                "manipulation_check": {...},
                "ai_generation_check": {...},
                "content_analysis": {...},
                "source_verification": {...}
            }
        """
        pass
```

### If You Don't Have This Module

If you don't have the visual detection module yet:

**Option 1: Disable the endpoint**
Comment out the `/detect-visual` route in `src/api/routes.py` (lines 220-273)

**Option 2: Create a placeholder**
Create a simple placeholder that returns "Not implemented":

```python
# src/enhancements/visual_detector.py
class VisualFakeNewsDetector:
    def __init__(self, google_credentials_path=None):
        pass
    
    def detect(self, image_path, context=None):
        return {
            "verdict": "UNCERTAIN",
            "fake_score": 0.5,
            "confidence": 0.0,
            "is_fake": False,
            "reasons": ["Visual detection not yet implemented"],
            "manipulation_check": None,
            "ai_generation_check": None,
            "content_analysis": None,
            "source_verification": None
        }
```

**Option 3: Use your existing module**
Since you mentioned you already have a complete visual detection system, just ensure it's in `src/enhancements/` and has the expected interface.

---

## Google Cloud Vision Credentials

### Required For
- Visual detection features only
- Not required for text-based fake news detection

### Setup
1. Download credentials JSON from Google Cloud Console
2. Place as `google-vision-credentials.json` in project root
3. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=google-vision-credentials.json
   ```

### If You Don't Have Credentials
- Text-based detection will work fine
- Visual detection endpoint will return an error
- All other endpoints will function normally

---

## Model Files

### Required Models
You MUST provide these files in `models/` directory:

```
models/
├── random_forest.joblib
├── lightgbm.joblib
└── xgboost.joblib
```

### Model Format
Each model must be a scikit-learn Pipeline:

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )),
    ('clf', RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))
])
```

### Testing Your Models
```python
import joblib

# Load model
model = joblib.load('models/random_forest.joblib')

# Verify it's a Pipeline
print(type(model))  # Should be Pipeline

# Verify it has the right steps
print(model.named_steps.keys())  # Should have 'tfidf' and 'clf'

# Test prediction
text = "Test article"
proba = model.predict_proba([text])[0]
print(f"Fake: {proba[0]:.2%}, Real: {proba[1]:.2%}")
```

---

## Dependencies

### Core Dependencies (Required)
- fastapi==0.115.0
- uvicorn==0.32.0
- scikit-learn==1.5.2
- lightgbm==4.5.0
- xgboost==2.1.2
- lime==0.2.0.1
- nltk==3.8.1

### Visual Detection Dependencies (Optional)
- torch==2.5.1
- transformers==4.56.1
- opencv-python==4.8.1.78
- google-cloud-vision==3.4.5

If you don't need visual detection, you can remove these from `requirements.txt`.

---

## Known Limitations

### Current Implementation
1. **In-memory cache**: Won't persist across restarts. For production, consider Redis.
2. **No authentication**: Add API keys or OAuth for production.
3. **No rate limiting**: Add rate limiting for production.
4. **Single-threaded**: Use Gunicorn workers for production.

### Recommendations for Production

**Add Authentication:**
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/predict")
async def predict(
    request: PredictRequest,
    api_key: str = Security(api_key_header)
):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403)
    # ... rest of code
```

**Add Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(...):
    # ... code
```

**Use Redis Cache:**
```python
import redis
from functools import lru_cache

redis_client = redis.Redis(host='localhost', port=6379)

def get_cached_prediction(text):
    key = hashlib.md5(text.encode()).hexdigest()
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None
```

**Use Gunicorn Workers:**
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## Environment Variables

### Required
```bash
# None - system works with defaults
```

### Recommended
```bash
HOST=0.0.0.0
PORT=8000
MODEL_DIR=models
CACHE_MAX_SIZE=1000
CACHE_TTL=3600
```

### Optional (for visual detection)
```bash
GOOGLE_APPLICATION_CREDENTIALS=google-vision-credentials.json
```

### Production
```bash
# Add these for production
API_KEY=your-secret-api-key
ALLOWED_ORIGINS=https://your-frontend.com
LOG_LEVEL=INFO
ENABLE_RATE_LIMIT=true
RATE_LIMIT=100/minute
```

---

## Troubleshooting Common Issues

### Issue: Models not loading
**Solution:**
```bash
# Check files exist
ls -la models/

# Verify format
python -c "import joblib; print(joblib.load('models/random_forest.joblib'))"

# Check Python version (3.8+ required)
python --version
```

### Issue: Import errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install fastapi uvicorn scikit-learn lightgbm xgboost lime nltk
```

### Issue: NLTK data not found
**Solution:**
```bash
# Run setup
python setup.py

# Or manual download
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Issue: Port already in use
**Solution:**
```bash
# Change port in .env
echo "PORT=5000" >> .env

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Issue: Visual detection fails
**Solution:**
```bash
# Check credentials exist
ls google-vision-credentials.json

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=google-vision-credentials.json

# Or disable visual detection endpoint
# Comment out lines 220-273 in src/api/routes.py
```

---

## Performance Tuning

### Increase Cache Size
Edit `.env`:
```bash
CACHE_MAX_SIZE=5000
CACHE_TTL=7200
```

### Use Multiple Workers
```bash
# With uvicorn
uvicorn main:app --workers 4

# With gunicorn (recommended)
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### Optimize Model Loading
Models are loaded once at startup using singleton pattern. No changes needed.

### Database for Persistent Cache
Replace in-memory cache with PostgreSQL or Redis for persistent caching.

---

## Security Checklist

Before deploying to production:

- [ ] Add API authentication
- [ ] Implement rate limiting
- [ ] Set specific CORS origins (not "*")
- [ ] Add input sanitization
- [ ] Enable HTTPS/SSL
- [ ] Set up logging
- [ ] Configure firewalls
- [ ] Use environment variables for secrets
- [ ] Implement request validation
- [ ] Add security headers
- [ ] Set up monitoring
- [ ] Configure backups

See `DEPLOYMENT.md` for detailed security setup.

---

## Next Steps

1. ✅ **Add your models** to `models/` directory
2. ✅ **Run setup**: `python setup.py`
3. ✅ **Start server**: `python main.py`
4. ✅ **Test API**: `python test_api.py`
5. ✅ **Read docs**: `http://localhost:8000/docs`
6. ⚠️ **Add authentication** for production
7. ⚠️ **Configure rate limiting** for production
8. ⚠️ **Set up monitoring** for production
9. ⚠️ **Deploy** using Docker or cloud platform

---

## Support

If you encounter issues:

1. Check `QUICK_REFERENCE.md` → Troubleshooting section
2. Review `COMPLETE.md` → Implementation details
3. Read `API_DOCUMENTATION.md` → Endpoint reference
4. Check logs for error messages
5. Verify all requirements are installed
6. Ensure models are in correct format

---

**Remember: The system is production-ready but should be hardened with authentication, rate limiting, and monitoring before public deployment!**
