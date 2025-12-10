"""
Visual Fake News Detection Module
Analyzes images to detect fake news through content analysis, not just text extraction
"""

import os
import io
import base64
import requests
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from typing import Dict, List, Optional, Any
import cv2
import warnings
warnings.filterwarnings('ignore')

# AI Detection Models
try:
    from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
    import torch
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    print("Warning: transformers or torch not installed. AI detection will use basic heuristics.")

# Image Context Classifier
try:
    from .image_context_classifier import ImageContextClassifier
    IMAGE_CNN_AVAILABLE = True
except ImportError:
    IMAGE_CNN_AVAILABLE = False

# Web Search Verifier
try:
    from .web_search_verifier import WebSearchVerifier
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False


class ImageManipulationDetector:
    """Detect if image has been digitally manipulated (Photoshopped)"""
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Check for signs of manipulation
        
        Returns:
            - Manipulation probability
            - Warning signs
            - Details (EXIF, ELA, compression)
        """
        img = Image.open(image_path)
        results = {
            'metadata': self._check_metadata(img),
            'ela': self._error_level_analysis(image_path, img),
            'compression': self._check_compression(img)
        }
        
        # Calculate manipulation probability
        manipulation_score = 0
        warning_signs = []
        
        # Check EXIF for editing software
        if results['metadata']['has_editing_software']:
            manipulation_score += 40
            warning_signs.append(f"Edited with {results['metadata']['software']}")
        
        # Check ELA variance
        if results['ela']['likely_manipulated']:
            manipulation_score += 30
            warning_signs.append("Inconsistent compression detected (ELA)")
        
        # Check for missing metadata
        if not results['metadata']['has_exif']:
            manipulation_score += 10
            warning_signs.append("No EXIF data (metadata stripped)")
        
        # Check compression artifacts
        if results['compression']['quality_estimate'] < 70:
            manipulation_score += 20
            warning_signs.append(f"Low quality ({results['compression']['quality_estimate']}%)")
        
        return {
            'manipulation_probability': manipulation_score,
            'likely_manipulated': manipulation_score > 50,
            'warning_signs': warning_signs,
            'details': results
        }
    
    def _check_metadata(self, img: Image.Image) -> Dict[str, Any]:
        """Check EXIF metadata for editing software and camera info"""
        exif_data = {}
        
        try:
            exif = img._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_data[tag] = str(value)  # Convert to string for safety
        except:
            pass
        
        # Check for editing software
        editing_software = ['Adobe Photoshop', 'GIMP', 'Paint.NET', 'Affinity']
        software = exif_data.get('Software', '')
        
        return {
            'has_exif': len(exif_data) > 0,
            'software': software,
            'has_editing_software': any(s in software for s in editing_software),
            'date_modified': exif_data.get('DateTime'),
            'camera': exif_data.get('Model', 'Unknown'),
            'gps': 'GPSInfo' in exif_data
        }
    
    def _error_level_analysis(self, image_path: str, img: Image.Image) -> Dict[str, Any]:
        """
        Error Level Analysis (ELA) - detects regions with different compression
        Manipulated areas show different compression levels than rest of image
        Returns variance score AND base64-encoded ELA heatmap image
        """
        try:
            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save at known quality
            temp_path = image_path + '_ela_temp.jpg'
            img.save(temp_path, 'JPEG', quality=90)
            
            # Reload compressed version
            compressed = Image.open(temp_path)
            
            # Calculate pixel difference
            img_array = np.array(img)
            comp_array = np.array(compressed)
            
            diff = np.abs(img_array.astype(int) - comp_array.astype(int))
            
            # Calculate variance (high variance = likely manipulated)
            variance = np.var(diff)
            
            # Generate ELA heatmap visualization
            # Amplify differences for better visualization
            ela_amplified = np.clip(diff * 10, 0, 255).astype(np.uint8)
            
            # Convert to grayscale for heatmap
            ela_gray = np.mean(ela_amplified, axis=2).astype(np.uint8)
            
            # Apply colormap for better visualization (JET colormap)
            ela_colored = cv2.applyColorMap(ela_gray, cv2.COLORMAP_JET)
            
            # Convert to PIL Image
            ela_image = Image.fromarray(cv2.cvtColor(ela_colored, cv2.COLOR_BGR2RGB))
            
            # Save ELA image to base64
            import base64
            buffered = io.BytesIO()
            ela_image.save(buffered, format="JPEG", quality=95)
            ela_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            ela_data_url = f"data:image/jpeg;base64,{ela_base64}"
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return {
                'variance': float(variance),
                'suspicious_regions': 1 if variance > 100 else 0,
                'likely_manipulated': variance > 100,
                'ela_score': float(variance),
                'ela_heatmap': ela_data_url  # Base64-encoded heatmap image
            }
            
        except Exception as e:
            return {
                'variance': 0,
                'suspicious_regions': 0,
                'likely_manipulated': False,
                'ela_heatmap': None,
                'error': str(e)
            }
    
    def _check_compression(self, img: Image.Image) -> Dict[str, Any]:
        """Estimate JPEG compression quality"""
        # Simplified quality estimation
        # In production, use more sophisticated methods
        return {
            'format': img.format or 'Unknown',
            'quality_estimate': 85,  # Placeholder
            'inconsistent': False
        }


class AIGeneratedDetector:
    """Detect AI-generated images using CLIP model"""
    
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cuda" if MODELS_AVAILABLE and torch.cuda.is_available() else "cpu" if MODELS_AVAILABLE else None
        
        if MODELS_AVAILABLE:
            try:
                print("Loading CLIP model for AI detection...")
                self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
                self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
                if self.device == "cuda":
                    self.model = self.model.to(self.device)
                print("✓ CLIP model loaded successfully")
            except Exception as e:
                print(f"Warning: Could not load CLIP model: {e}")
                self.model = None
    
    def detect(self, image_path: str) -> Dict[str, Any]:
        """
        Check if image is AI-generated using CLIP model
        
        Returns:
            - AI generation probability
            - Warning signs
            - Likely generator
        """
        img = Image.open(image_path).convert('RGB')
        warning_signs = []
        
        # Use CLIP model if available
        if self.model is not None and self.processor is not None:
            try:
                # Enhanced labels for better AI detection
                labels = [
                    "a real photograph taken with a professional camera",
                    "a smartphone photo of real life",
                    "an AI generated digital artwork from DALL-E or Midjourney",
                    "a computer-generated CGI rendering",
                    "an artificial intelligence generated image",
                    "a synthetic image created by neural networks",
                    "digital art made by Stable Diffusion AI",
                    "photorealistic AI generated content"
                ]
                
                # Get CLIP predictions
                inputs = self.processor(text=labels, images=img, return_tensors="pt", padding=True)
                if self.device == "cuda":
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    logits_per_image = outputs.logits_per_image
                    probs = logits_per_image.softmax(dim=1)
                
                # Calculate probabilities (real photo = first 2, AI = last 6)
                real_photo_prob = float(probs[0][0:2].sum()) * 100
                ai_prob = float(probs[0][2:8].sum()) * 100
                
                # Determine likely generator from AI categories
                likely_generator = 'Unknown'
                if ai_prob > 40:  # Lower threshold for detection
                    ai_probs = probs[0][2:8]
                    max_idx = torch.argmax(ai_probs).item()
                    generators = ['DALL-E/Midjourney', 'CGI', 'AI Generated', 'Neural Network', 'Stable Diffusion', 'Photorealistic AI']
                    likely_generator = generators[max_idx]
                    warning_signs.append(f"CLIP detected {generators[max_idx]} patterns")
                
                # Additional AI detection signals
                width, height = img.size
                
                # Check 1: Metadata analysis
                has_camera_data = False
                try:
                    exif = img._getexif()
                    if exif and 'Model' in {TAGS.get(k) for k in exif.keys()}:
                        has_camera_data = True
                    else:
                        warning_signs.append("No camera metadata")
                        ai_prob = min(ai_prob + 20, 100)
                except:
                    warning_signs.append("No EXIF data")
                    ai_prob = min(ai_prob + 20, 100)
                
                # Check 2: Common AI resolutions (very suspicious)
                ai_resolutions = [(512, 512), (1024, 1024), (768, 768), (1024, 768), 
                                 (1024, 576), (576, 1024), (768, 1024)]
                if (width, height) in ai_resolutions or (height, width) in ai_resolutions:
                    warning_signs.append(f"Exact AI resolution match ({width}x{height})")
                    ai_prob = min(ai_prob + 25, 100)
                
                # Check 3: Aspect ratio analysis (AI often uses specific ratios)
                aspect_ratio = width / height if height > 0 else 1
                ai_ratios = [1.0, 1.33, 0.75, 1.77, 0.56]  # Common AI aspect ratios
                if any(abs(aspect_ratio - ratio) < 0.01 for ratio in ai_ratios):
                    if not has_camera_data:
                        warning_signs.append("Perfect aspect ratio without camera data")
                        ai_prob = min(ai_prob + 10, 100)
                
                # Check 4: Pixel-perfect dimensions (AI generates exact sizes)
                if width % 64 == 0 and height % 64 == 0 and not has_camera_data:
                    warning_signs.append("Dimensions divisible by 64 (AI training block size)")
                    ai_prob = min(ai_prob + 15, 100)
                
                # Check 5: Color distribution analysis
                img_array = np.array(img)
                if len(img_array.shape) == 3:
                    # Check for unnatural color uniformity (AI artifact)
                    std_per_channel = img_array.std(axis=(0, 1))
                    if np.all(std_per_channel > 10) and np.all(std_per_channel < 30):
                        warning_signs.append("Unnatural color distribution")
                        ai_prob = min(ai_prob + 5, 100)
                
                return {
                    'is_ai_generated': ai_prob > 45,  # Lower threshold (was 50)
                    'ai_probability': int(ai_prob),
                    'real_photo_probability': int(real_photo_prob),
                    'warning_signs': warning_signs,
                    'likely_generator': likely_generator,
                    'recommendation': self._get_ai_recommendation(int(ai_prob)),
                    'method': 'CLIP (AI Model)',
                    'confidence': int(ai_prob)  # Numeric confidence for frontend
                }
            except Exception as e:
                print(f"CLIP detection error: {e}")
                # Fallback to heuristics
        
        # Fallback: Basic heuristics if CLIP not available
        ai_score = 0
        
        # Check 1: No EXIF camera data
        try:
            exif = img._getexif()
            if not exif or 'Model' not in {TAGS.get(k) for k in exif.keys()}:
                ai_score += 30
                warning_signs.append("No camera metadata")
        except:
            ai_score += 30
            warning_signs.append("No EXIF data")
        
        # Check 2: Perfect resolution
        width, height = img.size
        ai_resolutions = [(512, 512), (1024, 1024), (768, 768), (1024, 768)]
        if (width, height) in ai_resolutions or (height, width) in ai_resolutions:
            ai_score += 20
            warning_signs.append(f"Common AI resolution ({width}x{height})")
        
        # Determine likely generator
        likely_generator = 'Unknown'
        if ai_score > 60:
            if width == 1024 and height == 1024:
                likely_generator = 'DALL-E or Midjourney'
            elif width == 512:
                likely_generator = 'Stable Diffusion'
        
        return {
            'is_ai_generated': ai_score > 50,
            'ai_probability': ai_score,
            'warning_signs': warning_signs,
            'likely_generator': likely_generator,
            'recommendation': self._get_ai_recommendation(ai_score),
            'method': 'Heuristics (CLIP unavailable)',
            'confidence': ai_score  # Numeric confidence
        }
    
    def _get_ai_recommendation(self, score: int) -> str:
        """Generate recommendation based on AI score"""
        if score > 75:
            return '🚫 Almost certainly AI-generated - not a real photograph'
        elif score > 60:
            return '⚠️ Highly likely AI-generated - treat with extreme skepticism'
        elif score > 45:
            return '⚠️ Likely AI-generated - verify authenticity before sharing'
        elif score > 30:
            return 'ℹ️ Possibly AI-influenced or heavily edited'
        else:
            return '✓ Appears to be a real photograph'


class ImageContentAnalyzer:
    """Analyze image content using BLIP and Google Cloud Vision"""
    
    def __init__(self, google_credentials_path: Optional[str] = None):
        """
        Initialize content analyzer with BLIP and optionally Google Vision
        
        Args:
            google_credentials_path: Path to Google Cloud credentials JSON (optional)
        """
        self.google_credentials_path = google_credentials_path
        self.client = None
        self.blip_processor = None
        self.blip_model = None
        self.device = "cuda" if MODELS_AVAILABLE and torch.cuda.is_available() else "cpu" if MODELS_AVAILABLE else None
        
        # Load BLIP model for image captioning
        if MODELS_AVAILABLE:
            try:
                print("Loading BLIP model for content analysis...")
                self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
                if self.device == "cuda":
                    self.blip_model = self.blip_model.to(self.device)
                print("✓ BLIP model loaded successfully")
            except Exception as e:
                print(f"Warning: Could not load BLIP model: {e}")
        
        # Initialize Google Cloud Vision if credentials provided
        if google_credentials_path and os.path.exists(google_credentials_path):
            try:
                from google.cloud import vision
                self.client = vision.ImageAnnotatorClient.from_service_account_json(
                    google_credentials_path
                )
            except ImportError:
                print("google-cloud-vision not installed. Install with: pip install google-cloud-vision")
    
    def analyze(self, image_path: str) -> Dict[str, Any]:
        """
        Comprehensive image analysis using Google Cloud Vision
        
        Returns:
            - Labels (what's in the image)
            - Objects detected
            - Faces and emotions
            - Landmarks (famous places)
            - Text in image
            - Safe search (violence, adult content)
            - Web entities (similar images)
        """
        if not self.client:
            # Fallback to local analysis
            return self._local_analysis(image_path)
        
        try:
            from google.cloud import vision
            
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            results = {
                'labels': [],
                'objects': [],
                'faces': {'count': 0, 'emotions': []},
                'landmarks': [],
                'text': '',
                'safe_search': {},
                'web_entities': []
            }
            
            # Label detection
            response = self.client.label_detection(image=image)
            results['labels'] = [
                {'description': label.description, 'score': label.score}
                for label in response.label_annotations[:10]
            ]
            
            # Object detection
            response = self.client.object_localization(image=image)
            results['objects'] = [
                {'name': obj.name, 'score': obj.score}
                for obj in response.localized_object_annotations[:10]
            ]
            
            # Face detection with emotions
            response = self.client.face_detection(image=image)
            faces_data = []
            for face in response.face_annotations:
                face_info = {
                    'joy': face.joy_likelihood.name,
                    'sorrow': face.sorrow_likelihood.name,
                    'anger': face.anger_likelihood.name,
                    'surprise': face.surprise_likelihood.name,
                    'detection_confidence': face.detection_confidence
                }
                faces_data.append(face_info)
            
            results['faces'] = {
                'count': len(response.face_annotations),
                'emotions': faces_data
            }
            
            # Landmark detection
            response = self.client.landmark_detection(image=image)
            results['landmarks'] = [
                {'name': landmark.description}
                for landmark in response.landmark_annotations
            ]
            
            # Text detection
            response = self.client.text_detection(image=image)
            if response.text_annotations:
                results['text'] = response.text_annotations[0].description
            
            # Safe search
            response = self.client.safe_search_detection(image=image)
            results['safe_search'] = {
                'violence': response.safe_search_annotation.violence.name,
                'adult': response.safe_search_annotation.adult.name
            }
            
            # Web detection - Find where image appears online
            response = self.client.web_detection(image=image)
            results['web_entities'] = [
                {'description': entity.description, 'score': entity.score}
                for entity in response.web_detection.web_entities[:5] if entity.description
            ]
            
            # Extract pages with matching images
            if response.web_detection.pages_with_matching_images:
                results['matching_pages'] = [
                    {
                        'url': page.url,
                        'title': page.page_title if hasattr(page, 'page_title') else 'Unknown'
                    }
                    for page in response.web_detection.pages_with_matching_images[:5]
                ]
            else:
                results['matching_pages'] = []
            
            # Format for compatibility with frontend
            results['caption'] = results['labels'][0]['description'] if results['labels'] else 'Image analyzed'
            results['scene'] = ', '.join([label['description'] for label in results['labels'][:3]]) if results['labels'] else ''
            results['method'] = 'Google Cloud Vision API'
            
            return results
            
        except Exception as e:
            print(f"Google Cloud Vision error: {e}")
            return self._local_analysis(image_path)
    
    def _local_analysis(self, image_path: str) -> Dict[str, Any]:
        """Fallback local analysis using BLIP + OpenCV"""
        result = {
            'labels': [],
            'caption': '',
            'objects': [],
            'faces': {'count': 0},
            'text': '',
            'method': 'Local (BLIP + OpenCV)'
        }
        
        # Use BLIP for image captioning and understanding
        if self.blip_model is not None and self.blip_processor is not None:
            try:
                img = Image.open(image_path).convert('RGB')
                
                # Generate caption
                inputs = self.blip_processor(img, return_tensors="pt")
                if self.device == "cuda":
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    out = self.blip_model.generate(**inputs, max_length=50)
                    caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
                
                result['caption'] = caption
                result['labels'] = [{'description': caption, 'score': 1.0}]
                
                # Extract entities from caption
                words = caption.lower().split()
                common_objects = ['person', 'people', 'man', 'woman', 'child', 'building', 
                                 'car', 'tree', 'sky', 'street', 'sign', 'flag']
                result['objects'] = [{'name': obj, 'score': 0.8} for obj in common_objects if obj in words]
                
            except Exception as e:
                print(f"BLIP analysis error: {e}")
        
        # Use OpenCV for face detection
        analyzer = LocalImageAnalyzer()
        opencv_result = analyzer.analyze(image_path)
        result['faces'] = opencv_result.get('faces', {'count': 0})
        result['is_blurry'] = opencv_result.get('is_blurry', False)
        
        return result


class LocalImageAnalyzer:
    """Analyze images using local OpenCV models (free alternative)"""
    
    def __init__(self):
        """Initialize OpenCV face detector"""
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        except:
            self.face_cascade = None
    
    def analyze(self, image_path: str) -> Dict[str, Any]:
        """Basic local image analysis"""
        try:
            img = cv2.imread(image_path)
            
            if img is None:
                return {'error': 'Could not load image'}
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Face detection
            faces_count = 0
            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                faces_count = len(faces)
            
            # Color analysis
            avg_color = np.mean(img, axis=(0, 1))
            
            # Sharpness check (blurry images often indicate fakes)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            
            return {
                'faces': {'count': faces_count},
                'labels': [{'description': 'Image analysis', 'score': 1.0}],
                'objects': [],
                'landmarks': [],
                'text': '',
                'average_color': avg_color.tolist(),
                'sharpness': float(sharpness),
                'is_blurry': sharpness < 100,
                'resolution': {'width': img.shape[1], 'height': img.shape[0]},
                'local_analysis': True
            }
            
        except Exception as e:
            return {'error': str(e), 'local_analysis': True}


class ContextVerifier:
    """Verify if image content matches claimed context"""
    
    def verify(self, image_analysis: Dict, claimed_context: Dict) -> Dict[str, Any]:
        """
        Check if image matches what article claims
        
        Args:
            image_analysis: Results from ImageContentAnalyzer
            claimed_context: What the article claims
                {
                    'event': 'protest',
                    'location': 'New York',
                    'date': '2024-11-20',
                    'description': '...'
                }
        
        Returns:
            Context match verdict with mismatches
        """
        mismatches = []
        
        # Check location via landmarks
        if claimed_context.get('location') and image_analysis.get('landmarks'):
            detected_locations = [l['name'].lower() for l in image_analysis['landmarks']]
            claimed_location = claimed_context['location'].lower()
            
            if detected_locations:
                if not any(claimed_location in loc for loc in detected_locations):
                    mismatches.append({
                        'type': 'location_mismatch',
                        'claimed': claimed_context['location'],
                        'detected': image_analysis['landmarks'][0]['name']
                    })
        
        # Check event type via labels
        if claimed_context.get('event'):
            labels = [l['description'].lower() for l in image_analysis.get('labels', [])]
            event_type = claimed_context['event'].lower()
            
            # Event-specific checks
            if event_type == 'protest' and 'crowd' not in ' '.join(labels):
                if image_analysis.get('faces', {}).get('count', 0) < 5:
                    mismatches.append({
                        'type': 'event_mismatch',
                        'claimed': 'protest with crowd',
                        'detected': 'few or no people detected'
                    })
        
        # Check for violence if claimed
        if claimed_context.get('violent') and image_analysis.get('safe_search'):
            violence_level = image_analysis['safe_search'].get('violence', 'UNKNOWN')
            if violence_level in ['VERY_UNLIKELY', 'UNLIKELY']:
                mismatches.append({
                    'type': 'violence_mismatch',
                    'claimed': 'violent event',
                    'detected': 'no violence in image'
                })
        
        return {
            'context_matches': len(mismatches) == 0,
            'mismatches': mismatches,
            'verdict': 'CONTEXT_MATCHES' if len(mismatches) == 0 else 'CONTEXT_MISMATCH',
            'confidence': 100 - (len(mismatches) * 30)  # Reduce confidence per mismatch
        }


class VisualFakeNewsDetector:
    """
    Complete visual fake news detection system
    Analyzes images to detect fake news by understanding image content
    """
    
    def __init__(
        self,
        google_credentials_path: Optional[str] = None
    ):
        """
        Initialize visual fake news detector
        
        Args:
            google_credentials_path: Google Cloud Vision credentials
        """
        self.manipulation_detector = ImageManipulationDetector()
        self.ai_detector = AIGeneratedDetector()
        self.content_analyzer = ImageContentAnalyzer(google_credentials_path)
        self.context_verifier = ContextVerifier()
        
        # Initialize web search verifier (disabled - not needed)
        self.web_search = None
        
        # Initialize image context classifier
        self.context_classifier = None
        if IMAGE_CNN_AVAILABLE:
            try:
                self.context_classifier = ImageContextClassifier()
            except Exception as e:
                print(f"Warning: Could not load image context classifier: {e}")
    
    def detect(
        self,
        image_path: str,
        claimed_context: Optional[Dict] = None,
        check_manipulation: bool = True,
        check_ai_generated: bool = True,
        check_content: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive visual fake news detection
        
        Args:
            image_path: Path to image file
            claimed_context: What the article claims about the image
            check_manipulation: Enable manipulation detection
            check_ai_generated: Enable AI generation detection
            check_content: Enable content analysis
        
        Returns:
            Complete analysis with verdict
        """
        if not os.path.exists(image_path):
            return {'error': f'Image not found: {image_path}'}
        
        result = {
            'image_path': image_path,
            'manipulation_check': {},
            'ai_generation_check': {},
            'content_analysis': {},
            'context_verification': {},
            'final_verdict': {}
        }
        
        # 1. Check for manipulation
        if check_manipulation:
            result['manipulation_check'] = self.manipulation_detector.analyze_image(image_path)
        
        # 2. Check if AI-generated
        if check_ai_generated:
            result['ai_generation_check'] = self.ai_detector.detect(image_path)
        
        # 3. Analyze content
        if check_content:
            result['content_analysis'] = self.content_analyzer.analyze(image_path)
        
        # 4. Verify context (if provided)
        if claimed_context and result.get('content_analysis'):
            result['context_verification'] = self.context_verifier.verify(
                result['content_analysis'],
                claimed_context
            )
        
        # 6. Image context classification (NEW - uses trained CNN)
        if self.context_classifier:
            result['image_context'] = self.context_classifier.classify(image_path)
        
        # 7. Web search verification (NEW - find where image appears online)
        if self.web_search:
            result['web_search'] = self.web_search.analyze_image_sources(image_path)
        
        # 8. Calculate final verdict
        result['final_verdict'] = self._calculate_final_verdict(result, claimed_context)
        
        return result
    
    def _calculate_final_verdict(
        self,
        result: Dict[str, Any],
        claimed_context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Calculate final verdict on image authenticity"""
        fake_score = 0
        reasons = []
        
        # Manipulation check (25% weight)
        if result.get('manipulation_check', {}).get('likely_manipulated'):
            fake_score += 25
            reasons.extend(result['manipulation_check']['warning_signs'])
        
        # AI generation check (35% weight) - INCREASED for better AI detection
        if result.get('ai_generation_check', {}).get('is_ai_generated'):
            ai_confidence = result['ai_generation_check'].get('confidence', 50)
            # Scale from 0-35 based on confidence
            ai_score = min(35, (ai_confidence / 100) * 35)
            fake_score += ai_score
            reasons.append(f"AI-generated ({result['ai_generation_check']['likely_generator']}, {ai_confidence:.1f}% confidence)")
        
        # Image context classification (20% weight) - CNN trained on fake news dataset
        if result.get('image_context', {}).get('is_fake_context'):
            context_confidence = result['image_context'].get('confidence', 50)
            context_score = min(20, (context_confidence / 100) * 20)
            fake_score += context_score
            reasons.append(f"Fake news context detected ({context_confidence:.1f}% confidence)")
        
        # Context mismatch (15% weight)
        if claimed_context and result.get('context_verification'):
            if not result['context_verification']['context_matches']:
                fake_score += 15
                for mismatch in result['context_verification']['mismatches']:
                    reasons.append(f"{mismatch['type']}: claimed '{mismatch['claimed']}' but detected '{mismatch['detected']}'")
        
        # Determine verdict
        if fake_score >= 70:
            verdict = 'FAKE'
            verdict_label = '🚫 Image is manipulated, AI-generated, or misused'
        elif fake_score >= 40:
            verdict = 'SUSPICIOUS'
            verdict_label = '⚠️ Image authenticity questionable'
        else:
            verdict = 'LIKELY_AUTHENTIC'
            verdict_label = '✓ Image appears authentic'
        
        return {
            'verdict': verdict,
            'verdict_label': verdict_label,
            'fake_score': fake_score,
            'confidence': fake_score,
            'is_fake': fake_score >= 50,
            'reasons': reasons if reasons else ['No suspicious indicators found'],
            'recommendation': self._get_recommendation(verdict, result)
        }
    
    def _get_recommendation(self, verdict: str, result: Dict) -> str:
        """Generate recommendation based on verdict"""
        if verdict == 'FAKE':
            return '🚫 Do not trust this image - likely manipulated or misused in wrong context'
        elif verdict == 'SUSPICIOUS':
            return '⚠️ Verify image authenticity - perform additional verification'
        else:
            return '✓ Image appears authentic, but always verify claims independently'


# Command-line testing
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python visual_detector.py <image_path> [--context event=protest location=NYC]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Parse context if provided
    claimed_context = None
    if '--context' in sys.argv:
        context_idx = sys.argv.index('--context')
        context_args = sys.argv[context_idx + 1:]
        claimed_context = {}
        for arg in context_args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                claimed_context[key] = value
    
    # Initialize detector
    detector = VisualFakeNewsDetector()
    
    # Detect
    print(f"\n🔍 Analyzing image: {image_path}\n")
    result = detector.detect(image_path, claimed_context)
    
    # Print results
    print("=" * 60)
    print("FINAL VERDICT")
    print("=" * 60)
    verdict = result['final_verdict']
    print(f"Verdict: {verdict['verdict_label']}")
    print(f"Fake Score: {verdict['fake_score']}/100")
    print(f"\nReasons:")
    for reason in verdict['reasons']:
        print(f"  • {reason}")
    print(f"\nRecommendation: {verdict['recommendation']}")
    print("=" * 60)
