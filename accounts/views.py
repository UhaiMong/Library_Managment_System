from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, CreateView
from .forms import UserRegistrationForm, DepositForm
from .models import DepositModel, BorrowedBook
from stores.models import BookStore
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')

# email sending for deposit amount


def deposit_mail_sending(user, subject, amount, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class DepositCreationMixin(LoginRequiredMixin, CreateView):
    template_name = 'balance_deposit.html'
    title = ''
    model = DepositModel
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context


class DepositView(DepositCreationMixin):
    form_class = DepositForm
    title = 'Deposit Balance'

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(
            self.request, f'{"{:,.2f}".format(float(amount))} $ deposited successfully'
        )
        deposit_mail_sending(
            self.request.user, "Deposit message", amount, 'deposit_mail.html')
        return super().form_valid(form)


class UserProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['book_id']
        book = BookStore.objects.get(pk=book_id)
        user = request.user
        account = user.account

        if account.balance >= book.price:
            # Sufficient balance to borrow the book
            borrowed_book = BorrowedBook.objects.create(user=user, book=book)
            borrowed_book.save()

            # Update user's account balance
            account.balance -= book.price
            account.save()

            # Display success message
            messages.success(
                request, f"You have successfully borrowed {book.title}. Your new balance is {account.balance} taka.")

            # Redirect to a success page or any other appropriate page
            return redirect('success-page-url')
        else:
            # Insufficient balance
            messages.error(
                request, "You don't have enough balance to borrow this book.")
            return redirect('insufficient-balance-page-url')
