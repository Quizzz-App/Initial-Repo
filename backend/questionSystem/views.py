from django.shortcuts import render, redirect
from .models import *
import requests, json, random, ast

# Create your views here.

def index(request):
        context= {
            'categories': QuestionsCategory.objects.all(),
            'levels': QuestionLevel.objects.all(),
        }
        return render(request, 'quiz/quiz_index.html', context= context)

def startQuiz(request, category= None, level= None, limit= None):
    if request.method == 'POST':
        category= request.POST.get('category')
        level= request.POST.get('level')
        limit= request.POST.get('limit')
                
        levelObject= QuestionLevel.objects.get(name= level)
        categoryObject= QuestionsCategory.objects.get(name= category)
        questions= QuestionsModel.objects.filter(level= levelObject, category= categoryObject)
        qrl= [x for x in questions]
        selected_question= random.sample(qrl, int(limit))
        

        saveQuestions(request= request, category= category, level= level, limit= limit)
        questionsDict= {}
        limit= [_ for _ in range(0, int(limit))]
        
        for i,x in enumerate(selected_question):
            ansList= [_ for _ in ast.literal_eval(x.incorrect_answers)]
            ansList.append(x.correct_answer)
            random.shuffle(ansList)

            questionsDict[int(i)]= {
                 'question': x.question,
                 'answers': ansList,
            }
    context= {
        'questions': questionsDict,
        'limit': limit,
    }
    return render(request, 'quiz/start_test.html', context= context)

def fetchQuestions():
    pass

def saveQuestions(request, category, level, limit):
    url= f"https://the-trivia-api.com/api/questions?categories={category}&limit={int(limit)}&difficulty={level}"
    response= requests.get(url)
    if response.status_code == 200:
        response= response.json()
        for _ in range(0, int(limit)):
            id= response[_]['id']
            question= response[_]['question']
            level= response[_]['difficulty']
            answer= response[_]['correctAnswer']
            incorrect_answers= response[_]['incorrectAnswers']
            categoryDict= {
                'Music':'music',
                'Sport & Leisure': 'sport_and_leisure',
                'Film & TV': 'film_and_tv',
                'Arts & Literature': 'arts_and_literature',
                'History': 'history',
                'General Knowledge': 'general_knowledge',
                'Society & Culture': 'society_and_culture',
                'Science': 'science',
                'Geography': 'geography',
                'Food & Drink': 'food_and_drink'
            }
                
    levelObject= QuestionLevel.objects.get(name= level)
    categoryObject= QuestionsCategory.objects.get(name= category)
    saveQuestion=  QuestionsModel.objects.create(question=question, correct_answer=answer, incorrect_answers=incorrect_answers, category=categoryObject, level= levelObject, aurthor= request.user.username)
    saveQuestion.save()