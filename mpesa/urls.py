from django.urls import path
from . import views

urlpatterns = [
    # ✅ Use initiate_stk_push instead of stk_push
    path("stkpush/", views.initiate_stk_push, name="stk_push"),
    path("callback/", views.mpesa_callback, name="mpesa_callback"),
]
