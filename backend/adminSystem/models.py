from django.db import models
from authenticationSystem.models import CustomUserModel
from datetime import datetime
from decimal import Decimal


# Create your models here.
class AdminDeveloperStatusModel(models.Model):
    name= models.CharField(max_length= 20, blank= False, null= False)

    def __str__(self):
        return self.name

# model for creating developer's account
class AdminDeveloperUserModel(CustomUserModel):
    status= models.ForeignKey(AdminDeveloperStatusModel, on_delete= models.CASCADE)
    approved_status= models.BooleanField(default= False, blank= False)

    def __str__(self):
        return f'{self.username} --> {self.status.name}'

#project wallet status
class WalletModel(models.Model):
    wallet_name= models.CharField(max_length=20, default= '', unique= True)
    project_wallet= models.PositiveIntegerField(default= 0)
    users_wallet= models.PositiveBigIntegerField(default= 0)
    team_wallet= models.PositiveIntegerField(default= 0)
    date= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'Wallet for {self.wallet_name}'
    
    def updateBalance(self):
        self.project_wallet = self.project_wallet + 30
        self.users_wallet = self.users_wallet + 12
        self.team_wallet = self.team_wallet + 18

        self.save()

    def get_project_balance(self):
        return self.project_wallet
    
    def get_users_balance(self):
        return self.users_wallet
    
    def get_team_balance(self):
        return self.team_wallet
    

class developer_wallet(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)  # Can have multiple wallets
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=20, null=True)  # Store the wallet name as "Month Year"
    month = models.IntegerField(default=datetime.now().month)  # Store the month number
    year = models.IntegerField(default=datetime.now().year)   # Store the year number
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set the wallet name based on the month and year before saving
        self.name = datetime(self.year, self.month, 1).strftime('%B %Y')
        super().save(*args, **kwargs)
    
    def updateBalance(self):
       # 5% of every user deposit
       self.balance =self.balance + Decimal(0.9)
       
    def get_month_amount(self):
        return self.balance

    def __str__(self):
        return f"Wallet for {self.name} - User: {self.user.username}"
    
