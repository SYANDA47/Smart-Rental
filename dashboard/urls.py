from django.urls import path
from . import views

urlpatterns = [
    path("renter/", views.renter_dashboard, name="renter_dashboard"),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
]
