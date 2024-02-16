from django.urls import path
from .views import StoreViews, DetailsView
urlpatterns = [
    path('stores/', StoreViews.as_view(), name='stores'),
    path('details/<int:id>/', DetailsView.as_view(), name='details'),
    path('stores/<slug:slug>/',
         StoreViews.as_view(), name='category_book')
]
