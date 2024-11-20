from django.urls import path
from .views import *
from adminSystem.views import add_category, add_level, add_questions, updateCat, updatelevel, updateQuestion

urlpatterns = [
    path('get-questions-info/', get_quiz_data, name='get-questions-info'),
     path('initialize/', initializeQuiz, name= 'start-quiz'),
    path('start/', startQuiz, name= 'start-quiz'),
    path('validate/', validateAnswers, name= 'validate-answers'),
    path('get-question/<str:uid>/', getQuestion, name='get-question'),

    #Admin urls
    path('add-course/', add_category, name='add-course'),
    path('update-course/', updateCat, name='update-course'),
    path('add-level/', add_level, name='add-level'),
    path('update-level/', updatelevel, name='update-level'),
    path('add-questions/', add_questions, name='add-questions'),
    path('update-question/', updateQuestion, name='update-question'),

]