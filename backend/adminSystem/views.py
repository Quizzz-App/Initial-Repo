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
        fn= request.POST.get('first-name')
        ln= request.POST.get('last-name')
        username= request.POST.get('username')
        email= request.POST.get('email')
        pass1= request.POST.get('password')
        pass2= request.POST.get('password2')
        Userstatus= request.POST.get('status')
        print(fn, ln, username, email, pass1, Userstatus)
        if pass1 == pass2:
            try:
                checkUsername= AdminDeveloperUserModel.objects.get(username= username)
            except (AdminDeveloperUserModel.DoesNotExist):
                checkUsername= None
            if checkUsername is not None:
                messages.error(request, f"Dear user, an account with this username already exist")
                return redirect('admin-dev-signup')
            else:
                try:
                    checkEmail= AdminDeveloperUserModel.objects.get(email= email)
                except (AdminDeveloperUserModel.DoesNotExist):
                    checkEmail= None
                if checkEmail is not None:
                    messages.error(request, f"Dear user, an account with this email already exist")
                    return redirect('admin-dev-signup')
                else:
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
                    newUser.set_password(pass1)
                    newUser.save()
                    #create new developer wallet
                    create_developer_wallet=developer_wallet.objects.create(user=newUser)
                    create_developer_wallet.save()
                    send_activation_link(request, newUser, special= True)
                    messages.success(request, 'Please check your email to complete the registration..') #Notifying user after the mail has been sent
                    return redirect('admin-dev-login')
        else:
            messages.error(request, f"Dear user, passwords does not match")
            return redirect('admin-dev-signup')

    context= {
        'status': AdminDeveloperStatusModel.objects.all()
                }
    return render(request, 'dev_admin/register.html', context= context)

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
    context= {
    }
    return render(request, 'dev_admin/admin/questions_base.html', context= context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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


@login_required(login_url='login')
def add_questions(request):
    if request.method == 'POST':
        question= request.POST.get('question')
        correctAns= request.POST.get('correct-ans')
        incorrectAns= request.POST.get('incorrect-ans')
        category= request.POST.get('category')
        level= request.POST.get('level')

        categoryObject= QuestionsCategory.objects.get(name= category)
        levelObject= QuestionLevel.objects.get(name= level)

        new_question= QuestionsModel.objects.create(question=question, category=categoryObject, level=levelObject, correct_answer= correctAns, incorrect_answers= incorrectAns, aurthor= request.user.username)
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
