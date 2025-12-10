"""
Image Context Classifier
Uses trained CNN to classify if image is from fake/real news article
"""

import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
from typing import Dict, Any
from pathlib import Path


class FakeNewsImageCNN(nn.Module):
    """Same architecture as training script"""
    def __init__(self):
        super(FakeNewsImageCNN, self).__init__()
        
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)
        
        self.fc1 = nn.Linear(256 * 4 * 4, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 2)
        
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        
        x = x.view(-1, 256 * 4 * 4)
        
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x


class ImageContextClassifier:
    """Classifies if image is from fake or real news article"""
    
    def __init__(self, model_path: str = "models/image_cnn.pth"):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.model_loaded = False
        
        # Load model if exists
        if Path(model_path).exists():
            try:
                self.model = FakeNewsImageCNN().to(self.device)
                checkpoint = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.model.eval()
                self.model_loaded = True
                print(f"✓ Image CNN loaded (Accuracy: {checkpoint.get('accuracy', 'N/A')}%)")
            except Exception as e:
                print(f"Warning: Could not load image CNN: {e}")
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def classify(self, image_path: str) -> Dict[str, Any]:
        """
        Classify if image is from fake or real news article
        
        Returns:
            {
                'is_fake_context': bool,
                'confidence': float (0-100),
                'fake_probability': float (0-100),
                'real_probability': float (0-100),
                'verdict': str,
                'recommendation': str
            }
        """
        if not self.model_loaded:
            return {
                'available': False,
                'message': 'Image context classifier not available. Train the model first.'
            }
        
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Predict
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
                
                real_prob = float(probabilities[0]) * 100
                fake_prob = float(probabilities[1]) * 100
                
                predicted_class = 1 if fake_prob > real_prob else 0
                confidence = max(real_prob, fake_prob)
            
            # Generate verdict
            if fake_prob > 80:
                verdict = "FAKE_CONTEXT"
                verdict_label = "⚠️ Image likely from fake news article"
                recommendation = "🚫 This image appears in fake news contexts"
            elif fake_prob > 60:
                verdict = "SUSPICIOUS_CONTEXT"
                verdict_label = "⚠️ Image possibly from unreliable source"
                recommendation = "⚠️ Verify the source of this image"
            elif real_prob > 80:
                verdict = "AUTHENTIC_CONTEXT"
                verdict_label = "✓ Image likely from authentic news"
                recommendation = "✓ Image appears in legitimate news contexts"
            else:
                verdict = "UNCERTAIN"
                verdict_label = "ℹ️ Context unclear"
                recommendation = "ℹ️ Unable to determine image context with confidence"
            
            return {
                'available': True,
                'is_fake_context': predicted_class == 1,
                'confidence': float(confidence),
                'fake_probability': float(fake_prob),
                'real_probability': float(real_prob),
                'verdict': verdict,
                'verdict_label': verdict_label,
                'recommendation': recommendation,
                'method': 'CNN (32x32 Image Classifier)'
            }
            
        except Exception as e:
            return {
                'available': False,
                'error': str(e)
            }
