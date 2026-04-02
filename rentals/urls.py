from django.urls import path
from . import views

urlpatterns = [
    # --- Item Management ---
    path("items/", views.item_list, name="item_list"),
    path("add/", views.add_item, name="add_item"),   # ✅ renters can add items

    # --- Rental / Booking Management ---
    path("", views.rental_list, name="rental_list"),              # /rentals/ → rental list
    path("<int:rental_id>/", views.rental_detail, name="rental_detail"),

    # --- Booking Actions ---
    path("create/<int:item_id>/", views.rental_create, name="rental_create"),
    path("quick/<int:item_id>/", views.quick_rent, name="quick_rent"),
    path("<int:rental_id>/cancel/", views.rental_cancel, name="rental_cancel"),  # ✅ cancel rental
]
