from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.storePaymentProccess, name='store-payment-page'),
    path('confirm/', views.ConfirmPaymentProcess, name='confirm-payment-page'),
    path('intiate-Momo-transaction/', views.IntiateMoMoTransaction, name='make-momo-payment'),
    path('first-Momo-Transaction/submit-otp/', views.continueMoMoTransaction, name='submit-otp'),
    path('intiate-Bank-transaction/', views.IntiateBankTransaction, name='make-bank-payment'),
    path('verifyDeposite/<str:transactionID>/',views.verifyTransaction, name= 'verify-transaction'),
    # path('transaction\'s-history/',views.transactionHistory, name= 'transaction-history'),
    # path('successful-transaction/',views.successfulPayment, name= 'success'),
    # path('pay-methods/',views.paymentMethod, name='pay-methods'),
    path('issue-withdrawal/',views.issueWithdrawal, name='issue-withdrawal'),
    path('approve-withdrawal/',views.approveWithdrawalRequest, name='approve-withdrawal'),
    path('decline-withdrawal/',views.declineWithdrawalRequest, name='decline-withdrawal'),
    path('finalize-withdrawal/',views.FinalizeFunds, name='decline-withdrawal'),
    path('decide-payment-method/', views.decidePaymentMethod, name= 'decide-payment-method'),
    path('payment-method-manual/', views.manualPaymentMethod, name= 'payment-method-manual'),
    path('payment-method-manual-list/', views.generateExcelList, name= 'payment-method-manual-list'),
    path('pending-payment/', views.pendingPayment, name= 'pending-payment'),
    path('update-payment/<str:fileID>/', views.updatePayment, name= 'update-payment'),
    path('completed-transfer/', views.completedTransfer, name= 'completed-transfer'),
]