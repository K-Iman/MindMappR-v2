from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    # Gateway Route seamlessly retaining existing Dashboard variable paths inherently ('assessment' -> 'selection')
    path('', views.test_selection, name='assessment'),
    path('ai/', views.take_assessment, name='ai_assessment'),
    path('quick/', views.quick_test, name='quick_test'),
    path('deep/', views.deep_test, name='deep_test'),
    path('history/', views.history, name='history'),
    path('progress/', views.user_progress_view, name='progress'),
]
