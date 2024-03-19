from django.contrib import admin
from .models import UserDepositAccount, DepositModel, BorrowedBook

# Register your models here.
admin.site.register(UserDepositAccount)
admin.site.register(BorrowedBook)


@admin.register(DepositModel)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['get_account_username', 'amount',
                    'balance_after_deposit', 'timestamp']

    def get_account_username(self, obj):
        return obj.account.user

    get_account_username.short_description = 'Account Holder'

    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.balance_after_deposit = obj.account.balance
        obj.account.save()
        super().save_model(request, obj, form, change)
