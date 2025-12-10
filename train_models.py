"""
Sample training script for fake news detection models

This script shows how to train and save the three models (Random Forest, LightGBM, XGBoost)
that the API expects. Modify this to work with your dataset.
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier


def load_data():
    """
    Load your dataset here
    
    Expected format:
    - text: str (news article text)
    - label: int (0 = fake, 1 = real)
    
    Returns:
        X: array of text strings
        y: array of labels (0 or 1)
    """
    # Example: Load from CSV
    # df = pd.read_csv('your_dataset.csv')
    # X = df['text'].values
    # y = df['label'].values
    
    # For demonstration, create dummy data
    print("⚠ Using dummy data - replace with your actual dataset!")
    X = np.array([
        "SHOCKING: You won't believe this amazing discovery!!!",
        "According to the official report, the meeting concluded on Tuesday.",
        "BREAKING NEWS: Hidden truth revealed! They don't want you to know!",
        "The company announced quarterly earnings in a press release.",
        "Unbelievable miracle cure! Doctors hate this one simple trick!",
        "Research published in Nature shows promising results."
    ] * 100)  # Repeat for larger dataset
    
    y = np.array([0, 1, 0, 1, 0, 1] * 100)  # 0 = fake, 1 = real
    
    return X, y


def create_random_forest_pipeline():
    """Create Random Forest pipeline"""
    return Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True
        )),
        ('clf', RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ))
    ])


def create_lightgbm_pipeline():
    """Create LightGBM pipeline"""
    return Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True
        )),
        ('clf', LGBMClassifier(
            n_estimators=100,
            max_depth=10,
            learning_rate=0.1,
            random_state=42,
            verbose=-1
        ))
    ])


def create_xgboost_pipeline():
    """Create XGBoost pipeline"""
    return Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True
        )),
        ('clf', XGBClassifier(
            n_estimators=100,
            max_depth=10,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        ))
    ])


def train_and_save_model(name, pipeline, X_train, y_train, X_test, y_test):
    """Train model and save to disk"""
    print(f"\n{'='*60}")
    print(f"Training {name}...")
    print(f"{'='*60}")
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Training complete!")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))
    
    # Save model
    model_path = f'models/{name}.joblib'
    joblib.dump(pipeline, model_path)
    print(f"✓ Model saved to {model_path}")
    
    return accuracy


def main():
    """Train all three models"""
    print("="*60)
    print("Fake News Detection - Model Training")
    print("="*60)
    
    # Load data
    print("\nLoading dataset...")
    X, y = load_data()
    print(f"✓ Loaded {len(X)} samples")
    print(f"  Fake: {sum(y==0)} ({sum(y==0)/len(y)*100:.1f}%)")
    print(f"  Real: {sum(y==1)} ({sum(y==1)/len(y)*100:.1f}%)")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n✓ Train: {len(X_train)} samples")
    print(f"✓ Test:  {len(X_test)} samples")
    
    # Create models
    models = {
        'random_forest': create_random_forest_pipeline(),
        'lightgbm': create_lightgbm_pipeline(),
        'xgboost': create_xgboost_pipeline()
    }
    
    # Train all models
    results = {}
    for name, pipeline in models.items():
        accuracy = train_and_save_model(name, pipeline, X_train, y_train, X_test, y_test)
        results[name] = accuracy
    
    # Summary
    print("\n" + "="*60)
    print("Training Summary")
    print("="*60)
    for name, accuracy in results.items():
        print(f"{name:20s} {accuracy:.2%}")
    print(f"\nAverage Accuracy: {np.mean(list(results.values())):.2%}")
    print("="*60)
    print("\n✓ All models trained and saved!")
    print("\nYou can now start the API server:")
    print("  python main.py")


if __name__ == "__main__":
    main()
