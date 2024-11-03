from authenticationSystem.models import CustomUserModel as User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests, json, random, ast
from .models import *

# Create your views here.
@login_required(login_url= 'login')
def get_quiz_data(request):
        categories= QuestionsCategory.objects.all()
        levels= QuestionLevel.objects.all()
        data= {}
        for category in categories:
            data[str(category.name)]= {}
            for level in levels:
                limit= len(QuestionsModel.objects.filter(level= level, category= category))
                data[str(category.name)][str(level.name)]= limit
            data[str(category.name)]['img']= f'{category.categoryImg.url}'
        return JsonResponse(data)

@login_required(login_url= 'login')
def initializeQuiz(request):
    if request.method == 'POST':
        category= request.POST.get('category')
        level= request.POST.get('level')
        limit= request.POST.get('limit')

        QuizPreparation.objects.create(user= request.user, category= category, level= level, limit=limit).save()
        return JsonResponse({'msg': 'Ready'})

@login_required(login_url= 'login')
def startQuiz(request, category= None, level= None, limit= None):
    userQuizInit= QuizPreparation.objects.get(user= request.user) 
    category= userQuizInit.category
    level= userQuizInit.level
    limit= userQuizInit.limit
            
    levelObject= QuestionLevel.objects.get(name= level)
    categoryObject= QuestionsCategory.objects.get(name= category)
    questions= QuestionsModel.objects.filter(level= levelObject, category= categoryObject)
    qrl= [x for x in questions]
    selected_question= random.sample(qrl, int(limit))
    

    # saveQuestions(request= request, category= category, level= level, limit= limit)
    questionsDict= {}
    
    for i,x in enumerate(selected_question):
        # ansList= [_ for _ in ast.literal_eval(x.incorrect_answers)]
        ansList= x.incorrect_answers.split(',')
        ansList.append(x.correct_answer)
        random.shuffle(ansList)

        questionsDict[int(i)]= {
                'id': f'{x.uID}',
                'question': x.question,
                'answers': ansList,
            }
    userQuizInit.delete()
    context= {
         'quiz': {
             'category': category,
             'level': level,
             'limit': limit
         },
        'questions_js': json.dumps(questionsDict),
    }
    return render(request, 'sitepages/auxilliarypages/quizpage/index.html', context= context)

@login_required(login_url= 'login')
@csrf_exempt
def validateAnswers(request):
    if request.method == 'POST':
         valid_answers= 0
         invalid_answers= 0
         percentage= 0
         data = json.loads(request.body)
         for key, value in data.items():
            if value['id'] != '':
                print(value)
                getQuestion= QuestionsModel.objects.get(uID= value['id'])
                if value['userAns'] == getQuestion.correct_answer:
                    valid_answers += 1
                else:
                    invalid_answers += 1
         percentage= ((valid_answers / int(data['questions']['questions'])) * 100)
         response= {
            'message': 'Data received successfully',
            'status': 'ok',
            'user': request.user.username,
            'result': {
                'valid_answers': valid_answers,
                'invalid_answers': invalid_answers,
                'percentage': percentage
            }
        }
         user= User.objects.get(username= request.user.username)
         user.quiz_taken= user.quiz_taken + 1
         user.save()
         return JsonResponse(response)


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