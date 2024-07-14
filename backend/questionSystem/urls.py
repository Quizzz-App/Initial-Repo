from django.urls import path
from .views import *

urlpatterns = [
    path('test/', index, name= 'try-quiz'),
    path('test/start/', startQuiz, name= 'start-quiz'),
]