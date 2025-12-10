"""
Train Real Models on Fake News Dataset
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')


def load_data():
    """
    Load Fake and True news datasets and combine them
    
    Returns:
        X: array of text strings
        y: array of labels (0 = fake, 1 = real)
    """
    print("Loading datasets...")
    
    # Load Fake news
    df_fake = pd.read_csv('datasets/Fake.csv')
    df_fake['label'] = 0  # 0 = fake
    
    # Load True news
    df_true = pd.read_csv('datasets/True.csv')
    df_true['label'] = 1  # 1 = real
    
    # Combine datasets
    df = pd.concat([df_fake, df_true], ignore_index=True)
    
    # Combine title and text for better predictions
    df['combined_text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
    
    # Remove very short texts
    df = df[df['combined_text'].str.len() > 50]
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    X = df['combined_text'].values
    y = df['label'].values
    
    print(f"✓ Loaded {len(X)} samples")
    print(f"  Fake: {sum(y==0)} ({sum(y==0)/len(y)*100:.1f}%)")
    print(f"  Real: {sum(y==1)} ({sum(y==1)/len(y)*100:.1f}%)")
    
    return X, y


def create_random_forest_pipeline():
    """Create Random Forest pipeline"""
    return Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True,
            stop_words='english'
        )),
        ('clf', RandomForestClassifier(
            n_estimators=100,
            max_depth=30,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
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
            sublinear_tf=True,
            stop_words='english'
        )),
        ('clf', LGBMClassifier(
            n_estimators=100,
            max_depth=15,
            learning_rate=0.1,
            random_state=42,
            verbose=-1,
            class_weight='balanced'
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
            sublinear_tf=True,
            stop_words='english'
        )),
        ('clf', XGBClassifier(
            n_estimators=100,
            max_depth=15,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False
        ))
    ])


def train_and_save_model(name, pipeline, X_train, y_train, X_test, y_test):
    """Train model and save to disk"""
    print(f"\n{'='*70}")
    print(f"Training {name}...")
    print(f"{'='*70}")
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Training complete!")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))
    
    print(f"\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"              Predicted")
    print(f"              Fake  Real")
    print(f"Actual Fake   {cm[0][0]:5d} {cm[0][1]:5d}")
    print(f"       Real   {cm[1][0]:5d} {cm[1][1]:5d}")
    
    # Save model
    model_path = f'models/{name}.joblib'
    joblib.dump(pipeline, model_path)
    print(f"\n✓ Model saved to {model_path}")
    
    # Test a prediction
    sample_fake = X_test[y_test == 0][0]
    sample_real = X_test[y_test == 1][0]
    
    pred_fake = pipeline.predict_proba([sample_fake])[0]
    pred_real = pipeline.predict_proba([sample_real])[0]
    
    print(f"\nSample Predictions:")
    print(f"Fake article: Fake={pred_fake[0]:.2%}, Real={pred_fake[1]:.2%}")
    print(f"Real article: Fake={pred_real[0]:.2%}, Real={pred_real[1]:.2%}")
    
    return accuracy


def main():
    """Train all three models"""
    print("="*70)
    print("Fake News Detection - Real Model Training")
    print("="*70)
    
    # Load data
    X, y = load_data()
    
    # Split data (80% train, 20% test)
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
    print("\n" + "="*70)
    print("Training Summary")
    print("="*70)
    for name, accuracy in results.items():
        print(f"{name:20s} {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"\nAverage Accuracy: {np.mean(list(results.values())):.4f} ({np.mean(list(results.values()))*100:.2f}%)")
    print("="*70)
    print("\n✓ All models trained and saved!")
    print("\nYou can now start the API server:")
    print("  python main.py")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
