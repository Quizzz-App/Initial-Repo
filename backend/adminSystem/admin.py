from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(WalletModel)
admin.site.register(AdminDeveloperStatusModel)
admin.site.register(AdminDeveloperUserModel)
admin.site.register(developer_wallet)