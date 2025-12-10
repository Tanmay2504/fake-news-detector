"""
Text preprocessing utilities for fake news detection
"""
import re
from typing import Optional


def basic_clean(
    text: str,
    lowercase: bool = True,
    remove_urls: bool = True,
    remove_html: bool = True,
    remove_emails: bool = True,
    normalize_whitespace: bool = True
) -> str:
    """
    Clean and preprocess text before prediction
    
    Args:
        text: Input text to clean
        lowercase: Convert to lowercase
        remove_urls: Remove URLs (http/https/www)
        remove_html: Remove HTML tags
        remove_emails: Remove email addresses
        normalize_whitespace: Normalize whitespace to single spaces
        
    Returns:
        Cleaned text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    if remove_html:
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&[a-z]+;', ' ', text)  # HTML entities
    
    # Remove URLs
    if remove_urls:
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove email addresses
    if remove_emails:
        text = re.sub(r'\S+@\S+', '', text)
    
    # Convert to lowercase
    if lowercase:
        text = text.lower()
    
    # Normalize whitespace
    if normalize_whitespace:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
    
    return text


def advanced_clean(text: str) -> str:
    """
    Advanced cleaning with additional preprocessing steps
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text with advanced preprocessing
    """
    # Basic cleaning first
    text = basic_clean(text)
    
    # Remove special characters but keep alphanumeric and basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\'\"]', ' ', text)
    
    # Remove excessive punctuation (3+ repeated)
    text = re.sub(r'([\.!?]){3,}', r'\1\1', text)
    
    # Remove numbers longer than 4 digits (likely IDs, not meaningful)
    text = re.sub(r'\b\d{5,}\b', '', text)
    
    # Normalize quotation marks
    text = re.sub(r'[""''`]', '"', text)
    
    # Final whitespace normalization
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def extract_features(text: str) -> dict:
    """
    Extract statistical features from text
    
    Args:
        text: Input text
        
    Returns:
        Dictionary of text features
    """
    features = {
        'length': len(text),
        'word_count': len(text.split()),
        'avg_word_length': sum(len(word) for word in text.split()) / max(len(text.split()), 1),
        'caps_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
        'punctuation_ratio': sum(1 for c in text if c in '.,!?;:') / max(len(text), 1),
        'exclamation_count': text.count('!'),
        'question_count': text.count('?'),
        'url_count': len(re.findall(r'http[s]?://\S+', text)),
    }
    
    return features


def validate_text(text: str, min_length: int = 10, max_length: int = 50000) -> tuple[bool, Optional[str]]:
    """
    Validate if text is suitable for prediction
    
    Args:
        text: Input text to validate
        min_length: Minimum text length
        max_length: Maximum text length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text:
        return False, "Text is empty"
    
    if not isinstance(text, str):
        return False, "Text must be a string"
    
    if len(text.strip()) < min_length:
        return False, f"Text too short (minimum {min_length} characters)"
    
    if len(text) > max_length:
        return False, f"Text too long (maximum {max_length} characters)"
    
    # Check if text has enough words
    word_count = len(text.split())
    if word_count < 3:
        return False, "Text must contain at least 3 words"
    
    return True, None
