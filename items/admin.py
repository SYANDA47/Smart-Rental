from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_available', 'price_per_day', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('is_available', 'created_at')
