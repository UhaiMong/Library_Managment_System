from django import forms
from .constants import GENDER_TYPE
from .models import UserDepositAccount, DepositModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email', 'gender']

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save()
            gender = self.cleaned_data.get('gender')
            UserDepositAccount.objects.create(
                user=our_user,
                gender=gender,
                account_no=10000 + our_user.id
            )
        return our_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class TransactionForm(forms.ModelForm):
    class Meta:
        model = DepositModel
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_deposit = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'Minimum needed $ {min_deposit_amount}')
        return amount
