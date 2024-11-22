from django.contrib.auth.decorators import login_required
from authenticationSystem.models import CustomUserModel
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth 
from authenticationSystem.views import *
from authenticationSystem.forms import *
from questionSystem.models import *
from django.contrib import messages
from paymentSystem.models import *
from paymentSystem.views import *
from .models import *


# Create your views here.
# Admin features

@login_required(login_url='login')
def admin_index(request):
    userObject= AdminDeveloperUserModel.objects.get(username= request.user.username)
    availableCourses= QuestionsCategory.objects.all()
    team= []
    ovD= 0
    ovW= 0
    activeUsers= len(CustomUserModel.objects.filter(is_active= True))
    nonactiveUsers= len(CustomUserModel.objects.filter(is_active= False))
    premiumUsers= len(CustomUserModel.objects.filter(is_premium= True))
    NonPremiumUsers= len(CustomUserModel.objects.filter(is_premium= False))
    for x in AdminDeveloperUserModel.objects.all():
        if x.username != request.user.username:
            team.append(x)
    for x,_ in enumerate(TransactionModel.objects.all()):
        if _.transactionType == 'Deposit' and _.transactionTypeStatus == 'Success':
            ovD += int(_.amount)
        elif _.transactionType == 'Withdrawal' and _.transactionTypeStatus == 'Success':
            ovW += int(_.amount)
    print(ovD, ovW)
    context= {
        'user_status': userObject.status,
        'aC': len(availableCourses),
        'team': len(team),
        'accounts': {
            'aU': activeUsers,
            'naU': nonactiveUsers,
            'prU': premiumUsers,
            'nprU': NonPremiumUsers,
        },
        'finance': {
            'ovD': ovD,
            'ovW': ovW,
        }
    }
    return render(request, 'sitepages/admintetapages/dashboard/index.html', context= context)

@login_required(login_url='login')
def admin_indexT(request):
    all_users= CustomUserModel.objects.all()
    all_team= AdminDeveloperUserModel.objects.all()
    withdrawals= IssueWithdrawModel.objects.all()

    active_users= 0
    non_active_users= 0
    is_premium= 0
    non_premium= 0
    frontend_devs= 0
    backend_devs= 0
    administrator= 0

    projectBalance= 0
    usersBalance= 0
    teamBalance= 0

    completedWithdrawals= 0
    inprocessWithdrawals= 0


    msgs= Notifications.objects.filter(user= request.user, read= False)
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
        else: 
            non_active_users += 1

    for i, _ in enumerate(all_team):
        if str(_.status).lower() == 'frontend developer':
            frontend_devs += 1
        elif str(_.status).lower() == 'backend developer':
            backend_devs += 1
        elif str(_.status).lower() == 'administrator':
            administrator += 1
        else:
            pass
    
    for i, _ in enumerate(withdrawals):
        if _.status:
            completedWithdrawals += 1
        else:
            inprocessWithdrawals += 1

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
        },
        'msgs': msgs,
        'withdrawals': {
            'requested': len(withdrawals),
            'completed': completedWithdrawals,
            'inprocess': inprocessWithdrawals,
        },


    }
    return render(request, 'dev_admin/admin/index.html', context= context)

def admin_dev_register(request):
    if request.method == 'POST':
        fn= request.POST.get('fn')
        ln= request.POST.get('ln')
        username= request.POST.get('un')
        email= request.POST.get('em')
        pass1= request.POST.get('po')
        pass2= request.POST.get('pt')
        Userstatus= request.POST.get('status')
        print(fn, ln, username, email, pass1, Userstatus)
        response= makeCheck(username, email, pass1, pass2)
        if response['status']:  
            newUser= AdminDeveloperUserModel.objects.create(
                first_name= fn,
                last_name= ln,
                email= email,
                username= username,
                status= AdminDeveloperStatusModel.objects.get(name= Userstatus),
            )
            if str(Userstatus).lower() == 'backend':
                newUser.approved_status= True
            newUser.is_active= False
            newUser.is_staff= True
            newUser.is_superuser= True
            newUser.set_password(pass1)
            newUser.save()
            #create new developer wallet
            create_developer_wallet=developer_wallet.objects.create(user=newUser)
            create_developer_wallet.save()
            send_activation_link(request, newUser, special= True)
            messages.success(request, 'Please check your email to complete the registration..') #Notifying user after the mail has been sent
            response= {
                'status': 'ok'
            }
            return JsonResponse(response, safe= False)
        else:
            messages.error(request, f"Dear user, passwords does not match")
            return redirect('admin-dev-signup')
    status= AdminDeveloperStatusModel.objects.all()
    print(len(status))
    if len(status) == 0:
        AdminDeveloperStatusModel.objects.create(name= 'Backend Developer').save()
        AdminDeveloperStatusModel.objects.create(name= 'Administrator').save()
    else:
        pass
    context= {
        'status': status,
        'url': '/542b0993-3d6d-450c-89c0-191d6ad5fca6/admin-dev/register/'
                }
    return render(request, 'sitepages/adminauthpages/signuppage/index.html', context= context)

