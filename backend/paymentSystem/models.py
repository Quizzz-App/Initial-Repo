from django.db import models
from authenticationSystem.models import CustomUserModel as User
from decimal import Decimal
import uuid
# Create your models here.
class AccountModel(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    balance= models.DecimalField(max_digits= 10, decimal_places= 2, default= 0, blank= False, null= False)
    total_earnings= models.DecimalField(max_digits= 10, decimal_places= 2, default= 0, blank= False, null= False)

    def make_PremiumUser(self):
        self.user.is_premium = True
        self.user.save()
        return 'Premium User'
    
    def update_balance(self):
        user_points= self.user.points_earned
        user_total_points= self.user.total_points_earned
        self.balance= user_points * Decimal(30)
        self.total_earnings= user_total_points * Decimal(30)
        self.save()
        return 'Balance has been updated'
    
    def get_balance(self):
        self.update_balance()
        return self.balance
    
    def __str__(self):
        return f'{self.user.username}'
    

choices= [('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')]
status= [('success', 'Success'), ('failed', 'Failed')]
paymentMethod= [('mobile_money', 'Mobile Money')]

class PaymentChannels(models.Model):
    methods= models.CharField(max_length= 20, choices= paymentMethod, blank= False, null= False)
    name= models.CharField(max_length=100, blank= True)

    def save(self, *args, **kwargs):
        
        self.name = dict(paymentMethod).get(self.methods, self.methods)

        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.name}'

class StorePaymentProcess(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    amount= models.CharField(max_length= 256, blank= False, null= False)
    email= models.CharField(max_length= 256, blank= False, null= False)
    contact= models.CharField(max_length= 256, blank= False, null= False)
    payment_type= models.CharField(max_length= 256, blank= False, null= False)
    carrier_code= models.CharField(max_length= 50, blank= False, null= False)
    carrier_name= models.CharField(max_length= 50, blank= False, null= False)
    date_of_payment= models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} --- {self.amount}'
    

# All transactions    
class TransactionModel(models.Model):
    account= models.ForeignKey(AccountModel, on_delete= models.CASCADE)
    amount= models.DecimalField(max_digits= 10, decimal_places= 2, blank= False, null= False)
    timestamp= models.DateTimeField(auto_now_add= True)
    transactionType= models.CharField(max_length= 10, choices= choices)
    transactionTypeStatus= models.CharField(max_length= 10, choices= status)
    transactionRefrence= models.CharField(max_length= 30, blank= False, null= False, default= None)
    paymentMethod= models.CharField(max_length= 20, blank= False, null= False)
    mobileNumber= models.CharField(max_length= 15, blank= False, null= False)
    carrier= models.CharField(max_length= 20, blank= False, null= False)
    date= models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.paymentMethod = dict(paymentMethod).get(self.paymentMethod, self.paymentMethod)
        self.transactionType = dict(choices).get(self.transactionType, self.transactionType)
        self.transactionTypeStatus = dict(status).get(self.transactionTypeStatus, self.transactionTypeStatus)

        super().save(*args, **kwargs)
    
    def get_balance(self):
        return self.account.balance
    
    def process_transaction(self):
        if self.transactionType == 'deposit':
            self.account.balance = 0
            self.account.save()
        elif self.transactionType == 'withdrawal':
            if self.account.balance >= self.amount:
                self.account.balance -= self.amount
                self.account.save()
            else:
                self.transactionTypeStatus = 'failed'
        self.save()
        return self.transactionTypeStatus

    def __str__(self):
        return f'{self.account.user.username} ---> {self.amount} ---> {self.timestamp} ---> {self.transactionType} ---- {self.transactionTypeStatus}'
    
class PaymentInfoModel(models.Model):
    account= models.ForeignKey(User, on_delete= models.CASCADE)
    firstName= models.CharField(max_length= 50, blank= False, null= False, default= '')
    lastName= models.CharField(max_length= 50, blank= False, null= False, default= '')
    email= models.CharField(default= '', max_length= 240)
    paymentMethod= models.CharField(max_length= 20, choices=paymentMethod, default=paymentMethod[0][0])
    paymentMethodName= models.CharField(max_length=100, blank= True)
    accountNumber= models.CharField(max_length= 15, blank= False, null= False)
    carrier= models.CharField(max_length= 20, blank= False, null= False)

    def save(self, *args, **kwargs):

        self.paymentMethodName = dict(paymentMethod).get(self.paymentMethod, self.paymentMethod)
        # self.firstName = self.account.first_name
        # self.lastName = self.account.last_name
        # self.email = self.account.email

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.account.username} ---> {self.paymentMethod} ---> {self.accountNumber} ---> {self.carrier}'

#For paystack payment
class RecieptModel(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    recieptID=  models.CharField(max_length= 50, blank= False, null= False)
    recieptCode=  models.CharField(max_length= 50, blank= False, null= False)

    def __str__(self):
        return f'{self.user.username} ---> {self.recieptID} ---> {self.recieptCode}'

class IssueWithdrawModel(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    issuer= models.CharField(max_length= 50, blank= False, null= False, default= '')
    amount=  models.DecimalField(max_digits= 10, decimal_places= 2, blank= False, null= False)
    status= models.BooleanField(default= False)
    state= models.CharField(max_length= 50, blank= False, null= False, default= 'Pending')
    acN= models.CharField(max_length= 50, blank= False, null= False, default= '')
    timestamp= models.DateField(auto_now_add= True)
    refCode= models.CharField(max_length= 50, blank= False, null= False, default= '')

    def __str__(self):
        return f'{self.issuer} ---> {self.amount} ---> {self.status}'

class TransferModel(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    transfer_amount= models.DecimalField(max_digits= 10, decimal_places= 2, blank= False, null= False)
    transferID= models.CharField(max_length= 20, blank= False, null= False)
    transferReference= models.CharField(max_length= 100, blank= False, null= False)
    transferCode= models.CharField(max_length= 100, blank= False, null= False)
    recipientID= models.CharField(max_length= 20, blank= False, null= False)
    sender= models.CharField(max_length= 20, blank= False, null= False)

    def __str__(self):
        return f'Transfer to {self.recipientID} was approved by {self.sender}'

class DeclinedTransferModel(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    requestedBy= models.CharField(max_length= 100, blank= False, null= False)
    attendedBy= models.CharField(max_length= 100, blank= False, null= False)
    reason= models.CharField(max_length= 999999999999999999, blank= False, null= False)
    amountRequested=models.CharField(max_length= 100, blank= False, null= False)
    requestedBy_balance=models.CharField(max_length= 100, blank= False, null= False)

    def __str__(self):
        return f'Declined withdrawal by {self.attendedBy}.....Reason: {self.reason}'

class WithdrwalSheetsModel(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    generated_by= models.ForeignKey(User, on_delete= models.CASCADE)
    sheet= models.FileField(upload_to='excel_withdrwal_list/')
    timestamp= models.DateTimeField(auto_now_add= True)
    completedTransfers= models.BooleanField(default= False)

    def __str__(self):
        return f'Sheet generated by {self.generated_by.username} on {self.timestamp}'
    

