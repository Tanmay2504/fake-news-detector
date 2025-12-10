"""
Enhanced fake news detection with multi-layer verification.
Combines ML models with source verification, sentiment analysis, and more.
"""

from typing import Dict, Optional
from pathlib import Path

# Import existing components
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.ensemble import IntelligentEnsemble
from src.data.cleaning import basic_clean

# Import enhancement modules
from .source_verifier import SourceVerifier
from .sentiment_analyzer import SentimentAnalyzer

try:
    from .image_processor import ImageTextExtractor
    IMAGE_PROCESSOR_AVAILABLE = True
except:
    IMAGE_PROCESSOR_AVAILABLE = False


class EnhancedDetector:
    """
    Enhanced fake news detector with multiple verification layers
    """
    
    def __init__(self, newsapi_key: Optional[str] = None):
        """
        Initialize enhanced detector
        
        Args:
            newsapi_key: Optional NewsAPI key for source verification
        """
        # Load ML models
        self.ensemble = IntelligentEnsemble()
        self.ensemble.load_models()
        
        # Initialize verification components
        self.source_verifier = SourceVerifier(newsapi_key=newsapi_key)
        self.sentiment_analyzer = SentimentAnalyzer()
        
        if IMAGE_PROCESSOR_AVAILABLE:
            self.image_extractor = ImageTextExtractor(method='easyocr')
        else:
            self.image_extractor = None
    
    def detect(
        self,
        text: Optional[str] = None,
        url: Optional[str] = None,
        image_path: Optional[str] = None,
        mode: str = 'ensemble',
        check_source: bool = True,
        check_sentiment: bool = True
    ) -> Dict:
        """
        Comprehensive fake news detection
        
        Args:
            text: Article text (optional if image provided)
            url: Article URL for source verification
            image_path: Path to image (will extract text via OCR)
            mode: ML model mode ('fast', 'balanced', 'accurate', 'ensemble')
            check_source: Enable source verification
            check_sentiment: Enable sentiment analysis
            
        Returns:
            dict with comprehensive detection results
        """
        result = {
            'text_source': 'provided',
            'ml_prediction': {},
            'source_verification': {},
            'sentiment_analysis': {},
            'final_verdict': {}
        }
        
        # Step 1: Extract text from image if needed
        if image_path and not text:
            if not self.image_extractor:
                return {'error': 'Image processing not available. Install: pip install easyocr'}
            
            ocr_result = self.image_extractor.extract_text(image_path)
            text = ocr_result['text']
            result['text_source'] = 'image_ocr'
            result['ocr_confidence'] = ocr_result['confidence']
            result['ocr_method'] = ocr_result['method']
        
        if not text:
            return {'error': 'No text provided or extracted'}
        
        # Store processed text
        result['text_preview'] = text[:200] + '...' if len(text) > 200 else text
        result['text_length'] = len(text)
        
        # Step 2: ML Model Prediction
        ml_result = self.ensemble.predict(text, mode=mode)
        result['ml_prediction'] = ml_result
        
        # Step 3: Source Verification (if URL provided)
        if check_source and url:
            source_result = self.source_verifier.comprehensive_check(url, text[:100])
            result['source_verification'] = source_result
        
        # Step 4: Sentiment Analysis
        if check_sentiment:
            sentiment_result = self.sentiment_analyzer.analyze(text)
            result['sentiment_analysis'] = sentiment_result
        
        # Step 5: Calculate Final Verdict
        result['final_verdict'] = self._calculate_final_verdict(result)
        
        return result
    
    def _calculate_final_verdict(self, result: Dict) -> Dict:
        """
        Calculate final verdict combining all checks
        
        Scoring:
        - ML Model: 40% weight
        - Source Check: 30% weight  
        - Sentiment: 20% weight
        - OCR Confidence: 10% weight (if applicable)
        """
        fake_score = 0
        max_score = 0
        reasons = []
        confidence_factors = []
        
        # 1. ML Model (40% weight)
        ml_pred = result.get('ml_prediction', {})
        if ml_pred:
            ml_confidence = ml_pred.get('confidence', 0)
            if ml_pred.get('label') == 'fake':
                ml_contribution = 40 * ml_confidence
                fake_score += ml_contribution
                reasons.append(f"ML Model: {ml_confidence:.0%} fake ({ml_pred.get('mode', 'unknown')} mode)")
                confidence_factors.append(('ML Model', ml_contribution))
            max_score += 40
        
        # 2. Source Verification (30% weight)
        source_check = result.get('source_verification', {})
        if source_check:
            domain_check = source_check.get('domain_check', {})
            
            if domain_check.get('status') == 'KNOWN_FAKE':
                fake_score += 30
                reasons.append("Known fake news source")
                confidence_factors.append(('Source: Known Fake', 30))
            elif domain_check.get('trusted'):
                # Trusted source reduces fake score
                fake_score = max(0, fake_score - 30)
                reasons.append(f"Trusted source: {domain_check.get('domain')}")
                confidence_factors.append(('Source: Trusted', -30))
            elif domain_check.get('credibility_score', 0) < 4:
                fake_score += 15
                reasons.append("Low credibility source")
                confidence_factors.append(('Source: Low Credibility', 15))
            
            max_score += 30
        
        # 3. Sentiment Analysis (20% weight)
        sentiment = result.get('sentiment_analysis', {})
        if sentiment:
            manipulation_risk = sentiment.get('manipulation_risk', 'LOW')
            
            if manipulation_risk in ['VERY HIGH', 'HIGH']:
                sentiment_contribution = 20 if manipulation_risk == 'VERY HIGH' else 15
                fake_score += sentiment_contribution
                reasons.append(f"High emotional manipulation detected")
                confidence_factors.append(('Sentiment Manipulation', sentiment_contribution))
            elif manipulation_risk == 'MEDIUM':
                fake_score += 10
                reasons.append("Moderate emotional language")
                confidence_factors.append(('Sentiment: Moderate', 10))
            
            max_score += 20
        
        # 4. OCR Confidence (10% weight) - lower OCR confidence = less reliable
        if result.get('text_source') == 'image_ocr':
            ocr_conf = result.get('ocr_confidence', 1.0)
            if ocr_conf < 0.7:
                # Low OCR confidence means we're less sure
                uncertainty_penalty = (1 - ocr_conf) * 10
                fake_score += uncertainty_penalty
                reasons.append(f"Low OCR confidence ({ocr_conf:.0%})")
                confidence_factors.append(('OCR Uncertainty', uncertainty_penalty))
            max_score += 10
        
        # Calculate final percentage
        if max_score > 0:
            final_score = (fake_score / max_score) * 100
        else:
            final_score = ml_pred.get('confidence', 0.5) * 100
        
        # Determine verdict
        if final_score >= 80:
            verdict = 'FAKE'
            verdict_label = 'Very likely fake news'
        elif final_score >= 60:
            verdict = 'LIKELY FAKE'
            verdict_label = 'Probably fake news'
        elif final_score >= 40:
            verdict = 'SUSPICIOUS'
            verdict_label = 'Suspicious - verify independently'
        elif final_score >= 20:
            verdict = 'LIKELY REAL'
            verdict_label = 'Probably legitimate'
        else:
            verdict = 'REAL'
            verdict_label = 'Likely legitimate news'
        
        return {
            'verdict': verdict,
            'verdict_label': verdict_label,
            'confidence': round(final_score, 1),
            'is_fake': final_score >= 50,
            'fake_score': round(fake_score, 1),
            'max_score': max_score,
            'reasons': reasons,
            'confidence_breakdown': confidence_factors,
            'recommendation': self._get_recommendation(verdict, final_score)
        }
    
    def _get_recommendation(self, verdict: str, score: float) -> str:
        """Generate user recommendation"""
        if verdict == 'FAKE':
            return '🚫 Do not trust or share this content. Verify with credible sources.'
        elif verdict == 'LIKELY FAKE':
            return '⚠️ Highly questionable. Cross-check with multiple trusted sources.'
        elif verdict == 'SUSPICIOUS':
            return '⚡ Exercise caution. Verify key claims independently.'
        elif verdict == 'LIKELY REAL':
            return '✓ Appears credible, but always verify important claims.'
        else:
            return '✅ Likely legitimate, from credible source.'


