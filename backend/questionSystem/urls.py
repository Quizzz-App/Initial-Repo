from django.urls import path
from .views import *

urlpatterns = [
    path('test/', index, name= 'try-quiz'),
]