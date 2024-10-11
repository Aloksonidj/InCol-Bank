from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Account(models.Model):
    
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    balance = models.BigIntegerField(default=2000)
    status = models.BooleanField(default=True)
    Mobile_no = models.BigIntegerField(max_length=10)
    pin = models.IntegerField(max_length=6,null=True)

    def __str__(self):
        return f"{self.user_name}"
    
class statement(models.Model):

    acc_no = models.ForeignKey(Account,on_delete=models.CASCADE, related_name="account_no")
    before_balance = models.BigIntegerField()
    cash_flow = models.BigIntegerField()
    detail = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.id}"
    