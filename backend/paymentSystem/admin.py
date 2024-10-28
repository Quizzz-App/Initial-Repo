from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AccountModel)
admin.site.register(TransactionModel)
admin.site.register(PaymentChannels)
admin.site.register(PaymentInfoModel)
admin.site.register(IssueWithdrawModel)
admin.site.register(RecieptModel)
admin.site.register(TransferModel)
admin.site.register(DeclinedTransferModel)
admin.site.register(WithdrwalSheetsModel)
