from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from adminSystem.models import AdminDeveloperUserModel
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth.models import User, auth 
# from django.shortcuts import get_object_or_404
from questionSystem.models import QuizHistory
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.contrib import messages
from paymentSystem.models import *
from referralSystem.views import *
from questionSystem.views import *
from paymentSystem.views import *
from django.conf import settings
from django.urls import reverse
from .tokensGenerator import *
from .models import *
from .forms import *

# Create your views here.
# @login_required(login_url='login')

def send_message(recipient, message, action_required= False, action= '', actionID= ''):
    msg= Notifications.objects.create(user= recipient, notification= message, action_required= action_required, action= action, actionID= actionID)
    msg.save()

def index(request):
    messages_to_display= messages.get_messages(request)
    userAccountType= 'Non-Premium User'
    userAccountBalance= 0
    refLink= ''   
    msgs= ''
    specialAccount= False
    specialAccountType= ''
    userObject= None
    notWithDraw= True
    try:
        userObject= AdminDeveloperUserModel.objects.get(username= request.user.username)
        specialAccount= True
        if str(userObject.status).lower() == 'administrator':
            specialAccountType= 'admin'
    except (AdminDeveloperUserModel.DoesNotExist):
        print('Does not exist')
    try:
        if request.user.is_authenticated:
            userAccount= AccountModel.objects.get(user=request.user)
            if request.user.is_premium:
                userAccountType= 'Premium User'
                refLink= referral_link(get_current_site(request), request.user.referral_code)
                msgs= Notifications.objects.filter(user= request.user, read= False)
            userAccount.update_balance()
            userAccountBalance= userAccount.balance
            if userAccountBalance > 0:
                notWithDraw= False
        else:
            pass
    except AccountModel.DoesNotExist:
        pass

    return render(request, 'landingpage.html', context= {
        'messages': messages_to_display,
        'isPremium': {
            'accountType': userAccountType,
            'accountBalance': userAccountBalance,
            'refLink': refLink,
            'ref_data': get_referrals_data(request),
        },
        'ntfs': msgs,
        'notWithDraw': notWithDraw,
        'specialAccount': {
            'exist': specialAccount,
            'type': specialAccountType,
        },
    })

def inviteRedirect(request, code):
    return redirect(reverse('register') + '?ref=' + code)


def makeCheck(un, em, p1, p2):
    if p1 != p2:
        response= {
            'status': False,
            'msg': 'Password\'s doesn\'t match'
        }
        return response
    else:
        if CustomUserModel.objects.filter(username= un).exists():
            response= {
            'status': False,
            'msg': 'Username already exist'
        }
            return response
        elif CustomUserModel.objects.filter(email= em).exists():
            response= {
            'status': False,
            'msg': 'Email already exist'
        }
            return response
        else:
            response= {
            'status': True,
            'msg': ''
        }
            return response
def register_user(request):
    refCode=None
    try:
        refCode= request.GET.get('ref')
    except:
        pass
    messages_to_display= messages.get_messages(request)
    form= RegistrationForm()
    if request.method == 'POST':
        firstName= request.POST.get("fn")
        lastName= request.POST.get("ln")
        userName= request.POST.get("un")
        userEmail= request.POST.get("em")
        userPassword= request.POST.get("po")
        userConfirmPassword= request.POST.get("pt")
        response= makeCheck(un= userName, em= userEmail, p1= userPassword, p2= userConfirmPassword)
        refCode= request.POST.get('ref')
        if refCode is None:
            refCode= ''
        if response['status']:
            user= CustomUserModel.objects.create_user(first_name= firstName, last_name= lastName, username= userName, email= userEmail, password= userPassword)
            user.save()
            current_site= get_current_site(request) #Geting the curent site domain
            token= TokenGeneratorValidator.make_token(user) #Generating hash 
            tokenID= TokensModel.objects.create(token=token, user_id=user.id, refCode= refCode) # Registering token to database
            tokenID.save()
            mail_subject= 'Account Activation' #Email to be sent preparation process
            message= render_to_string('auth/mail/accountActivation.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
                'special': 0,
            })
            email= EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.send()
            response= {
                'status': 'ok'
            }
            return JsonResponse(response, safe= False)
        else:
            messages.error(request, response['msg'])
            return redirect(reverse('register') + '?ref=' + refCode)
            
    return render(request, 'sitepages/signuppage/index.html', context= {
        'form': RegistrationForm,
        'messages': messages_to_display, 
        'refCode': refCode
    })

