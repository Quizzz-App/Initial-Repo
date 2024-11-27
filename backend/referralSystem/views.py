from authenticationSystem.models import CustomUserModel as User
from authenticationSystem.models import Notifications as nft
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from datetime import datetime, timedelta  
from django.http import JsonResponse
from decimal import Decimal
from .models import *
import random, string
import calendar  
# Create your views here.


def get_last_5_months():  
    today = datetime.now()  
    last_5_months = []  

    # Loop for the last 5 months  
    for i in range(5):  
        # Calculate the month and year  
        month = today.month - i 

        if month <= 0:  
            month += 12 

        # Use the month to get the abbreviated month name  
        month_abbr = calendar.month_abbr[month]  
        
        # Append the result (format: "Month Year")  
        last_5_months.append(f"{month_abbr}")  

    return last_5_months[::-1]  # Reverse the list to show oldest first 

def get_last_5_years():
    today= datetime.now() 
    last_5_years= []

    for i in range(5):
        last_5_years.append(str(today.year - i))
    return last_5_years[::-1]

def pay_commission(referred_by_code, new_user_referral_code, commission_rate):
    referrer = User.objects.get(referral_code=referred_by_code)
    new_user = User.objects.get(referral_code=new_user_referral_code)

    referrer.points_earned = Decimal(referrer.points_earned) + commission_rate
    referrer.total_points_earned = Decimal(referrer.total_points_earned) + commission_rate
    referrer.save()
    ReferralModelHistory.objects.create(user= referrer, ref= new_user, relationship= 'Direct', points_earned= commission_rate).save()
    send_message= nft.objects.create(user= referrer, notificationType= 'Transaction', notification= f'You just received {round((100*commission_rate),1)}% commission from {new_user.username} initial deposit')
    send_message.save()

    #Check if referrer was also referred by someone
    first_ref= referrer
    cmr= Decimal(round((commission_rate * Decimal( 0.5)), 2))
    while True:
        if first_ref.referred_by != '':
            referrer_referral = User.objects.get(referral_code=first_ref.referred_by)
            referrer_referral.points_earned = Decimal(referrer_referral.points_earned) + cmr
            referrer_referral.total_points_earned = Decimal(referrer_referral.total_points_earned) + cmr
            ReferralModelHistory.objects.create(user= referrer_referral, ref= new_user, relationship= 'Indirect', points_earned= cmr).save()
            send_message= nft.objects.create(user= referrer_referral, notificationType= 'Transaction', notification= f'You just received {round((100*cmr),1)}%  commission from a referral\'s initial deposit')
            send_message.save()
            if referrer_referral.indirect_referrals == '':
                referrer_referral.indirect_referrals += str(new_user.username)
            else:
                referrer_referral.indirect_referrals += ',' + str(new_user.username)
            referrer_referral.indirectReferrals += 1
            referrer_referral.save()
            first_ref = referrer_referral
            cmr= Decimal(round((cmr * Decimal( 0.5)), 2))
            if cmr < 0.01:
                cmr= Decimal(0.01)
            else:
                pass
        else:
            break

@login_required
def refAnalytics(request):
    past_five_months= get_last_5_months()
    userRefHistory= ReferralModelHistory.objects.filter(user= request.user)
    monthsDict= {}
    for month in past_five_months:
        monthsDict[month]={
            'refAmount':0,
            'refEarn': 0
        }
    for x in userRefHistory:
        refMonth= calendar.month_abbr[int(f'{x.date}'.split('-')[1])] 
        for key in monthsDict:
            if key == refMonth:
                monthsDict[refMonth]['refAmount'] += 1
                monthsDict[refMonth]['refEarn'] += (x.points_earned * 30)
    return JsonResponse(monthsDict, safe= False)

def new_referral(referred_by_code, new_user_referral_code):
    new_user = User.objects.get(referral_code=new_user_referral_code)
    referred_by= User.objects.get(referral_code=referred_by_code)


    if referred_by.referral_code_expired:
        store_ref(new_user, referred_by)
        # ref_search(new_user, referred_by)
    else:
        non_pro_list= str(referred_by.non_pro_referrals).split(',')
        for _ in non_pro_list:
            if _ == str(new_user.username):
                non_pro_list.remove(_)
        if non_pro_list != '':
            non_pro= ''
            for _ in non_pro_list:
                if _ != '':
                    non_pro += _ + ','
        else:
            non_pro= ''
        referred_by.non_pro_referrals= non_pro
        referred_by.referrals += 1
        if referred_by.referrals == 2:
            referred_by.referral_code_expired= True
        if referred_by.direct_referrals == '':
            referred_by.direct_referrals += str(new_user.username)
        else:
            referred_by.direct_referrals += ',' + str(new_user.username)
        referred_by.save()
        pay_commission(referred_by_code, new_user_referral_code, Decimal(0.2))

        new_user.referred_by = referred_by.referral_code
        print('added', referred_by.points_earned)
        new_user.save()
