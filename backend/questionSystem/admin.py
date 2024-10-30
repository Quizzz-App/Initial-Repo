from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(QuestionsCategory)
admin.site.register(QuestionLevel)
admin.site.register(QuestionsModel)
admin.site.register(QuizPreparation)