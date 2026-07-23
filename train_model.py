import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def train_and_save():
    # Make directory if not exists
    os.makedirs(os.path.join('prediction', 'ml_models'), exist_ok=True)
    
    # 1. Dummy training data (e.g., [sleep_hours, stress_level (1-10), mood_score (1-10)])
    # Target: 0 (Low Risk), 1 (High Risk)
    X = pd.DataFrame([
        [8, 2, 8], [7, 3, 7], [9, 1, 9], [8, 4, 6],  # Low Risk
        [4, 9, 2], [5, 8, 3], [3, 10, 1], [4, 7, 3]  # High Risk
    ], columns=['sleep_hours', 'stress_level', 'mood_score'])
    
    y = [0, 0, 0, 0, 1, 1, 1, 1]
    
    # 2. Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    
    # 3. Save model
    model_path = os.path.join('prediction', 'ml_models', 'model.pkl')
    joblib.dump(model, model_path)
    print(f"Model successfully trained and saved to {model_path}")

if __name__ == "__main__":
    train_and_save()
