"""
Setup script to prepare the environment
"""
import os
import sys


def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("Downloading NLTK data...")
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        print("✓ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"⚠ Error downloading NLTK data: {e}")
        return False


def check_models():
    """Check if model files exist"""
    model_dir = "models"
    required_models = [
        "random_forest.joblib",
        "lightgbm.joblib",
        "xgboost.joblib"
    ]
    
    print("\nChecking for model files...")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"✓ Created {model_dir}/ directory")
    
    missing_models = []
    for model in required_models:
        model_path = os.path.join(model_dir, model)
        if os.path.exists(model_path):
            print(f"✓ Found {model}")
        else:
            print(f"✗ Missing {model}")
            missing_models.append(model)
    
    if missing_models:
        print("\n⚠ Please place your trained models in the models/ directory:")
        for model in missing_models:
            print(f"  - models/{model}")
        return False
    else:
        print("\n✓ All model files found")
        return True


def check_google_credentials():
    """Check if Google Cloud credentials exist"""
    creds_file = "google-vision-credentials.json"
    print(f"\nChecking for Google Cloud credentials...")
    
    if os.path.exists(creds_file):
        print(f"✓ Found {creds_file}")
        return True
    else:
        print(f"⚠ Missing {creds_file}")
        print("  Visual detection features will not work without credentials")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env from .env.example")
        else:
            print("⚠ No .env.example found to copy")
    else:
        print("✓ .env file already exists")


def main():
    """Run setup checks"""
    print("=" * 60)
    print("Fake News Detection API - Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Create .env
    create_env_file()
    
    # Download NLTK data
    download_nltk_data()
    
    # Check models
    models_ok = check_models()
    
    # Check Google credentials
    creds_ok = check_google_credentials()
    
    print("\n" + "=" * 60)
    if models_ok:
        print("✓ Setup complete! You can now run the server:")
        print("  python main.py")
        print("  or")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("⚠ Setup incomplete - please add model files")
    print("=" * 60)
    
    return models_ok


if __name__ == "__main__":
    main()
