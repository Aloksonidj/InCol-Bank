from django.contrib import admin
from login.models import Account, User, statement

# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(statement)