from django.urls import path
from .views import *

urlpatterns = [
    path('payment-url/', payment_url)
]