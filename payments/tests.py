from django.test import TestCase
from django.contrib.auth import get_user_model
from items.models import Item
from rentals.models import Rental
from .models import Payment
from datetime import date

class PaymentModelTests(TestCase):
    def test_create_payment(self):
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
        payment = Payment.objects.create(
            rental=rental,
            user=renter,
            amount=400.00,
            status='COMPLETED',
            transaction_id='TX123456'
        )
        self.assertEqual(payment.status, 'COMPLETED')
        self.assertEqual(payment.amount, 400.00)
