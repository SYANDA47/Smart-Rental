from django.contrib import admin
from .models import Rental

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'renter',
        'start_date',
        'end_date',
        'total_price',
        'status',        # ✅ replaced is_active with status
        'created_at',
    )
    list_filter = ('status', 'start_date', 'end_date')  # ✅ filter by status instead of is_active
    search_fields = ('item__name', 'renter__username')
    ordering = ('-created_at',)  # newest rentals first
