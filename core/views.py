from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from prediction.utils import get_user_recommendations
from .models import MoodLog
from .forms import MoodLogForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    recommendations = get_user_recommendations(request.user)
    return render(request, 'core/dashboard.html', {'recommendations': recommendations})

@login_required
def zen_log_view(request):
    if request.method == 'POST':
        form = MoodLogForm(request.POST)
        if form.is_valid():
            mood_log = form.save(commit=False)
            mood_log.user = request.user
            mood_log.save()
            return redirect('zen')
    else:
        form = MoodLogForm()
        
    past_logs = MoodLog.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/zen.html', {'form': form, 'past_logs': past_logs})
