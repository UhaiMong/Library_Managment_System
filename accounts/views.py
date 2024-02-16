from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView

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
