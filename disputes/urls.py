from django.urls import path
from . import views

urlpatterns = [
    path('', views.dispute_list, name='dispute_list'),
    path('<int:pk>/', views.dispute_detail, name='dispute_detail'),
    path('create/', views.dispute_create, name='dispute_create'),  # ✅ new form route
]
