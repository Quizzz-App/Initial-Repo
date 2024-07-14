from django.db import models
import uuid

# Create your models here.
class QuestionsCategory(models.Model):
    name= models.CharField(max_length= 50, unique= True, blank= False, null= False)

    def __str__(self):
        return f'Category: {self.name}'
    
class QuestionLevel(models.Model):
    name= models.CharField(max_length= 50, unique= True, blank= False, null= False)

    def __str__(self):
        return f'Question level: {self.name}'

class QuestionsModel(models.Model):
    uID= models.UUIDField(default= uuid.uuid4, unique= True)
    question= models.CharField(max_length= 99999999999999999999999999999999999999, unique= True, blank= False, null= False)
    correct_answer= models.CharField(max_length= 999999999999999999999, blank= False, null= False)
    incorrect_answers= models.CharField(max_length= 999999999999999999999999999999, blank= False, null= False)
    category= models.ForeignKey(QuestionsCategory, on_delete= models.CASCADE)
    level= models.ForeignKey(QuestionLevel, on_delete= models.CASCADE)
    aurthor= models.CharField(max_length= 50, blank= False, null= False)
    created_on= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'Aurthor: {self.aurthor} -----> created_on: {self.created_on}'
