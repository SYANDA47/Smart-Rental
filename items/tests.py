from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Item

class ItemModelTests(TestCase):
    def test_create_item(self):
        User = get_user_model()
        user = User.objects.create_user(username='owner', password='pass123')
        item = Item.objects.create(
            name='Test Item',
            description='A test item',
            owner=user,
            price_per_day=50.00
        )
        self.assertEqual(item.name, 'Test Item')
        self.assertTrue(item.is_available)
