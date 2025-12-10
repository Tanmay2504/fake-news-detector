"""
Sentiment analysis to detect emotional manipulation in news articles.
Fake news often uses extreme sentiment and subjective language.
"""

from typing import Dict, List
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False


class SentimentAnalyzer:
    """Analyze sentiment and detect emotional manipulation"""
    
    def __init__(self):
        """Initialize sentiment analyzer"""
        if not TEXTBLOB_AVAILABLE:
            raise ImportError("textblob not installed. Run: pip install textblob")
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment and manipulation indicators
        
        Args:
            text: Article text to analyze
            
        Returns:
            dict with sentiment analysis results
        """
        blob = TextBlob(text)
        
        polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
        
        # Analyze manipulation indicators
        is_extreme = abs(polarity) > 0.5
        is_very_extreme = abs(polarity) > 0.7
        is_subjective = subjectivity > 0.6
        is_very_subjective = subjectivity > 0.8
        
        # Calculate manipulation risk
        manipulation_score = 0
        if is_extreme:
            manipulation_score += 30
        if is_very_extreme:
            manipulation_score += 20
        if is_subjective:
            manipulation_score += 30
        if is_very_subjective:
            manipulation_score += 20
        
        manipulation_risk = self._get_risk_level(manipulation_score)
        
        # Analyze sentence-level sentiment
        sentences = list(blob.sentences)
        sentence_polarities = [s.sentiment.polarity for s in sentences if s.sentiment.polarity != 0]
        
        # Check for sentiment consistency
        sentiment_variance = self._calculate_variance(sentence_polarities) if sentence_polarities else 0
        is_inconsistent = sentiment_variance > 0.3
        
        return {
            'polarity': round(polarity, 3),
            'polarity_label': self._get_polarity_label(polarity),
            'subjectivity': round(subjectivity, 3),
            'subjectivity_label': self._get_subjectivity_label(subjectivity),
            'is_extreme_sentiment': is_extreme,
            'is_highly_subjective': is_subjective,
            'manipulation_score': manipulation_score,
            'manipulation_risk': manipulation_risk,
            'sentence_count': len(sentences),
            'sentiment_variance': round(sentiment_variance, 3),
            'is_inconsistent': is_inconsistent,
            'warning_flags': self._get_warning_flags(
                is_extreme, is_subjective, is_inconsistent
            ),
            'recommendation': self._get_recommendation(manipulation_risk, is_extreme, is_subjective)
        }
    
    def _get_polarity_label(self, polarity: float) -> str:
        """Convert polarity score to label"""
        if polarity > 0.7:
            return 'Very Positive'
        elif polarity > 0.3:
            return 'Positive'
        elif polarity > 0.1:
            return 'Slightly Positive'
        elif polarity > -0.1:
            return 'Neutral'
        elif polarity > -0.3:
            return 'Slightly Negative'
        elif polarity > -0.7:
            return 'Negative'
        else:
            return 'Very Negative'
    
    def _get_subjectivity_label(self, subjectivity: float) -> str:
        """Convert subjectivity score to label"""
        if subjectivity > 0.8:
            return 'Highly Subjective'
        elif subjectivity > 0.6:
            return 'Subjective'
        elif subjectivity > 0.4:
            return 'Somewhat Subjective'
        elif subjectivity > 0.2:
            return 'Mostly Objective'
        else:
            return 'Objective'
    
    def _get_risk_level(self, score: int) -> str:
        """Convert manipulation score to risk level"""
        if score >= 70:
            return 'VERY HIGH'
        elif score >= 50:
            return 'HIGH'
        elif score >= 30:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of values"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def _get_warning_flags(self, extreme: bool, subjective: bool, inconsistent: bool) -> List[str]:
        """Generate warning flags"""
        flags = []
        
        if extreme:
            flags.append('Extreme emotional language')
        if subjective:
            flags.append('Highly opinionated content')
        if inconsistent:
            flags.append('Inconsistent sentiment (potential manipulation)')
        
        return flags
    
    def _get_recommendation(self, risk: str, extreme: bool, subjective: bool) -> str:
        """Generate recommendation based on analysis"""
        if risk in ['VERY HIGH', 'HIGH']:
            return 'High risk of emotional manipulation - verify facts independently'
        elif risk == 'MEDIUM' and (extreme or subjective):
            return 'Moderate manipulation risk - cross-check with neutral sources'
        elif subjective:
            return 'Opinion-heavy content - look for factual reporting'
        else:
            return 'Appears relatively objective'


# Convenience function
def analyze_sentiment(text: str) -> Dict:
    """Quick sentiment analysis"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)


if __name__ == '__main__':
    # Test sentiment analysis
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sentiment_analyzer.py \"<text>\"")
        print("\nExample:")
        print("  python sentiment_analyzer.py \"Breaking news: Scientists make amazing discovery!\"")
        sys.exit(1)
    
    text = ' '.join(sys.argv[1:])
    
    print("\nAnalyzing sentiment...\n")
    print("="*60)
    
    try:
        result = analyze_sentiment(text)
        
        print(f"Polarity: {result['polarity']} ({result['polarity_label']})")
        print(f"Subjectivity: {result['subjectivity']} ({result['subjectivity_label']})")
        print(f"\nManipulation Risk: {result['manipulation_risk']} ({result['manipulation_score']}/100)")
        print(f"\nWarning Flags:")
        for flag in result['warning_flags']:
            print(f"  ⚠️  {flag}")
        
        print(f"\nRecommendation: {result['recommendation']}")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have installed textblob:")
        print("  pip install textblob")
        print("  python -m textblob.download_corpora")
