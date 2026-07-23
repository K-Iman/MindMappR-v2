from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AssessmentForm, QuickTestForm, DeepTestForm
from .utils import predict_risk, get_user_recommendations
from .models import PredictionRecord
import json

@login_required
def test_selection(request):
    return render(request, 'prediction/selection.html')

@login_required
def take_assessment(request):
    # Old Random Forest Logic securely mapped! Does not overlap the PHQ system.
    result = None
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            result = predict_risk(data)
            PredictionRecord.objects.create(
                user=request.user,
                test_type='AI_Assessment',
                inputs=data,
                result=result,
            )
    else:
        form = AssessmentForm()
    
    recommendations = get_user_recommendations(request.user)
    return render(request, 'prediction/assessment.html', {'form': form, 'result': result, 'recommendations': recommendations})

@login_required
def quick_test(request):
    result = None
    if request.method == 'POST':
        form = QuickTestForm(request.POST)
        if form.is_valid():
            try:
                # Safe parsing logic protecting entirely against explicit crash loops natively
                score = int(form.cleaned_data.get('q1', 0)) + int(form.cleaned_data.get('q2', 0))
                sleep = int(form.cleaned_data.get('sleep_hours') or 0)
                stress = int(form.cleaned_data.get('stress_level') or 1)
                mood = str(form.cleaned_data.get('mood') or 'Neutral')
                
                # Primary risk logic securely mapped mathematically matching PHQ-2 boundaries natively
                risk = determine_quick_risk(score)
                
                # Supplementary tracking matrices pushing explicit auxiliary context points
                flags = []
                if sleep < 5: 
                    flags.append("Limited sleep detected (Negative factor)")
                if stress == 3: 
                    flags.append("High stress threshold indicates elevated immediate concern")
                if mood == 'Low': 
                    flags.append("A consistently low ambient mood reinforces the underlying risk category")

                # Explicit mapping enforcing default variables cleanly
                PredictionRecord.objects.create(
                    user=request.user,
                    test_type='Quick Test',
                    score=score,
                    sleep_hours=sleep,
                    stress_level=stress,
                    mood=mood,
                    inputs=form.cleaned_data,
                    result=risk
                )
                result = {'score': score, 'risk': risk, 'flags': flags}
                
            except (ValueError, TypeError) as e:
                # Handle gracefully preventing standard server 500 error crashes securely
                form.add_error(None, f"Internal Error: Failed to successfully evaluate matrix due to invalid inputs.")
    else:
        form = QuickTestForm()
        
    recommendations = get_user_recommendations(request.user)
    return render(request, 'prediction/quick_test.html', {'form': form, 'result': result, 'recommendations': recommendations})

def determine_quick_risk(score):
    if score <= 2: return "Low risk"
    elif score <= 4: return "Moderate risk"
    return "High risk"

@login_required
def user_progress_view(request):
    records = PredictionRecord.objects.filter(
        user=request.user,
        test_type__in=['Quick Test', 'Deep Test']
    ).exclude(score__isnull=True).order_by('timestamp')

    all_data = []
    for r in records:
        all_data.append({
            'date': r.timestamp.strftime('%b %d'),
            'type': r.test_type,
            'score': r.score
        })

    context = {
        'all_data': json.dumps(all_data),
        'has_data': len(records) > 0
    }
    
    return render(request, 'prediction/progress.html', context)

@login_required
def deep_test(request):
    result = None
    if request.method == 'POST':
        form = DeepTestForm(request.POST)
        if form.is_valid():
            # Mathematically bounds PHQ scoring logic strictly calculating standard indices
            score = sum(int(form.cleaned_data[f'q{i}']) for i in range(1, 10))
            severity = determine_deep_severity(score)
            
            PredictionRecord.objects.create(
                user=request.user,
                test_type='Deep Test',
                score=score,
                inputs=form.cleaned_data,
                result=severity
            )
            
            # Explicit boolean intercepting Q9 threshold limits cleanly
            result = {'score': score, 'severity': severity, 'q9_high': int(form.cleaned_data['q9']) > 0}
    else:
        form = DeepTestForm()
        
    recommendations = get_user_recommendations(request.user)
    return render(request, 'prediction/deep_test.html', {'form': form, 'result': result, 'recommendations': recommendations})

def determine_deep_severity(score):
    if score <= 4: return "Minimal"
    elif score <= 9: return "Mild"
    elif score <= 14: return "Moderate"
    elif score <= 19: return "Moderately severe"
    return "Severe"

@login_required
def history(request):
    records = PredictionRecord.objects.filter(user=request.user)
    return render(request, 'prediction/history.html', {'records': records})