# Account activation
def activate(request, uidb64, token, special): 
    user= auth.get_user_model()

    try: # Decoding the hashes recieved from the link to verify if it a valid link to activate their account
        uid= force_str(urlsafe_base64_decode(uidb64))
        if int(special) == 1:
            user= AdminDeveloperUserModel.objects.get(pk= uid)
        else:
            user= User.objects.get(pk= uid)
    except (TypeError, ValidationError, OverflowError, User.DoesNotExist):
        user= None

    if user is not None and TokenGeneratorValidator.check_token(user, token, settings.ACCOUNT_ACTIVATION_TOKEN_EXPIRY_DURATION, special= int(special)): # checking the validity of the token
        user.is_active= True
        user.save()
        TokensModel.objects.get(token= token).delete()
        # auth.login(request, user)
        messages.success(request, 'Your account has been activated successfully')
        if int(special) == 1:
            return redirect(reverse('admin-dev-login'))
        else:
            return redirect(reverse('login'))
    else:
        messages.error(request, 'Your account activation failed the link has been expired')
        return redirect('index')
    
def send_activation_link(request,user, special= False):
    if special:
        adminRequest= 1
    else:
        adminRequest= 0
    try:
        get_old_token= TokensModel.objects.get(user_id=user.id)
        refCode= get_old_token.refCode
        get_old_token.delete() # Deleting the old token before creating a new one
    except (TokensModel.DoesNotExist):
        refCode= ''
    current_site= get_current_site(request) #Geting the curent site domain
    token= TokenGeneratorValidator.make_token(user) #Generating hash 
    tokenID= TokensModel.objects.create(token=token, user_id=user.id, refCode= refCode) # Registering token to database
    tokenID.save()
    mail_subject= 'Account Activation' #Email to be sent preparation process
    message= render_to_string('auth/mail/accountActivation.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
        'special': adminRequest,
    })
    email= EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.send()

def login_page(request, *args, **kwargs):
    messages_to_display= messages.get_messages(request) #Checking if any message is available to be displayed to the user 
    form= LoginForm()
    if request.user.is_authenticated:
        return redirect("user-dashboard", username= request.user.username)
    else:
        if request.method == 'POST':
            activation_needed= False
            userObject= None
            username= request.POST.get("un")
            password= request.POST.get("ps")

            print(password)

            #Checking if account is active
            user= CustomUserModel.objects.get(username= username)
            if user.is_active:
                activation_needed= False
            else:
                activation_needed= True
                userObject= user

            if not activation_needed:
                user= auth.authenticate(request, username= username, password= password)
                if user is not None:
                    auth.login(request, user)
            
                    if request.user.is_premium:
                        #get notifications if any
                        messages.info(request, f'Dear {request.user.username} you have 4 unread notifications.')
                    else:
                        messages.info(request, f'Dear {request.user.username} your account is not a premium account you can upgrade to a premium account to enjoy the full benefits.')
                    print("redirecting")
                    response= {
                        'status': 200,
                        'un': request.user.username,
                        'state': 'Success'

                    }
                    return JsonResponse(response, safe= False)
                return JsonResponse({'status': 200, 'state': 'Failed', 'msg': 'Make sure your are credentials are valid'})
            else:
                if activation_needed:
                    # messages.error(request, 'Your account is not yet activated. Please check your email for the activation link we just sent to you to activate the account.')
                    send_activation_link(request, userObject)
                    return JsonResponse({'status': 200, 'state': 'activation', 'msg': 'Your account is not yet activated. Please check your email for the activation link we just sent to you to activate the account.'})
                else:
                    # messages.error(request, f'Make sure your are credentials are valid')
                    return JsonResponse({'status': 200, 'state': 'Failed', 'msg': 'DDD'})
        elif request.method == 'GET':
            return render(request, 'sitepages/loginpage/index.html', context= {
    'form': LoginForm,
    'messages': messages_to_display
    })

