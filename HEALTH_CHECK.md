# System Health Check & Monitoring

## 🎯 Overview

The backend now includes a **comprehensive health monitoring system** that automatically checks all components every time you start the server.

## 🚀 Quick Start

### Option 1: Use the Health Monitor Script (Recommended)

```powershell
start-backend-with-health.bat
```

This will:
- ✅ Check if Python is installed
- ✅ Run comprehensive health check on startup
- ✅ Display colorful status of all components
- ✅ Start the backend server
- ✅ Keep it running with auto-reload

### Option 2: Manual Start

```powershell
python -m uvicorn main:app --reload
```

---

## 📊 What Gets Checked on Startup

The health check system validates **6 critical areas**:

### 1. **Python Dependencies** ✅
Checks if all required packages are installed:
- FastAPI, Uvicorn (API framework)
- scikit-learn, joblib (Machine Learning)
- LIME (Explainability)
- Transformers, PyTorch (Deep Learning)
- PIL, OpenCV (Image Processing)
- Google Cloud Vision (Optional)

### 2. **ML Models** 🤖
Verifies that trained models exist and load correctly:
- Random Forest (60% weight)
- LightGBM (20% weight)
- XGBoost (20% weight)

Shows file size and loading status for each model.

### 3. **Datasets** 📁
Checks if training/test datasets are available:
- datasets/train.csv
- datasets/test.csv
- datasets/Constraint_Train.csv
- datasets/Constraint_Test.csv

### 4. **Google Cloud Vision API** 👁️
Verifies credentials file and API availability:
- Checks for google-vision-credentials.json
- Tests API client initialization
- Falls back to local models if unavailable

### 5. **Port Availability** 🔌
Ensures port 8000 is available for the backend.

### 6. **Project Structure** 📂
Validates all required directories exist:
- src/api, src/ml, src/utils
- models/, datasets/

---

## 🎨 Color-Coded Output

The health check uses **color-coded console output**:

- 🟢 **Green (✓)** - Component is working correctly
- 🟡 **Yellow (⚠)** - Warning, component has minor issues
- 🔴 **Red (✗)** - Error, critical component missing
- 🔵 **Blue (ℹ)** - Informational message

---

## 📊 Sample Output

```
======================================================================
  FAKE NEWS DETECTION API - SYSTEM HEALTH CHECK
======================================================================
Date: December 13, 2025

======================================================================
  1. CHECKING PYTHON DEPENDENCIES
======================================================================
✓ FastAPI Framework       (fastapi)
✓ ASGI Server            (uvicorn)
✓ Machine Learning       (scikit-learn)
✓ Model Persistence      (joblib)
✓ Explainability        (lime)
✓ Deep Learning         (transformers)
✓ PyTorch              (torch)
✓ Image Processing     (PIL)
✓ Computer Vision      (cv2)
⚠ Google Vision API    (google.cloud.vision) - NOT INSTALLED

======================================================================
  2. CHECKING ML MODELS
======================================================================
✓ Random Forest         loaded (15.2 MB)
✓ LightGBM             loaded (3.8 MB)
✓ XGBoost              loaded (2.1 MB)
ℹ Ensemble ready: 3/3 models loaded

======================================================================
  3. CHECKING DATASETS
======================================================================
✓ datasets/train.csv                      (12.5 MB)
✓ datasets/test.csv                       (3.2 MB)
⚠ datasets/Constraint_Train.csv           not found
⚠ datasets/Constraint_Test.csv            not found
ℹ Found 2 dataset files

======================================================================
  4. CHECKING GOOGLE CLOUD VISION
======================================================================
✓ Credentials file found: google-vision-credentials.json
⚠ Google Vision API: BILLING_DISABLED
ℹ Falling back to local models (BLIP, CLIP, CNN)

======================================================================
  5. CHECKING PORT AVAILABILITY
======================================================================
✓ Port 8000 is available for backend

======================================================================
  6. CHECKING PROJECT STRUCTURE
======================================================================
✓ Directory exists: src/
✓ Directory exists: src/api/
✓ Directory exists: src/ml/
✓ Directory exists: src/utils/
✓ Directory exists: models/
✓ Directory exists: datasets/

======================================================================
  SYSTEM STATUS SUMMARY
======================================================================

  ✓ SYSTEM OPERATIONAL  
All critical components are working
Components: 18/20 OK

======================================================================

🚀 API Documentation: http://localhost:8000/docs
💚 Health Check Endpoint: http://localhost:8000/health
======================================================================
```

