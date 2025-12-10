"""
FastAPI routes for fake news detection
"""
import os
from typing import Optional, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
import traceback

from src.ml.ensemble import get_ensemble
from src.ml.rules import get_detector
from src.ml.explainer import get_explainer
from src.utils.preprocessing import basic_clean, validate_text
from src.utils.cache import get_cache


# Request/Response Models
class PredictRequest(BaseModel):
    text: str = Field(..., description="News article text to classify")
    clean: bool = Field(True, description="Whether to clean text before prediction")
    mode: str = Field("ensemble", description="Prediction mode: 'ensemble' or model name")


class BatchPredictRequest(BaseModel):
    texts: List[str] = Field(..., description="List of news articles to classify")
    clean: bool = Field(True, description="Whether to clean text before prediction")


class ExplainRequest(BaseModel):
    text: str = Field(..., description="News article text to explain")
    num_features: int = Field(10, description="Number of top features to show", ge=1, le=50)
    model_name: Optional[str] = Field(None, description="Specific model to explain")


class PredictResponse(BaseModel):
    prediction: str = Field(..., description="Predicted label: 'fake' or 'real'")
    confidence: float = Field(..., description="Confidence score (0-1)")
    probability_fake: float = Field(..., description="Probability of being fake")
    probability_real: float = Field(..., description="Probability of being real")
    proba: List[float] = Field(..., description="[fake_prob, real_prob]")
    individual_predictions: dict = Field(..., description="Predictions from each model")
    models_used: List[str] = Field(..., description="Models used in prediction")
    rule_based_analysis: Optional[dict] = Field(None, description="Rule-based pattern analysis")
    cached: bool = Field(False, description="Whether result was from cache")


class BatchPredictResponse(BaseModel):
    predictions: List[str] = Field(..., description="List of predictions")
    confidences: List[float] = Field(..., description="List of confidence scores")
    probas: List[List[float]] = Field(..., description="List of probability arrays")


class ExplainResponse(BaseModel):
    prediction: str = Field(..., description="Predicted label")
    confidence: float = Field(..., description="Confidence score")
    weights: List[List] = Field(..., description="List of [word, weight] pairs")
    explanation_text: Optional[str] = Field(None, description="Human-readable explanation")
    individual_explanations: Optional[dict] = Field(None, description="Explanations per model")


class HealthResponse(BaseModel):
    ok: bool = Field(..., description="System health status")
    ensemble_loaded: bool = Field(..., description="Whether ensemble is loaded")
    models_available: List[str] = Field(..., description="Available models")
    model_dir: str = Field(..., description="Model directory path")
    cache_stats: Optional[dict] = Field(None, description="Cache statistics")


# Initialize router
router = APIRouter()

# Initialize components
ensemble = get_ensemble()
detector = get_detector()
cache = get_cache()


@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Predict if news article is fake or real using ensemble of models
    """
    try:
        # Validate text
        is_valid, error_msg = validate_text(request.text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Check cache
        cached_result = cache.get(request.text, request.mode)
        if cached_result:
            cached_result['cached'] = True
            return cached_result
        
        # Clean text if requested
        text = request.text
        if request.clean:
            text = basic_clean(text)
        
        # Get ensemble prediction
        result = ensemble.predict_ensemble(text)
        
        # Add rule-based analysis
        rule_analysis = detector.analyze(text)
        result['rule_based_analysis'] = rule_analysis
        
        # Format response
        response = PredictResponse(
            prediction=result['prediction'],
            confidence=result['confidence'],
            probability_fake=result['probability_fake'],
            probability_real=result['probability_real'],
            proba=result['proba'],
            individual_predictions=result['individual_predictions'],
            models_used=result['models_used'],
            rule_based_analysis=rule_analysis,
            cached=False
        )
        
        # Cache result
        cache.set(request.text, response.model_dump(), request.mode)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /predict: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/batch", response_model=BatchPredictResponse)
async def batch_predict(request: BatchPredictRequest):
    """
    Predict multiple news articles at once
    """
    try:
        if not request.texts:
            raise HTTPException(status_code=400, detail="No texts provided")
        
        if len(request.texts) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 texts per batch")
        
        # Validate all texts
        for i, text in enumerate(request.texts):
            is_valid, error_msg = validate_text(text)
            if not is_valid:
                raise HTTPException(
                    status_code=400,
                    detail=f"Text {i+1}: {error_msg}"
                )
        
        # Clean texts if requested
        texts = request.texts
        if request.clean:
            texts = [basic_clean(text) for text in texts]
        
        # Batch prediction
        result = ensemble.predict_batch(texts)
        
        return BatchPredictResponse(
            predictions=result['predictions'],
            confidences=result['confidences'],
            probas=result['probas']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /batch: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@router.post("/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest):
    """
    Explain prediction using LIME word weights
    """
    try:
        # Validate text
        is_valid, error_msg = validate_text(request.text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Get or create explainer
        explainer = get_explainer(ensemble)
        if explainer is None:
            raise HTTPException(status_code=503, detail="Explainer not initialized")
        
        # Generate explanation
        explanation = explainer.explain(
            request.text,
            num_features=request.num_features,
            model_name=request.model_name
        )
        
        return ExplainResponse(
            prediction=explanation['prediction'],
            confidence=explanation['confidence'],
            weights=explanation['weights'],
            explanation_text=explanation.get('explanation_text'),
            individual_explanations=explanation.get('individual_explanations')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /explain: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")


@router.post("/detect-visual")
async def detect_visual(
    image: UploadFile = File(...),
    event: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    date: Optional[str] = Form(None)
):
    """
    Detect fake images using visual analysis
    """
    try:
        # Import visual detector (only when needed)
        try:
            from src.enhancements.visual_detector import VisualFakeNewsDetector
        except ImportError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Visual detection not available: {str(e)}"
            )
        
        # Set Google Cloud credentials
        google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'google-vision-credentials.json')
        if not os.path.exists(google_creds):
            print(f"Warning: Google Cloud credentials not found at {google_creds}")
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_creds
        
        # Initialize detector
        detector = VisualFakeNewsDetector(google_credentials_path=google_creds)
        
        # Save uploaded image temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            content = await image.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Build context
            context = {}
            if event:
                context['event'] = event
            if location:
                context['location'] = location
            if date:
                context['date'] = date
            
            # Detect
            result = detector.detect(tmp_path, context if context else None)
            
            return result
            
        finally:
            # Clean up temp file
            import os as os_module
            if os_module.path.exists(tmp_path):
                os_module.remove(tmp_path)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /detect-visual: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Visual detection failed: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health():
    """
    Check system health and model status
    """
    try:
        model_info = ensemble.get_model_info()
        cache_stats = cache.get_stats()
        
        return HealthResponse(
            ok=True,
            ensemble_loaded=model_info['loaded'],
            models_available=model_info['models_available'],
            model_dir=model_info['model_dir'],
            cache_stats=cache_stats
        )
        
    except Exception as e:
        print(f"Error in /health: {str(e)}")
        return HealthResponse(
            ok=False,
            ensemble_loaded=False,
            models_available=[],
            model_dir="models",
            cache_stats=None
        )


@router.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "name": "Fake News Detection API",
        "version": "1.0.0",
        "endpoints": {
            "POST /predict": "Classify single news article",
            "POST /batch": "Classify multiple articles",
            "POST /explain": "Explain prediction with LIME",
            "POST /detect-visual": "Detect fake images",
            "GET /health": "System health check"
        },
        "documentation": "/docs"
    }
