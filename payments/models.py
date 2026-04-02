from django.db import models
from django.contrib.auth import get_user_model
from rentals.models import RentalItem, Rental   # ✅ use RentalItem instead of Item

User = get_user_model()

class Payment(models.Model):
    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name="payments"   # allows multiple payments per rental
    )
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    item = models.ForeignKey(RentalItem, on_delete=models.CASCADE, related_name="payments")  # ✅ FIXED
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    method = models.CharField(
        max_length=20,
        choices=[
            ('paypal', 'PayPal'),
            ('card', 'Bank Card'),
            ('mpesa', 'M-Pesa'),
        ],
        default='card'
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )

    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # gateway reference

    def __str__(self):
        return f"Payment {self.id} - {self.renter.username} - {self.item.title} ({self.status})"  # ✅ FIXED

    class Meta:
        ordering = ['-date']
