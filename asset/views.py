from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserCreationForm
from django.contrib.auth import logout, login
from django.views.generic import View, TemplateView, CreateView, ListView, RedirectView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
# import pandas as pd
# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class LoginView(RedirectView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(data = request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    
class LogoutView(RedirectView):
    def get(self, request):
        logout(request)
        return redirect('login')

class RegisterView(View):
    form_class = UserCreationForm
    template_name = 'register.html'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    
    def post(self, request):
        form = self.form_class(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    
class AssetsView(View):
    tickers_list = []
    # tickers_df = pd.read_csv("data/tickers.csv", sep = ';')
    # tickers_list = tickers_df['TckrSymb'].tolist()
    template_name = 'assets.html'
    def get(self, request):
        return render(request, self.template_name, {'tickers' : self.tickers_list})
        




