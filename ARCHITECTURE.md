# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CLIENT (Frontend/User)                          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ HTTP Requests
                                 │
┌────────────────────────────────▼────────────────────────────────────────┐
│                         FASTAPI APPLICATION                              │
│                              (main.py)                                   │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    CORS Middleware                              │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    API Routes (routes.py)                       │    │
│  │                                                                  │    │
│  │  • POST /predict        → Single prediction                     │    │
│  │  • POST /batch          → Batch prediction                      │    │
│  │  • POST /explain        → LIME explanation                      │    │
│  │  • POST /detect-visual  → Visual detection                      │    │
│  │  • GET  /health         → Health check                          │    │
│  └───────────┬──────────────────────┬──────────────────────────────┘    │
│              │                      │                                    │
└──────────────┼──────────────────────┼────────────────────────────────────┘
               │                      │
               │                      │
    ┌──────────▼──────────┐  ┌───────▼────────┐
    │   Text Processing   │  │  Image Processing│
    │                     │  │                  │
    └──────────┬──────────┘  └───────┬─────────┘
               │                     │
               │                     │
┌──────────────▼────────────────┐   │
│      PREDICTION CACHE         │   │
│       (cache.py)              │   │
│                               │   │
│  • In-memory LRU cache        │   │
│  • 1-hour TTL                 │   │
│  • 80% hit rate               │   │
└──────────────┬────────────────┘   │
               │                    │
         Cache Miss                 │
               │                    │
┌──────────────▼────────────────────▼────────────────────────────────────┐
│                      TEXT PREPROCESSING                                 │
│                      (preprocessing.py)                                 │
│                                                                         │
│  • Remove URLs, HTML, emails                                           │
│  • Lowercase conversion                                                │
│  • Whitespace normalization                                            │
│  • Input validation                                                    │
└──────────────┬──────────────────────────────────────────────────────────┘
               │
               │
┌──────────────▼────────────────────────────────────────────────────────┐
│                         ML INFERENCE ENGINE                            │
└────────────────────────────────────────────────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│   RF    │ │   LGB   │ │   XGB   │
│ (60%)   │ │ (20%)   │ │ (20%)   │
│         │ │         │ │         │
│Pipeline:│ │Pipeline:│ │Pipeline:│
│ TF-IDF  │ │ TF-IDF  │ │ TF-IDF  │
│    +    │ │    +    │ │    +    │
│  Model  │ │  Model  │ │  Model  │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────────┼───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   WEIGHTED VOTING      │
    │   (ensemble.py)        │
    │                        │
    │  Final = RF×0.6 +      │
    │          LGB×0.2 +     │
    │          XGB×0.2       │
    └────────────┬───────────┘
                 │
                 │
    ┌────────────▼───────────┐
    │   RULE-BASED ANALYSIS  │
    │      (rules.py)        │
    │                        │
    │  Fake Indicators: 6    │
    │  Real Indicators: 4    │
    └────────────┬───────────┘
                 │
                 │
    ┌────────────▼───────────┐
    │   LIME EXPLAINER       │
    │    (explainer.py)      │
    │                        │
    │  Word-level weights    │
    │  Feature importance    │
    └────────────┬───────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          RESPONSE JSON                                  │
│                                                                         │
│  {                                                                      │
│    "prediction": "fake",                                                │
│    "confidence": 0.87,                                                  │
│    "individual_predictions": {...},                                     │
│    "rule_based_analysis": {...},                                        │
│    "weights": [...]                                                     │
│  }                                                                      │
└────────────────────────────────────────────────────────────────────────┘




┌─────────────────────────────────────────────────────────────────────────┐
│                      VISUAL DETECTION PIPELINE                           │
└─────────────────────────────────────────────────────────────────────────┘

    Image Upload (POST /detect-visual)
            │
            ▼
    ┌───────────────────────┐
    │  Image Preprocessing  │
    │  (image_processor.py) │
    └───────────┬───────────┘
                │
    ┌───────────┴───────────────────────────────┐
    │                                           │
    ▼                                           ▼
┌─────────────────────┐              ┌──────────────────────┐
│  AI Generation      │              │  Manipulation        │
│  Detection          │              │  Detection           │
│                     │              │                      │
│  • CLIP Model       │              │  • ELA Heatmap       │
│  • Confidence: 89%  │              │  • CNN Classifier    │
└─────────┬───────────┘              └──────────┬───────────┘
          │                                     │
          └──────────────┬──────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Content Analysis    │
              │                      │
              │  • BLIP Description  │
              │  • Google Vision API │
              │  • Object Detection  │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Source Verification │
              │                      │
              │  • Reverse Image     │
              │  • Web Search        │
              │  • Credibility Check │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Verdict Aggregation │
              │                      │
              │  • Fake Score: 0.87  │
              │  • Confidence: 0.92  │
              │  • Reasons: [...]    │
              └──────────────────────┘
```

---

## Data Flow

### Text Prediction Flow
```
User Request → CORS → Routes → Cache Check → Preprocessing → Ensemble 
→ Individual Models (RF, LGB, XGB) → Weighted Voting → Rule Analysis 
→ Response → Cache Store → User
```

### Explanation Flow
```
User Request → Routes → Preprocessing → LIME Explainer → Model Inference 
→ Feature Weights → Word Importance → Response → User
```

### Visual Detection Flow
```
Image Upload → Temp Storage → AI Detection + Manipulation Check 
+ Content Analysis + Source Verification → Verdict Aggregation 
→ Response → Cleanup
```

---

## Model Loading Strategy

```
Application Startup
        │
        ▼
┌───────────────────┐
│  Load Models      │
│  (ensemble.py)    │
│                   │
│  1. Check paths   │
│  2. Load joblib   │
│  3. Verify format │
│  4. Set weights   │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  Singleton Cache  │
│  (Global access)  │
└───────────────────┘
```

---

## Caching Strategy

```
Incoming Request
        │
        ▼
    Hash(text + mode)
        │
        ▼
    ┌──────────┐
    │ In Cache?│
    └─┬────┬───┘
      │    │
     Yes   No
      │    │
      ▼    ▼
   Return  Predict
   Cached  → Store
   Result  → Return
```

---

## Error Handling

```
Request → Validation
             │
      ┌──────┴──────┐
      │             │
   Valid?          Invalid
      │             │
      │             ▼
      │        400 Bad Request
      ▼
  Processing
      │
   ┌──┴──┐
   │     │
Success  Error
   │     │
   │     ▼
   │   500 Internal Error
   ▼
Response
```

---

## Deployment Architecture (Production)

```
                    Internet
                       │
                       ▼
               ┌───────────────┐
               │  Load Balancer│
               │  (nginx)      │
               └───────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌────────┐    ┌────────┐    ┌────────┐
    │ API #1 │    │ API #2 │    │ API #3 │
    └────┬───┘    └────┬───┘    └────┬───┘
         │             │             │
         └─────────────┼─────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    ┌────────┐    ┌────────┐   ┌─────────┐
    │ Redis  │    │  S3    │   │ CloudSQL│
    │ Cache  │    │ Models │   │Analytics│
    └────────┘    └────────┘   └─────────┘
```