@login_required(login_url='login')
def userDashboard(request, username):
    user= CustomUserModel.objects.get(username= username)
    context= {
        "user": user
    }
    return render(request, 'sitepages/userpages/dashboard/index.html',context= context)

@login_required(login_url='login')
def userRef(request, username):
    dram= 0
    indram= 0
    user= CustomUserModel.objects.get(username= username)
    userAccount= AccountModel.objects.get(user=request.user)
    userBalance= userAccount.update_balance()
    refLink= referral_link(get_current_site(request), request.user.referral_code)
    refHistory= ReferralModelHistory.objects.filter(user= request.user)
    for x in refHistory:
        x.points_earned *= 30
        if str(x.relationship) == "Direct":
            dram += x.points_earned 
        else:
            indram += x.points_earned
    context= {
        "user": user,
        "refLink": refLink,
        "refData": get_referrals_data(request),
        "wBalance": userAccount.balance,
        "refHistory": refHistory,
        "dram": dram,
        "inram": indram
    }
    return render(request, 'sitepages/userpages/referrals/index.html',context= context)

@login_required(login_url='login')
def userQuiz(request, username):
    generalQuizAccuracy=0
    highestScore=0
    quizTaken=0
    userQuizzes= []
    try:
        userQuizzes= QuizHistory.objects.filter(user= request.user)
        quizTaken= len(userQuizzes)
        for x in userQuizzes:
            if float(x.score) > float(highestScore):
                highestScore= float(x.score)
            generalQuizAccuracy += float(x.score)
        generalQuizAccuracy= (generalQuizAccuracy/float(quizTaken))
    except:
        pass

    context= {
        "user": request.user,
        "qT": quizTaken,
        "gA": generalQuizAccuracy,
        "hS": highestScore,
        "qRs": userQuizzes,
    }
    return render(request, 'sitepages/userpages/quizpage/index.html',context= context)

@login_required(login_url='login')
def userWallet(request, username):
    error= False
    transactions= []
    totalW= 0.00
    userBalance= 0
    userTotalEarnings= 0
    user= CustomUserModel.objects.get(username= username)
    try:
        userAccount= AccountModel.objects.get(user=request.user)
        userBalance= userAccount.update_balance()
        userBalance= userAccount.balance
        userTotalEarnings= userAccount.total_earnings
        transactions= TransactionModel.objects.filter(account= userAccount)
        for key,element in enumerate(transactions):
            if element.transactionType == 'Withdrawal' and element.transactionTypeStatus == 'Success':
                totalW += (element.account * 30)
    except:
        error= True
    carriers= get_carriers_banks(request)
    context= {
        "user": user,
        "carriers": carriers,
        "T_history": transactions,
        "error": error,
        "wBalance": userBalance,
        "tEarnings": userTotalEarnings,
        "totalW": totalW,
    }
    return render(request, 'sitepages/userpages/walletandtransaction/index.html',context= context)

@login_required(login_url='login')
def userT(request, username):
    user= CustomUserModel.objects.get(username= username)
    context= {
        "user": user,
    }
    return render(request, 'sitepages/userpages/challenge/index.html',context= context)

@login_required(login_url='login')
def userUP(request, username):
    user= CustomUserModel.objects.get(username= username)
    context= {
        "user": user
        
    }
    return render(request, 'sitepages/userpages/profile/index.html',context= context)

def aboutUP(request):
    context= {

    }
    return render(request, 'sitepages/aboutpage/index.html',context= context)
def logout_page(request, *args, **kwargs):
    auth.logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('index')

