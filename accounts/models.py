from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Extended user model with profile details, role, and item type.
    """

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    preferred_payment_method = models.CharField(
        max_length=20,
        choices=[
            ("mpesa", "M-Pesa"),
            ("card", "Card"),
            ("cash", "Cash"),
        ],
        default="mpesa",
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ("owner", "Owner"),
            ("renter", "Renter"),
        ],
        default="renter",
        help_text="Defines whether the user is an Owner or Renter.",
    )

    item_type = models.CharField(
        max_length=20,
        choices=[
            ("vehicle", "Vehicle"),
            ("house", "House"),
            ("item", "Item"),
        ],
        blank=True,
        null=True,
        help_text="Specifies what type of items the renter offers.",
    )

    # ✅ Keep username as the login field
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
