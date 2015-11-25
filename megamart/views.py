from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Q, F
from django.utils import timezone
from django.db.models import Count, Min, Sum, Avg
from django.utils.timezone import localtime, now

from datetime import time
import datetime
import psutil
import string
import re

from .mixins import AdminRequiredMixin
from admins.models import City, Branch, StoreAdmin
from store.models import Employee, ProductSet
from product_manager.models import ProductManager, Product
from customer.models import MegaMartUser, OrderSet, Order

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

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
					pass

				try:
					store_admin = StoreAdmin.objects.get(user=user)
					login(request, user)
					return redirect('store:home')
				except StoreAdmin.DoesNotExist:
					pass
					
				try:
					customer = MegaMartUser.objects.get(user=user)
					login(request, user)
					return redirect('customer:home')
				except MegaMartUser.DoesNotExist:
					return render(request, self.template_name, {"loginError": True})
		else:
			return render(request, self.template_name, {"loginError": True})

class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('home')


class RegisterPageView(TemplateView):
	template_name = "megamart/register.html"

	def post(self, request):

		if request.is_ajax():
			uname = request.POST['uname']
			try:
				User.objects.get(username=uname)
				return JsonResponse({"success": False})
			except User.DoesNotExist:
				return JsonResponse({"success": True})

		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		full_name = request.POST['full_name']
		phone = request.POST['phone']

		# password = ''.join(['$' for x in range(password.count('$'))])
		# print password	

		# special_chars =  string.punctuation
		# k = ''
		# for i in password:
		# 	if i in special_chars:
		# 		k += i
		# password = k

		if not username or not EMAIL_REGEX.match(email) or not password or not full_name or not phone:
			return redirect('register')
		first_name = full_name.split()[0]
		last_name = full_name.split()[1]
		try:
			user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
			user.save()
		except:
			return redirect('register')

		customer = MegaMartUser(user=user, name=full_name, phone=phone, email=email)
		customer.save()
		logout(request)
		return redirect('login')

class QueryView(View):
	def get(self, request):

		# All Customers who ordered Product(68) more than 3 quantities
		# all_orders = Order.objects.filter(Q(product__id=68), Q(quantity__gte=3)).values('order_set')
		# all_cust = MegaMartUser.objects.filter(orderset__in=all_orders)
		# print all_cust

		# Branches having more than 2 customers ordered more than 100
		# all_branches = OrderSet.objects.filter(bill_amount__gte=100).values("megamartuser").distinct().values("branch").annotate(n=Count("megamartuser", distinct=True)).filter(n__gte=2)
		# print all_branches

		# all_emps = Employee.objects.filter(Q(branch__title="J P Nagar") | Q(branch__title="KORAMANGALA"), Q(salary__gte=20000), Q(salary__lte=30000)).values("name", "salary", "branch__title")
		# print all_emps

		# t = OrderSet.objects.filter(branch__title="KORAMANGALA").aggregate(bill=Sum("bill_amount"))
		# print t

		# all_branches = Branch.objects.all()
		# l = OrderSet.objects.filter(branch__in=all_branches).values("branch").distinct().annotate(s=Sum("bill_amount")).values("branch__title", "s")
		# print l

		# PASSWORD
		
		# from django.contrib.auth.hashers import PBKDF2PasswordHasher
		# salt = '6t8NwyMTnpPi'
		# iter = 20000
		# a = PBKDF2PasswordHasher()
		# encoded_str = a.encode(password='robin', salt=salt, iterations=iter)
		# a.verify('robin', encoded_str) # True

		pass



