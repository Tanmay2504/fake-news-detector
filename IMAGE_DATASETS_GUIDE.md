# Image Datasets for Fake News Detection

## 📊 Recommended Image Datasets

### 1. **FakeNewsNet** (Most Comprehensive)
- **Size**: ~23,000 images with news articles
- **Labels**: Real/Fake news images
- **Source**: https://github.com/KaiDMML/FakeNewsNet
- **Download**: 
```bash
git clone https://github.com/KaiDMML/FakeNewsNet.git
```

### 2. **MediaEval Fake News Dataset**
- **Size**: 20,000+ images
- **Labels**: Real/Fake, Manipulation detected
- **Source**: https://multimediaeval.github.io/

### 3. **COCO-Text + Fake Context**
- **Size**: 60,000+ images
- **Use**: For training CNN on real vs fake contexts
- **Source**: https://vision.cornell.edu/se3/coco-text-2/

### 4. **Constraint@AAAI 2021 Multimodal Dataset**
- **Size**: 10,000+ memes with images
- **Labels**: Real/Fake classification
- **Source**: https://constraintloc.github.io/
- **Already Have**: Constraint_Train.csv, Constraint_Test.csv (check if they have image URLs)

### 5. **Fakeddit (Reddit Fake News Images)**
- **Size**: 1 million+ submissions
- **Labels**: 2-way, 3-way, 6-way classification
- **Source**: https://github.com/entitize/Fakeddit

### 6. **AI-Generated Images Datasets**

#### DALL-E 2 Generated Images
- **Source**: https://huggingface.co/datasets/dalle-mini/dalle-mini

#### Midjourney/Stable Diffusion Detection
- **Dataset**: GenImage
- **Size**: 1.3M images
- **Source**: https://github.com/GenImage-Dataset/GenImage

#### CIFAKE (CIFAR-10 + AI Generated)
- **Size**: 120,000 images (60k real, 60k AI)
- **Source**: https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images

### 7. **Image Manipulation Datasets**

#### CASIA v2.0
- **Size**: 12,614 images
- **Labels**: Authentic vs Tampered
- **Source**: https://github.com/namtpham/casia2groundtruth

#### Columbia Uncompressed Image Splicing Detection
- **Size**: 933 authentic, 912 spliced
- **Source**: https://www.ee.columbia.edu/ln/dvmm/downloads/authsplcuncmp/

#### NIST Nimble Challenge 2016
- **Size**: Large-scale manipulation detection
- **Source**: https://www.nist.gov/itl/iad/mig/nimble-challenge-2017-evaluation

## 🚀 Quick Start - Download Script

Use the `download_image_datasets.py` script in this directory to automatically download and organize datasets.

## 📁 Recommended Folder Structure

```
datasets/
├── images/
│   ├── real/
│   │   ├── train/
│   │   ├── test/
│   │   └── val/
│   ├── fake/
│   │   ├── train/
│   │   ├── test/
│   │   └── val/
│   ├── ai_generated/
│   │   ├── dall-e/
│   │   ├── midjourney/
│   │   └── stable-diffusion/
│   └── manipulated/
│       ├── photoshopped/
│       └── spliced/
└── metadata/
    ├── labels.csv
    └── image_info.json
```

## 🎯 Training Recommendations

### For CNN Classifier (Fake Context Detection)
- **Minimum**: 10,000 images (5,000 real, 5,000 fake)
- **Recommended**: 50,000+ images
- **Use**: FakeNewsNet + Fakeddit

### For AI Generation Detection (CLIP Fine-tuning)
- **Minimum**: 5,000 AI images + 5,000 real
- **Recommended**: 50,000+ mixed
- **Use**: GenImage + CIFAKE

### For Manipulation Detection
- **Minimum**: 2,000 manipulated + 2,000 authentic
- **Recommended**: 10,000+ mixed
- **Use**: CASIA + Columbia dataset

## 📊 Current Dataset Status

Check your Constraint datasets - they may already contain image URLs:

```python
import pandas as pd

# Check if Constraint dataset has images
train_df = pd.read_csv('datasets/Constraint_Train.csv')
print(train_df.columns)
print(train_df.head())
```

## 🔗 Kaggle Datasets (Ready to Download)

1. **Fake and Real News Dataset**
   - https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

2. **CIFAKE - Real and AI-Generated Images**
   - https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images

3. **140k Real and Fake Faces**
   - https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces

4. **Deepfake Detection Challenge**
   - https://www.kaggle.com/c/deepfake-detection-challenge/data

## 💡 Tips

1. **Start Small**: Begin with 5,000-10,000 images to test your pipeline
2. **Balance Classes**: Keep equal numbers of real/fake images
3. **Augmentation**: Use image augmentation to expand your dataset
4. **Validation Split**: Always keep 20% for validation, 10% for testing
5. **Metadata**: Keep CSV files with labels, sources, and classifications

## 🛠️ Next Steps

1. Run `download_image_datasets.py` to start downloading
2. Check your Constraint datasets for existing image URLs
3. Organize images into the folder structure above
4. Run `train_image_models.py` to train the CNN classifier
5. Fine-tune CLIP model for AI detection
