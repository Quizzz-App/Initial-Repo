from django.db import models
from authenticationSystem.models import CustomUserModel as User
import uuid

# Create your models here.
class ReferralModel(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    referral_code= models.CharField(max_length=8, unique= True)
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} ---> {self.referral_code}'

class StoreNewRef(models.Model):
    uID= models.UUIDField(default= uuid.uuid4, unique= True)
    new_ref= models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'store_new_ref')
    ref_king= models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'store_king')

    def __str__(self):
        return f'Parent: {self.ref_king.username} ---> child: {self.new_ref.username}'

class ReferralModelHistory(models.Model):
    uID= models.UUIDField(default= uuid.uuid4, unique= True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    ref= models.ForeignKey(User, on_delete=models.CASCADE, related_name='ref')
    relationship= models.CharField(max_length=50, blank= False, null= False)
    points_earned= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date= models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.user.username} ---> {self.ref}'
