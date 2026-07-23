from django.db import models
from django.contrib.auth.models import User

class MoodLog(models.Model):
    MOOD_CHOICES = [
        ('Very good', 'Very good'),
        ('Good', 'Good'),
        ('Neutral', 'Neutral'),
        ('Low', 'Low'),
        ('Very low', 'Very low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    current_mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    extra_concerns = models.TextField(blank=True, null=True)
    feeling_description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.current_mood} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
