"""
Image text extraction using OCR for fake news detection.
Supports processing screenshots and photos of news articles.
"""

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


class ImageTextExtractor:
    """Extract text from images using OCR"""
    
    def __init__(self, method='easyocr', languages=['en']):
        """
        Initialize OCR engine
        
        Args:
            method: 'easyocr' or 'tesseract'
            languages: List of language codes
        """
        self.method = method
        self.languages = languages
        
        if method == 'easyocr' and EASYOCR_AVAILABLE:
            self.reader = easyocr.Reader(languages)
        elif method == 'tesseract' and not TESSERACT_AVAILABLE:
            raise ImportError("pytesseract not installed. Run: pip install pytesseract Pillow")
        elif method == 'easyocr' and not EASYOCR_AVAILABLE:
            raise ImportError("easyocr not installed. Run: pip install easyocr")
    
    def extract_text(self, image_path):
        """
        Extract text from image
        
        Args:
            image_path: Path to image file or image bytes
            
        Returns:
            dict: {
                'text': extracted text,
                'confidence': average confidence score,
                'method': OCR method used
            }
        """
        if self.method == 'easyocr':
            return self._extract_with_easyocr(image_path)
        elif self.method == 'tesseract':
            return self._extract_with_tesseract(image_path)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def _extract_with_easyocr(self, image_path):
        """Extract text using EasyOCR"""
        result = self.reader.readtext(image_path)
        
        # Combine all detected text
        text_parts = []
        confidences = []
        
        for detection in result:
            bbox, text, confidence = detection
            text_parts.append(text)
            confidences.append(confidence)
        
        full_text = ' '.join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'text': full_text,
            'confidence': avg_confidence,
            'method': 'easyocr',
            'detections': len(result)
        }
    
    def _extract_with_tesseract(self, image_path):
        """Extract text using Tesseract OCR"""
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        # Get confidence data
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data['conf'] if conf != '-1']
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'text': text.strip(),
            'confidence': avg_confidence / 100,  # Convert to 0-1 scale
            'method': 'tesseract',
            'detections': len(confidences)
        }


# Convenience functions
def extract_text_from_image(image_path, method='easyocr'):
    """
    Quick function to extract text from image
    
    Args:
        image_path: Path to image
        method: 'easyocr' or 'tesseract'
        
    Returns:
        str: Extracted text
    """
    extractor = ImageTextExtractor(method=method)
    result = extractor.extract_text(image_path)
    return result['text']


if __name__ == '__main__':
    # Test OCR
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python image_processor.py <image_path>")
        print("\nExample:")
        print("  python image_processor.py screenshot.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    print("Extracting text from image...")
    try:
        extractor = ImageTextExtractor(method='easyocr')
        result = extractor.extract_text(image_path)
        
        print(f"\n{'='*60}")
        print(f"Method: {result['method']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Detections: {result['detections']}")
        print(f"{'='*60}")
        print(f"\nExtracted Text:\n{result['text']}")
        print(f"{'='*60}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have installed:")
        print("  pip install easyocr")
        print("  or")
        print("  pip install pytesseract Pillow")