def admin_dev_logIn(request):
    messages_to_display= messages.get_messages(request)
    if request.method == 'POST':
        activation_needed= False
        userObject= None
        username= request.POST.get('username')
        password= request.POST.get('password')

        #Checking if account is active
        try:
            userObject= AdminDeveloperUserModel.objects.get(username= username)
        except (AdminDeveloperUserModel.DoesNotExist):
            return JsonResponse({'msg':'Account does not exist', 'status': 'Failed'}, safe= False)
        if userObject.is_active:
            activation_needed= False
        else:
            activation_needed= True

        if activation_needed:
            send_activation_link(request, userObject)
            return JsonResponse({'msg': 'Your account is not yet activated. Please check your email for the activation link we just sent to you to activate the account.', 'status': 'Failed'}, safe= False)
        else:
            user= auth.authenticate(request, username= username, password= password)
            if user is not None:
                url= ''
                auth.login(request, user)
                if str(userObject.status).lower() == 'frontend developer' or str(userObject.status).lower() == 'backend developer' :
                    url= '/542b0993-3d6d-450c-89c0-191d6ad5fca6/admin-dev/developers/'
                elif str(userObject.status).lower() == 'administrator':
                    url= '/542b0993-3d6d-450c-89c0-191d6ad5fca6/admin-dev/admin/'
                else:
                    pass
                response= {
                    'msg': 'Authenticated',
                    'status': 'Success',
                    'url': url
                }
                return JsonResponse(response, safe= False)
            else:
                return JsonResponse({'msg':'Invalid Credentials', 'status': 'Failed'})
    return render(request, 'sitepages/adminauthpages/loginpage/index.html', context= {})

@login_required(login_url='login')
def questions_base(request):
    questions= QuestionsModel.objects.all()
    categories= QuestionsCategory.objects.all()
    levels= QuestionLevel.objects.all()
    lD={}
    mg_cat= {}
    mg_lev= {}
    for level in levels:
        lD[level.name] = len(QuestionsModel.objects.filter(level= level))
    for index, element in enumerate(categories):
        mg_cat[index]= {
            'name': f'{element.name}',
            'img_url': f'{element.categoryImg.url}',
            'questions': len(QuestionsModel.objects.filter(category= element))
        }
    for index, element in enumerate(levels):
        mg_lev[index]= {
            'name': f'{element.name}',
            'questions': len(QuestionsModel.objects.filter(level= element))
        }
    print(mg_cat)
    context= {
        'data': {
            'questions':len(questions),
            'categories': len(categories),
            'level': len(levels),
            'levelsData': lD,
            'cat': categories,
            'lev': levels
            },
        'mg_course': mg_cat,
        'mg_level': mg_lev,
        'allQ': questions,
    }
    return render(request, 'sitepages/admintetapages/uploadpage/index.html', context= context)

@login_required(login_url='login')
@csrf_exempt
def add_level(request):
    if request.method == 'POST':
        level= request.POST.get('question-level')
        try:
            checkIfCatExist= QuestionLevel.objects.get(name= level)
        except QuestionLevel.DoesNotExist:
            checkIfCatExist= None
        if checkIfCatExist is not None:
            return JsonResponse({'status': 'Failed', 'msg': 'Level already exist'}, safe= False)
        else:
            newlevel= QuestionLevel.objects.create(name= level)
            newlevel.save()
            return JsonResponse({'status': 'Success', 'msg': 'Level added successfully'}, safe= False)
    levels= QuestionLevel.objects.all()
    context= {
        'levels': levels
    }
    return render(request, 'dev_admin/admin/add_level.html', context= context)

@login_required(login_url='login')
@csrf_exempt
def updatelevel(request):
    if request.method == 'POST':
        level= request.POST.get('question-level')
        old= request.POST.get('old')
        try:
            checkIfCatExist= QuestionLevel.objects.get(name= old)
        except QuestionLevel.DoesNotExist:
            checkIfCatExist= None
        if checkIfCatExist is not None:
            checkIfCatExist.name = level
            checkIfCatExist.save()
            return JsonResponse({'status': 'Success', 'msg': 'Level updated successfully'}, safe= False)
        else:
            return JsonResponse({'status': 'Failed', 'msg': 'Level does not exist'}, safe= False)

    levels= QuestionLevel.objects.all()
    context= {
        'levels': levels
    }
    return render(request, 'dev_admin/admin/update_level.html', context= context)

