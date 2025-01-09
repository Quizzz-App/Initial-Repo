from authenticationSystem.models import CustomUserModel as User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests, json, datetime, ast, openpyxl, os
from django.shortcuts import render, redirect
from paystackapi.paystack import Paystack
from authenticationSystem.models import Notifications
from django.http import JsonResponse
from django.contrib import messages
from django.core.files import File
from referralSystem.views import *
from django.conf import settings
from adminSystem.models import *
from decimal import Decimal
from .models import *
from datetime import datetime
from adminSystem.models import AdminDeveloperUserModel as developers_account

key= settings.PAYSTACK_SECRET_KEY_TEST
# key= settings.PAYSTACK_SECRET_KEY_LIVE
# Create your views here.


#Create a notification object to be sent to a user
def send_message(recipient, message, notificationType, action_required= False, action= '', actionID= ''):
    msg= Notifications.objects.create(user= recipient, notification= message, action_required= action_required, action= action, actionID= actionID, notificationType= notificationType)
    msg.save()

#Fetching of the available carriers which supports our payment methods
@login_required(login_url='login')
def get_carriers_banks(request):
    if not request.user.is_premium:
        headers = {
        'Authorization': f'Bearer {key}'
    }
        list_of_carriers= requests.get(url='https://api.paystack.co/bank?currency=GHS&type=mobile_money', headers= headers)
        # list_of_banks= requests.get(url='https://api.paystack.co/bank?country=ghana&pay_with_bank=true', headers= headers)
        response_carriers= list_of_carriers.json()
        # response_banks= list_of_banks.json()
        list_ofc= []
        # list_ofb= []
        for i in response_carriers['data']:
            list_ofc.append(i)
        # for i in response_banks['data']:
        #     list_ofb.append(i)
        return list_ofc
    else:
        # messages.error(request, 'You are already a premium user')
        return {'status': '404'}

#Storing of the payment process created by the user (It is temporal)
@csrf_exempt
def storePaymentProccess(request):
    stored= StorePaymentProcess.objects.filter(user= request.user)

    for x in stored:
        x.delete()
    if request.method == 'POST':
        amount= request.POST.get('amount')
        email= request.POST.get('email')
        contact= request.POST.get('contact')
        payment_type= request.POST.get('payment_type')
        carrier_code= request.POST.get('carrier_code')
        carrier_name= request.POST.get('carrier_name')
        # New 
        if int(amount) == 30:
            StorePaymentProcess.objects.create(user= request.user, amount= amount, email= email,
                                           carrier_code= carrier_code, carrier_name= carrier_name, contact= contact, payment_type= payment_type).save()
            return JsonResponse({'status': 'ok'}, safe= False)
        else:
            return JsonResponse({'code': 400, 'state': 'activation', 'msg': f'Dear {request.user.username}, your amount you entered must be GH₵ 30'})

    else:
        return JsonResponse('Bad request', safe= False)


#Rendering of the final page to complete the transactions
def ConfirmPaymentProcess(request):
    try:
        userPaymentStoreProcess= StorePaymentProcess.objects.get(user= request.user)
        context= {
            'pt': userPaymentStoreProcess.payment_type,
            'amount': userPaymentStoreProcess.amount,
            'email': userPaymentStoreProcess.email,
            'contact': userPaymentStoreProcess.contact,
            'dop': userPaymentStoreProcess.date_of_payment,
            'network': userPaymentStoreProcess.carrier_name
        }
        return render(request, 'sitepages/auxilliarypages/paymentpage/index.html', context= context)
    except StorePaymentProcess.DoesNotExist:
        return redirect('user-wallet', username= request.user.username)

#Initalizing the Momo transaction using the payment process created by the user
@csrf_exempt
def IntiateMoMoTransaction(request):
    if not request.user.is_premium:
        if request.method == 'POST':
            userStore= StorePaymentProcess.objects.get(user= request.user)
            email= userStore.email
            phone= userStore.contact
            amount= userStore.amount
            carrier= f'{userStore.carrier_code}'.lower()

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
        elif request.method == 'DELETE':
            StorePaymentProcess.objects.get(user= request.user).delete()
            return JsonResponse({'status': 200, 'user': request.user.username}, safe= False)
        else:
            return redirect('index')
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')

#Continuering of the transaction if otp is required
@csrf_exempt
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

#Intializing of bank transaction (Currently on hold)
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

 #Creating of paymentrecipiet on paystack for payment   

#Creating of transfer recipient on paystack to enable us to transfer money to our users
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
        return response['data']['recipient_code']
    else:
        print(response)

