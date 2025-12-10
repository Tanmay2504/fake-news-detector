"""
Rule-based fake news detection patterns
"""
import re
from typing import Dict, List, Tuple


class RuleBasedDetector:
    """
    Detect fake news using pattern matching and linguistic indicators
    """
    
    def __init__(self):
        # Fake news indicators (6 patterns)
        self.fake_indicators = {
            'sensational': [
                r'\bshocking\b', r'\bunbelievable\b', r'\bbreaking\b',
                r'\bexclusive\b', r'\byou won\'t believe\b', r'\bamaze\b',
                r'\bstunning\b', r'\bmind[- ]blowing\b', r'\binsane\b'
            ],
            'clickbait': [
                r'what happens next', r'will shock you', r'you need to know',
                r'this is why', r'the truth about', r'number \d+ will',
                r'doctors hate', r'one simple trick'
            ],
            'excessive_caps': r'[A-Z\s]{15,}',  # 15+ consecutive caps
            'excessive_punctuation': r'[!?]{3,}',  # Multiple !!! or ???
            'conspiracy': [
                r'\bcover[- ]?up\b', r'\bthey don\'t want\b', r'\bhidden truth\b',
                r'\bwake up\b', r'\bsheeple\b', r'\bmainstream media lies\b'
            ],
            'urgency': [
                r'\bright now\b', r'\bimmediately\b', r'\bact fast\b',
                r'\blimited time\b', r'\bhurry\b', r'\bdon\'t wait\b'
            ]
        }
        
        # Real news indicators (4 patterns)
        self.real_indicators = {
            'citations': [
                r'according to', r'reported by', r'said in a statement',
                r'told reporters', r'sources say', r'officials said'
            ],
            'formal_language': [
                r'\bhowever\b', r'\bnevertheless\b', r'\bfurthermore\b',
                r'\bmoreover\b', r'\btherefore\b', r'\bconsequently\b'
            ],
            'specific_dates': r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b',
            'quotes': r'"[^"]{20,}"'  # Quoted text 20+ chars
        }
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze text using rule-based patterns
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with analysis results and indicators found
        """
        text_lower = text.lower()
        
        # Count fake indicators
        fake_score = 0
        fake_matches = []
        
        for category, patterns in self.fake_indicators.items():
            if isinstance(patterns, list):
                for pattern in patterns:
                    matches = re.findall(pattern, text_lower)
                    if matches:
                        fake_score += len(matches)
                        fake_matches.append({
                            'category': category,
                            'pattern': pattern,
                            'matches': matches
                        })
            else:
                matches = re.findall(patterns, text, re.IGNORECASE)
                if matches:
                    fake_score += len(matches)
                    fake_matches.append({
                        'category': category,
                        'pattern': patterns,
                        'matches': matches
                    })
        
        # Count real indicators
        real_score = 0
        real_matches = []
        
        for category, patterns in self.real_indicators.items():
            if isinstance(patterns, list):
                for pattern in patterns:
                    matches = re.findall(pattern, text_lower)
                    if matches:
                        real_score += len(matches)
                        real_matches.append({
                            'category': category,
                            'pattern': pattern,
                            'matches': matches
                        })
            else:
                matches = re.findall(patterns, text, re.IGNORECASE)
                if matches:
                    real_score += len(matches)
                    real_matches.append({
                        'category': category,
                        'pattern': patterns,
                        'matches': matches[:3]  # Limit matches for quotes
                    })
        
        # Calculate confidence based on scores
        total_score = fake_score + real_score
        if total_score == 0:
            confidence = 0.5  # Neutral
            prediction = "uncertain"
        else:
            if fake_score > real_score:
                confidence = min(0.5 + (fake_score / (total_score * 2)), 0.95)
                prediction = "fake"
            else:
                confidence = min(0.5 + (real_score / (total_score * 2)), 0.95)
                prediction = "real"
        
        return {
            "prediction": prediction,
            "confidence": float(confidence),
            "fake_score": fake_score,
            "real_score": real_score,
            "fake_indicators_found": len(fake_matches),
            "real_indicators_found": len(real_matches),
            "fake_matches": fake_matches[:10],  # Limit output
            "real_matches": real_matches[:10]   # Limit output
        }
    
    def get_explanation(self, text: str) -> List[str]:
        """
        Get human-readable explanation of why text is classified as fake/real
        
        Args:
            text: Input text to explain
            
        Returns:
            List of explanation strings
        """
        analysis = self.analyze(text)
        explanations = []
        
        if analysis['fake_score'] > 0:
            explanations.append(f"Found {analysis['fake_indicators_found']} fake news indicators")
            
            # Summarize by category
            categories = {}
            for match in analysis['fake_matches']:
                cat = match['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in categories.items():
                explanations.append(f"  - {count} {cat} pattern(s)")
        
        if analysis['real_score'] > 0:
            explanations.append(f"Found {analysis['real_indicators_found']} credibility indicators")
            
            # Summarize by category
            categories = {}
            for match in analysis['real_matches']:
                cat = match['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in categories.items():
                explanations.append(f"  - {count} {cat} pattern(s)")
        
        if not explanations:
            explanations.append("No strong indicators found")
        
        return explanations


# Global detector instance
_detector = None


def get_detector() -> RuleBasedDetector:
    """
    Get or create global detector instance (singleton pattern)
    
    Returns:
        RuleBasedDetector instance
    """
    global _detector
    if _detector is None:
        _detector = RuleBasedDetector()
    return _detector
