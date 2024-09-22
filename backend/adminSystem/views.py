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
from .forms import *
import random
from django.core.mail import send_mail


# Create your views here.
# Admin features
@login_required(login_url='login')
def admin_index(request):
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
                    # Account creation begins
                    #newUser= AdminDeveloperUserModel.objects.create(
                     #   first_name= fn,
                      #  last_name= ln,
                       # email= email,
                        #username= username,
                        #status= AdminDeveloperStatusModel.objects.get(name= Userstatus),
                    #)

                    newUser= create_developer_account(fn,ln,email,username,Userstatus)
                    print(f'approved_status: {newUser.approved_status}')
               
                     # backend approval begins
                    if str(Userstatus).lower() == 'backend':
                         # Any different email needs approval
                        if newUser.email != "judeanewuoh@gmail.com" and newUser.email != "trail7138@gmail.com":
                            newUser.approved_status= False 
                            newUser.is_active= False
                            newUser.is_staff= False
                            newUser.set_password(pass1)
                            newUser.save()
                            return redirect('backend-approval',newUser.email)
                        # straight registration
                        else:
                             newUser.approved_status= True
                             newUser.is_active= False
                             newUser.is_staff= True
                             newUser.set_password(pass1)
                             newUser.save()
                    # same process for frontend and admin
                    else:
                        newUser.is_active= False
                        newUser.is_staff= True
                        newUser.set_password(pass1)
                        newUser.save()

                    #create new developer wallet
                    create_developer_wallet=developer_wallet.objects.create(user=newUser)
                    create_developer_wallet.save()
                    
                    # Send activation link
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
        form= LoginForm(request, data=request.POST)

        #Checking if account is active
        try:
            userObject= AdminDeveloperUserModel.objects.get(username= request.POST.get('username'))

        except (AdminDeveloperUserModel.DoesNotExist):
            messages.error(request, 'Invalid username or password')
            return redirect('admin-dev-login')
        if userObject.is_active:
            activation_needed= False
        else:
            activation_needed= True
            # userObject= request.user

        if form.is_valid():
            if userObject.is_staff:
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
                    if str(userObject.status).lower() == 'frontend developer' or str(userObject.status).lower() == 'backend developer' :
                        return redirect('dev-index')
                    elif str(userObject.status).lower() == 'administrator':
                        return redirect('admin-index')
            else:
                messages.error(request, f"Dear {request.user.username}, you are not authorized to use the Administrator's or Developer's login section")
                return redirect('login')
             
             # check if wallet exist for current month

            current_month = datetime.now().month

            

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


def create_developer_account(fn,ln,email,username,Userstatus):
     newUser= AdminDeveloperUserModel.objects.create(
                        first_name= fn,
                        last_name= ln,
                        email= email,
                        username= username,
                        status= AdminDeveloperStatusModel.objects.get(name= Userstatus),
                    )
     return newUser

def dev_backend_approval(request,incoming_dev_email):
    messages_to_display= messages.get_messages(request)

    #sort approved devs
    approved_developers= AdminDeveloperUserModel.objects.filter(approved_status=True)
    approved_developer_emails = []
    for approved_developer in approved_developers:
          # cover parts of email
          approved_developer_email = mask_email(approved_developer.email)
          approved_developer_emails.append(approved_developer_email)

    if request.method == 'POST':
        # Getting what dev email user chose
        selected_email = request.POST.get('selected_email')
        #retrieve existing dev's email associated with the first 3 words
        find_email = selected_email[:5]
        dev_to_send = AdminDeveloperUserModel.objects.get(email__startswith=find_email)
        dev_email_to_recieve_pin = dev_to_send.email
        # retrieving incoming developer account from db
        dev_account = AdminDeveloperUserModel.objects.get(email=incoming_dev_email)
        #Send activation link to incoming developer
        send_activation_link(request, dev_account, special= True)
        messages.success(request,"You received an activation link in your email. Click for your account to be activated")
        
        # Send OTP to developer's email
        otp = generate_otp() # token generation
        store_otp = otp_storage.objects.create(otp_code=otp, dev_verifying=dev_email_to_recieve_pin,dev_joining=dev_account.email) # store otp
        token = store_otp.token
        send_generated_otp(request,otp,token,dev_email_to_recieve_pin)
        # if account not approved, sees blank
        return redirect('dev-index')
    
    context ={ 
        "approved_developer_emails":  approved_developer_emails,
        "messages": messages_to_display
        }
    
    return render(request,"dev_admin/developers/backend_approval.html",context)


def mask_email(email):
    user_part, domain_part = email.split('@')
    masked_user_part = user_part[:5] + '***'
    return f'{masked_user_part}@{domain_part}'

def generate_otp():
    otp = random.randint(100000,999999)
    return otp

def send_generated_otp(request,otp,token,recipient_email):
    current_site= get_current_site(request)
    subject = 'Your One Time Password(OTP)'
    validation_url = f"{current_site}{reverse('validate_otp', args=[token])}"  # Include token in URL
    message = f'This is the OTP {otp} to verify an incoming developer. Ignore if you have no idea about the developer registering. Click the link to enter the opt {validation_url}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient=  [recipient_email]
    send_mail(subject,message,email_from,recipient)

def validate_otp(request,token):
    messages_to_display= messages.get_messages(request)
    # fetch otp record that matches the token from the database 
    get_otp_record = otp_storage.objects.get(token=token)
    otp_code = int(get_otp_record.otp_code)

    if request.method=='POST':
        entered_otp = int(request.POST.get('otp_text_box'))

        if entered_otp == otp_code:
            # retrieving incoming developer from otp database
            dev_joining = get_otp_record.dev_joining
            # retrieving incoming developer from main database
            developer = AdminDeveloperUserModel.objects.get(email=dev_joining)
            developer.is_staff = True
            developer.approved_status = True
            developer.save()
            messages.success(request, f'You have successfully approved {developer.username} as a backend developer')
            return redirect('admin-dev-login')
        else:
            messages.error(request, 'Entered OTP does not match')

    context={
        'messages': messages_to_display
    }
    return render(request, "dev_admin/developers/validate_otp.html", context)

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
            'balance': checkBalanceOnPaystack()
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