#Verifying of transaction on paystack since we are not using webhook
def verifyTransaction(request, transactionID):
    if not request.user.is_premium:
        response_from_api= reusableVerification(request.user, transactionID)
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')
    
    return JsonResponse({'api':response_from_api, 'user': request.user.username}, safe= False)

#Verifying function
def reusableVerification(user, transactionID):
    user= User.objects.get(email=user.email)
    transactionExist= False
    paystack= Paystack(secret_key=key)
    response_from_api= paystack.transaction.verify(str(transactionID))
    # print(response_from_api['data'])
    if response_from_api['message'] == "Transaction reference not found.":
        return JsonResponse({'code': 400, 'state': 'Failed', 'msg':  'Transaction not found'})
    elif response_from_api['message'] != "Transaction reference not found":
        try:
            reflist= TransactionModel.objects.filter(transactionRefrence= response_from_api['data']['reference'])
            for transaction in reflist:
                if transaction.account.user.email == user.email:
                    transactionExist= True
                    break
        except:
            transactionExist= False
        if transactionExist:
            print("breaking")
            return JsonResponse({'code': 400, 'state': 'Failed', 'msg':  'Transaction already made'})
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
            try:
                check= TransactionModel.objects.get(transactionRefrence= transactionRefrence)
            except TransactionModel.DoesNotExist:
                check= None
            if check == None:
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
                user.is_premium= True
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
                month_name= datetime.now().strftime('%B')
                year= datetime.now().year
                account_name= f'{month_name} {year}'
                try:
                    createWalletObject= WalletModel.objects.create(wallet_name= account_name)
                    createWalletObject.save()
                    createWalletObject.updateBalance()

                except:
                    createWalletObject= WalletModel.objects.get(wallet_name= account_name)
                    createWalletObject.updateBalance()
                
                # Get developers account
                # Check if an account exists
                        #update
                #Create a new account and update balance
                # developers_account = AdminDeveloperUserModel.objects.all()
                # for developer in developers_account:
                #      wallet,created = developer_wallet.objects.get_or_create(
                #                         user=developer,
                #                         month=datetime.now().month,
                #                         year=datetime.now().year,
                #                     )
                        
                #      wallet.updateBalance()
                #      wallet.save()
                        

                send_message(user, 'Your payment was successfull', 'Transaction')
                if user.referred_by != '':
                    new_referral(user.referred_by, user.referral_code)
                createTransferRecienpt(
                    name= f'{user.username}',
                    paymentType= response_from_api['data']['channel'],
                    accountNumber= response_from_api['data']['authorization']['mobile_money_number'],
                    bankCode= response_from_api['data']['authorization']['bank'],
                    currency= response_from_api['data']['currency'],
                    user= user
                )
                try:
                    StorePaymentProcess.objects.get(user= user).delete()
                except StorePaymentProcess.DoesNotExist:
                    pass
    return response_from_api


# def successfulPayment(request):
#     return render(request, 'pay/paymentSuccess.html')

# @login_required(login_url='login')
# def transactionHistory(request):
#     if request.user.is_premium:
#         try:
#             account= AccountModel.objects.get(user= User.objects.get(email=request.user.email))
#         except AccountModel.DoesNotExist:
#             return redirect('index')
#         transactions= TransactionModel.objects.filter(account= account)
#         return render(request, 'pay/transactionHistory.html', context= {
#             'transactions': transactions,
#         })
#     else:
#         messages.error(request, 'You are not a premium user. Please upgrade to continue.')
#         return redirect('index')
    
# def paymentMethod(request):
#     if request.user.is_premium:
#         if request.method == 'POST':
#             user= User.objects.get(email=request.user.email)
#             userPaymentMethod= PaymentInfoModel.objects.get(account= user)
#             first_name= request.POST.get('fn')
#             last_name= request.POST.get('ln')
#             email= request.POST.get('ea')
#             accountNumber= request.POST.get('mn')
#             carrier= request.POST.get('network-carriers')
#             paymentMethod= request.POST.get('paym')

#             userPaymentMethod.firstName= first_name
#             userPaymentMethod.lastName= last_name
#             userPaymentMethod.email= email
#             userPaymentMethod.accountNumber= accountNumber
#             userPaymentMethod.carrier= carrier
#             userPaymentMethod.paymentMethod= paymentMethod
#             userPaymentMethod.save()
#             messages.success(request, 'Payment method updated successfully')
#             return redirect('index')


