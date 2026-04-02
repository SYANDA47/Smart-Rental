from django.test import TestCase
from django.contrib.auth import get_user_model
from items.models import Item
from .models import Rental
from datetime import date

class RentalModelTests(TestCase):
    def test_create_rental(self):
        User = get_user_model()
        owner = User.objects.create_user(username='owner', password='pass123')
        renter = User.objects.create_user(username='renter', password='pass123')
        item = Item.objects.create(
            name='Test Item',
            description='A test item',
            owner=owner,
            price_per_day=100.00
        )
        rental = Rental.objects.create(
            item=item,
            renter=renter,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 5),
            total_price=400.00
        )
        self.assertEqual(rental.duration(), 4)
        self.assertTrue(rental.is_active)
