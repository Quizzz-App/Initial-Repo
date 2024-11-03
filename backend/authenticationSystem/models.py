from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
import uuid

# Create your models here.
#Custom User Manager for Custom User Model
class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The given password must be set")
        if not first_name:
            raise ValueError("The given first name must be set")
        if not last_name:
            raise ValueError("The given last name must be set")
        email = self.normalize_email(email)
        # username = 
        user = self.model(username=username, email=self.normalize_email(email), first_name= first_name, last_name= last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(username, email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, username, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        

        return self._create_user(username, email, password, first_name, last_name, **extra_fields)


#Custom User Model for creating accounts
class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    first_name= models.CharField(max_length= 240)
    last_name= models.CharField(max_length= 240)
    email= models.EmailField(db_index= True, unique= True, max_length= 240)
    username= models.CharField(unique= True, max_length= 240)


    referred_by= models.CharField(max_length= 240, blank= True)
    referral_code= models.CharField(max_length= 240, blank= True)
    referrals= models.PositiveIntegerField(default= 0, blank= True)
    indirectReferrals= models.PositiveIntegerField(default= 0, blank= True)
    referral_code_expired= models.BooleanField(default= False, blank= True)
    points_earned= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_points_earned= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    direct_referrals= models.CharField(max_length= 99999, blank= True, default='')
    indirect_referrals= models.CharField(max_length= 99999, blank= True, default='')
    non_pro_referrals= models.CharField(max_length= 99999, blank= True, default='')
    quiz_taken= models.PositiveIntegerField(default= 0, blank= True)

    is_premium= models.BooleanField(default= False)
    is_staff= models.BooleanField(default= False)
    is_active= models.BooleanField(default= False)
    is_superuser= models.BooleanField(default= False)

    objects= CustomUserManager()

    USERNAME_FIELD= 'username' # Username field must not be included in the required field
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name= 'User'
        verbose_name_plural= 'Users'



#Token model
class TokensModel(models.Model):
    token= models.CharField(blank=False, null=False, max_length= 999999999999)
    timestamp= models.DateTimeField(blank=False, null=False, auto_now_add= True)
    user_id= models.IntegerField(blank=False, null=False)
    refCode= models.CharField(max_length= 240, null= True, default='')

    def __str__(self):
        return f'{self.user_id} ---> {self.timestamp}'
    
class Notifications(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    user= models.ForeignKey(CustomUserModel, on_delete= models.CASCADE)
    notification= models.CharField(max_length= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999, blank= False)
    timestamp= models.DateTimeField(auto_now_add= True)
    read= models.BooleanField(default= False)
    action_required= models.BooleanField(default= False)
    action= models.CharField(max_length=100, default='')
    actionID= models.CharField(max_length=100, default='')

    def __str__(self):
        return f'{self.user.username} ---> Status: {self.read}'

class ReviewModel(models.Model):
    uuid= models.UUIDField(default= uuid.uuid4, unique= True)
    message= models.CharField(max_length= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999, blank= False)
    user= models.CharField(max_length=100, blank= False)
    review_type= models.CharField(max_length=20, blank= False)
    timestamp= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.uuid}'