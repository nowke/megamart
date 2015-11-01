from django.views.generic.base import TemplateView

from django.shortcuts import render
from django.http import HttpResponse

class HomePageView(TemplateView):
	template_name = "megamart/home.html"

class LoginPageView(TemplateView):
	template_name = "megamart/login.html"

class RegisterPageView(TemplateView):
	template_name = "megamart/register.html"