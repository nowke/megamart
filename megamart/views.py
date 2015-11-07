from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from .mixins import AdminRequiredMixin
from admins.models import City, Branch, StoreAdmin

class HomePageView(TemplateView):
	template_name = "megamart/home.html"

class LoginPageView(TemplateView):
	template_name = "megamart/login.html"

	def get(self, request):
		if request.user.is_authenticated and request.user.is_active and request.user.is_superuser:
			return redirect('admin_home')
		else:
			return render(request, self.template_name)

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

	def get(self, request):
		cities = City.objects.all().order_by('name')
		context = {
			'cities': cities,
		}
		return render(request, self.template_name, context)

class AdminAddBranchView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/new_branch.html"

	def get(self, request):
		default_city_id = request.GET.get('city', 0)
		cities = City.objects.all().order_by('name')
		context = {
			'cities': cities,
			'default_city_id': int(default_city_id),
		}
		return render(request, self.template_name, context)

	def post(self, request):

		name = request.POST['name']
		city = request.POST['city']
		address = request.POST['address']

		city_obj = City.objects.get(id=int(city))
		branch = Branch(title=name, city=city_obj, address=address)
		branch.save()

		if request.is_ajax():
			return JsonResponse({"success": True, "branch_title": branch.title})