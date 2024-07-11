from django.urls import path
from .views import *

urlpatterns = [
    path('gift/', gift_referral, name= 'manual-gift-ref'),
]