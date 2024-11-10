from django.urls import path
from .views import *

urlpatterns = [
    path('gift/<str:uID>/', gift_referral, name= 'manual-gift-ref'),
    path('get-ref-analytics/', refAnalytics, name= 'get-ref-analytics'),
]