def store_ref(new_user, referred_by):
    store= StoreNewRef.objects.create(new_ref= new_user, ref_king= referred_by)
    store.save()
    non_pro_list= str(referred_by.non_pro_referrals).split(',')
    for _ in non_pro_list:
        if _ == str(new_user.username):
            non_pro_list.remove(_)
    if non_pro_list != '':
        non_pro= ''
        for _ in non_pro_list:
            if _ != '':
                non_pro += _ + ','
    else:
        non_pro= ''
    referred_by.non_pro_referrals= non_pro
    referred_by.save()
    msg= f'Dear {referred_by.username}, {new_user.username} just became a premium user but you have reached your maximum premium referrals. You must decide whom you will like to give {new_user.username} to.'
    message= nft.objects.create(user= referred_by, notificationType= 'Referral', notification= msg, action_required= True, action= 'Gift ref', actionID= store.uID)
    message.save()

def ref_search(new_user, referred_by):
    gift_reciver=None
    giver= referred_by
    direct_receivers= str(giver.direct_referrals).split(',')
    for _ in direct_receivers:
        if _ != '':
            receiverObject= User.objects.get(username= _)
            if int(receiverObject.referrals) != 2:
                gift_reciver= receiverObject
                break
    if gift_reciver == None:
        indirect_receivers= str(giver.indirect_referrals).split(',')
        for _ in direct_receivers:
            if _ != '':
                receiverObject= User.objects.get(username= _)
                if int(receiverObject.referrals) != 2:
                    gift_reciver= receiverObject
                    break

    auto_gift_ref(new_user, gift_reciver)
def generate_unique_referral_code(length=8, userName=None):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))

    while ReferralModel.objects.filter(referral_code=code).exists():
        code = ''.join(random.choice(characters) for _ in range(length))
    if userName:
        user= User.objects.get(username=userName)
        user_ref= ReferralModel.objects.create(referral_code= code, user= user)
        user_ref.save()

    return code
    
def referral_link(host, code):
    return f'{host}/accounts/invite/{code}'

def get_referrals_data(request):
    tr= 0
    npr= 0
    pr= 0
    ir= 0
    nprL= ''
    prL= ''
    irL= ''
    if request.user.is_authenticated and request.user.non_pro_referrals != '':
        nprL= (request.user.non_pro_referrals).split(',')
        for _ in nprL:
            if _ != '':
                npr+= 1
    if request.user.is_authenticated and request.user.direct_referrals != '':
        prL= (request.user.direct_referrals).split(',')
        for _ in prL:
            if _ != '':
                pr+= 1
    if request.user.is_authenticated and request.user.direct_referrals != '':
        irL= (request.user.indirect_referrals).split(',')
        for _ in irL:
            if _ != '':
                ir+= 1
    tr= npr + pr + ir
    result= {
        'tr': tr,
        'npr': npr,
        'pr': pr,
        'ir': ir
    }
    return result

@login_required(login_url='login')
def gift_referral(request, uID):
    if request.method == 'POST':
        receiver= request.POST.get('receiver-name')
        giftID= request.POST.get('gift-id')
        receiverObject= User.objects.get(username= receiver)
        giftObject= None
        try:
            giftObject= StoreNewRef.objects.get(uID= giftID)
        except StoreNewRef.DoesNotExist:
            return HttpResponseBadRequest('Invalid Gift ID')
        if giftObject != None:
            giftContent= giftObject.new_ref
            new_referral(receiverObject.referral_code, giftContent.referral_code)
            message= nft.objects.create(user= receiverObject, notificationType= 'Notice', notification= f'Dear {receiverObject.username}, {request.user.username} has given you a referral as a gift 😊💕')
            message.save()
            message= nft.objects.create(user= request.user, notificationType= 'Notice', notification= f'Dear {request.user.username}, {receiverObject.username} has received your referral gift successfully 😊💕')
            message.save()
            giftObject.delete()
            update_nft= nft.objects.get(actionID= giftID)
            update_nft.action= 'Done'
            update_nft.action_required= False
            update_nft.save()
            return redirect('user-dashboard', username= request.user.username)
    else:
        gift_recivers=None
        giver= User.objects.get(email= request.user.email)
        direct_receivers= str(giver.direct_referrals).split(',')
        indirect_receivers= str(giver.indirect_referrals).split(',')
        dR= {}
        iR= {}
        for index, value in enumerate(direct_receivers):
            get_ref= User.objects.get(username= value)
            if get_ref.referrals != 2:
                dR[index]= {
                    'name': value,
                    'rate': 'High',
                    'relationship':'Direct Referral',
                    'refs': get_ref.referrals
                }
        for index, value in enumerate(indirect_receivers):
            if value!= '':
                get_ref= User.objects.get(username= value)
                if get_ref.referrals != 2:
                    iR[index]= {
                        'name': value,
                        'rate': 'Low',
                        'relationship':'Indirect Referral',
                        'refs': get_ref.referrals
                    }

        context= {
            'dr_ref': dR,
            'ir_ref': iR,
            'giftID': uID
        }
        return render(request, 'ref/gift.html', context= context)
        
                
def auto_gift_ref(giftID, recipient):
    pass


