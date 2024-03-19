from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, View
from .models import BookStore, Category, Review
from accounts.models import BorrowedBook
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.


class StoreViews(TemplateView):
    template_name = 'stores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            books = BookStore.objects.filter(category=category)
        else:
            category = None
            books = BookStore.objects.all()

        context['categories'] = Category.objects.all()
        context['category'] = category
        context['books'] = books
        return context


# details view


class DetailsView(TemplateView):
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = kwargs.get('id')
        single_book = get_object_or_404(BookStore, id=book_id)
        reviews = Review.objects.filter(book=single_book)
        context['single_book'] = single_book
        context['reviews'] = reviews
        return context


# Success mail sending
def borrow_mail_sending(user, subject, amount, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


# borrow book view
class BorrowBookView(View):
    def get(self, request, book_id):
        if request.user.is_authenticated:
            book = BookStore.objects.get(pk=book_id)
            user = request.user
            account = user.account

            if account.balance >= book.price:
                # borrow the book
                borrowed_book = BorrowedBook.objects.create(
                    user=user, book=book)
                borrowed_book.save()

                # Update
                account.balance -= book.price
                account.save()

                # success message
                messages.success(
                    request, f"You have successfully borrowed {book.title}. Your new balance is {account.balance} taka.")
                borrow_mail_sending(
                    self.request.user, "Borrowed message", book.title, 'borrow_mail.html')
                return redirect('profile')
            else:
                # Insufficient balance
                messages.error(
                    request, "You don't have enough balance to borrow this book.")
                return redirect('profile')
        else:
            return redirect('login')


@login_required
def profile(request):
    borrowings = BorrowedBook.objects.filter(user=request.user)
    return render(request, 'profile.html', {'borrowings': borrowings})
