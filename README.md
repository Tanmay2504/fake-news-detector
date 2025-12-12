<div align="center">

# Fake News Detection System - Backend

[![CI](https://github.com/Tanmay2504/fake-news-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/Tanmay2504/fake-news-detector/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

Production-ready fake news detection API using ensemble ML models and visual analysis.

## Features

- **Ensemble ML System**: Random Forest (60%) + LightGBM (20%) + XGBoost (20%)
- **Visual Detection**: AI-generated image detection, manipulation analysis, reverse image search
- **Rule-based Patterns**: Fake/real news indicators
- **LIME Explainability**: Word-level prediction explanations
- **In-memory Caching**: Fast repeated predictions
- **CORS Enabled**: Ready for frontend integration

## Quick Start

Clone and set up (Windows PowerShell):

```powershell
git clone https://github.com/Tanmay2504/fake-news-detector.git
cd fake-news-detector
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Download NLTK Data**
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

3. **Place Your Models**
```
models/
├── random_forest.joblib
├── lightgbm.joblib
├── xgboost.joblib
└── image_cnn.pth
```

4. **Set Up Google Cloud Vision**
- Place `google-vision-credentials.json` in project root

5. **Run Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Text Detection

**POST /predict**
```json
{
  "text": "Breaking news article...",
  "clean": true,
  "mode": "ensemble"
}
```

**POST /batch**
```json
{
  "texts": ["Article 1", "Article 2"],
  "clean": true
}
```

**POST /explain**
```json
{
  "text": "Article to explain",
  "num_features": 10
}
```

### Visual Detection

**POST /detect-visual**
- Multipart form with image file
- Optional: event, location, date context

### Health Check

**GET /health**
```json
{
  "ok": true,
  "ensemble_loaded": true,
  "models_available": ["random_forest", "lightgbm", "xgboost"]
}
```

## Project Structure

```
Fake News V2/
├── main.py                          # FastAPI application
├── requirements.txt                  # Dependencies
├── models/                          # Model files (.joblib, .pth)
├── src/
│   ├── api/
│   │   └── routes.py                # API endpoints
│   ├── ml/
│   │   ├── ensemble.py              # SmartEnsemble class
│   │   ├── rules.py                 # Rule-based detection
│   │   └── explainer.py             # LIME explainability
│   ├── utils/
│   │   ├── cache.py                 # Caching system
│   │   └── preprocessing.py         # Text cleaning
│   └── enhancements/
│       └── visual_detector.py       # Visual detection (existing)
└── google-vision-credentials.json   # GCloud credentials
```

## Architecture

### Ensemble Voting
- Random Forest: 60% weight (primary model)
- LightGBM: 20% weight (gradient boosting)
- XGBoost: 20% weight (gradient boosting)

### Pipeline Structure
Each model is a scikit-learn Pipeline:
```python
Pipeline([
    ('tfidf', TfidfVectorizer(...)),
    ('clf', Classifier(...))
])
```

### Visual Detection
- CNN classifier (95.72% accuracy)
- CLIP AI generation detection
- ELA manipulation heatmaps
- BLIP content analysis
- Google Cloud Vision labels
- Reverse image search verification

## License

MIT