#         headers = {
#         'Authorization': f'Bearer {key}'
#         }
#         list_of_carriers= requests.get(url='https://api.paystack.co/bank?currency=GHS&type=mobile_money', headers= headers)
#         response_carriers= list_of_carriers.json()
#         list_ofc= []
#         for i in response_carriers['data']:
#             list_ofc.append(i)
#         userPaymentMethod= PaymentInfoModel.objects.get(account= User.objects.get(email= request.user.email))
#         print(userPaymentMethod.accountNumber)
#         context= {
#             'first_name': userPaymentMethod.firstName,
#             'last_name': userPaymentMethod.lastName,
#             'email': userPaymentMethod.email,
#             'phone': userPaymentMethod.accountNumber,
#             'carrier': userPaymentMethod.carrier,
#             'paymentMethod': userPaymentMethod.paymentMethod,
#             'paymentMethodName': userPaymentMethod.paymentMethodName,
#             'otherCarriers': list_ofc,
#             'otherpaymentMethods': PaymentChannels.objects.all(),
#         }
#         return render(request, 'pay/paymentMethod.html', context= context)
#     else:
#         messages.error(request, 'You are not a premium user. Please upgrade to continue.')
#         return redirect('index')

#Handling of issued withdrawal and notifying admins
@login_required(login_url='login')
@csrf_exempt 
def issueWithdrawal(request):
    if request.method == 'POST':
        amount= request.POST.get('amount')
        acN= request.POST.get('acN')
        issuer= request.user.username

        newWithdrawal= IssueWithdrawModel.objects.create(amount= Decimal(amount), issuer= issuer, acN= acN, refCode= generate_unique_referral_code(length=15))
        newWithdrawal.save()

        newTransaction= TransactionModel.objects.create(
            account= AccountModel.objects.get(user= request.user),
            amount= newWithdrawal.amount,
            transactionType= 'Withdrawal',
            transactionTypeStatus= newWithdrawal.state, 
            transactionRefrence= newWithdrawal.refCode,
            paymentMethod= 'Mobile Money',
            mobileNumber= newWithdrawal.acN,
            carrier= ''
        )
        newTransaction.save()

        # Send notification to admin
        adminObject= AdminDeveloperUserModel.objects.filter(
            status= AdminDeveloperStatusModel.objects.get(name= 'Administrator')
        )
        for _ in adminObject:
            send_message(
                recipient= _,
                message= f'Dear {_.username}, {issuer} has requested for a withdrawal on {newWithdrawal.timestamp}. Please take immedite action',
                action_required= True,
                action= 'Withdrawal',
                actionID= f'{newWithdrawal.uuid}',
                notificationType= 'Transaction'
            )
        response= {
            'status': 'ok',
            'message': f'Dear {request.user.username}, your withdrawal request has been sent to the team. You will get a feedback from the team within 24hrs'
        }
    return JsonResponse(response, safe= False)

#Declining of withdrawal request
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
        TransactionObj= TransactionModel.objects.get(transactionRefrence= withDrawal.refCode)
        TransactionObj.transactionTypeStatus= 'Failed'
        TransactionObj.save()
        declineDeclineObject= DeclinedTransferModel.objects.create(requestedBy= issuer, attendedBy= request.user.username, reason= reason, amountRequested= withDrawal.amount, requestedBy_balance=AccountModel.objects.get(user= issuerObject).get_balance())
        declineDeclineObject.save()
        for _ in nftObject:
            _.action= 'Done'
            _.action_required= False
            _.save()
        
        teamsStatus= AdminDeveloperStatusModel.objects.get(name= 'Administrator')
        AdminsObjects= AdminDeveloperUserModel.objects.filter(status= teamsStatus)
        for _ in AdminsObjects:
            if str(_.username) != str(request.user.username):
                msg= f'{request.user.username} has declined withdrawal for {withDrawal.issuer}.\nReason: {reason}'
                send_message(recipient= _, message= msg, notificationType= 'Transaction')

        send_message(
            recipient= issuerObject,
            notificationType= 'Transaction',
            message= f'Dear {issuerObject.username}, your withdrawal request with refrence {withDrawal.refCode} has been declined.\n Reason: {reason}'
        )
        response= {
            'status': 'ok',
            'message': f'Feedback sent successfully'
        }
        return JsonResponse(response, safe= False)
        
#Approving of withdrawal on paystack
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

#Checking of balance on paystack
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

#Making a transfer on paystack
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

