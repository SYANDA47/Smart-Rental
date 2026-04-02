from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rental",
        "renter",
        "item",
        "amount",
        "method",
        "status",
        "transaction_id",
        "date",
    )
    list_filter = ("method", "status", "date")
    search_fields = ("renter__username", "item__name", "transaction_id")
    ordering = ("-date",)
