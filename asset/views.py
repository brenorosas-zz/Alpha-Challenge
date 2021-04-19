from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView
from .models import *
# Create your views here.
class TemplateHomeView(TemplateView):
    template_name = 'home.html'

class TemplateLoginView(Viwe):
     template_name = 'login.html'