@login_required(login_url='login')
@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        category= request.POST.get('question-category')
        img= request.FILES.get('img')
        try:
            checkIfCatExist= QuestionsCategory.objects.get(name= category)
        except QuestionsCategory.DoesNotExist:
            checkIfCatExist= None
        if checkIfCatExist is not None:
            return JsonResponse({'status': 'Failed', 'msg': 'Course already exist'}, safe= False)
        else:
            newcategory= QuestionsCategory.objects.create(name= category, categoryImg= img)
            newcategory.save()
            return JsonResponse({'status': 'Success', 'msg': 'Course added successfully'}, safe= False)

    categorys= QuestionsCategory.objects.all()
    context= {
        'categorys': categorys
    }
    return render(request, 'dev_admin/admin/add_category.html', context= context)

@login_required(login_url='login')
@csrf_exempt
def updateCat(request):
    if request.method == 'POST':
        title= request.POST.get('course')
        img= request.POST.get('img')
        old= request.POST.get('old')
        obj= QuestionsCategory.objects.get(name= old)
        if img == '':
            obj.name= title
        else:
            obj.name= title
            obj.categoryImg= img
        obj.save()
        return JsonResponse({'status': 'Success', 'msg': 'Course added successfully'}, safe= False)
@login_required(login_url='login')
@csrf_exempt
def add_questions(request):
    if request.method == 'POST':
        question= request.POST.get('question')
        correctAns= request.POST.get('correct-ans')
        incorrectAns= request.POST.get('incorrect-ans')
        category= request.POST.get('category')
        level= request.POST.get('level')
        try:
            categoryObject= QuestionsCategory.objects.get(name= category)
            levelObject= QuestionLevel.objects.get(name= level)
        except (QuestionsCategory.DoesNotExist, QuestionLevel.DoesNotExist):
            return JsonResponse({'status': 'Failed', 'msg': 'Please select the correct course or level. One of them does not exist.'}, safe= False)

        new_question= QuestionsModel.objects.create(question=question, category=categoryObject, level=levelObject, correct_answer= correctAns, incorrect_answers= incorrectAns, aurthor= request.user.username)
        new_question.save()
        return JsonResponse({'status': 'Success', 'msg': 'Question added successfully'}, safe= False)
    categories= QuestionsCategory.objects.all()
    levels= QuestionLevel.objects.all()
    context= {
        'categories': categories,
        'levels': levels,
    }
    return render(request, 'dev_admin/admin/add_questions.html', context= context)

@login_required(login_url='login')
@csrf_exempt
def updateQuestion(request):
    if request.method == 'POST':
        uid= request.POST.get('id')
        question= request.POST.get('question')
        correctAns= request.POST.get('correct-ans')
        incorrectAns= request.POST.get('incorrect-ans')
        
        questionObject= QuestionsModel.objects.get(uID= uid)
        questionObject.question= question
        questionObject.correct_answer= correctAns
        questionObject.incorrect_answers= incorrectAns
        questionObject.save()
        return JsonResponse({'status': 'Success', 'msg': 'Question updated successfully'}, safe= False)

def getQuery(list):
    if len(list) >= 5:
        return 5
    else:
        return len(list)

@login_required(login_url='login')
def userManagement(request):
    query= 0
    usersObj=[]
    all_accounts= CustomUserModel.objects.all()
    devs= AdminDeveloperUserModel.objects.all()
    for x in all_accounts:
        if x not in devs:
            usersObj.append(x)
    usersObj= usersObj[::-1][:getQuery(usersObj)]
    contex= {
        'UAI': usersObj,
        'query': query,
        'active': len(CustomUserModel.objects.filter(is_active= True)),
        'deactive': len(CustomUserModel.objects.filter(is_active= False)),
        'team': len(AdminDeveloperUserModel.objects.all())
    }
    return render(request, 'sitepages/admintetapages/usermanagement/index.html', context=contex)

@login_required(login_url='login')
def financePage(request):
    deposits, withdrawals= [], []
    query= 5
    ovD=0
    ovW=0
    for x in TransactionModel.objects.all():
        if x.transactionType == 'Withdrawal':
            withdrawals.append(x)
        elif x.transactionType == 'Deposit':
            deposits.append(x)
    deposits= deposits[::-1][:getQuery(deposits)]
    withdrawals= withdrawals[::-1][:getQuery(deposits)]
    for x,_ in enumerate(TransactionModel.objects.all()):
        if _.transactionType == 'Deposit' and _.transactionTypeStatus == 'Success':
            ovD += int(_.amount)
        elif _.transactionType == 'Withdrawal' and _.transactionTypeStatus == 'Success':
            ovW += int(_.amount)
    contex={
        'd': deposits,
        'w': withdrawals,
        'ovD': ovD,
        'ovW': ovW,
    }
    return render(request, 'sitepages/admintetapages/financials/index.html', context=contex)
