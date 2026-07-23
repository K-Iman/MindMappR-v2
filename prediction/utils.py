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

# Recommendation logic matching trends and scoring locally
from prediction.models import PredictionRecord

def get_user_recommendations(user):
    if not user.is_authenticated:
        return _get_neutral_recs("Welcome! Here are some general resources to get you started.")
        
    records = list(PredictionRecord.objects.filter(user=user).exclude(score__isnull=True).order_by('-timestamp')[:5])
    
    if not records:
        return _get_neutral_recs("Welcome! Here are some general resources to get you started.")
        
    # Reverse to chronological: index 0 is oldest of the set, -1 is latest
    records.reverse()
    latest = records[-1]
    
    is_severe = False
    result_lower = latest.result.lower() if latest.result else ""
    if 'high' in result_lower or 'sever' in result_lower:
        is_severe = True
        
    if len(records) < 2:
        if is_severe:
            return _get_priority_recs("Your recent assessment indicates high risk. Please consider these priority resources.")
        else:
            return _get_neutral_recs("Based on your recent assessment, here are some helpful resources.")
            
    first_score = records[0].score or 0
    last_score = latest.score or 0
    
    if is_severe:
        return _get_priority_recs("Your assessments remain in a high-risk range. Professional support is strongly recommended.")
        
    if last_score < first_score:
        return _get_reinforcement_recs("Based on your recent progress, these may help you maintain improvement.")
    elif last_score > first_score:
        return _get_support_recs("We noticed your scores have increased lately. These coping strategies might help.")
    else:
        return _get_preventive_recs("Your condition appears stable. These preventive resources can help you maintain your balance.")

def _get_neutral_recs(msg):
    return {
        "message": msg,
        "resources": [
            {"title": "Mental Wellness Support", "desc": "Access critical coping strategies and emergency contacts.", "link": "/resources/"},
            {"title": "Deep Breathing (4-7-8)", "desc": "Inhale for 4s, hold for 7s, and exhale for 8s to relax.", "link": "/resources/"},
            {"title": "Mindfulness & Calm", "desc": "Explore selected reading on mindfulness.", "link": "/resources/"}
        ]
    }

def _get_priority_recs(msg):
    return {
        "message": msg,
        "resources": [
            {"title": "Emergency Contacts", "desc": "Access verified global crisis lines. Connect with a professional immediately.", "link": "/resources/"},
            {"title": "Professional Counseling", "desc": "Therapy or psychiatric help provides structural support.", "link": "/resources/"},
            {"title": "Grounding (5-4-3-2-1)", "desc": "Find 5 things you can see, 4 you can touch, 3 hear, 2 smell, 1 taste.", "link": "/resources/"}
        ]
    }

def _get_support_recs(msg):
    return {
        "message": msg,
        "resources": [
            {"title": "Deep Breathing (4-7-8)", "desc": "A fast technique to reduce cortisol rapidly.", "link": "/resources/"},
            {"title": "Progressive Relaxation", "desc": "Tense and relax muscle groups to relieve somatic stress.", "link": "/resources/"},
            {"title": "Anxiety & Stress Reading", "desc": "Recommended reading from our open library.", "link": "/resources/"}
        ]
    }

def _get_reinforcement_recs(msg):
    return {
        "message": msg,
        "resources": [
            {"title": "Mindfulness & Calm", "desc": "Explore selected reading on mindfulness to reinforce positive neuroplasticity.", "link": "/resources/"},
            {"title": "Habit Tracking", "desc": "Maintaining a daily log of positive activities can solidify long-term improvements.", "link": "/dashboard/"},
            {"title": "Self-Help Books", "desc": "Read self-help books to build constructive habits.", "link": "/resources/"}
        ]
    }

def _get_preventive_recs(msg):
    return {
        "message": msg,
        "resources": [
            {"title": "Daily Routine Check", "desc": "Consistent sleep and moderate activity levels are the foundation for a stable mood.", "link": "/dashboard/"},
            {"title": "Stoicism & Philosophy", "desc": "Timeless perspectives to build mental resilience against future stressors.", "link": "/resources/"},
            {"title": "Grounding (5-4-3-2-1)", "desc": "A great mental exercise to perform even when feeling stable.", "link": "/resources/"}
        ]
    }