# Convenience function
def detect_fake_news(
    text: Optional[str] = None,
    url: Optional[str] = None,
    image_path: Optional[str] = None,
    newsapi_key: Optional[str] = None
) -> Dict:
    """Quick enhanced detection"""
    detector = EnhancedDetector(newsapi_key=newsapi_key)
    return detector.detect(text=text, url=url, image_path=image_path)


if __name__ == '__main__':
    # Test enhanced detector
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python enhanced_detector.py \"<text>\" [url] [newsapi_key]")
        print("\nExamples:")
        print("  python enhanced_detector.py \"Scientists discover cure for all diseases!\"")
        print("  python enhanced_detector.py \"Breaking news...\" https://example.com")
        sys.exit(1)
    
    text = sys.argv[1]
    url = sys.argv[2] if len(sys.argv) > 2 else None
    newsapi_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    print("\n" + "="*80)
    print("ENHANCED FAKE NEWS DETECTION")
    print("="*80 + "\n")
    
    try:
        result = detect_fake_news(text=text, url=url, newsapi_key=newsapi_key)
        
        # Display results
        final = result['final_verdict']
        
        print(f"📊 VERDICT: {final['verdict']} ({final['confidence']:.1f}% confidence)")
        print(f"   {final['verdict_label']}\n")
        
        print(f"📝 ML Model Prediction:")
        ml = result['ml_prediction']
        print(f"   {ml['label'].upper()} - {ml['confidence']:.0%} confidence ({ml['mode']} mode)\n")
        
        if result.get('source_verification'):
            print(f"🔍 Source Verification:")
            sv = result['source_verification']
            domain = sv['domain_check']
            print(f"   Domain: {domain['domain']}")
            print(f"   Status: {domain['status']}")
            print(f"   Credibility: {domain['credibility_score']}/10\n")
        
        if result.get('sentiment_analysis'):
            print(f"💭 Sentiment Analysis:")
            sa = result['sentiment_analysis']
            print(f"   Manipulation Risk: {sa['manipulation_risk']}")
            print(f"   Polarity: {sa['polarity_label']}")
            print(f"   Subjectivity: {sa['subjectivity_label']}\n")
        
        print(f"📌 Key Reasons:")
        for reason in final['reasons']:
            print(f"   • {reason}")
        
        print(f"\n💡 {final['recommendation']}")
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
