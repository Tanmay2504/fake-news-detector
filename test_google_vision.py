"""
Test if Google Cloud Vision API is working
"""
import os
from pathlib import Path

# Set credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-vision-credentials.json'

try:
    from google.cloud import vision
    
    # Create client
    client = vision.ImageAnnotatorClient()
    
    # Test with a simple image - create a small test image
    from PIL import Image
    import io
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Test label detection
    image = vision.Image(content=img_byte_arr.read())
    response = client.label_detection(image=image)
    
    if response.error.message:
        print(f"❌ Google Cloud Vision API Error: {response.error.message}")
        print("\nPossible reasons:")
        print("1. Billing is not enabled for this project")
        print("2. Vision API is not enabled")
        print("3. Service account doesn't have proper permissions")
        print("\nTo fix:")
        print("1. Go to https://console.cloud.google.com/billing")
        print("2. Enable billing for project: linear-yen-479309-q7")
        print("3. Enable Vision API: https://console.cloud.google.com/apis/library/vision.googleapis.com")
    else:
        print("✅ Google Cloud Vision API is working!")
        print(f"\nLabels detected: {len(response.label_annotations)}")
        for label in response.label_annotations[:5]:
            print(f"  - {label.description} ({label.score:.2%})")
            
except ImportError:
    print("❌ google-cloud-vision package not installed")
    print("\nInstall with:")
    print("pip install google-cloud-vision")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\nError type: {type(e).__name__}")
