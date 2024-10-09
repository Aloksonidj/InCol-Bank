from django.contrib import admin
from login.models import Account, User

# Register your models here.
admin.site.register(User)
admin.site.register(Account)