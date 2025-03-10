from django.contrib.auth.forms import *
from django import forms
from .models import CustomUserModel as User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    email= forms.EmailField(required= True)
    first_name= forms.CharField(required= True)
    last_name= forms.CharField(required= True)
    
    class Meta:
        model= User
        fields= ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data= super().clean()
        email= self.cleaned_data.get('email')
        username= self.cleaned_data.get('username')
        if User.objects.filter(username= username).exists():
            # raise ValidationError('An account with this username already exists')
            pass
        elif User.objects.filter(email= email).exists():
            # raise ValidationError('An account with this email address already exists')
            pass
        return cleaned_data


class LoginForm(AuthenticationForm):
    # username= forms.CharField(required= True)

    class Meta:
        fields= ['username', 'password']

class PasswordResetRequestForm(forms.ModelForm):
    email= forms.EmailField(required= True)

    class Meta:
        model= User
        fields= ['email']

class PasswordChangeForm(PasswordResetForm):
    passwordOne= forms.CharField(label= 'New password', widget=forms.PasswordInput)
    passwordTwo= forms.CharField(label= 'Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        model= User
        fields= ['passwordOne', 'passwordTwo']

    def clean(self):
        cleaned_data= super().clean()
        passwordOne= cleaned_data.get('passwordOne')
        passwordTwo= cleaned_data.get('passwordTwo')
        if passwordOne and passwordTwo and passwordOne != passwordTwo:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data