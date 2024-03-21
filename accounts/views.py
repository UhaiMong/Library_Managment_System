from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, CreateView, View
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
from django.shortcuts import get_object_or_404
from stores.forms import ReviewForm

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


# class UserLogoutView(LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             pass
#         return super().dispatch(request, *args, **kwargs)

#     next_page = reverse_lazy('home')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter borrowed books for the logged-in user
        borrowed_books = BorrowedBook.objects.filter(user=self.request.user)
        context['borrowed_books'] = borrowed_books
        return context

# Return Book view


class ReturnBookView(View):
    def post(self, request):
        if request.user.is_authenticated:
            book_id = request.POST.get('book_id')
            try:
                borrowed_book = BorrowedBook.objects.get(
                    user=request.user, book_id=book_id, returned=False)
            except BorrowedBook.DoesNotExist:
                messages.error(request, "This book has already been returned.")
                return redirect('profile')

            # Mark the book as returned
            borrowed_book.returned = True
            borrowed_book.save()

            # Add the book price back to the user's account
            request.user.account.balance += borrowed_book.book.price
            request.user.account.save()

            messages.success(
                request, f"The book \"{borrowed_book.book.title}\" has been returned successfully.")
            return redirect('profile')
        else:
            return redirect('login')

# Review the book


class ReviewBookView(TemplateView):
    template_name = 'review_book.html'

    def post(self, request, *args, **kwargs):
        # Handle POST request to post a new review
        review_form = ReviewForm(data=request.POST)
        # context = super().get_context_data(**kwargs)
        book_id = kwargs.get('book_id')
        print(book_id)
        single_book = get_object_or_404(BookStore, id=book_id)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = single_book
            new_review.save()
            # Redirect to the profile page after posting the review
            return redirect('stores')
        else:
            # Invalid form, handle appropriately
            context = self.get_context_data()
            context['review_form'] = review_form
            return self.render_to_response(context)
