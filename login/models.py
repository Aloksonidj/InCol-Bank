from django.db import models

# Create your models here.
class Account(models.Model):
    
    user_name = models.CharField(max_length=64)
    balance = models.BigIntegerField()
    passwords = models.CharField(max_length=20)
    status = models.CharField(max_length=8)
    Mobile_no = models.BigIntegerField(max_length=10)
    pin = models.IntegerField(max_length=6,null=True)

