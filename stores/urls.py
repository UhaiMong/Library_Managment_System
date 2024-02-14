from django.urls import path
from .views import StoreViews, DetailsView
urlpatterns = [
    path('', StoreViews.as_view(), name='books'),
    path('details/', DetailsView.as_view(), name='details')
]
