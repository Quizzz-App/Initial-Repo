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
    try:
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
    except QuizPreparation.DoesNotExist:
        return redirect('user-quiz', username= request.user.username)

@login_required(login_url= 'login')
@csrf_exempt
def validateAnswers(request):
    if request.method == 'POST':
         valid_answers= 0
         invalid_answers= 0
         percentage= 0
         data = json.loads(request.body)
         for key, value in data['quizData'].items():
            if value['id'] != '':
                print(value)
                getQuestion= QuestionsModel.objects.get(uID= value['id'])
                if value['userAns'] == getQuestion.correct_answer:
                    valid_answers += 1
                else:
                    invalid_answers += 1
         percentage= ((valid_answers / int(data['quizData']['questions']['questions'])) * 100)
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
         newHistory= QuizHistory.objects.create(
             user= request.user,
             category= data['quizInfo']['cat'],
             level= data['quizInfo']['level'],
             limit= data['quizInfo']['limit'],
             time_taken= data['quizInfo']['time'],
             score=percentage,
         )
         newHistory.save()
         return JsonResponse(response)


def getQuestion(request,uid):
    question= QuestionsModel.objects.get(uID= uid)
    q= question.question
    a= question.correct_answer
    i= question.incorrect_answers
    uid= question.uID
    return JsonResponse({'id':uid, 'question':q, 'answer': a, 'incorrect': i}, safe= False)