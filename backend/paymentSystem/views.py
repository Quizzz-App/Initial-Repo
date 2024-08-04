from authenticationSystem.models import CustomUserModel as User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from adminSystem.models import *
from paystackapi.paystack import Paystack
from authenticationSystem.views import *
from django.http import JsonResponse
from django.contrib import messages
from referralSystem.views import *
from django.conf import settings
from decimal import Decimal
from .models import *
import requests, json, datetime


key= settings.PAYSTACK_SECRET_KEY_TEST
# Create your views here.

@login_required(login_url='login')
def pay(request):
    if not request.user.is_premium:
        headers = {
        'Authorization': f'Bearer {key}'
    }
        list_of_carriers= requests.get(url='https://api.paystack.co/bank?currency=GHS&type=mobile_money', headers= headers)
        list_of_banks= requests.get(url='https://api.paystack.co/bank?country=ghana&pay_with_bank=true', headers= headers)
        response_carriers= list_of_carriers.json()
        response_banks= list_of_banks.json()
        list_ofc= []
        list_ofb= []
        for i in response_carriers['data']:
            list_ofc.append(i)
        for i in response_banks['data']:
            list_ofb.append(i)
        return render(request, 'pay/pay.html')
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')

def IntiateMoMoTransaction(request):
    if not request.user.is_premium:
        if request.method == 'POST':
            email= request.POST.get('email')
            phone= request.POST.get('phone')
            amount= request.POST.get('amount')
            carrier= request.POST.get('carrier')

            headers = {
                            'Authorization': f'Bearer {key}',
                            'Content-Type': 'application/json'
                        }

            url = 'https://api.paystack.co/charge'
            params = {
                        "amount": float(amount) * 100,
                        "email": email,
                        "currency": "GHS",
                        "mobile_money": {
                            "phone": phone,
                            "provider": carrier,
                        }
                    }
            make_a_charge= requests.post(url, headers={
                            'Authorization': f'Bearer {key}',
                            'Content-Type': 'application/json'
                        }, json=params)
            response= make_a_charge.json()
            return JsonResponse(response, safe= False)
        else:
            return redirect('index')
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')

def continueMoMoTransaction(request):
    if request.method == 'POST':
        opt_code= request.POST.get('opt_code')
        ref_code= request.POST.get('ref_code')

        url="https://api.paystack.co/charge/submit_otp"
        data={ 
        "otp": opt_code, 
        "reference": ref_code,
        }

        continue_charge= requests.post(url, headers={
                        'Authorization': f'Bearer {key}',
                        'Content-Type': 'application/json'
                    }, json=data)
        response= continue_charge.json()
        return JsonResponse(response, safe= False)
    else:
        return redirect('index')

def IntiateBankTransaction(request):
    if request.method == 'POST':
        acN= request.POST.get('accountNumber')
        dob= request.POST.get('dob')
        amount= request.POST.get('amount')
        bank= request.POST.get('bank')
        url="https://api.paystack.co/charge"
        data={ 
            "email": str(request.user.email),
            "amount": str(amount),
            "bank": {
                'code': str(bank),
                'account_number': str(acN)
                },
            }

        continue_charge= requests.post(url, headers={
                        'Authorization': f'Bearer {key}',
                        'Content-Type': 'application/json'
                    }, json=data)
        response= continue_charge.json()
        return JsonResponse(response, safe= False)
    
def createTransferRecienpt(name, paymentType, accountNumber, bankCode, currency, user):
    url="https://api.paystack.co/transferrecipient"
    data={ 
        "type": paymentType,
        "name": name,
        "account_number": accountNumber,
        "bank_code": bankCode,
        "currency": currency
    }
    create_reciept= requests.post(url, headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }, json=data)
    response= create_reciept.json()
    if response['status']:
        newReciept= RecieptModel.objects.create(user= user, recieptID= response['data']['id'], recieptCode= response['data']['recipient_code'])
        newReciept.save()
        print(response['message'], response['data']['id'])
        return response['data']['recipient_code']
    else:
        print(response)