#Completing of approved transfer using of the otp
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
        send_message(recipient= issuerObject, message= message_to_issuer, notificationType= 'Notice')
        newPoints= Decimal(withDrawal.amount / 30)
        issuerObject.points_earned= issuerObject.points_earned - round(newPoints, 2)
        issuerObject.save()
        AccountModel.objects.get(user= issuerObject).update_balance()


        transferObject= TransferModel.objects.create(transfer_amount= Decimal(amount), transferID= transferID, transferReference= transferRef, transferCode= transferCode, recipientID= recipientID, sender= sender)
        transferObject.save()

        teamsStatus= AdminDeveloperStatusModel.objects.get(name= 'Administrator')
        AdminsObjects= AdminDeveloperUserModel.objects.filter(status= teamsStatus)
        for _ in AdminsObjects:
            if str(_.username) != str(request.user.username):
                msg= f'{request.user.username} has approved withdrawal of {withDrawal.amount} for {withDrawal.issuer} '
                send_message(recipient= _, message= msg, notificationType= 'Notice')

        if transferFundsR:
            pass
            return JsonResponse(transferFundsR, safe= False)
        else:
            return JsonResponse(transferFundsR, safe= False)
    else:
        return JsonResponse(transferFundsR, safe= False)
    print(transferFundsR)

#Manual pay to select requested withdrawals to generate an excel sheet
@login_required(login_url='login')
def manualPaymentMethod(request):
    pendingPaymentObjects= WithdrwalSheetsModel.objects.filter(completedTransfers= False)
    if len(pendingPaymentObjects) != 0:
        messages.error(request, 'Please complete all pending payments')
        return redirect('pending-payment')
    requestedWithdrawalObj= IssueWithdrawModel.objects.filter(status= False)
    iOD= {}
    for index,Object in enumerate(requestedWithdrawalObj):
        iOD[index]= {
            'issuer': Object,
            'balance': AccountModel.objects.get(user= CustomUserModel.objects.get(username= Object.issuer)).get_balance(),
        }
    context= {
        'issuers': iOD
    }
    return render(request, 'dev_admin/admin/manualPay.html', context= context)


#Deciding on which payment method to use paystack or manual pay
@login_required(login_url='login')
def decidePaymentMethod(request):
    pendingPaymentObjects= WithdrwalSheetsModel.objects.filter(completedTransfers= False)
    if len(pendingPaymentObjects) != 0:
        messages.error(request, 'Please complete all pending payments')
        return redirect('pending-payment')
    context= {
    }
    return render(request, 'dev_admin/admin/decidePaymentMethod.html', context= context)

#Generating an excel sheet with the selected users
@login_required(login_url='login')
@csrf_exempt         
def generateExcelList(request):
    if request.method == 'POST':
        idListData= request.POST.get('nftIDs')
        idList= ast.literal_eval(idListData)
        if len(idList) != 0:
            # Create directory if it doesn't exist
            # excelFileDir='./exceldata'
            excelFileDir=os.path.join(settings.MEDIA_ROOT, 'exceldata')
            # if not os.path.exists(excelFileDir):
            os.makedirs(excelFileDir, exist_ok= True)
            # else:
            #     pass
            
            month_name= datetime.now().strftime('%B')
            fileName= f'withdrawal_request_list_createdby_{request.user.username}_{month_name}_{int(datetime.now().second) + int(datetime.now().minute) + int(datetime.now().hour) + (int(datetime.now().microsecond))}.xlsx'
            filePath= os.path.join(excelFileDir, fileName)

            # create a new workbook
            newWorkbook = openpyxl.Workbook()

            # get the active worksheet
            newWorksheet = newWorkbook.active
            data= [
                ['Request ID', 'Issuer\'s Name','Requested Amount', 'Account Number', 'Time Requested']
            ]
            for i in idList:
                try:
                    RequestObject= IssueWithdrawModel.objects.get(uuid= i)
                    ID=f'{i}'
                    IssuerName=f'{RequestObject.issuer}'
                    RequestedAmount= f'{RequestObject.amount}'
                    acN= f'{RequestObject.acN}'
                    timeR= f'{RequestObject.timestamp}'
                    newData= [ID, IssuerName, RequestedAmount, acN, timeR]
                    data.append(newData)
                except (IssueWithdrawModel.DoesNotExist):
                    response= {
                'status': 'ok',
                'message': 'Invalid data entry',
            }
                    return JsonResponse(response, safe= False)
            
            for i in data:
                newWorksheet.append(i)
            newWorkbook.save(filePath)
            saveFileToServer= WithdrwalSheetsModel.objects.create(generated_by= request.user)
            # Writing the file to the specified dir in the model
            with open(filePath, 'rb') as f:

                saveFileToServer.sheet.save(os.path.basename(filePath), File(f))
            saveFileToServer.save()
            # saveFileToServer.sheet.
            os.remove(filePath)

            response= {
                'status': 'ok',
                'message': 'Done',
                'path': saveFileToServer.sheet.url
            }
            return JsonResponse(response, safe= False)
        else:
            response= {
                'status': 'ok',
                'message': 'You failed to select a user',
            }
            return JsonResponse(response, safe= False)
    pendingPaymentObjects= WithdrwalSheetsModel.objects.filter(completedTransfers= False)
    if len(pendingPaymentObjects) != 0:
        messages.error(request, 'Please complete all pending payments')
        return redirect('pending-payment')
    context= {
        
    }
    return render(request, 'dev_admin/admin/manualPay.html', context= context)

