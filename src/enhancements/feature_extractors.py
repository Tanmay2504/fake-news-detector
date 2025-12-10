"""
Enhanced feature extractors for fake news detection
"""
import numpy as np
import re
from sklearn.base import BaseEstimator, TransformerMixin


class StyleMetricFeatures(BaseEstimator, TransformerMixin):
    """Extract stylometric features (writing style patterns)"""
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for text in X:
            text_str = str(text)
            
            # Count basic elements
            words = text_str.split()
            sentences = re.split(r'[.!?]+', text_str)
            sentences = [s for s in sentences if s.strip()]
            
            # Feature 1-5: Punctuation patterns
            exclamation_ratio = text_str.count('!') / max(len(text_str), 1)
            question_ratio = text_str.count('?') / max(len(text_str), 1)
            quote_ratio = text_str.count('"') / max(len(text_str), 1)
            ellipsis_count = text_str.count('...') + text_str.count('…')
            multiple_punct = len(re.findall(r'[!?]{2,}', text_str))
            
            # Feature 6-10: Capitalization patterns
            caps_words = sum(1 for w in words if w.isupper() and len(w) > 1)
            caps_ratio = caps_words / max(len(words), 1)
            title_case = sum(1 for w in words if w.istitle())
            title_ratio = title_case / max(len(words), 1)
            all_caps_chars = sum(1 for c in text_str if c.isupper())
            caps_char_ratio = all_caps_chars / max(len(text_str), 1)
            
            # Feature 11-15: Sentence structure
            avg_sentence_length = np.mean([len(s.split()) for s in sentences]) if sentences else 0
            max_sentence_length = max([len(s.split()) for s in sentences]) if sentences else 0
            min_sentence_length = min([len(s.split()) for s in sentences]) if sentences else 0
            sentence_length_std = np.std([len(s.split()) for s in sentences]) if len(sentences) > 1 else 0
            num_sentences = len(sentences)
            
            # Feature 16-20: Word patterns
            avg_word_length = np.mean([len(w) for w in words]) if words else 0
            long_words = sum(1 for w in words if len(w) > 6)
            long_word_ratio = long_words / max(len(words), 1)
            unique_words = len(set(words))
            lexical_diversity = unique_words / max(len(words), 1)
            
            # Feature 21-25: Special characters
            digit_ratio = sum(c.isdigit() for c in text_str) / max(len(text_str), 1)
            special_char_ratio = sum(not c.isalnum() and not c.isspace() for c in text_str) / max(len(text_str), 1)
            space_ratio = text_str.count(' ') / max(len(text_str), 1)
            newline_count = text_str.count('\n')
            url_count = len(re.findall(r'http[s]?://\S+|www\.\S+', text_str))
            
            features.append([
                exclamation_ratio, question_ratio, quote_ratio, ellipsis_count, multiple_punct,
                caps_ratio, title_ratio, caps_char_ratio, caps_words, title_case,
                avg_sentence_length, max_sentence_length, min_sentence_length, sentence_length_std, num_sentences,
                avg_word_length, long_word_ratio, lexical_diversity, unique_words, long_words,
                digit_ratio, special_char_ratio, space_ratio, newline_count, url_count
            ])
        
        return np.array(features)


class SentimentFeatures(BaseEstimator, TransformerMixin):
    """Extract sentiment and emotional features"""
    
    def __init__(self):
        # Emotion lexicons (simplified - can be expanded)
        self.fear_words = {'fear', 'afraid', 'scary', 'terror', 'panic', 'worried', 'anxious', 'nervous'}
        self.anger_words = {'angry', 'furious', 'outrage', 'hate', 'rage', 'mad', 'disgusted'}
        self.joy_words = {'happy', 'joy', 'excited', 'great', 'amazing', 'wonderful', 'fantastic'}
        self.sensational_words = {'shocking', 'breaking', 'bombshell', 'explosive', 'unbelievable', 'secret', 'hidden'}
        self.hedge_words = {'allegedly', 'reportedly', 'sources', 'claims', 'suggests', 'might', 'could', 'possibly'}
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for text in X:
            text_lower = str(text).lower()
            words = text_lower.split()
            
            # Emotion counts
            fear_count = sum(1 for w in words if w in self.fear_words)
            anger_count = sum(1 for w in words if w in self.anger_words)
            joy_count = sum(1 for w in words if w in self.joy_words)
            sensational_count = sum(1 for w in words if w in self.sensational_words)
            hedge_count = sum(1 for w in words if w in self.hedge_words)
            
            # Ratios
            total_words = max(len(words), 1)
            fear_ratio = fear_count / total_words
            anger_ratio = anger_count / total_words
            joy_ratio = joy_count / total_words
            sensational_ratio = sensational_count / total_words
            hedge_ratio = hedge_count / total_words
            
            # Overall emotionality
            total_emotion = fear_count + anger_count + joy_count
            emotion_ratio = total_emotion / total_words
            
            # Subjectivity indicators
            subjective_pronouns = sum(text_lower.count(p) for p in [' i ', ' we ', ' you ', ' my ', ' our '])
            subjective_ratio = subjective_pronouns / total_words
            
            features.append([
                fear_ratio, anger_ratio, joy_ratio, sensational_ratio, hedge_ratio,
                emotion_ratio, subjective_ratio, fear_count, anger_count, sensational_count
            ])
        
        return np.array(features)


class LinguisticComplexity(BaseEstimator, TransformerMixin):
    """Extract linguistic complexity features"""
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for text in X:
            text_str = str(text)
            words = text_str.split()
            
            # Type-Token Ratio (vocabulary richness)
            ttr = len(set(words)) / max(len(words), 1)
            
            # Function word ratio (the, a, an, of, in, etc.)
            function_words = {'the', 'a', 'an', 'of', 'in', 'to', 'for', 'with', 'on', 'at', 'by', 'from'}
            function_count = sum(1 for w in words if w.lower() in function_words)
            function_ratio = function_count / max(len(words), 1)
            
            # Pronoun usage
            pronouns = {'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
            pronoun_count = sum(1 for w in words if w.lower() in pronouns)
            pronoun_ratio = pronoun_count / max(len(words), 1)
            
            # Quote presence (real news often has quotes)
            quote_count = text_str.count('"')
            has_quotes = 1 if quote_count >= 2 else 0
            
            # Number/statistic presence (real news cites data)
            numbers = re.findall(r'\d+', text_str)
            number_count = len(numbers)
            has_statistics = 1 if number_count > 0 else 0
            
            features.append([
                ttr, function_ratio, pronoun_ratio, has_quotes, quote_count,
                has_statistics, number_count
            ])
        
        return np.array(features)
