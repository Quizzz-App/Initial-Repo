from authenticationSystem.models import CustomUserModel as User
from authenticationSystem.models import Notifications as nft
from django.shortcuts import render
from decimal import Decimal
from .models import *
import random, string

# Create your views here.

def pay_commission(referred_by_code, new_user_referral_code, commission_rate):
    referrer = User.objects.get(referral_code=referred_by_code)
    new_user = User.objects.get(referral_code=new_user_referral_code)

    referrer.points_earned = Decimal(referrer.points_earned) + commission_rate
    referrer.save()

    #Check if referrer was also referred by someone
    first_ref= referrer
    cmr= Decimal(round((commission_rate * Decimal( 0.5)), 2))
    while True:
        if first_ref.referred_by != '':
            referrer_referral = User.objects.get(referral_code=first_ref.referred_by)
            referrer_referral.points_earned = Decimal(referrer_referral.points_earned) + cmr
            print(cmr)
            if referrer_referral.indirect_referrals == '':
                referrer_referral.indirect_referrals += str(new_user.username)
            else:
                referrer_referral.indirect_referrals += ',' + str(new_user.username)
            referrer_referral.indirectReferrals += 1
            referrer_referral.save()
            first_ref = referrer_referral
            print(cmr * Decimal( 0.5))
            cmr= Decimal(round((cmr * Decimal( 0.5)), 2))
            if cmr < 0.01:
                cmr= Decimal(0.01)
            else:
                pass
        else:
            break

def new_referral(referred_by_code, new_user_referral_code):
    new_user = User.objects.get(referral_code=new_user_referral_code)
    referred_by= User.objects.get(referral_code=referred_by_code)


    if referred_by.referrals >= 2:
        store_ref(new_user, referred_by)
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
    msg= f'Dear {referred_by.username}, {new_user.username} just became a premium user but you have reached your maximum premium referrals. You must decide whom you will like to give {new_user.username} to.'
    message= nft.objects.create(user= referred_by, notification= msg)
    message.save()

# def ref_tree_search(ref):
#     new_king= ''
#     ref_direct_refs_max= False
#     list_of_direct_ref= (ref.direct_referrals).split(',')
#     for _ in list_of_direct_ref:
#         if _.referrals < 2:
#             new_king= User.objects.get(username= str(_))
#             ref_direct_refs_max= False
#             break
#         else:
#             ref_direct_refs_max= True

#     if ref_direct_refs_max:
#     return new_king

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
    nprL= ''
    prL= ''
    if request.user.is_authenticated and request.user.non_pro_referrals != '':
        nprL= (request.user.non_pro_referrals).split(',')
        npr= len(nprL)
    if request.user.is_authenticated and request.user.direct_referrals != '':
        prL= (request.user.direct_referrals).split(',')
        pr= len(prL)
    tr= npr + pr
    result= {
        'tr': tr,
        'npr': npr,
        'pr': pr,
    }
    return result
