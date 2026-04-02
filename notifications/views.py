from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    # Get all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Count unread notifications
    unread_count = notifications.filter(is_read=False).count()

    # Pass both notifications and unread count to template
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_notifications_count': unread_count
    })
