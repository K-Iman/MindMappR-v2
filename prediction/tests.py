from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import PredictionRecord
import os

class PredictionSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='preduser', password='testpassword123')
        self.ass_url = reverse('prediction:assessment')
        self.hist_url = reverse('prediction:history')

    def test_anonymous_access_denied(self):
        # Validate that unauthenticated users cannot hit prediction bounds
        response = self.client.get(self.ass_url)
        self.assertEqual(response.status_code, 302) 
        self.assertTrue('login' in response.url)

    def test_prediction_flow_and_db_write(self):
        self.client.login(username='preduser', password='testpassword123')
        
        # Verify initial state
        self.assertEqual(PredictionRecord.objects.count(), 0)

        # Trigger Prediction via POST
        response = self.client.post(self.ass_url, {
            'sleep_hours': 8,
            'stress_level': 2,
            'mood_score': 8
        })
        
        # Should return rendering output (not redirect) mapping the result dynamically
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assessment Result")

        # Validate Database Persistence
        self.assertEqual(PredictionRecord.objects.count(), 1)
        record = PredictionRecord.objects.first()
        self.assertEqual(record.user, self.user)
        self.assertEqual(record.inputs['sleep_hours'], 8)
        self.assertEqual(record.result, "Low Risk")

    def test_history_rendering(self):
        self.client.login(username='preduser', password='testpassword123')
        
        # Seed test data explicitly
        PredictionRecord.objects.create(
            user=self.user,
            inputs={'sleep_hours': 4, 'stress_level': 9, 'mood_score': 2},
            result="High Risk"
        )
        
        # Query History view
        response = self.client.get(self.hist_url)
        self.assertEqual(response.status_code, 200)
        
        # Validate DOM outputs template variables intelligently
        self.assertContains(response, "High Risk")
        self.assertContains(response, "Sleep: 4h")
