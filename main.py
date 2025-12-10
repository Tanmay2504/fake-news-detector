"""
Fake News Detection API - Main Application
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Import routes
from src.api.routes import router

# Create FastAPI app
app = FastAPI(
    title="Fake News Detection API",
    description="Production-ready fake news detection using ensemble ML models and visual analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Initialize models and components on startup
    """
    print("=" * 60)
    print("Starting Fake News Detection API...")
    print("=" * 60)
    
    # Set Google Cloud credentials
    google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'google-vision-credentials.json')
    if os.path.exists(google_creds):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_creds
        print(f"✓ Google Cloud credentials: {google_creds}")
    else:
        print(f"⚠ Google Cloud credentials not found: {google_creds}")
    
    # Load models
    from src.ml.ensemble import get_ensemble
    ensemble = get_ensemble()
    
    if ensemble.loaded:
        print(f"✓ Loaded {len(ensemble.models)} models successfully")
        for model_name in ensemble.models.keys():
            weight = ensemble.weights.get(model_name, 0)
            print(f"  - {model_name}: {weight*100}% weight")
    else:
        print("⚠ Warning: No models loaded")
        print("  Place your trained models in the 'models/' directory:")
        print("  - models/random_forest.joblib")
        print("  - models/lightgbm.joblib")
        print("  - models/xgboost.joblib")
    
    # Initialize cache
    from src.utils.cache import get_cache
    cache = get_cache()
    print(f"✓ Cache initialized (max size: {cache.max_size})")
    
    # Initialize explainer
    from src.ml.explainer import get_explainer
    if ensemble.loaded:
        explainer = get_explainer(ensemble)
        if explainer:
            print("✓ LIME explainer initialized")
    
    print("=" * 60)
    print("API ready! Visit http://localhost:8000/docs for documentation")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on shutdown
    """
    print("\nShutting down Fake News Detection API...")


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    # Run server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