---

## 🌐 Health Check API Endpoint

### GET /health

Returns detailed JSON with system status:

```bash
# Using curl
curl http://localhost:8000/health

# Using PowerShell
(Invoke-WebRequest http://localhost:8000/health).Content | ConvertFrom-Json
```

**Response Example:**
```json
{
  "ok": true,
  "status": "OPERATIONAL",
  "ensemble_loaded": true,
  "models_available": ["Random Forest", "LightGBM", "XGBoost"],
  "models_count": 3,
  "model_dir": "models",
  "cache_stats": {
    "size": 15,
    "max_size": 1000,
    "hits": 42,
    "misses": 58
  },
  "dependencies": {
    "fastapi": true,
    "scikit-learn": true,
    "lime": true,
    "transformers": true,
    "torch": true
  },
  "datasets_found": 2,
  "google_vision_available": false
}
```

### Status Values

- **`OPERATIONAL`** - All systems working (3/3 models loaded)
- **`PARTIAL`** - Some issues but functional (1-2 models loaded)
- **`NOT_READY`** - Critical components missing (0 models)
- **`ERROR`** - System error occurred

---

## 🔍 Using the Health Check

### For Exhibition Demo:

**Before the exhibition:**
```powershell
# Start backend
start-backend-with-health.bat

# Check health
curl http://localhost:8000/health
```

Look for:
- ✅ `"status": "OPERATIONAL"` or `"PARTIAL"`
- ✅ `"models_count": 3` (all models loaded)
- ✅ `"ok": true`

### For Development:

The health check runs automatically every time you start the backend, showing you exactly what's working and what needs attention.

### For Testing:

The `quick_test.py` script also checks the /health endpoint:

```powershell
python quick_test.py
```

---

## ⚙️ Troubleshooting

### If Health Check Shows Errors:

**Missing Dependencies:**
```
✗ Machine Learning (scikit-learn) - NOT INSTALLED
```
**Fix:**
```powershell
pip install -r requirements.txt
```

**Missing Models:**
```
✗ Random Forest not found at models/random_forest.joblib
```
**Fix:**
```powershell
python train_models.py
```

**Port In Use:**
```
⚠ Port 8000 is already in use
```
**Fix:**
- Stop other backend instance
- Or use different port: `uvicorn main:app --port 8001`

**Google Vision Issues:**
```
⚠ Google Vision API: BILLING_DISABLED
```
**Fix:**
- Enable billing in Google Cloud Console
- Or ignore (system uses local models)

---

## 📝 Integration with Tests

The health check integrates with your test suite:

```powershell
# Run all tests (includes health check)
python quick_test.py

# Test specific endpoint
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

---

## 🎯 Benefits

1. **Instant Status** - See what's working the moment backend starts
2. **Debugging** - Quickly identify missing components
3. **Exhibition Ready** - Verify system health before demos
4. **API Monitoring** - Check /health endpoint anytime
5. **Professional** - Color-coded, detailed diagnostics

---

## 💡 Tips

**For Exhibition:**
- Start backend 5 minutes early
- Check for green "SYSTEM OPERATIONAL" message
- Screenshot the health check for backup reference
- Have /health endpoint open in browser

**For Development:**
- Use health check to verify model changes
- Monitor cache statistics via /health
- Check dependencies after pip install
- Verify datasets are found

---

## 🚀 Next Steps

1. **Start the backend:**
   ```powershell
   start-backend-with-health.bat
   ```

2. **Verify health:**
   - Look for "SYSTEM OPERATIONAL" in console
   - Visit http://localhost:8000/health

3. **Start frontend:**
   ```powershell
   cd frontend
   npm run dev
   ```

4. **Run tests:**
   ```powershell
   python quick_test.py
   ```

**You're ready for the exhibition! 🎉**
