from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

# Create your models here.


class UserDepositAccount(models.Model):
    user = models.OneToOneField(
        User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.account_no)


class DepositModel(models.Model):
    account = models.ForeignKey(
        UserDepositAccount, related_name='deposit', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_deposit = models.DecimalField(
        decimal_places=2, max_digits=12)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