def verifyTransaction(request, transactionID):
    if not request.user.is_premium:
        user= User.objects.get(email=request.user.email)
        transactionExist= False
        paystack= Paystack(secret_key=key)
        response_from_api= paystack.transaction.verify(str(transactionID))
        if response_from_api['message'] == "Transaction reference not found":
            messages.error(request, 'Transaction not found')
            return redirect('index')
        elif response_from_api['message'] != "Transaction reference not found":
            reflist= TransactionModel.objects.filter(transactionRefrence= response_from_api['data']['reference'])
            for transaction in reflist:
                if transaction.account.user.email == request.user.email:
                    transactionExist= True
                    break
            if transactionExist:
                messages.error(request, 'Transaction already made')
                return redirect('index')
            else:
                try:
                    account= AccountModel.objects.get(user= user)
                except AccountModel.DoesNotExist:
                    account= AccountModel.objects.create(user= user)
                    account.save()
                amount= Decimal(response_from_api['data']['amount'] / 100)
                transactionType= 'deposit'
                transactionTypeStatus= response_from_api['data']['status']
                transactionRefrence= response_from_api['data']['reference']
                paymentMethod= response_from_api['data']['channel']
                mobileNumber= response_from_api['data']['authorization']['mobile_money_number']
                carrier= response_from_api['data']['authorization']['bank']
                transaction_made= TransactionModel.objects.create(
                    account= account,
                    amount= amount,
                    transactionType= transactionType,
                    transactionTypeStatus= transactionTypeStatus,
                    transactionRefrence= transactionRefrence,
                    paymentMethod= paymentMethod,
                    mobileNumber= mobileNumber,
                    carrier= carrier
                )
                transaction_made.save()
                if response_from_api['data']['status'] == 'success':
                    resp= account.make_PremiumUser()
                    print(resp)
                    user.referral_code= generate_unique_referral_code(userName= user.username)
                    user.save()
                    userPaymentMethod= PaymentInfoModel.objects.create(
                        account= user,
                        paymentMethod= paymentMethod,
                        accountNumber= mobileNumber,
                        carrier= carrier,
                        firstName= user.first_name,
                        lastName= user.last_name,
                        email= user.email
                    )
                    userPaymentMethod.save()
                    month_name= datetime.datetime.now().strftime('%B')
                    year= datetime.datetime.now().year
                    account_name= f'{month_name} {year}'
                    try:
                        createWalletObject= WalletModel.objects.create(wallet_name= account_name)
                        createWalletObject.save()
                        createWalletObject.updateBalance()
                    except:
                        createWalletObject= WalletModel.objects.get(wallet_name= account_name)
                        createWalletObject.updateBalance()
                    if user.referred_by != '':
                        new_referral(user.referred_by, user.referral_code)
                    createTransferRecienpt(
                        name= f'{request.user.username}',
                        paymentType= response_from_api['data']['channel'],
                        accountNumber= response_from_api['data']['authorization']['mobile_money_number'],
                        bankCode= response_from_api['data']['authorization']['bank'],
                        currency= response_from_api['data']['currency'],
                        user= request.user
                    )
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')

    response= JsonResponse(response_from_api, safe= False)
    return response

def successfulPayment(request):
    return render(request, 'pay/paymentSuccess.html')

@login_required(login_url='login')
def transactionHistory(request):
    if request.user.is_premium:
        try:
            account= AccountModel.objects.get(user= User.objects.get(email=request.user.email))
        except AccountModel.DoesNotExist:
            return redirect('index')
        transactions= TransactionModel.objects.filter(account= account)
        return render(request, 'pay/transactionHistory.html', context= {
            'transactions': transactions,
        })
    else:
        messages.error(request, 'You are not a premium user. Please upgrade to continue.')
        return redirect('index')
    
