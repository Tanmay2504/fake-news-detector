"""
LIME explainability for fake news predictions
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from lime.lime_text import LimeTextExplainer


class NewsExplainer:
    """
    Generate word-level explanations for fake news predictions using LIME
    """
    
    def __init__(self, model=None, class_names: List[str] = None):
        """
        Initialize LIME explainer
        
        Args:
            model: Trained model with predict_proba method
            class_names: Names of prediction classes (default: ['fake', 'real'])
        """
        self.model = model
        self.class_names = class_names or ['fake', 'real']
        self.explainer = LimeTextExplainer(
            class_names=self.class_names,
            bow=True,  # Use bag of words
            random_state=42
        )
    
    def set_model(self, model):
        """
        Set or update the model to explain
        
        Args:
            model: Trained model with predict_proba method
        """
        self.model = model
    
    def explain(
        self,
        text: str,
        num_features: int = 10,
        num_samples: int = 5000
    ) -> Dict:
        """
        Generate LIME explanation for a single prediction
        
        Args:
            text: Input text to explain
            num_features: Number of top features to show
            num_samples: Number of samples for LIME
            
        Returns:
            Dictionary with explanation and word weights
        """
        if self.model is None:
            raise ValueError("Model not set. Call set_model() first.")
        
        # Get prediction
        prediction_proba = self.model.predict_proba([text])[0]
        predicted_class = np.argmax(prediction_proba)
        confidence = prediction_proba[predicted_class]
        
        # Generate LIME explanation
        exp = self.explainer.explain_instance(
            text,
            self.model.predict_proba,
            num_features=num_features,
            num_samples=num_samples
        )
        
        # Extract word weights for predicted class
        weights = exp.as_list(label=predicted_class)
        
        # Sort by absolute weight (importance)
        weights_sorted = sorted(weights, key=lambda x: abs(x[1]), reverse=True)
        
        return {
            "prediction": self.class_names[predicted_class],
            "confidence": float(confidence),
            "probability_fake": float(prediction_proba[0]),
            "probability_real": float(prediction_proba[1]),
            "weights": weights_sorted,
            "num_features": len(weights_sorted),
            "explanation_text": self._format_explanation(weights_sorted)
        }
    
    def explain_batch(
        self,
        texts: List[str],
        num_features: int = 10
    ) -> List[Dict]:
        """
        Generate explanations for multiple texts
        
        Args:
            texts: List of input texts
            num_features: Number of top features to show
            
        Returns:
            List of explanation dictionaries
        """
        return [self.explain(text, num_features) for text in texts]
    
    def _format_explanation(self, weights: List[Tuple[str, float]]) -> str:
        """
        Format word weights into human-readable explanation
        
        Args:
            weights: List of (word, weight) tuples
            
        Returns:
            Formatted explanation string
        """
        if not weights:
            return "No explanation available"
        
        top_fake = [w for w in weights if w[1] > 0][:5]
        top_real = [w for w in weights if w[1] < 0][:5]
        
        explanation = []
        
        if top_fake:
            words = ", ".join([f"'{w[0]}'" for w in top_fake])
            explanation.append(f"Words suggesting FAKE: {words}")
        
        if top_real:
            words = ", ".join([f"'{w[0]}'" for w in top_real])
            explanation.append(f"Words suggesting REAL: {words}")
        
        return " | ".join(explanation) if explanation else "No strong indicators found"
    
    def get_top_words(
        self,
        text: str,
        num_words: int = 5,
        word_type: str = "both"
    ) -> List[Tuple[str, float]]:
        """
        Get top words contributing to prediction
        
        Args:
            text: Input text
            num_words: Number of words to return
            word_type: 'fake', 'real', or 'both'
            
        Returns:
            List of (word, weight) tuples
        """
        exp_result = self.explain(text, num_features=20)
        weights = exp_result['weights']
        
        if word_type == "fake":
            return [w for w in weights if w[1] > 0][:num_words]
        elif word_type == "real":
            return [w for w in weights if w[1] < 0][:num_words]
        else:
            return weights[:num_words]


class EnsembleExplainer:
    """
    Explain predictions from ensemble of models
    """
    
    def __init__(self, ensemble):
        """
        Initialize ensemble explainer
        
        Args:
            ensemble: SmartEnsemble instance
        """
        self.ensemble = ensemble
        self.explainers = {}
        
        # Create explainer for each model
        for model_name, model in ensemble.models.items():
            self.explainers[model_name] = NewsExplainer(model)
    
    def explain(
        self,
        text: str,
        num_features: int = 10,
        model_name: Optional[str] = None
    ) -> Dict:
        """
        Explain prediction from ensemble or specific model
        
        Args:
            text: Input text to explain
            num_features: Number of top features
            model_name: Specific model to explain (None = all models)
            
        Returns:
            Explanation dictionary
        """
        if model_name:
            # Explain single model
            if model_name not in self.explainers:
                raise ValueError(f"Model '{model_name}' not available")
            return self.explainers[model_name].explain(text, num_features)
        
        # Explain all models and combine
        explanations = {}
        all_weights = {}
        
        for name, explainer in self.explainers.items():
            exp = explainer.explain(text, num_features)
            explanations[name] = exp
            
            # Aggregate weights across models
            weight = self.ensemble.weights.get(name, 0.0)
            for word, word_weight in exp['weights']:
                if word not in all_weights:
                    all_weights[word] = 0.0
                all_weights[word] += word_weight * weight
        
        # Sort combined weights
        combined_weights = sorted(
            all_weights.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:num_features]
        
        # Get ensemble prediction
        ensemble_pred = self.ensemble.predict_ensemble(text)
        
        return {
            "prediction": ensemble_pred['prediction'],
            "confidence": ensemble_pred['confidence'],
            "weights": combined_weights,
            "individual_explanations": explanations,
            "models_used": list(self.explainers.keys())
        }


# Global explainer instance
_explainer = None


def get_explainer(ensemble=None) -> Optional[EnsembleExplainer]:
    """
    Get or create global explainer instance
    
    Args:
        ensemble: SmartEnsemble instance
        
    Returns:
        EnsembleExplainer instance or None
    """
    global _explainer
    if _explainer is None and ensemble is not None:
        _explainer = EnsembleExplainer(ensemble)
    return _explainer
