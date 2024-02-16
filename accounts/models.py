from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE
from stores.models import BookStore
from django.utils import timezone

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

# Borrow Book report model


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    returned_date = models.DateField(null=True, blank=True)

    @property
    def is_returned(self):
        return self.returned

    def returned_book(self):
        self.returned = True
        self.returned_date = timezone.now()
        self.save()
        return self.book.price

    def __str__(self):
        return self.book.title


class User(models.Model):
    ...

    def borrowing_history(self):
        return BorrowedBook.objects.filter(user=self)