#Listing of any uncompleted payment
@login_required(login_url='login')
def pendingPayment(request):
    messages_to_display= messages.get_messages(request)
    pendingPaymentObjects= WithdrwalSheetsModel.objects.filter(completedTransfers= False)
    if len(pendingPaymentObjects) == 0:
        return redirect('decide-payment-method')
    context= {
        'messages': messages_to_display,
        'pendingPayment': pendingPaymentObjects
    }
    return render(request, 'dev_admin/admin/pendingPayment.html', context= context)

#For manual pay only updating of requested withdrawals
@login_required(login_url='login')
def updatePayment(request, fileID):
    messages_to_display= messages.get_messages(request)
    fileObject= WithdrwalSheetsModel.objects.get(uuid= fileID)
    filePath= fileObject.sheet.url
    loadingFile= openpyxl.load_workbook(f'.{filePath}')
    sheet= loadingFile.active
    idData= sheet['A']
    issuersList= []
    for _ in idData:
        if _.value == 'Request ID':
            continue
        else:
            issuerObject= IssueWithdrawModel.objects.get(uuid= _.value)
            issuersList.append(issuerObject)

    context= {
        'messages': messages_to_display,
        'issuersList': issuersList,
        'paymentID': fileID
    }
    return render(request, 'dev_admin/admin/updatePayment.html', context= context)


@login_required(login_url='login')
@csrf_exempt 
def completedTransfer(request):
    if request.method == 'POST':
        noftifcationID= request.POST.get('nftID')
        fileID= request.POST.get('ID')

        fileObject= WithdrwalSheetsModel.objects.get(uuid= fileID)
        filePath= fileObject.sheet.url
        loadingFile= openpyxl.load_workbook(f'.{filePath}')
        sheet= loadingFile.active
        idData= sheet['A']
        issuersList= []
        notCompleted= False
        for _ in idData:
            if _.value == 'Request ID':
                continue
            else:
                issuerObject= IssueWithdrawModel.objects.get(uuid= _.value)
                issuerObject.state= 'Success'
                issuerObject.status= True
                issuerObject.save()
                transactionOnj= TransactionModel.objects.get(transactionRefrence= issuerObject.refCode)
                transactionOnj.transactionTypeStatus= 'success'
                transactionOnj.save()
                issuersList.append(issuerObject.status)
        for i in issuersList:
            if i == False:
                notCompleted= True
                break
        print(issuersList)
        if notCompleted:
            pass
        else:
            fileObject.completedTransfers= True
            fileObject.save()
        nftObject= Notifications.objects.filter(actionID= noftifcationID)
        for _ in nftObject:
            _.action= 'Done'
            _.save()
        withDrawal= IssueWithdrawModel.objects.get(uuid= noftifcationID)

        issuerObject= CustomUserModel.objects.get(username= withDrawal.issuer)
        message_to_issuer= f'Dear {issuerObject.username}, the team has attended to you concerning your withdrwal request...'
        send_message(recipient= issuerObject, message= message_to_issuer, notificationType= 'Transaction')
        newPoints= Decimal(withDrawal.amount / 30)
        issuerObject.points_earned= issuerObject.points_earned - round(newPoints, 2)
        issuerObject.save()
        AccountModel.objects.get(user= issuerObject).update_balance()

        teamsStatus= AdminDeveloperStatusModel.objects.get(name= 'Administrator')
        AdminsObjects= AdminDeveloperUserModel.objects.filter(status= teamsStatus)
        for _ in AdminsObjects:
            if str(_.username) != str(request.user.username):
                msg= f'{request.user.username} has approved withdrawal of {withDrawal.amount} for {withDrawal.issuer} '
                send_message(recipient= _, message= msg, notificationType= 'Notice')

        response= {
            'status': 'ok',
            'message': 'Succesfully updated'
        }
        return JsonResponse(response, safe= False)


