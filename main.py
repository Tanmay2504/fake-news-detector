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


# System Health Check
def check_system_health():
    """
    Comprehensive system health check with colorful console output
    Returns dict with component status
    """
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    
    health_status = {
        "overall": True,
        "components": {}
    }
    
    def print_header(text):
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"{Fore.CYAN}{Style.BRIGHT}  {text}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}")
    
    def print_success(text):
        print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")
    
    def print_warning(text):
        print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")
    
    def print_error(text):
        print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")
    
    def print_info(text):
        print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")
    
    print_header("FAKE NEWS DETECTION API - SYSTEM HEALTH CHECK")
    print(f"{Fore.WHITE}Date: December 13, 2025{Style.RESET_ALL}")
    
    # Check 1: Python Dependencies
    print_header("1. CHECKING PYTHON DEPENDENCIES")
    required_packages = {
        'fastapi': 'FastAPI Framework',
        'uvicorn': 'ASGI Server',
        'scikit-learn': 'Machine Learning',
        'joblib': 'Model Persistence',
        'lime': 'Explainability',
        'transformers': 'Deep Learning',
        'torch': 'PyTorch',
        'PIL': 'Image Processing',
        'cv2': 'Computer Vision',
        'google.cloud.vision': 'Google Vision API'
    }
    
    missing_packages = []
    for package, description in required_packages.items():
        try:
            if package == 'PIL':
                from PIL import Image
            elif package == 'cv2':
                import cv2
            elif package == 'google.cloud.vision':
                from google.cloud import vision
            else:
                __import__(package)
            print_success(f"{description:<25} ({package})")
            health_status["components"][package] = True
        except ImportError:
            print_warning(f"{description:<25} ({package}) - NOT INSTALLED")
            missing_packages.append(package)
            health_status["components"][package] = False
            health_status["overall"] = False
    
    # Check 2: Model Files
    print_header("2. CHECKING ML MODELS")
    from pathlib import Path
    import joblib
    
    models_dir = Path("models")
    model_files = {
        'Random Forest': 'random_forest.joblib',
        'LightGBM': 'lightgbm.joblib',
        'XGBoost': 'xgboost.joblib'
    }
    
    loaded_models = 0
    total_models = len(model_files)
    
    for model_name, filename in model_files.items():
        model_path = models_dir / filename
        if model_path.exists():
            try:
                model = joblib.load(model_path)
                size_mb = model_path.stat().st_size / (1024 * 1024)
                print_success(f"{model_name:<20} loaded ({size_mb:.1f} MB)")
                loaded_models += 1
                health_status["components"][model_name] = True
            except Exception as e:
                print_error(f"{model_name:<20} failed to load: {str(e)[:40]}")
                health_status["components"][model_name] = False
                health_status["overall"] = False
        else:
            print_warning(f"{model_name:<20} not found at {model_path}")
            health_status["components"][model_name] = False
    
    if loaded_models == total_models:
        print_info(f"Ensemble ready: {loaded_models}/{total_models} models loaded")
    elif loaded_models > 0:
        print_warning(f"Partial ensemble: {loaded_models}/{total_models} models loaded")
    else:
        print_error(f"No models loaded! Train models first: python train_models.py")
        health_status["overall"] = False
    
    # Check 3: Datasets
    print_header("3. CHECKING DATASETS")
    dataset_files = [
        'datasets/train.csv',
        'datasets/test.csv',
        'datasets/Constraint_Train.csv',
        'datasets/Constraint_Test.csv'
    ]
    
    found_datasets = 0
    for dataset in dataset_files:
        if os.path.exists(dataset):
            size_mb = os.path.getsize(dataset) / (1024 * 1024)
            print_success(f"{dataset:<40} ({size_mb:.1f} MB)")
            found_datasets += 1
        else:
            print_warning(f"{dataset:<40} not found")
    
    health_status["components"]["datasets"] = found_datasets > 0
    if found_datasets > 0:
        print_info(f"Found {found_datasets} dataset files")
    
    # Check 4: Google Cloud Vision
    print_header("4. CHECKING GOOGLE CLOUD VISION")
    google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'google-vision-credentials.json')
    
    if os.path.exists(google_creds):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_creds
        print_success(f"Credentials file found: {google_creds}")
        
        try:
            from google.cloud import vision
            client = vision.ImageAnnotatorClient()
            print_success("Google Vision API client initialized")
            print_warning("Note: API may require billing to be enabled")
            health_status["components"]["google_vision"] = True
        except Exception as e:
            print_warning(f"Google Vision API: {str(e)[:60]}")
            print_info("Falling back to local models (BLIP, CLIP, CNN)")
            health_status["components"]["google_vision"] = False
    else:
        print_warning(f"Credentials not found: {google_creds}")
        print_info("Using local models only (BLIP, CLIP, CNN)")
        health_status["components"]["google_vision"] = False
    
    # Check 5: Port Availability
    print_header("5. CHECKING PORT AVAILABILITY")
    import socket
    
    def is_port_available(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except OSError:
            return False
    
    if is_port_available(8000):
        print_success("Port 8000 is available for backend")
        health_status["components"]["port_8000"] = True
    else:
        print_warning("Port 8000 is already in use")
        print_info("Backend will attempt to use this port")
        health_status["components"]["port_8000"] = False
    
    # Check 6: File Structure
    print_header("6. CHECKING PROJECT STRUCTURE")
    required_dirs = ['src', 'src/api', 'src/ml', 'src/utils', 'models', 'datasets']
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print_success(f"Directory exists: {dir_path}/")
        else:
            print_error(f"Directory missing: {dir_path}/")
            health_status["overall"] = False
    
    # Final Summary
    print_header("SYSTEM STATUS SUMMARY")
    
    total_components = len([v for v in health_status["components"].values() if v is not False])
    total_checks = len(health_status["components"])
    
    if health_status["overall"] and loaded_models >= 2:
        print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT}  ✓ SYSTEM OPERATIONAL  {Style.RESET_ALL}")
        print(f"{Fore.GREEN}All critical components are working{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Components: {total_components}/{total_checks} OK{Style.RESET_ALL}")
    elif loaded_models > 0:
        print(f"\n{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT}  ⚠ SYSTEM PARTIALLY READY  {Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Some components have issues but system can run{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Components: {total_components}/{total_checks} OK{Style.RESET_ALL}")
    else:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT}  ✗ SYSTEM NOT READY  {Style.RESET_ALL}")
        print(f"{Fore.RED}Critical components missing - fix issues before running{Style.RESET_ALL}")
        print(f"{Fore.RED}Components: {total_components}/{total_checks} OK{Style.RESET_ALL}")
    
    if missing_packages:
        print(f"\n{Fore.YELLOW}Missing packages: {', '.join(missing_packages)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Install: pip install {' '.join(missing_packages)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    return health_status


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Initialize models and components on startup
    """
    # Run comprehensive health check
    health = check_system_health()
    
    # Load models
    from src.ml.ensemble import get_ensemble
    ensemble = get_ensemble()
    
    # Initialize cache
    from src.utils.cache import get_cache
    cache = get_cache()
    
    # Initialize explainer
    from src.ml.explainer import get_explainer
    if ensemble.loaded:
        explainer = get_explainer(ensemble)
    
    print(f"\n🚀 API Documentation: http://localhost:8000/docs")
    print(f"💚 Health Check Endpoint: http://localhost:8000/health")
    print(f"{'='*70}\n")


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
