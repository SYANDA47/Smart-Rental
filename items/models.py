from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    is_available = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    # ✅ New field to control whether the owner's name is shown
    show_owner_name = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def daily_cost(self, days=1):
        """Helper method to calculate rental cost for given days."""
        return self.price_per_day * days

    def average_rating(self):
        """Calculate average rating from reviews."""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0

    def star_rating(self):
        """Return star symbols for display in templates."""
        full_stars = int(self.average_rating())
        empty_stars = 5 - full_stars
        return "★" * full_stars + "☆" * empty_stars


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=0)  # 1–5 stars only
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('item', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.rating}★)"
