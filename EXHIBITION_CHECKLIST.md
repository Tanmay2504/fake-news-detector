# 🎯 Exhibition Checklist - Tomorrow, December 14, 2025

## ✅ Before You Leave Home

### Hardware:
- [ ] Laptop fully charged
- [ ] Laptop charger packed
- [ ] Backup power bank (if available)
- [ ] Mouse (optional, for better demo)
- [ ] USB drive with project backup

### Software:
- [ ] Run quick test: `python quick_test.py`
- [ ] Verify both servers start: `start-all.bat`
- [ ] Test one complete workflow (text + image)
- [ ] Take screenshots of successful tests

---

## 🚀 Exhibition Setup (15 minutes before)

### Step 1: Start Backend (2 minutes)
```powershell
start-backend-with-health.bat
```
**Wait for:** Green checkmarks and "SYSTEM OPERATIONAL" message

### Step 2: Start Frontend (1 minute)
```powershell
start-frontend.bat
```
**Wait for:** "Local: http://localhost:5173"

### Step 3: Open Browser (30 seconds)
- Navigate to: `http://localhost:5173`
- Verify all 3 tabs load (Dashboard, Text Analysis, Visual Detection)

### Step 4: Prepare Demo Data (1 minute)
- Open `EXHIBITION_DEMO_DATA.md` on second monitor or phone
- Download 2-3 AI faces from: https://thispersondoesnotexist.com
- Download 2-3 real photos from: https://unsplash.com

### Step 5: Test Run (5 minutes)
- Test Example 1: Fake news text
- Test Example 2: Real news text
- Upload AI-generated image
- Upload real photo
- Verify everything works

---

## 🎬 4-Minute Demo Script

### Opening (30 seconds)
**Say:** "This is a multi-modal fake news detection system that combines ensemble machine learning with computer vision to identify misinformation in both text and images."

**Show:** Dashboard tab with feature overview

### Text Analysis Demo (2 minutes)

#### Demo 1 - Fake News (1 minute)
1. Switch to "Text Analysis" tab
2. Paste Example 1 from `EXHIBITION_DEMO_DATA.md`
3. Click "Analyze"
4. **Point out:**
   - "This article is 92% likely to be FAKE"
   - "See the red highlighted words? Those are fake indicators"
   - "LIME shows WHY: words like 'BREAKING', 'shocking', 'you won't believe'"
   - "Three ML models agree: Random Forest 88%, LightGBM 85%, XGBoost 90%"

#### Demo 2 - Real News (1 minute)
1. Clear the text
2. Paste Example 3 (real news)
3. Click "Analyze"
4. **Point out:**
   - "This article is 88% likely to be REAL"
   - "Green highlights show credibility markers"
   - "Words like 'according to', 'reported', 'confirmed' indicate reliable sourcing"

### Visual Detection Demo (1 minute)

#### Demo 3 - AI-Generated Image
1. Switch to "Visual Detection" tab
2. Upload AI-generated face
3. **Point out:**
   - "SUSPICIOUS verdict - 85% likely AI-generated"
   - "CLIP model detects StyleGAN/DALL-E patterns"
   - "Face detection: 1 face found"
   - "BLIP describes what's in the image"

#### Demo 4 - Real Photo (Optional, if time)
1. Upload real photo
2. Show "AUTHENTIC" verdict

### Closing (30 seconds)
**Say:** "The system achieves 89.7% accuracy on 387,000 training samples. It combines 6 AI models with explainable predictions, making it useful for fact-checkers, journalists, and social media platforms."

---

## 💡 Key Talking Points

### When asked about accuracy:
"The ensemble achieves **89.7% accuracy** on test data, outperforming individual models."

### When asked about how it works:
"We use **weighted ensemble learning** - Random Forest (60%), LightGBM (20%), and XGBoost (20%) vote together. For images, we combine CNN, CLIP, and BLIP models."

### When asked about LIME:
"LIME provides **word-level explanations** - it shows which specific words influenced the prediction. Red = fake indicators, Green = real indicators."

### When asked about data:
"Trained on **387,000+ articles** from WELFake, Constraint, and other datasets. Visual models trained on CIFAKE with 120,000 images."

### When asked about real-world use:
"Perfect for **fact-checkers and journalists** who need to verify news quickly. Processing takes only 2-3 seconds per article."

### When asked about technology:
"**Backend:** FastAPI with Python, scikit-learn, LightGBM, XGBoost  
**Frontend:** React with TypeScript  
**Models:** 3 ML models + 3 computer vision models  
**Explainability:** LIME for transparency"

---

## 🛠️ Troubleshooting

### Backend won't start:
```powershell
# Check if port 8000 is busy
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /F /PID <PID>

# Restart
start-backend-with-health.bat
```

### Frontend won't start:
```powershell
# Navigate to frontend
cd frontend

# Install dependencies (if needed)
npm install

# Start again
npm run dev
```

### Models not loading:
- Check `models/` folder has 3 files:
  - random_forest.joblib
  - lightgbm.joblib
  - xgboost.joblib
- Check health check shows green checkmarks for models

### "Module not found" errors:
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

### Demo data not working:
- Copy from `EXHIBITION_DEMO_DATA.md`
- Use manual examples:
  - **Fake:** "BREAKING: You won't believe what scientists discovered!"
  - **Real:** "According to Reuters, the government announced new policies today."

---

## 📱 Emergency Backup Plan

### If Backend Crashes:
1. Show health check screenshot
2. Show quick_test.py results screenshot
3. Walk through code in `main.py` and `src/`
4. Explain architecture from `PROJECT_OVERVIEW.md`

### If Frontend Crashes:
1. Show screenshots of working UI
2. Demonstrate backend directly: http://localhost:8000/docs
3. Test API with curl or browser

### If Everything Fails:
1. Show `PROJECT_OVERVIEW.md` with diagrams
2. Explain architecture and approach
3. Show code structure
4. Discuss results and accuracy
5. Walk through GitHub repository

---

## 📊 Quick Stats to Memorize

| Metric | Value |
|--------|-------|
| Text Accuracy | 89.7% |
| Training Samples | 387,000+ |
| Processing Time | 2-3 seconds |
| Models Used | 6 (3 text + 3 visual) |
| Tech Stack | React + FastAPI |
| Lines of Code | 5,000+ |

---

## ✅ Final Checklist

**10 minutes before exhibition:**
- [ ] Both servers running
- [ ] Browser open to http://localhost:5173
- [ ] Demo data ready
- [ ] Screenshots taken
- [ ] Laptop plugged in
- [ ] Confident and ready!

**Remember:**
- ✅ Speak clearly and slowly
- ✅ Point at screen while explaining
- ✅ Let predictions load fully before talking
- ✅ Smile and make eye contact
- ✅ Be ready for questions
- ✅ Have fun! You built something amazing!

---

## 🎉 You Got This!

You've built a **professional-grade AI system** that combines:
- ✅ Ensemble machine learning
- ✅ Computer vision
- ✅ Explainable AI
- ✅ Full-stack development
- ✅ Production-ready deployment

**This is impressive work. Own it. Be proud. Good luck tomorrow! 🚀**
