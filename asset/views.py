from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import logout, login
from django.views.generic import View, TemplateView, CreateView, ListView, RedirectView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
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
        if(form.is_valid()):
            login(request, form.get_user())
            return redirect('home')
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    
class LogoutView(RedirectView):
    def get(self, request):
        logout(request)
        return redirect('login')



