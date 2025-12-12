"""
SmartEnsemble: Ensemble fake news detection with Random Forest, LightGBM, and XGBoost
"""
import os
import joblib
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class SmartEnsemble:
    """
    Ensemble model that combines predictions from Random Forest, LightGBM, and XGBoost
    using weighted voting (RF=60%, LGB=20%, XGB=20%)
    """
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize ensemble by loading all three models
        
        Args:
            model_dir: Directory containing model files
        """
        self.model_dir = Path(model_dir)
        self.models = {}
        self.weights = {
            'random_forest': 0.6,
            'lightgbm': 0.2,
            'xgboost': 0.2
        }
        self.model_files = {
            'random_forest': 'random_forest.joblib',
            'lightgbm': 'lightgbm.joblib',
            'xgboost': 'xgboost.joblib'
        }
        self.loaded = False
        
    def load_models(self) -> bool:
        """
        Load all three models from disk
        
        Returns:
            True if all models loaded successfully, False otherwise
        """
        try:
            for model_name, filename in self.model_files.items():
                model_path = self.model_dir / filename
                
                if not model_path.exists():
                    print(f"Warning: Model file not found: {model_path}")
                    continue
                
                print(f"Loading {model_name} from {model_path}...")
                self.models[model_name] = joblib.load(model_path)
                print(f"[OK] {model_name} loaded successfully")
            
            if len(self.models) == 0:
                print("Error: No models were loaded")
                return False
            
            self.loaded = True
            print(f"\n[OK] Loaded {len(self.models)}/3 models successfully")
            return True
            
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            return False
    
    def predict_single(self, text: str, model_name: str) -> Dict:
        """
        Get prediction from a single model
        
        Args:
            text: Input text to classify
            model_name: Name of the model to use
            
        Returns:
            Dictionary with prediction details
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not available")
        
        model = self.models[model_name]
        
        # Get probabilities [fake_prob, real_prob]
        proba = model.predict_proba([text])[0]
        
        # Determine prediction (index 0 = fake, index 1 = real)
        prediction = "fake" if proba[0] > proba[1] else "real"
        confidence = max(proba[0], proba[1])
        
        return {
            "prediction": prediction,
            "probability_fake": float(proba[0]),
            "probability_real": float(proba[1]),
            "confidence": float(confidence)
        }
    
    def predict_ensemble(self, text: str) -> Dict:
        """
        Get ensemble prediction combining all models with weighted voting
        
        Args:
            text: Input text to classify
            
        Returns:
            Dictionary with ensemble and individual predictions
        """
        if not self.loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        if len(self.models) == 0:
            raise RuntimeError("No models available for prediction")
        
        # Get predictions from each model
        individual_predictions = {}
        ensemble_fake_prob = 0.0
        ensemble_real_prob = 0.0
        
        for model_name in self.models.keys():
            pred = self.predict_single(text, model_name)
            individual_predictions[model_name] = pred
            
            # Weighted voting
            weight = self.weights.get(model_name, 0.0)
            ensemble_fake_prob += pred['probability_fake'] * weight
            ensemble_real_prob += pred['probability_real'] * weight
        
        # Normalize if not all models are available
        total_weight = sum(self.weights[name] for name in self.models.keys())
        if total_weight > 0 and total_weight != 1.0:
            ensemble_fake_prob /= total_weight
            ensemble_real_prob /= total_weight
        
        # Determine final prediction
        ensemble_prediction = "fake" if ensemble_fake_prob > ensemble_real_prob else "real"
        ensemble_confidence = max(ensemble_fake_prob, ensemble_real_prob)
        
        return {
            "prediction": ensemble_prediction,
            "confidence": float(ensemble_confidence),
            "probability_fake": float(ensemble_fake_prob),
            "probability_real": float(ensemble_real_prob),
            "proba": [float(ensemble_fake_prob), float(ensemble_real_prob)],
            "individual_predictions": individual_predictions,
            "models_used": list(self.models.keys())
        }
    
    def predict_batch(self, texts: List[str]) -> Dict:
        """
        Predict multiple texts at once
        
        Args:
            texts: List of input texts
            
        Returns:
            Dictionary with batch predictions
        """
        predictions = []
        confidences = []
        probas = []
        
        for text in texts:
            result = self.predict_ensemble(text)
            predictions.append(result['prediction'])
            confidences.append(result['confidence'])
            probas.append(result['proba'])
        
        return {
            "predictions": predictions,
            "confidences": confidences,
            "probas": probas
        }
    
    def get_model_info(self) -> Dict:
        """
        Get information about loaded models
        
        Returns:
            Dictionary with model status and configuration
        """
        return {
            "loaded": self.loaded,
            "models_available": list(self.models.keys()),
            "total_models": len(self.models),
            "weights": self.weights,
            "model_dir": str(self.model_dir)
        }
    
    def get_feature_names(self, model_name: str = 'random_forest') -> Optional[List[str]]:
        """
        Extract feature names from a model's vectorizer for LIME explanations
        
        Args:
            model_name: Name of the model to extract features from
            
        Returns:
            List of feature names or None if not available
        """
        if model_name not in self.models:
            return None
        
        try:
            model = self.models[model_name]
            # Extract vectorizer from pipeline
            if hasattr(model, 'named_steps') and 'tfidf' in model.named_steps:
                vectorizer = model.named_steps['tfidf']
                return vectorizer.get_feature_names_out().tolist()
            return None
        except Exception as e:
            print(f"Error extracting feature names: {str(e)}")
            return None


# Global ensemble instance
_ensemble = None


def get_ensemble(model_dir: str = "models") -> SmartEnsemble:
    """
    Get or create global ensemble instance (singleton pattern)
    
    Args:
        model_dir: Directory containing model files
        
    Returns:
        SmartEnsemble instance
    """
    global _ensemble
    if _ensemble is None:
        _ensemble = SmartEnsemble(model_dir)
        # Allow CI/tests to skip model loading to avoid heavy dependencies
        if os.getenv("SKIP_MODEL_LOAD") == "1":
            print("[INFO] SKIP_MODEL_LOAD=1: Skipping model loading for tests/CI")
        else:
            _ensemble.load_models()
    return _ensemble