def paymentMethod(request):
    if request.user.is_premium:
        if request.method == 'POST':
            user= User.objects.get(email=request.user.email)
            userPaymentMethod= PaymentInfoModel.objects.get(account= user)
            first_name= request.POST.get('fn')
            last_name= request.POST.get('ln')
            email= request.POST.get('ea')
            accountNumber= request.POST.get('mn')
            carrier= request.POST.get('network-carriers')
            paymentMethod= request.POST.get('paym')

            userPaymentMethod.firstName= first_name
            userPaymentMethod.lastName= last_name
            userPaymentMethod.email= email
            userPaymentMethod.accountNumber= accountNumber
            userPaymentMethod.carrier= carrier
            userPaymentMethod.paymentMethod= paymentMethod
            userPaymentMethod.save()
            messages.success(request, 'Payment method updated successfully')
            return redirect('index')


        headers = {
        'Authorization': f'Bearer {key}'
        }
        list_of_carriers= requests.get(url='https://api.paystack.co/bank?currency=GHS&type=mobile_money', headers= headers)
        response_carriers= list_of_carriers.json()
        list_ofc= []
        for i in response_carriers['data']:
            list_ofc.append(i)
        userPaymentMethod= PaymentInfoModel.objects.get(account= User.objects.get(email= request.user.email))
        print(userPaymentMethod.accountNumber)
        context= {
            'first_name': userPaymentMethod.firstName,
            'last_name': userPaymentMethod.lastName,
            'email': userPaymentMethod.email,
            'phone': userPaymentMethod.accountNumber,
            'carrier': userPaymentMethod.carrier,
            'paymentMethod': userPaymentMethod.paymentMethod,
            'paymentMethodName': userPaymentMethod.paymentMethodName,
            'otherCarriers': list_ofc,
            'otherpaymentMethods': PaymentChannels.objects.all(),
        }
        return render(request, 'pay/paymentMethod.html', context= context)
    else:
        messages.error(request, 'You are not a premium user. Please upgrade to continue.')
        return redirect('index')

@login_required(login_url='login')
@csrf_exempt 
def issueWithdrawal(request):
    if request.method == 'POST':
        amount= request.POST.get('amount')
        issuer= request.user.username

        newWithdrawal= IssueWithdrawModel.objects.create(amount= Decimal(amount), issuer= issuer)
        newWithdrawal.save()

        # Send email notification to admin
        adminObject= AdminDeveloperUserModel.objects.filter(
            status= AdminDeveloperStatusModel.objects.get(name= 'Administrator')
        )
        for _ in adminObject:
            send_message(
                recipient= _,
                message= f'Dear {_.username}, {issuer} has requested for a withdrawal on {newWithdrawal.timestamp}. Please take immedite action',
                action_required= True,
                action= 'Withdrawal',
                actionID= f'{newWithdrawal.uuid}'
            )
        response= {
            'status': 'ok',
            'message': f'Dear {request.user.username}, your withdrawal request has been sent to the team. You will get a feedback from the team within 24hrs'
        }
    return JsonResponse(response, safe= False)

@login_required(login_url='login')
@csrf_exempt 
def declineWithdrawalRequest(request):
    if request.method == 'POST':
        reason= request.POST.get('reason')
        issuer= request.POST.get('issuer')
        nftID= request.POST.get('nftID')

        issuerObject= CustomUserModel.objects.get(username= issuer)
        nftObject= Notifications.objects.filter(actionID= nftID)
        withDrawal= IssueWithdrawModel.objects.get(uuid= nftID)
        withDrawal.status= True
        withDrawal.save()

        declineDeclineObject= DeclinedTransferModel.objects.create(requestedBy= issuer, attendedBy= request.user.username, reason= reason, amountRequested= withDrawal.amount, requestedBy_balance=AccountModel.objects.get(user= issuerObject).get_balance())
        declineDeclineObject.save()
        for _ in nftObject:
            _.action= 'Done'
            _.save()
        
        teamsStatus= AdminDeveloperStatusModel.objects.get(name= 'Administrator')
        AdminsObjects= AdminDeveloperUserModel.objects.filter(status= teamsStatus)
        for _ in AdminsObjects:
            if str(_.username) != str(request.user.username):
                msg= f'{request.user.username} has declined withdrawal for {withDrawal.issuer}.\nReason: {reason}'
                send_message(recipient= _, message= msg)

        send_message(
            recipient= issuerObject,
            message= f'Dear {issuerObject.username}, your withdrawal request has been declined.\n Reason: {reason}'
        )
        response= {
            'status': 'ok',
            'message': f'Feedback sent successfully'
        }
        return JsonResponse(response, safe= False)
        

