from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class StoreViews(TemplateView):
    template_name = 'stores.html'


class DetailsView(TemplateView):
    template_name = 'details.html'
