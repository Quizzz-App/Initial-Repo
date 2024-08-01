from django.db import models
from authenticationSystem.models import CustomUserModel

# Create your models here.
class AdminDeveloperStatusModel(models.Model):
    name= models.CharField(max_length= 20, blank= False, null= False)

    def __str__(self):
        return self.name

class AdminDeveloperUserModel(CustomUserModel):
    status= models.ForeignKey(AdminDeveloperStatusModel, on_delete= models.CASCADE)
    approved_status= models.BooleanField(default= False, blank= False)

    def __str__(self):
        return f'{self.username} --> {self.status.name}'

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
    
