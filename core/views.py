from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

def home(request):
    return HttpResponse("MindMappR is running")

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')
