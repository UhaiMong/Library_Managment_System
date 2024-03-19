from django.urls import path
from .views import StoreViews, DetailsView, BorrowBookView, profile
urlpatterns = [
    path('stores/', StoreViews.as_view(), name='stores'),
    path('details/<int:id>/', DetailsView.as_view(), name='details'),
    path('borrow/<int:book_id>/', BorrowBookView.as_view(), name='borrow'),
    path('profile/', profile, name='profile'),
    path('stores/<slug:slug>/',
         StoreViews.as_view(), name='category_book')
]