@login_required(login_url='login')
@csrf_exempt 
def approveWithdrawalRequest(request):
    if request.method == 'POST':
        issuer= request.POST.get('issuer')
        issuerID= request.POST.get('issuerID')
        withdrawalID= request.POST.get('withdrawalID')
        noftifcationID= request.POST.get('nftID')

        issuerReciept= RecieptModel.objects.get(uuid= issuerID)
        issuerObject= IssueWithdrawModel.objects.get(uuid= withdrawalID)

        make_a_transfer= intiateFunds(amount= float(issuerObject.amount) * 100, recipientID= issuerReciept.recieptCode, nftID= noftifcationID)
        print('Retruning...')
        return JsonResponse(make_a_transfer, safe= False)

        


def checkBalanceOnPaystack():
    url="https://api.paystack.co/balance"
    response= requests.get(url, headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    })
    response= response.json()
    if response['status']:
        return (response['data'][0]['balance'] / 100)
    else:
        print(response)

def intiateFunds(amount, recipientID, source= 'balance', nftID= ''):
    print('called')
    url="https://api.paystack.co/transfer"
    data={ 
    "source": source, 
    "reason": "Payment to customer", 
    "amount":amount, "recipient": recipientID
    }
    print('Making request')
    transferFundsR= requests.post(url, headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }, json=data)
    transferFundsR= transferFundsR.json()
    print('Data recieved')
    if transferFundsR['status']:
        if transferFundsR['data']['status'] == 'otp':
            transferCode= transferFundsR['data']['transfer_code']
            response= {
            'status': 'ok',
            'message': transferFundsR['message'],
            'transferCode': transferCode,
            'nftID': nftID
            }
            print('Maing a return')
            return response
        else:
            print('Error at otp junction')
            print(transferFundsR)
    else:
        print('Error at status junction')
        print(transferFundsR)
    print(transferFundsR)

@login_required(login_url='login')
@csrf_exempt         
def FinalizeFunds(request):
    if request.method == 'POST':
        otpCode= request.POST.get('otp')
        transferCode= request.POST.get('transferCode')
        nftID= request.POST.get('nftID')
    url="https://api.paystack.co/transfer/finalize_transfer"
    data={ 
   "transfer_code": transferCode, 
    "otp": otpCode
    }
    transferFundsR= requests.post(url, headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }, json=data)
    transferFundsR= transferFundsR.json()
    if transferFundsR['status']:
        amount= transferFundsR['data']['amount'] / 100
        transferID= transferFundsR['data']['id']
        transferRef= transferFundsR['data']['reference']
        transferCode= transferFundsR['data']['transfer_code']
        recipientID= transferFundsR['data']['recipient']
        sender= request.user.username
        
        nftObject= Notifications.objects.filter(actionID= nftID)
        for _ in nftObject:
            _.action= 'Done'
            _.save()
        withDrawal= IssueWithdrawModel.objects.get(uuid= nftID)
        withDrawal.status= True
        withDrawal.save()

        issuerObject= CustomUserModel.objects.get(username= withDrawal.issuer)
        message_to_issuer= f'Dear {issuerObject.username}, the team has attended to you and you will recieve your money in less than an hour'
        send_message(recipient= issuerObject, message= message_to_issuer)
        newPoints= Decimal(withDrawal.amount / 30)
        issuerObject.points_earned= newPoints
        issuerObject.save()
        AccountModel.objects.get(user= issuerObject).update_balance()


        transferObject= TransferModel.objects.create(transfer_amount= Decimal(amount), transferID= transferID, transferReference= transferRef, transferCode= transferCode, recipientID= recipientID, sender= sender)
        transferObject.save()

        teamsStatus= AdminDeveloperStatusModel.objects.get(name= 'Administrator')
        AdminsObjects= AdminDeveloperUserModel.objects.filter(status= teamsStatus)
        for _ in AdminsObjects:
            if str(_.username) != str(request.user.username):
                msg= f'{request.user.username} has approved withdrawal of {withDrawal.amount} for {withDrawal.issuer} '
                send_message(recipient= _, message= msg)

        if transferFundsR:
            pass
            return JsonResponse(transferFundsR, safe= False)
        else:
            return JsonResponse(transferFundsR, safe= False)
    else:
        return JsonResponse(transferFundsR, safe= False)
    print(transferFundsR)
    '''
    '''


