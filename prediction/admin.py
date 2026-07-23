from django.contrib import admin
from .models import PredictionRecord

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'result', 'timestamp')
    list_filter = ('result', 'timestamp')
    search_fields = ('user__username',)
