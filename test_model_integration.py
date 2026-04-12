import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from prediction.utils import predict_risk

if __name__ == "__main__":
    # Test Data: 8 hours sleep, stress 2, mood 8 
    data = [8, 2, 8]
    print(f"Testing Prediction Setup with Data: {data}")
    result = predict_risk(data)
    print(f"Output 1: {result}")
    
    # Test Data 2: 4 hours sleep, stress 9, mood 2 
    data_2 = [4, 9, 2]
    print(f"Testing Prediction Setup with Data 2: {data_2}")
    result_2 = predict_risk(data_2)
    print(f"Output 2: {result_2}")
