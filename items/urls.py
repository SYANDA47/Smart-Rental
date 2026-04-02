from django.urls import path
from . import views

urlpatterns = [
    # Item browsing
    path('', views.item_list, name='item_list'),
    path('<int:pk>/', views.item_detail, name='item_detail'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Reviews
    path('<int:pk>/review/', views.add_review, name='add_review'),

    # Rentals
    path('rental/<int:rental_id>/extend/', views.extend_rental, name='extend_rental'),
    path('rental/<int:rental_id>/cancel/', views.cancel_rental, name='cancel_rental'),
]