def passwordReset(request):
    messages_to_display= messages.get_messages(request)
    form= PasswordResetRequestForm()
    if request.method == 'POST':
        form= PasswordResetRequestForm(request.POST)
        if form.is_valid():
            data= form.cleaned_data.get('email')
            try:
                user= User.objects.get(email= data)
            except (TypeError, ValidationError, User.DoesNotExist):
                user= None

            if user is not None:
                token= TokenGeneratorValidator.make_token(user) #Generating hash 
                tokenID= TokensModel.objects.create(token=token, user_id=user.id) # Registering token to database
                current_site= get_current_site(request) #Geting the curent site domain
                mail_subject= 'Password Reset' #Email to be sent preparation process
                message= render_to_string('auth/mail/passwordResetMail.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token
                })
                to_email= form.cleaned_data.get('email')
                email= EmailMessage(
                mail_subject, message, to=[to_email]
            )
                email.send()
                tokenID.save()
                messages.success(request, 'Please check your email to reset your password..')
                return redirect('index')
            
            
            else:
                messages.error(request, 'No account was found with the provided E-mail. Please check and try again...')
                return redirect('password-reset-request')
    return render(request, 'auth/passwordReset.html', context={
        'form': PasswordResetRequestForm,
        'messages': messages_to_display
    })

def passwordResetConfirm(request, uidb64, token):
    user= auth.get_user_model()

    try: # Decoding the hashes recieved from the link to verify if it a valid link to activate their account
        uid= force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk= uid)
    except (TypeError, ValidationError, OverflowError, User.DoesNotExist):
        user= None
    print(token)
    not_expired = TokenGeneratorValidator.check_token(user, token, settings.PASSWORD_RESET_TOKEN_EXPIRY_DURATION)
    if user is not None and not_expired:
        # TokensModel.delete(token= token)
        return redirect('password-change', id=uidb64)
    else:
        messages.error(request, 'Password reset failed the link has been expired')
        return redirect('index')
    
def passwordChange(request, id):
    forms= PasswordChangeForm()
    if request.method == 'POST':
        form= PasswordChangeForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data.get('email')
            passwordOne= form.cleaned_data.get('passwordOne')
            # passwordTwo= form.cleaned_data.get('passwordTwo')
            try: 
                user= User.objects.get(email= email)
            except (TypeError, ValidationError, User.DoesNotExist):
                user= None
            if user is not None and user.id == int(force_str(urlsafe_base64_decode(id))):
                user.set_password(passwordOne)
                user.save()
                TokensModel.objects.get(user_id= user.id).delete()
                current_site= get_current_site(request) #Geting the curent site domain
                mail_subject= 'Password Reset Confirmation' #Email to be sent preparation process
                message= render_to_string('auth/mail/passwordResetDone.html', {
                    'user': user,
                    'domain': current_site,
                })
                to_email= form.cleaned_data.get('email')
                email= EmailMessage(
                mail_subject, message, to=[to_email]
            )
                email.send()
                messages.success(request, 'Your password has been changed successfully')
                return redirect('index')
            else:
                messages.error(request, 'Password reset failed make sure to use the required E-mail and link')
                return redirect('index')
        else:
            messages.error(request, f'{next(iter(form.errors.values()))[0]}')
            return redirect('index')
    else:
        return render(request, 'auth/newPassword.html', {'form': PasswordChangeForm, 'id': id})
    
@login_required(login_url='login')
def notificationsPage(request):
    userNotifications= Notifications.objects.filter(user= request.user)
    context= {
        'Nft': userNotifications
    }
    return render(request, 'auth/mail/notifications.html', context= context)

