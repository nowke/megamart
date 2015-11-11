from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User

from .mixins import AdminRequiredMixin
from admins.models import City, Branch, StoreAdmin
from store.models import Employee
from product_manager.models import ProductManager

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
				try:
					product_manager = ProductManager.objects.get(user=user)
					login(request, user)
					return redirect('product_manager:home')
				except ProductManager.DoesNotExist:
					store_admin = StoreAdmin.objects.get(user=user)
					login(request, user)
					return redirect('store:home')
				except StoreAdmin.DoesNotExist:
					print 'No store admin'
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

class AdminBranchDetailView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/branch_detail.html"

	def get(self, request, branch_id):
		try:
			branch = Branch.objects.get(id=branch_id)

			context = {
				'branch': branch,
			}

			return render(request, self.template_name, context)

		except Branch.DoesNotExist:
			raise Http404("Branch does not exist")

class AdminEmployeeNewView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/employee_new.html"

	def get(self, request, branch_id):
		try:
			branch = Branch.objects.get(id=branch_id)

			context = {
				'branch': branch,
			}

			return render(request, self.template_name, context)

		except Branch.DoesNotExist:
			raise Http404("Branch does not exist")

	def post(self, request, branch_id):

		name = request.POST['name']
		salary = request.POST['salary']
		phone = request.POST['phone']

		branch_obj = Branch.objects.get(id=int(branch_id))
		employee = Employee(name=name, salary=salary, phone=phone, branch=branch_obj)
		employee.save()

		if request.is_ajax():
			return JsonResponse({"success": True, "employee_name": employee.name})

class AdminEditEmployeeView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/employee_new.html"

	def get(self, request, branch_id, employee_id):
		try:
			employee = Employee.objects.get(id=employee_id)
			branch = Branch.objects.get(id=branch_id)

			context = {
				'employee': employee,
				'branch': branch,
			}

			return render(request, self.template_name, context)
		except Employee.DoesNotExist:
			raise Http404("Employee does not exist")

	def post(self, request, branch_id, employee_id):
		name = request.POST['name']
		salary = request.POST['salary']
		phone = request.POST['phone']

		branch_obj = Branch.objects.get(id=int(branch_id))
		employee_obj = Employee.objects.get(id=employee_id)
		employee_obj.name = name;
		employee_obj.salary = salary;
		employee_obj.phone = phone;
		employee_obj.save()

		print employee_obj.salary

		if request.is_ajax():
			return JsonResponse({"success": True, "employee_name": employee_obj.name})

class AdminStoreView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/store.html"

	def get(self, request, branch_id):
		try:
			branch = Branch.objects.get(id=branch_id)
			context = {
				'branch': branch,
			}

			return render(request, self.template_name, context)

		except Branch.DoesNotExist:
			raise Http404("Branch does not exist")

	def post(self, request, branch_id):
		name = request.POST['name']
		username = request.POST['username']
		password = request.POST['password']

		try:
			branch = Branch.objects.get(id=branch_id)
			storeadmin = StoreAdmin.objects.get(branch=branch)
			storeadmin.name = name
			storeadmin.save()
			user = User.objects.get(username=storeadmin.user.username)
			user.username = username
			user.set_password(password)
			user.save()

		except StoreAdmin.DoesNotExist:
			user = User.objects.create_user(username=username,
											password=password)
			storeadmin = StoreAdmin(name=name, user=user, branch=branch)
			storeadmin.save()

		if request.is_ajax():
			return JsonResponse({"success": True, "storeadmin_name": storeadmin.name})