from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin_index, name= 'admin-index'),
    path('register/', admin_dev_register, name= 'admin-dev-signup'),
    path('login/', admin_dev_logIn, name= 'admin-dev-login'),
    
    path('questions-base/', questions_base, name= 'questions-base'),
    path('add-questions/', add_questions, name= 'add-questions'),
    path('add-level/', add_level, name= 'add-level'),
    path('add-category/', add_category, name= 'add-category'),

    #Developers urls
     path('developers/', dev_index, name= 'dev-index'),

    path('logout/', dev_admin_logout, name= 'dev-admin-logout'),
]