from django.shortcuts import render
from django.views.generic import FormView, TemplateView, CreateView
from .forms import UserRegistrationForm, DepositForm
from .models import DepositModel
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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
        return super().form_valid(form)


class UserProfileView(TemplateView):
    template_name = 'profile.html'

    # def get(self, request):
    #     form = UserUpdateForm(instance=request.user)
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request):
    #     form = UserUpdateForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profile')
    #     return render(request, self.template_name, {'form': form})
