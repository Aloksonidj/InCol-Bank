from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Account(models.Model):
    '''user_name : model.object(User) | balance: Integer | status: Boolen(default = True) | Mobile_no: Integer | pin: Integer '''
    
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    balance = models.BigIntegerField(default=2000)
    status = models.BooleanField(default=True)
    Mobile_no = models.BigIntegerField()
    pin = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user_name}"
    
class statement(models.Model):

    acc_no = models.ForeignKey(Account,on_delete=models.CASCADE, related_name="account_no")
    After_balance = models.BigIntegerField()
    cash_flow = models.BigIntegerField()
    detail = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    