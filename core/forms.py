from django import forms
from .models import MoodLog

class MoodLogForm(forms.ModelForm):
    class Meta:
        model = MoodLog
        fields = ['current_mood', 'extra_concerns', 'feeling_description', 'notes']
        labels = {
            'current_mood': 'How are you currently feeling?',
            'extra_concerns': 'Is there anything bothering you right now? (optional)',
            'feeling_description': 'Would you like to describe how you feel in more detail? (optional)',
            'notes': 'Additional notes (optional)',
        }
        widgets = {
            'current_mood': forms.RadioSelect(attrs={'class': 'form-radio'}),
            'extra_concerns': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief concern...'}),
            'feeling_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Describe your feelings...'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Any other thoughts...'}),
        }
