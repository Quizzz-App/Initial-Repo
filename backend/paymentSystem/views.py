from django.contrib.auth.decorators import login_required
from paystackapi.paystack import Paystack
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests


key= settings.PAYSTACK_SECRET_KEY_LIVE
# Create your views here.

@login_required(login_url='login')
def pay(request):
    headers = {
    'Authorization': f'Bearer {key}'
}
    list_of_carriers= requests.get(url='https://api.paystack.co/bank?currency=GHS&type=mobile_money', headers= headers)
    response= list_of_carriers.json()
    list= []
    for i in response['data']:
        list.append(i)
    return render(request, 'pay/pay.html', context= {
        'response': list
    })

def IntiateTransaction(request):
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

def continueTransaction(request):
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

def verifyTransaction(request, transactionID):
    paystack= Paystack(secret_key=key)
    response_from_api= paystack.transaction.verify(transactionID)
    response= JsonResponse(response_from_api, safe= False)
    return response