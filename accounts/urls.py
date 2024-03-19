from django.urls import path
from .views import RegistrationView, UserLoginView, UserLogoutView, UserProfileView, DepositView, ReturnBookView, ReviewBookView
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('return-book/', ReturnBookView.as_view(), name='return_book'),
    path('review_book/<int:book_id>/', ReviewBookView.as_view(), name='review'),
]
