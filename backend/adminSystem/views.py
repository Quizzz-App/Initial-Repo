from authenticationSystem.models import CustomUserModel
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth 
from authenticationSystem.views import *
from authenticationSystem.forms import *
from questionSystem.models import *
from django.contrib import messages
from .models import *


# Create your views here.
# Admin features
def admin_index(request):
    all_users= CustomUserModel.objects.all()
    active_users= 0
    non_active_users= 0
    is_premium= 0
    non_premium= 0
    frontend_devs= 0
    backend_devs= 0


    projectBalance= 0
    usersBalance= 0
    teamBalance= 0

    for x,_ in enumerate(WalletModel.objects.all()):
        projectBalance += _.get_project_balance()
        usersBalance += _.get_users_balance()
        teamBalance += _.get_team_balance()

    for i, _ in enumerate(all_users):
        if _.is_active:
            active_users += 1
            if _.is_premium:
                is_premium += 1
            else:
                non_premium += 1
            if str(_.dev_type).lower() == 'frontend':
                frontend_devs += 1
            elif str(_.dev_type).lower() == 'backend':
                backend_devs += 1
            else:
                pass
        else: 
            non_active_users += 1

    context= {
        'users': {
            'active_users': active_users,
            'non_active_users': non_active_users,
            'total_users': (active_users + non_active_users),
            'is_premium': is_premium,
            'non_premium': non_premium,
        },
        'dev': {
            'frontend': frontend_devs,
            'backend': backend_devs,
            'total_devs': (frontend_devs + backend_devs),
        },
        'wallet': {
            'project': projectBalance,
            'users': usersBalance,
            'team': teamBalance,
            'allWallets': WalletModel.objects.all(),
        }
    }
    return render(request, 'dev_admin/admin/index.html', context= context)

def admin_register(request):
    context= {
        'status': AdminDeveloperStatusModel.objects.all()
    }
    return render(request, 'dev_admin/register.html', context= context)

def admin_logIn(request):
    messages_to_display= messages.get_messages(request)
    if request.method == 'POST':
        activation_needed= False
        userObject= None
        form= LoginForm(request, data=request.POST)

        #Checking if account is active
        user= CustomUserModel.objects.get(username= request.POST.get('username'))
        if user.is_active:
            activation_needed= False
        else:
            activation_needed= True
            userObject= user

        if form.is_valid():
            if user.is_staff:
                username= form.cleaned_data.get('username')
                password= form.cleaned_data.get('password')
                user= auth.authenticate(request, username= username, password= password)
                if user is not None:
                    auth.login(request, user)
                    if request.user.is_premium:
                        #get notifications if any
                        messages.info(request, f'Dear {request.user.username} you have 4 unread notifications.')
                    else:
                        messages.info(request, f'Dear {request.user.username} your account is not a premium account you can upgrade to a premium account to enjoy the full benefits.')
                    if request.user.dev_type != '':
                        return redirect('dev-index')
                    else:
                        return redirect('admin-index')
            else:
                messages.error(request, f"Dear {user.username}, you are not authorized to use the Administrator's or Developer's login section")
                return redirect('login')

            return redirect('index')
        else:
            if activation_needed:
                 messages.error(request, 'Your account is not yet activated. Please check your email for the activation link we just sent to you to activate the account.')
                 send_activation_link(request, userObject)
                 return redirect('login')
            else:
                messages.error(request, f'Make sure your are credentials are valid')
                return redirect('login')
    context= {
        'messages': messages_to_display,
        'form': LoginForm
    }
    return render(request, 'dev_admin/login.html', context= context)

def questions_base(request):
    context= {

    }
    return render(request, 'dev_admin/admin/questions_base.html', context= context)

def add_level(request):
    if request.method == 'POST':
        level= request.POST.get('question-level')
        checkIfCatExist= QuestionLevel.objects.get(name= level)
        if checkIfCatExist is not None:
            messages.error(request, f'Level {level} exist already')
            return redirect('add-level')
        else:
            newlevel= QuestionLevel.objects.create(name= level)
            newlevel.save()
            messages.success(request, 'Level added successfully')
            return redirect('questions-base')
    levels= QuestionLevel.objects.all()
    context= {
        'levels': levels
    }
    return render(request, 'dev_admin/admin/add_level.html', context= context)

def add_category(request):
    if request.method == 'POST':
        category= request.POST.get('question-category')
        checkIfCatExist= QuestionsCategory.objects.get(name= category)
        if checkIfCatExist is not None:
            messages.error(request, f'Category {category} exist already')
            return redirect('add-category')
        else:
            newcategory= QuestionsCategory.objects.create(name= category)
            newcategory.save()
            messages.success(request, 'Category added successfully')
            return redirect('questions-base')
    categorys= QuestionsCategory.objects.all()
    context= {
        'categorys': categorys
    }
    return render(request, 'dev_admin/admin/add_category.html', context= context)


def add_questions(request):
    if request.method == 'POST':
        question= request.POST.get('question')
        correctAns= request.POST.get('correct-ans')
        incorrectAns= request.POST.get('incorrect-ans')
        category= request.POST.get('category')
        level= request.POST.get('level')

        categoryObject= QuestionsCategory.objects.get(name= category)
        levelObject= QuestionLevel.objects.get(name= level)

        new_question= QuestionsModel.objects.create(question=question, category=categoryObject, level=levelObject, correct_answer= correctAns, incorrect_answers= incorrectAns)
        new_question.save()
        messages.success(request, 'Question added successfully')
        return redirect('questions-base')
    categories= QuestionsCategory.objects.all()
    levels= QuestionLevel.objects.all()
    context= {
        'categories': categories,
        'levels': levels,
    }
    return render(request, 'dev_admin/admin/add_questions.html', context= context)

# End of admin features
# Developers features
def dev_index(request):
    context= {

    }
    return render(request, 'dev_admin/developers/index.html', context= context)

def dev_register(request):
    pass

def dev_logIn(request):
    pass

# End of Developers features 

def dev_admin_logout(request):
    logout_page()
