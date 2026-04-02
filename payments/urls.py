from django.urls import path
from . import views

urlpatterns = [
    # Show all payments for the logged-in user
    path('', views.payment_list, name='payment_list'),

    # Checkout flow: Step 1 - choose payment method
    path('<int:rental_id>/checkout/', views.checkout, name='checkout'),

    # ✅ Success page must come BEFORE the generic <str:method> route
    path('<int:rental_id>/success/', views.payment_success, name='payment_success'),

    # Checkout flow: Step 2 - method-specific form (PayPal, Card, M-Pesa)
    path('<int:rental_id>/<str:method>/', views.payment_method_step, name='payment_method_step'),

    # Optional: view payment detail by ID
    path('<int:payment_id>/', views.payment_detail, name='payment_detail'),
]
