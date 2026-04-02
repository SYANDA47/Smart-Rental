from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# Simple home view
def home(request):
    return render(request, 'home.html')

# About Us view
def about(request):
    return render(request, 'about.html')

urlpatterns = [
    # Core pages
    path('', home, name='home'),
    path('about/', about, name='about'),

    # Admin
    path('admin/', admin.site.urls),

    # App routes
    path('accounts/', include('accounts.urls')),
    path('items/', include('items.urls')),
    path('rentals/', include('rentals.urls')),
    path('disputes/', include('disputes.urls')),
    path('notifications/', include('notifications.urls')),
    path('payments/', include('payments.urls')),
    path("dashboard/", include("dashboard.urls")),

    # ✅ M-Pesa integration (STK Push)
    path('mpesa/', include('mpesa.urls')),  # you’ll create mpesa/urls.py
]

# ✅ Serve uploaded images (like gowns, cars, etc.) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
