from django.contrib import admin
from .models import UserDepositAccount, DepositModel

# Register your models here.
admin.site.register(UserDepositAccount)


@admin.register(DepositModel)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['get_account_username', 'amount',
                    'balance_after_deposit', 'timestamp']

    def get_account_username(self, obj):
        return obj.account.username

    get_account_username.short_description = 'Account Username'

    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.balance_after_deposit = obj.account.balance
        obj.account.save()
        super().save_model(request, obj, form, change)