def getMetrics(request, username):
    user= CustomUserModel.objects.get(username= username)
    useraccount= None
    usertransactions= None
    try:
        useraccount= AccountModel.objects.get(user= user)
        usertransactions= TransactionModel.objects.filter(account= useraccount)
    except:
        pass
    generalQuizAccuracy= 0
    highestScore=0
    quizTaken=0
    userQuizzes= []
    td=0
    tw=0
    ub=0
    tre=0
    try:
        userQuizzes= QuizHistory.objects.filter(user= user)
        quizTaken= len(userQuizzes)
        for x in userQuizzes:
            if float(x.score) > float(highestScore):
                highestScore= float(x.score)
            generalQuizAccuracy += float(x.score)
        try:
            generalQuizAccuracy= float(generalQuizAccuracy/float(quizTaken))
        except ZeroDivisionError:
            generalQuizAccuracy= 0
    except:
        pass
    if usertransactions is not None and useraccount is not None:
        for x in usertransactions:
            if x.transactionType == 'Deposit' and x.transactionTypeStatus == 'Success':
                td += x.amount
            if x.transactionType == 'Withdrawal' and x.transactionTypeStatus == 'Failed':
                tw += x.amount
        ub= useraccount.get_balance()
    for x in ReferralModelHistory.objects.filter(user= user):
        tre += float(x.points_earned) * 30

    data= {
        'userID': f"User_{user.pk}",
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'is_premium': user.is_premium,
        'tr': (user.referrals + user.indirectReferrals),
        'qt': len(userQuizzes),
        'hq': highestScore,
        'gqa': generalQuizAccuracy,
        'wb': ub,
        'td': td,
        'tw': tw,
        'tre': tre,
    }
    return JsonResponse(data, safe= True)

@login_required(login_url='login')
def siteAnalytics(request):
    contex={
        'active': len(CustomUserModel.objects.filter(is_active= True)),
        'signups': len(CustomUserModel.objects.all()),
    }
    return render(request, 'sitepages/admintetapages/analytics/index.html', context=contex)

@login_required(login_url='login')
def teamInfo(request):
    contex={
    }
    return render(request, 'sitepages/admintetapages/teaminfo/index.html', context=contex)

@login_required(login_url='login')
def make_payment(request, paymentID):
    pendingPaymentObjects= WithdrwalSheetsModel.objects.filter(completedTransfers= False)
    if len(pendingPaymentObjects) != 0:
        messages.error(request, 'Please complete all pending payments')
        return redirect('pending-payment')
    issuedWithdrawalObject= IssueWithdrawModel.objects.get(uuid= paymentID)
    issuerObject= CustomUserModel.objects.get(username= issuedWithdrawalObject.issuer)
    recipeitObject= RecieptModel.objects.get(user= issuerObject)
    context= {
        'issuer': {
            'name': issuerObject.username,
            'balance': AccountModel.objects.get(user= issuerObject).balance,
            'withdrawal': issuedWithdrawalObject.amount,
            'ID': recipeitObject.uuid,
            'withdrawalID': issuedWithdrawalObject.uuid,
        },
        'pWallet': {
            'balance': 90 #checkBalanceOnPaystack()
        },
        'nftID': paymentID,
    }
    return render(request, 'dev_admin/admin/payment.html', context= context)


# End of admin features
# Developers features
@login_required(login_url='login')
def dev_index(request):
    developers_wallet = developer_wallet.objects.get(user=request.user)
    msgs= Notifications.objects.filter(user= request.user, read= False)

    context= {
        'msgs': msgs,
        'wallet_balance': developers_wallet.balance,
        'month_name': developers_wallet.name
    }
    
    return render(request, 'dev_admin/developers/index.html', context= context)


@login_required(login_url='login')
def dev_transaction_history(request):
    # retreive the developer's wallet
    developers_wallet = developer_wallet.objects.get(user=request.user)
    month = developers_wallet.name
    amount = developers_wallet.get_month_amount()
    
    context= {
    'month': month,
    'amount': amount
    }
    return render(request,'dev_admin/developers/transaction.html',context= context)



def dev_register(request):
    pass

def dev_logIn(request):
    pass

# End of Developers features 

def dev_admin_logout(request):
    logout_page()
