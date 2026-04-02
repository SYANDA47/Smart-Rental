from django.contrib import admin
from .models import Dispute

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('rental', 'raised_by', 'status', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('rental__item__name', 'raised_by__username')
