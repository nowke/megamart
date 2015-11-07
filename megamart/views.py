from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy

from .mixins import AdminRequiredMixin

class HomePageView(TemplateView):
	template_name = "megamart/home.html"

class LoginPageView(TemplateView):
	template_name = "megamart/login.html"

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active and user.is_superuser:
				print 'Yes admin'
				login(request, user)
				return redirect('admin_home')
			else:
				print 'Disabled'
		else:
			print 'Invalid login'

class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('home')


class RegisterPageView(TemplateView):
	template_name = "megamart/register.html"

# DB Admin specific views
class AdminHomeView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/home.html"

class AdminBranchesView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/branches.html"