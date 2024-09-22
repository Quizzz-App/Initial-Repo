from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin_index, name= 'admin-index'),
    path('register/', admin_dev_register, name= 'admin-dev-signup'),
    path('login/', admin_dev_logIn, name= 'admin-dev-login'),
    path('backend-approval/<str:incoming_dev_email>/', dev_backend_approval, name= 'backend-approval'),

    
    path('questions-base/', questions_base, name= 'questions-base'),
    path('add-questions/', add_questions, name= 'add-questions'),
    path('add-level/', add_level, name= 'add-level'),
    path('add-category/', add_category, name= 'add-category'),
    path('make-payment/<str:paymentID>/', make_payment, name= 'make-payment'),

    #Developers urls
     path('developers/', dev_index, name= 'dev-index'),
     path('transaction-history/', dev_transaction_history, name= 'transaction-history'),
     path('validate_otp/<str:token>/', validate_otp, name= 'validate_otp'),
    path('logout/', dev_admin_logout, name= 'dev-admin-logout'),
]