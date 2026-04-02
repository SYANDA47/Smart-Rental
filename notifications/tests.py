from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification

class NotificationModelTests(TestCase):
    def test_create_notification(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='pass123')
        notification = Notification.objects.create(
            user=user,
            message='Your rental has been confirmed.'
        )
        self.assertEqual(notification.user.username, 'testuser')
        self.assertFalse(notification.is_read)
