import os
import joblib
from django.conf import settings
import pandas as pd

def get_model_path():
    # settings.BASE_DIR points to root MindMappR
    return os.path.join(settings.BASE_DIR, 'prediction', 'ml_models', 'model.pkl')

_model = None

def load_model():
    """
    Loads and caches the ML model into memory.
    """
    global _model
    if _model is None:
        path = get_model_path()
        try:
            _model = joblib.load(path)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return _model

def predict_risk(data):
    """
    Takes a dataset/list of features (e.g., [sleep_hours, stress_level, mood_score])
    and passes it into the loaded ML model for inference.
    
    Returns:
        dict: A dictionary containing the prediction status and risk value.
    """
    model = load_model()
    if model is None:
        return {"status": "error", "message": "Model could not be loaded."}
    
    # Convert incoming data to DataFrame to match expected feature names (to avoid sklearn warnings)
    df = pd.DataFrame([data], columns=['sleep_hours', 'stress_level', 'mood_score'])
    
    # Inference
    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    
    # Evaluate risk
    result_text = "High Risk" if prediction == 1 else "Low Risk"
    confidence = probabilities[prediction]
    
    return {
        "status": "success",
        "risk_level": prediction,
        "risk_text": result_text,
        "confidence": round(confidence * 100, 2)
    }
