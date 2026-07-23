from django.db import models
from django.contrib.auth.models import User

class PredictionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    test_type = models.CharField(max_length=50, default='AI_Assessment')
    score = models.IntegerField(null=True, blank=True)
    inputs = models.JSONField(help_text="Stores the user inputs")
    result = models.CharField(max_length=50)
    sleep_hours = models.IntegerField(null=True, blank=True)
    stress_level = models.IntegerField(null=True, blank=True)
    mood = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - [{self.test_type}] {self.result} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-timestamp']
