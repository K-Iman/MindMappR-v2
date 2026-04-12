from django import forms

class AssessmentForm(forms.Form):
    # Preserved securely mapping the old ML matrix natively
    sleep_hours = forms.IntegerField(label='Average hours of sleep per night (0-24)', min_value=0, max_value=24, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    stress_level = forms.IntegerField(label='Current stress level (1-10)', min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    mood_score = forms.IntegerField(label='Current mood score (1-10)', min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'form-input'}))

FREQUENCY_CHOICES = [
    (0, 'Not at all'),
    (1, 'Several days'),
    (2, 'More than half the days'),
    (3, 'Nearly every day')
]

DIFFICULTY_CHOICES = [
    (0, 'Not difficult at all'),
    (1, 'Somewhat difficult'),
    (2, 'Very difficult'),
    (3, 'Extremely difficult')
]

class QuickTestForm(forms.Form):
    q1 = forms.ChoiceField(label='Little interest or pleasure in doing things', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q2 = forms.ChoiceField(label='Feeling down, depressed, or hopeless', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    
    sleep_hours = forms.IntegerField(
        label='How many hours do you sleep on average? (0-12)',
        min_value=0, max_value=12,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 7'})
    )
    
    stress_level = forms.ChoiceField(
        label='Current stress level',
        choices=[(1, 'Low'), (2, 'Moderate'), (3, 'High')],
        widget=forms.Select(attrs={'class': 'form-input', 'style': 'padding: 0.8rem; border-radius: 8px; border: 1px solid var(--surface-border); background-color: var(--bg-color); color: var(--text-primary);'})
    )
    
    mood = forms.ChoiceField(
        label='Current mood',
        choices=[('Good', 'Good'), ('Neutral', 'Neutral'), ('Low', 'Low')],
        widget=forms.Select(attrs={'class': 'form-input', 'style': 'padding: 0.8rem; border-radius: 8px; border: 1px solid var(--surface-border); background-color: var(--bg-color); color: var(--text-primary);'})
    )

class DeepTestForm(forms.Form):
    q1 = forms.ChoiceField(label='Little interest or pleasure in doing things', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q2 = forms.ChoiceField(label='Feeling down, depressed, or hopeless', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q3 = forms.ChoiceField(label='Trouble falling/staying asleep, or sleeping too much', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q4 = forms.ChoiceField(label='Feeling tired or having little energy', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q5 = forms.ChoiceField(label='Poor appetite or overeating', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q6 = forms.ChoiceField(label='Feeling bad about yourself, or that you are a failure', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q7 = forms.ChoiceField(label='Trouble concentrating on things, such as reading the newspaper or watching television', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q8 = forms.ChoiceField(label='Moving or speaking so slowly that other people could have noticed? Or the opposite—being so fidgety or restless that you have been moving around a lot more than usual', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    q9 = forms.ChoiceField(label='Thoughts that you would be better off dead or of hurting yourself in some way', choices=FREQUENCY_CHOICES, widget=forms.RadioSelect)
    
    q10 = forms.ChoiceField(
        label='How difficult have these problems made it for you to do your work, take care of things at home, or get along with other people?',
        choices=DIFFICULTY_CHOICES, 
        widget=forms.RadioSelect
    )