@login_required(login_url='login')
def notificationsRead(request, nftID):
    notification_to_display= Notifications.objects.get(uuid= nftID)
    action_todo= ''
    action_required= False
    action_text= 'Action required'
    if notification_to_display.action_required:
        action= notification_to_display.action
        action_required= True
        if str(action) == 'Gift ref':
            action_todo= f'/ref/gift/{notification_to_display.actionID}'
        elif str(action) == 'Withdrawal':
            action_todo= f'/542b0993-3d6d-450c-89c0-191d6ad5fca6/admin-dev/make-payment/{notification_to_display.actionID}'
        elif str(action) == 'Done':
            action_todo= f'#'
            action_text= 'Action Completed'
    context= {
        'message':notification_to_display,
        'action_required': action_required,
        'action_todo': action_todo,
        'action_text': action_text,
        }
    return render(request, 'auth/mail/notifications_page.html', context= context)

@login_required(login_url='login')
def notificationsReadUpdate(request):
    if request.method == 'POST':
        id= request.POST.get('nftID')
        notification_to_display= Notifications.objects.get(uuid= id)
        if notification_to_display.read == True:
            response= {
                'id': f'{id}',
                'message': f'Notification {id} has already been updated',
                'status': 'not_ok'
            }
        else:
            notification_to_display.read= True
            notification_to_display.save()
            response= {
                'id': f'{id}',
                'message': f'Notification {id} has been updated',
                'status': 'ok'
            } 
        return JsonResponse(response, safe= False)

@login_required(login_url='login')
def complainsComments(request):
    if request.method == 'POST':
        review= request.POST.get('review')
        reviewType= request.POST.get('review-type')
        newReview= ReviewModel.objects.create(
            message= review,
            review_type= reviewType,
            user= request.user.username,

        )
        newReview.save()
        if reviewType == 'Complaints':
            developersObjectList= AdminDeveloperUserModel.objects.all()
            for _ in developersObjectList:
                if str(_.status).lower() != 'administrator': 
                    msg= f'New complaints from user\'s.\nComplaints ID: {newReview.uuid}'
                    send_message(_, msg)
        messages.success(request, f'Dear {request.user.username}, your message has been sent successfully. {get_current_site(request)}\'s team will respond to you shortly.....')
        return redirect('index')
    context= {

    }
    return render(request, 'auth/mail/complainsComments.html', context= context)

@login_required(login_url='login')
@csrf_exempt
def updateProfile(request):
    if request.method == 'POST':
        fn= request.POST.get('fn')
        ln= request.POST.get('ln')
        email= request.POST.get('email')
        ps= request.POST.get('ps')
        try:
            user= CustomUserModel.objects.get(username= request.user.username)
            if auth.authenticate(request, username= user.username, password= ps) is not None:
                user.first_name= fn
                user.last_name= ln
                user.email= email
                user.save()
                return JsonResponse({'user': request.user.username,'status': 200, 'state': 'Success','msg':'Your profile has been updated successfully'})
            else:
                return JsonResponse({'status': 200, 'state': 'Failed','msg':'Failed to update profile due to incorrect password'})
        except CustomUserModel.DoesNotExist:
            return JsonResponse({'status': 200, 'state': 'Failed','msg':'User does not exist'})

@login_required(login_url='login')
@csrf_exempt
def updatePassword(request):
    if request.method == 'POST':
        oldpassword= request.POST.get('oldP')
        newpassword= request.POST.get('np')
        confirmpassword= request.POST.get('cp')
        try:
            user= CustomUserModel.objects.get(username= request.user.username)
            if auth.authenticate(request, username= user.username, password= oldpassword) is not None:
                if newpassword == confirmpassword:
                    user.set_password(newpassword)
                    user.save()
                    login= auth.authenticate(request, username= user.username, password= newpassword)
                    auth.login(request, login)
                    return JsonResponse({'user': request.user.username,'status': 200, 'state': 'Success','msg':'Your password has been updated successfully'})
                else:
                    return JsonResponse({'status': 200, 'state': 'Failed','msg':'Failed to update password due to new and confirm password not matching'})
            else:
                return JsonResponse({'status': 200, 'state': 'Failed','msg':'Failed to update password due to incorrect old password'})
        except CustomUserModel.DoesNotExist:
            return JsonResponse({'status': 200, 'state': 'Failed','msg':'User does not exist'})