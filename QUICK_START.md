# Quick Start Guide

## 🚀 Easiest Way to Run

### Option 1: Run Everything (Recommended)
**Double-click:** `start-all.bat`

This will:
- ✅ Start the backend server (port 8000)
- ✅ Start the frontend server (port 5173)
- ✅ Open both in separate terminal windows
- ✅ Automatically check dependencies

Then visit: **http://localhost:5173**

---

### Option 2: Run Backend Only
**Double-click:** `start-backend.bat`

Backend will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

### Option 3: Run Frontend Only
**Double-click:** `start-frontend.bat`

Frontend will be available at:
- App: http://localhost:5173

*(Requires backend to be running separately)*

---

## 📋 Manual Commands (Alternative)

### Backend:
```powershell
cd "C:\Users\Tanmay Patel\Desktop\Fake News V2"
.venv\Scripts\python.exe main.py
```

### Frontend:
```powershell
cd "C:\Users\Tanmay Patel\Desktop\Fake News V2\frontend"
npm run dev
```

---

## 🛠️ First Time Setup

### Backend Setup:
```powershell
cd "C:\Users\Tanmay Patel\Desktop\Fake News V2"
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python.exe train_models.py
```

### Frontend Setup:
```powershell
cd "C:\Users\Tanmay Patel\Desktop\Fake News V2\frontend"
npm install
```

---

## 🎯 What Each Server Does

### Backend (Port 8000)
- ML models for text prediction
- Visual detection with AI models
- LIME explainability
- API endpoints

### Frontend (Port 5173)
- Dashboard
- Text Analysis
- Visual Detection
- Detailed Analysis with model breakdowns

---

## 🔧 Troubleshooting

### Backend won't start?
1. Make sure virtual environment exists: `.venv` folder should be present
2. Install dependencies: `.venv\Scripts\pip install -r requirements.txt`
3. Train models: `.venv\Scripts\python.exe train_models.py`

### Frontend won't start?
1. Make sure Node.js is installed
2. Install dependencies: `cd frontend && npm install`
3. Check if port 5173 is available

### Models not loading?
Run the training script:
```powershell
.venv\Scripts\python.exe train_models.py
```

---

## 📊 Default Ports

| Service  | Port | URL |
|----------|------|-----|
| Backend  | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| Frontend | 5173 | http://localhost:5173 |

---

## ⚡ Tips

- **Stop servers**: Press `Ctrl+C` in the terminal window
- **Restart**: Close terminal windows and double-click the `.bat` file again
- **Check status**: Backend shows "Application startup complete" when ready
- **API testing**: Visit http://localhost:8000/docs for interactive API documentation

---

## 🎨 Features Available

✅ **Dashboard** - Overview with stats and features  
✅ **Text Analysis** - Quick fake news detection for articles  
✅ **Visual Detection** - AI-powered image manipulation detection  
✅ **Detailed Analysis** - In-depth breakdown with:
  - Individual model predictions (Random Forest, LightGBM, XGBoost)
  - LIME word-level explanations
  - Text statistics
  - Rule-based pattern analysis

---

## 📝 Notes

- Backend must be running for frontend to work properly
- First startup may take longer as models load
- Google Cloud Vision requires billing (optional - system works without it)
- Models are pre-trained with 90.94% accuracy
