# Complete Setup Guide - Fake News Detector

## Backend + Frontend Full Stack Setup

### Prerequisites

1. **Python 3.13**
2. **Node.js 18+** and npm
3. **Git**

### Step 1: Clone and Setup Backend

```powershell
git clone https://github.com/Tanmay2504/fake-news-detector.git
cd fake-news-detector

# Create Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

### Step 2: Setup Frontend

```powershell
cd frontend
npm install
```

### Step 3: Run Both Services

**Terminal 1 - Backend API:**
```powershell
# In project root
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend Dev Server:**
```powershell
# In frontend folder
cd frontend
npm run dev
```

### Step 4: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Features

### Frontend
- ✨ Animated landing page with framer-motion
- 📝 Text analysis interface
- 📊 Real-time confidence scores
- 🎨 Dark mode support
- 📱 Responsive design

### Backend
- 🤖 Ensemble ML (Random Forest + LightGBM + XGBoost)
- 🖼️ Visual fake news detection
- 📈 LIME explainability
- 🔍 Rule-based pattern detection
- ⚡ In-memory caching

## Production Build

### Frontend
```powershell
cd frontend
npm run build
# Output in frontend/dist/
```

### Backend
```powershell
# Use Docker or deploy to cloud
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

Create `.env` file in project root:

```env
GOOGLE_APPLICATION_CREDENTIALS=google-vision-credentials.json
```

## Troubleshooting

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check Vite proxy config in `frontend/vite.config.ts`

### Python module errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### NLTK data missing
- Run download command again:
  ```powershell
  python -c "import nltk; nltk.download('all')"
  ```

## License

MIT License - see LICENSE file
