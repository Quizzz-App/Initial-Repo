from django.contrib.auth.forms import *
from django import forms
from .models import AdminDeveloperUserModel
from django.core.exceptions import ValidationError

class list_of_approved_backend_devs(forms.ModelForm):
    class Meta:
        model = AdminDeveloperUserModel 
        fields = ['email'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get a list of approved developers
        approved_developers = AdminDeveloperUserModel.objects.filter(approved_status=True)

        # Mask and populate the dropdown list with masked email addresses
        # self.fields['approved_status'].choices = [
        #     (dev.email, self.mask_email(dev.email)) for dev in approved_developers
        # ]

    def mask_email(self, email):
        """
        Mask the email address for privacy (e.g., john***@example.com)
        """
        user_part, domain_part = email.split('@')
        masked_user_part = user_part[:3] + '***'
        return f'{masked_user_part}@{domain_part}'