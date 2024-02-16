from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from .models import BookStore, Category, Review
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import ReviewForm

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


class DetailsView(TemplateView):
    template_name = 'details.html'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book_id = kwargs.get('id')
        single_book = get_object_or_404(BookStore, id=book_id)

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = single_book
            new_review.save()
        else:
            # Handle invalid form here, maybe re-render the page with error messages
            pass

        return redirect('details', id=book_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = kwargs.get('id')
        single_book = get_object_or_404(BookStore, id=book_id)
        reviews = Review.objects.filter(book=single_book)
        review_form = ReviewForm()
        context['single_book'] = single_book
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context
