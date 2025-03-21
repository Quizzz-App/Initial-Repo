from django.urls import path
from .views import *
from adminSystem.views import getMetrics

urlpatterns = [
    path('logout-account', logout_page, name= 'logout'),
    path('sign-in/', login_page, name= 'login'),
    path('register/', register_user, name= 'register'),
    path('notifications/', notificationsPage, name= 'notificaions-page'),
    path('notifications/<str:nftID>', notificationsRead, name= 'read-notificaions-page'),
    path('notifications-update/', notificationsReadUpdate, name= 'read-notificaions-update'),
    path('notifications-delete/', notificationsDelete, name= 'delete-notificaions'),
    path('activate/<str:uidb64>/<str:token>/<int:special>/', activate, name='activate'),
    path('password-reset/request/', passwordReset, name= 'password-reset-request'), #send mail
    path('password-reset/confirm/<str:uidb64>/<str:token>/', passwordResetConfirm, name= 'password-reset-confirm'), #verify token and redirect
    # path('password-reset/complete/', passwordResetComplete, name= 'password-reset-complete'), send mail on completion
    # path('password-reset/done/', passwordResetDone, name= 'password-reset-done'), show reset done page
    path('password-change/<str:id>/', passwordChange, name= 'password-change'),# change password
    path('invite/<str:code>/', inviteRedirect, name= 'invite-redirect'),
    path('comments-complains/', complainsComments, name= 'comments-complains'),

    #user urls
    path('user/<str:username>/dashboard/', userDashboard, name= 'user-dashboard'),
    path('user/<str:username>/referrals/', userRef, name= 'user-referrals'),
    path('user/<str:username>/quiz/', userQuiz, name= 'user-quiz'),
    path('user/<str:username>/wallet/', userWallet, name= 'user-wallet'),
    path('user/<str:username>/transactions/', userT, name= 'user-transactions'),
    path('user/<str:username>/update-profile/', userUP, name= 'user-update-profile'),
    path('user/update/profile/', updateProfile, name='update-profile'),
    path('user/update/password/', updatePassword, name='update-password'),
    path('user/notifications/', notifications, name='user-notifications'),
    path('user/<str:username>/metrics/', getMetrics, name='user-metrics'),

]