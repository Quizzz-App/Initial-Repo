from django.urls import path
from .views import *

urlpatterns = [
    path('get-questions-info/', get_quiz_data, name='get-questions-info'),
     path('initialize/', initializeQuiz, name= 'start-quiz'),
    path('start/', startQuiz, name= 'start-quiz'),
    path('validate/', validateAnswers, name= 'validate-answers'),
]