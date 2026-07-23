from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-input', 'placeholder': field.label})
            if field_name == 'username':
                field.widget.attrs.update({'minlength': '3', 'maxlength': '25', 'required': 'required'})
                field.help_text = "Letters, digits and @/./+/-/_ only."
            elif 'password' in field_name.lower():
                field.widget.attrs.update({'minlength': '8', 'required': 'required'})

    def clean_username(self):
        # We must call super to cleanly protect standard functionality
        username = super().clean_username() 
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long")
        if len(username) > 25:
            raise forms.ValidationError("Username cannot exceed 25 characters")
        return username

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-input', 'placeholder': field.label})
            if field_name == 'username':
                field.widget.attrs.update({'minlength': '3', 'required': 'required'})
                # Intentionally NOT applying maxlength to prevent blocking existing long usernames
            elif 'password' in field_name.lower():
                field.widget.attrs.update({'minlength': '8', 'required': 'required'})
