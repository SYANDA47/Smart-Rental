from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class RentalItem(models.Model):
    """The physical item available for rent."""
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_items"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="rental_items/", blank=True, null=True)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ new field to control whether the owner's name is shown
    show_owner_name = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Rental(models.Model):
    """The transaction/booking of a RentalItem."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    item = models.ForeignKey(
        RentalItem,
        on_delete=models.CASCADE,
        related_name="rentals"
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_rentals"
    )

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.title} rented by {self.renter.username} ({self.status})"

    @property
    def duration(self):
        """Return rental duration in days."""
        if self.start_date and self.end_date:
            diff = (self.end_date - self.start_date).days
            return max(diff, 0)
        return 0

    def calculate_total_price(self):
        """Calculate total price based on duration and item price."""
        return self.duration * self.item.price_per_day

    def save(self, *args, **kwargs):
        # Auto-calculate total price before saving
        if self.start_date and self.end_date and self.item:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def is_overdue(self):
        """Check if rental is overdue compared to today's date."""
        return self.end_date < timezone.now().date() and self.status == "active"

    def extend(self, days=1):
        """Extend rental by given days."""
        self.end_date += timedelta(days=days)
        self.status = "active"
        self.save()

    def cancel(self):
        """Cancel rental."""
        self.status = "cancelled"
        self.save()
