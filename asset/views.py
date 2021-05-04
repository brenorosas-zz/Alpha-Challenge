from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserCreationForm, AssetForm
from django.contrib.auth import logout, login
from django.views.generic import View, TemplateView, CreateView, ListView, RedirectView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
import pandas as pd
from .tasks import calculate_next_monitoring_date

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
    tickers_df = pd.read_csv("data/tickers.csv", sep = ';')
    tickers_list = tickers_df['TckrSymb'].tolist()
    template_name = 'assets.html'
    def get(self, request):
        return render(request, self.template_name, {'tickers' : self.tickers_list})

class DetailAssetView(View):
    template_name = 'detail_asset.html'
    form_class = AssetForm
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        kwargs['form'] = form
        return render(request, self.template_name, kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data = request.POST)
        if form.is_valid():
            asset = form.save(ticker = kwargs['ticker'], id = request.user.id)
            as1 = Management.objects.create(
                asset = asset,
                next_time = calculate_next_monitoring_date(asset)
            )
            as1.save()
            return redirect('home')
        form = self.form_class()
        kwargs['form'] = form
        return render(request, self.template_name, kwargs)
        
class MonitoringView(View):
    template_name = "monitoring.html"
    def get(self, request):
        assets = User.objects.get(id = request.user.id).asset_set.all()
        return render(request, self.template_name, {'assets': assets})

class RemoveAssetView(RedirectView):
    def get(self, request, *args, **kwargs):
        asset = Asset.objects.get(id = kwargs['id'])
        asset.delete()
        return redirect('monitoring')

class SettingsAssetView(View):
    template_name = "settings.html"