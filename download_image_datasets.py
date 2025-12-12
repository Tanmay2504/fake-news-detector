"""
Download and Prepare Image Datasets for Fake News Detection
"""

import os
import requests
import pandas as pd
from pathlib import Path
import json
from tqdm import tqdm
import zipfile
import shutil

class ImageDatasetDownloader:
    def __init__(self, base_dir="datasets/images"):
        self.base_dir = Path(base_dir)
        self.create_directory_structure()
    
    def create_directory_structure(self):
        """Create organized folder structure"""
        folders = [
            "real/train", "real/test", "real/val",
            "fake/train", "fake/test", "fake/val",
            "ai_generated/dall-e", "ai_generated/midjourney", "ai_generated/stable-diffusion",
            "manipulated/photoshopped", "manipulated/spliced",
            "../metadata"
        ]
        
        for folder in folders:
            (self.base_dir / folder).mkdir(parents=True, exist_ok=True)
        
        print("✅ Directory structure created")
    
    def check_constraint_dataset(self):
        """Check if Constraint dataset has image URLs"""
        print("\n🔍 Checking Constraint dataset...")
        
        try:
            train_df = pd.read_csv('datasets/Constraint_Train.csv')
            test_df = pd.read_csv('datasets/Constraint_Test.csv')
            
            print(f"\nTrain dataset columns: {list(train_df.columns)}")
            print(f"Train dataset shape: {train_df.shape}")
            print(f"\nFirst few rows:")
            print(train_df.head())
            
            # Check for image URLs or paths
            image_cols = [col for col in train_df.columns if 'image' in col.lower() or 'url' in col.lower()]
            if image_cols:
                print(f"\n✅ Found image columns: {image_cols}")
                print(f"\nSample image URLs:")
                print(train_df[image_cols].head())
                return True, image_cols
            else:
                print("\n❌ No image columns found in Constraint dataset")
                return False, []
                
        except Exception as e:
            print(f"❌ Error reading Constraint dataset: {e}")
            return False, []
    
    def download_cifake_instructions(self):
        """Provide instructions for CIFAKE dataset"""
        print("\n📥 CIFAKE Dataset (Best for AI-Generated Images)")
        print("=" * 60)
        print("1. Go to: https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images")
        print("2. Click 'Download' (requires Kaggle account)")
        print("3. Extract to: datasets/images/cifake/")
        print("4. Run: python organize_cifake.py")
        print("\nDataset Info:")
        print("  - 60,000 real images (from CIFAR-10)")
        print("  - 60,000 AI-generated images (from Stable Diffusion)")
        print("  - 32x32 resolution")
        print("  - Perfect for training AI detection models")
    
    def download_from_kaggle(self, dataset_name, output_path):
        """
        Download dataset from Kaggle using Kaggle API
        Requires: pip install kaggle
        """
        try:
            import kaggle
            print(f"\n📥 Downloading {dataset_name} from Kaggle...")
            
            # Example: kaggle.api.dataset_download_files('birdy654/cifake-real-and-ai-generated-synthetic-images')
            kaggle.api.dataset_download_files(dataset_name, path=output_path, unzip=True)
            print(f"✅ Downloaded to {output_path}")
            
        except ImportError:
            print("\n❌ Kaggle API not installed")
            print("Install with: pip install kaggle")
            print("\nSetup instructions:")
            print("1. Create Kaggle account: https://www.kaggle.com")
            print("2. Go to: https://www.kaggle.com/settings")
            print("3. Click 'Create New API Token'")
            print("4. Move kaggle.json to: ~/.kaggle/kaggle.json (Linux/Mac)")
            print("   or C:\\Users\\YourName\\.kaggle\\kaggle.json (Windows)")
        except Exception as e:
            print(f"❌ Error downloading: {e}")
    
    def create_sample_dataset(self, num_samples=100):
        """Create a small sample dataset for testing"""
        print(f"\n🎨 Creating sample dataset with {num_samples} images...")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            import random
            
            labels_data = []
            
            # Create fake images
            for i in range(num_samples // 2):
                # Create random colored image
                img = Image.new('RGB', (256, 256), 
                              color=(random.randint(0, 255), 
                                   random.randint(0, 255), 
                                   random.randint(0, 255)))
                
                draw = ImageDraw.Draw(img)
                draw.text((10, 10), f"FAKE {i}", fill=(255, 255, 255))
                
                # Save to train/test/val
                split = 'train' if i < num_samples * 0.7 / 2 else ('test' if i < num_samples * 0.9 / 2 else 'val')
                img_path = self.base_dir / f"fake/{split}/fake_{i}.png"
                img.save(img_path)
                
                labels_data.append({
                    'image_path': str(img_path),
                    'label': 'fake',
                    'split': split
                })
            
            # Create real images
            for i in range(num_samples // 2):
                img = Image.new('RGB', (256, 256), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)
                draw.text((10, 10), f"REAL {i}", fill=(0, 0, 0))
                
                split = 'train' if i < num_samples * 0.7 / 2 else ('test' if i < num_samples * 0.9 / 2 else 'val')
                img_path = self.base_dir / f"real/{split}/real_{i}.png"
                img.save(img_path)
                
                labels_data.append({
                    'image_path': str(img_path),
                    'label': 'real',
                    'split': split
                })
            
            # Save labels CSV
            labels_df = pd.DataFrame(labels_data)
            labels_path = self.base_dir / '../metadata/labels.csv'
            labels_df.to_csv(labels_path, index=False)
            
            print(f"✅ Created {num_samples} sample images")
            print(f"✅ Saved labels to: {labels_path}")
            print(f"\nDataset split:")
            print(labels_df['split'].value_counts())
            
        except Exception as e:
            print(f"❌ Error creating sample dataset: {e}")
    
    def show_dataset_sources(self):
        """Display all available dataset sources"""
        print("\n📊 AVAILABLE IMAGE DATASETS FOR DOWNLOAD")
        print("=" * 60)
        
        datasets = [
            {
                "name": "CIFAKE (Real + AI Images)",
                "size": "120,000 images",
                "kaggle": "birdy654/cifake-real-and-ai-generated-synthetic-images",
                "best_for": "AI-generated detection"
            },
            {
                "name": "140k Real and Fake Faces",
                "size": "140,000 images",
                "kaggle": "xhlulu/140k-real-and-fake-faces",
                "best_for": "Deepfake detection"
            },
            {
                "name": "Fake and Real News Dataset",
                "size": "~40,000 articles with images",
                "kaggle": "clmentbisaillon/fake-and-real-news-dataset",
                "best_for": "News context classification"
            },
            {
                "name": "CASIA v2.0 Tampered Images",
                "size": "12,614 images",
                "github": "namtpham/casia2groundtruth",
                "best_for": "Manipulation detection"
            }
        ]
        
        for idx, ds in enumerate(datasets, 1):
            print(f"\n{idx}. {ds['name']}")
            print(f"   Size: {ds['size']}")
            print(f"   Best for: {ds['best_for']}")
            if 'kaggle' in ds:
                print(f"   Kaggle: https://www.kaggle.com/datasets/{ds['kaggle']}")
            if 'github' in ds:
                print(f"   GitHub: https://github.com/{ds['github']}")
        
        print("\n" + "=" * 60)
        print("\n💡 QUICK START OPTIONS:")
        print("1. Download CIFAKE from Kaggle (recommended for beginners)")
        print("2. Use sample dataset generator (for testing pipeline)")
        print("3. Check Constraint dataset for existing images")


if __name__ == "__main__":
    print("🚀 Image Dataset Downloader for Fake News Detection")
    print("=" * 60)
    
    downloader = ImageDatasetDownloader()
    
    # Check existing Constraint dataset
    has_images, image_cols = downloader.check_constraint_dataset()
    
    # Show all available datasets
    downloader.show_dataset_sources()
    
    print("\n📋 WHAT WOULD YOU LIKE TO DO?")
    print("=" * 60)
    print("1. Create sample dataset (100 images for testing)")
    print("2. Show CIFAKE download instructions")
    print("3. Download from Kaggle (requires API setup)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        num_samples = input("Number of sample images (default 100): ").strip()
        num_samples = int(num_samples) if num_samples else 100
        downloader.create_sample_dataset(num_samples)
        
    elif choice == "2":
        downloader.download_cifake_instructions()
        
    elif choice == "3":
        print("\nAvailable Kaggle datasets:")
        print("1. CIFAKE (birdy654/cifake-real-and-ai-generated-synthetic-images)")
        print("2. 140k Faces (xhlulu/140k-real-and-fake-faces)")
        
        dataset = input("\nEnter dataset name or number: ").strip()
        if dataset == "1":
            dataset = "birdy654/cifake-real-and-ai-generated-synthetic-images"
        elif dataset == "2":
            dataset = "xhlulu/140k-real-and-fake-faces"
        
        output = input("Output path (default: datasets/images/downloaded): ").strip()
        output = output if output else "datasets/images/downloaded"
        
        downloader.download_from_kaggle(dataset, output)
    
    print("\n✅ Done! Check IMAGE_DATASETS_GUIDE.md for more information")
