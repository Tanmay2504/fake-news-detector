"""
Model Accuracy Testing - Calculate real performance metrics
Run this to get actual accuracy numbers for your exhibition
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def load_test_data():
    """Load test dataset"""
    print("\n📂 Loading test data...")
    
    test_files = [
        'datasets/test.csv',
        'datasets/english_test_with_labels.csv',
        'datasets/Constraint_Test.csv'
    ]
    
    for filepath in test_files:
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                print(f"✅ Loaded: {filepath}")
                print(f"   → {len(df)} samples")
                
                # Try to find text and label columns
                text_cols = [col for col in df.columns if 'text' in col.lower() or 'title' in col.lower()]
                label_cols = [col for col in df.columns if 'label' in col.lower() or 'class' in col.lower()]
                
                if text_cols and label_cols:
                    print(f"   → Text column: {text_cols[0]}")
                    print(f"   → Label column: {label_cols[0]}")
                    return df, text_cols[0], label_cols[0]
                    
            except Exception as e:
                print(f"⚠️  Error loading {filepath}: {e}")
                continue
    
    print("❌ No valid test dataset found")
    return None, None, None

def test_individual_model(model, X_test, y_test, model_name):
    """Test a single model and return metrics"""
    print(f"\n🤖 Testing {model_name}...")
    
    try:
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"   Accuracy:  {accuracy:.2%}")
        print(f"   Precision: {precision:.2%}")
        print(f"   Recall:    {recall:.2%}")
        print(f"   F1 Score:  {f1:.2%}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n   Confusion Matrix:")
        print(f"   {cm}")
        
        return {
            'model': model_name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'predictions': y_pred
        }
        
    except Exception as e:
        print(f"❌ Error testing {model_name}: {e}")
        return None

def test_ensemble(predictions_dict, y_test):
    """Test ensemble prediction with weighted voting"""
    print(f"\n🎯 Testing Ensemble (Weighted Voting)...")
    
    # Weights: RF=60%, LGB=20%, XGB=20%
    weights = {
        'Random Forest': 0.60,
        'LightGBM': 0.20,
        'XGBoost': 0.20
    }
    
    try:
        # Get predictions from each model
        rf_pred = predictions_dict.get('Random Forest')
        lgb_pred = predictions_dict.get('LightGBM')
        xgb_pred = predictions_dict.get('XGBoost')
        
        if rf_pred is None or lgb_pred is None or xgb_pred is None:
            print("❌ Missing predictions from one or more models")
            return None
        
        # Weighted voting
        ensemble_pred = []
        for i in range(len(y_test)):
            votes = (
                rf_pred[i] * weights['Random Forest'] +
                lgb_pred[i] * weights['LightGBM'] +
                xgb_pred[i] * weights['XGBoost']
            )
            ensemble_pred.append(1 if votes > 0.5 else 0)
        
        ensemble_pred = np.array(ensemble_pred)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, ensemble_pred)
        precision = precision_score(y_test, ensemble_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, ensemble_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, ensemble_pred, average='weighted', zero_division=0)
        
        print(f"   Accuracy:  {accuracy:.2%}")
        print(f"   Precision: {precision:.2%}")
        print(f"   Recall:    {recall:.2%}")
        print(f"   F1 Score:  {f1:.2%}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, ensemble_pred)
        print(f"\n   Confusion Matrix:")
        print(f"   {cm}")
        
        return {
            'model': 'Ensemble',
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
        
    except Exception as e:
        print(f"❌ Error testing ensemble: {e}")
        return None

def run_accuracy_tests():
    """Run all accuracy tests"""
    print_header("MODEL ACCURACY TEST SUITE")
    
    # Load test data
    df, text_col, label_col = load_test_data()
    
    if df is None:
        print("\n❌ Cannot proceed without test data")
        print("\nTo run this test, you need a test.csv file with:")
        print("  - A text column (e.g., 'text', 'title', 'content')")
        print("  - A label column (e.g., 'label', 'class')")
        print("  - Labels: 0 = Real, 1 = Fake")
        return False
    
    # Prepare data
    print(f"\n🔧 Preparing test data...")
    X_test_text = df[text_col].fillna('').astype(str)
    y_test = df[label_col].values
    
    # Load vectorizer (if exists) or create new one
    vectorizer_path = 'models/vectorizer.joblib'
    if os.path.exists(vectorizer_path):
        print(f"✅ Loading saved vectorizer")
        vectorizer = joblib.load(vectorizer_path)
    else:
        print(f"⚠️  No saved vectorizer, creating new one")
        vectorizer = TfidfVectorizer(max_features=5000)
        # This won't work perfectly without training data, but gives estimate
        vectorizer.fit(X_test_text)
    
    X_test = vectorizer.transform(X_test_text)
    print(f"✅ Vectorized {len(X_test)} samples")
    
    # Load models
    print(f"\n📦 Loading models...")
    models = {}
    model_files = {
        'Random Forest': 'models/random_forest.joblib',
        'LightGBM': 'models/lightgbm.joblib',
        'XGBoost': 'models/xgboost.joblib'
    }
    
    for name, path in model_files.items():
        if os.path.exists(path):
            try:
                models[name] = joblib.load(path)
                print(f"✅ Loaded {name}")
            except Exception as e:
                print(f"❌ Failed to load {name}: {e}")
        else:
            print(f"❌ {name} not found at {path}")
    
    if len(models) == 0:
        print("\n❌ No models loaded, cannot proceed")
        return False
    
    # Test each model
    print_header("INDIVIDUAL MODEL PERFORMANCE")
    
    results = {}
    predictions = {}
    
    for name, model in models.items():
        result = test_individual_model(model, X_test, y_test, name)
        if result:
            results[name] = result
            predictions[name] = result['predictions']
    
    # Test ensemble
    if len(predictions) == 3:
        print_header("ENSEMBLE PERFORMANCE")
        ensemble_result = test_ensemble(predictions, y_test)
        if ensemble_result:
            results['Ensemble'] = ensemble_result
    else:
        print("\n⚠️  Skipping ensemble test (need all 3 models)")
    
    # Summary
    print_header("SUMMARY")
    
    if results:
        print("\n📊 Model Comparison:\n")
        print(f"{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1 Score':<12}")
        print("-" * 70)
        
        for name, metrics in results.items():
            print(f"{name:<20} {metrics['accuracy']:<12.2%} {metrics['precision']:<12.2%} "
                  f"{metrics['recall']:<12.2%} {metrics['f1']:<12.2%}")
        
        # Best model
        best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
        print(f"\n🏆 Best Model: {best_model[0]} ({best_model[1]['accuracy']:.2%} accuracy)")
        
        # For exhibition
        print("\n💡 FOR EXHIBITION:")
        if 'Ensemble' in results:
            acc = results['Ensemble']['accuracy']
            print(f"   → \"Our ensemble achieves {acc:.1%} accuracy on test data\"")
        
        if 'Random Forest' in results:
            acc = results['Random Forest']['accuracy']
            print(f"   → \"Random Forest: {acc:.1%} accuracy\"")
        
        if len(results) > 1:
            avg_acc = np.mean([r['accuracy'] for r in results.values()])
            print(f"   → \"Average model accuracy: {avg_acc:.1%}\"")
        
        return True
    else:
        print("\n❌ No results to display")
        return False

if __name__ == "__main__":
    print("\n")
    success = run_accuracy_tests()
    print("\n" + "="*70 + "\n")
    sys.exit(0 if success else 1)
