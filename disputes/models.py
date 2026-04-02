from django.db import models
from django.contrib.auth import get_user_model
from rentals.models import Rental

User = get_user_model()

class Dispute(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disputes')
    description = models.TextField()
    status_choices = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Dispute {self.id} - {self.status}"