# DB Admin specific views
class AdminHomeView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/home.html"

	def get(self, request):
		if request.is_ajax() and request.GET.get('cpu', None):
			cpu_percentage =  psutil.cpu_percent(interval=1)

			data = {
				'cpu': cpu_percentage,
			}
			return JsonResponse(data)

		if request.is_ajax() and request.GET.get('getBranches', None):
			city_id = int(request.GET['city_id'])
			all_branches = Branch.objects.filter(city__id=city_id)
			branches = []
			for branch in all_branches:
				b_dict = {
					'id': int(branch.id),
					'name': str(branch.title),
				}
				branches.append(b_dict)
			return JsonResponse(branches, safe=False)

		if request.is_ajax() and request.GET.get('getBranchSales', None):
			branch_id = int(request.GET['branch_id'])

			
			return JsonResponse(data, safe=False)

		today = timezone.now().date()
		today_start = timezone.datetime.combine(today, time())
		cpu_percentage =  psutil.cpu_percent(interval=1)

		unique_orders = OrderSet.objects.filter(~Q(megamartuser__user__username='anonymous')).count()
		no_of_users = MegaMartUser.objects.count()
		today_users = MegaMartUser.objects.filter(user__date_joined__gte=today_start).count()

		all_cities = City.objects.all()

		context = {
			'total_users': no_of_users,
			'today_users': today_users,
			'unique_orders': unique_orders,
			'cpu_percentage': cpu_percentage,
			'cities': all_cities,
		}
		return render(request, self.template_name, context)

	def post(self, request):
		branch_id = int(request.POST['branch'])

		today = localtime(timezone.now())
		week_dates = [today - timezone.timedelta(days=i) for i in range(7)]
		data = []
		for day in week_dates[::-1]:
			sale_sum = OrderSet.objects.filter(branch__id=branch_id, bill_date__startswith=day.date()).aggregate(bill=Sum("bill_amount"))
			data_dict = {
				'day': str(day.day) + " " + day.strftime("%a"),
				'sales': sale_sum["bill"] or 0,
			}
			data.append(data_dict)
		all_cities = City.objects.all()
		cur_branch = Branch.objects.get(id=branch_id)

		all_branches_city = Branch.objects.filter(city=cur_branch.city)

		today = timezone.now().date()
		today_start = timezone.datetime.combine(today, time())
		cpu_percentage =  psutil.cpu_percent(interval=1)

		unique_orders = OrderSet.objects.filter(~Q(megamartuser__user__username='anonymous')).count()
		no_of_users = MegaMartUser.objects.count()
		today_users = MegaMartUser.objects.filter(user__date_joined__gte=today_start).count()


		context = {
			'branchData': data,
			'branch': cur_branch,
			'cities': all_cities,
			'all_branches_city': all_branches_city,
			'total_users': no_of_users,
			'today_users': today_users,
			'unique_orders': unique_orders,
			'cpu_percentage': cpu_percentage,
		}
		return render(request, self.template_name, context)


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
			user.is_staff=True
			store_admin_group = Group.objects.get(name='store_admin')
			user.groups.add(store_admin_group)
			user.save()

			storeadmin = StoreAdmin(name=name, user=user, branch=branch)
			storeadmin.save()

		if request.is_ajax():
			return JsonResponse({"success": True, "storeadmin_name": storeadmin.name})

class AdminDeleteEmployeeView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/employee_delete.html"

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

		employee = Employee.objects.get(id=employee_id)
		employee.delete()

		if request.is_ajax():
			return JsonResponse({"success": True})

class AdminStoreDeleteView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/store_admin_delete.html"

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
		try:
			branch = Branch.objects.get(id=branch_id)
			store_admin = StoreAdmin.objects.get(branch=branch)
			store_admin.delete()

			if request.is_ajax():
				return JsonResponse({"success": True})
		except Branch.DoesNotExist:
			raise Http404("Branch does not exist")

class AdminReportView(AdminRequiredMixin, TemplateView):
	template_name = "megamart/admin/report.html"

	def get(self, request):
		all_branches = Branch.objects.all()
		k = OrderSet.objects.filter(branch__in=all_branches).values("branch").distinct().annotate(s=Sum("bill_amount")).values("branch__title", "branch__city__name", "s")
		print k
		context = {
			'report': k,
		}

		return render(request, self.template_name, context)