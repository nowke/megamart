from django.views.generic.base import TemplateView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.db.models import F

from collections import Counter

from .mixins import StoreAdminRequiredMixin
from .models import City, Branch, StoreAdmin
from store.models import ProductSet
from product_manager.models import Product, Category
from customer.models import MegaMartUser, OrderSet, Order

def getBranch(user):
	store_admin = StoreAdmin.objects.get(user=user)
	return store_admin.branch

class StoreHomeView(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/home.html"

	def get(self, request):
		branch = getBranch(request.user)

		all_product_cat = ProductSet.objects.filter(branch=branch).values('product__category')
		cat_unique = Counter([v['product__category'] for v in all_product_cat])
		categories = []

		for cat in cat_unique:
			cat_obj = Category.objects.get(id=cat)
			count = cat_unique[cat]
			categories.append({'cat': cat_obj, 'count': count})

		context = {
			'categories_stock': categories,
		}

		return render(request, self.template_name, context)

class StoreCategoryView(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/category.html"

	def get(self, request, category_id):
		branch = getBranch(request.user)
		category = Category.objects.get(id=category_id)

		all_products = ProductSet.objects.filter(branch=branch, product__category=category)

		context = {
			'category': category,
			'products': all_products,
		}

		return render(request, self.template_name, context)

class StoreAddProductView(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/add_product.html"

	def get(self, request):
		all_categories = Category.objects.all()

		context = {
			'categories': all_categories,
		}

		return render(request, self.template_name, context)

	def post(self, request):
		if "getCat" in request.POST:
			all_products_cat = Product.objects.filter(category__id=request.POST["cat_id"])
			products = []
			for product in all_products_cat:
				prod_dict = {
					'id': product.id,
					'title': product.name,
				}
				products.append(prod_dict)
			if request.is_ajax():	
				return JsonResponse(products, safe=False)

		else:
			category = Category.objects.get(id=request.POST['category'])
			product = Product.objects.get(id=request.POST['product'])
			min_quantity = request.POST['min_quantity']
			quantity = request.POST['quantity']
			expiry_date = request.POST['expiry_date']

			product_set_obj = ProductSet(
								product=product,
								branch=getBranch(request.user),
								quantity=float(quantity),
								expiry_date=expiry_date,
								min_quantity_retain=float(min_quantity),
							  )
			product_set_obj.save()

			if request.is_ajax():
				return JsonResponse({"success": True, "product_name": product.name})

class StoreBillView(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/bill.html"

	def get(self, request):
		branch = getBranch(request.user)
		context = {
			'branch': branch,
		}
		return render(request, self.template_name, context)

	@transaction.atomic
	def post(self, request):
		if "findUser" in request.POST:
			username = request.POST['username']
			try:
				mega_user = MegaMartUser.objects.get(user__username=username)
				context = {
					"username": mega_user.user.username,
					"name": mega_user.name,
					"phone": mega_user.phone,
					"email": mega_user.email,
				}
				return JsonResponse(context)
			except MegaMartUser.DoesNotExist:
				return JsonResponse({"userSuccess": False})

		elif "getProdDetail" in request.POST:
			product_id = request.POST["product_id"]
			try:
				product = Product.objects.get(id=product_id)
				context = {
					"name": product.name,
					"price": product.price,
				}
				return JsonResponse(context)
			except Product.DoesNotExist:
				return JsonResponse({"prodSuccess": False})
		else:
			username = request.POST['custname']
			try:
				mega_user = MegaMartUser.objects.get(user__username=username)
			except MegaMartUser.DoesNotExist:
				mega_user = MegaMartUser.objects.get(user__username='anonymous')

			if 'anonymous' in request.POST:
				mega_user = MegaMartUser.objects.get(user__username='anonymous')				
			
			product_ids = request.POST.getlist('product_id')
			product_quantities = request.POST.getlist('product_quantity')
			branch = getBranch(request.user)

			total_products = len(product_ids)

			with transaction.atomic():
				order_set = OrderSet(megamartuser=mega_user, branch=branch)
				order_set.save()

				bill_amount = 0

				for i in range(total_products):
					product = Product.objects.get(id=product_ids[i])
					quantity = float(product_quantities[i])
					total_amount = product.price * quantity * 1.0

					order_obj = Order(
									order_set=order_set,
									product=product,
									quantity=quantity,
									total_amount=total_amount,
							 	)

					bill_amount += total_amount
					order_obj.save()
					
					try:
						product_set_branch = ProductSet.objects.filter(product=product, branch=branch)[0]
						product_set_branch.quantity -= quantity
						if product_set_branch.quantity < 0:
							product_set_branch.quantity = 0
						product_set_branch.save()
					except IndexError:
						pass

				order_set.bill_amount = bill_amount
				order_set.save()



			return redirect("store:billView", order_set.id)

class StoreBillGenView(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/bill_view.html"

	def get(self, request, order_set_id):
		try:
			order_set_obj = OrderSet.objects.get(id=order_set_id)
			context = {
				"order_set": order_set_obj
			}
			return render(request, self.template_name, context)
		except OrderSet.DoesNotExist:
			pass

class StoreExpiredView(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/expired.html"

	def get(self, request):
		branch = getBranch(request.user)
		now = timezone.now()
		expired_product_set = ProductSet.objects.filter(branch=branch, expiry_date__lte=now)
		context = {
			'branch': branch,
			'expired': expired_product_set,
		}

		return render(request, self.template_name, context)

class StoreOutOfStock(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/out.html"

	def get(self, request):
		branch = getBranch(request.user)
		out_of_stock = ProductSet.objects.filter(branch=branch, quantity__lte=F('min_quantity_retain'))

		context = {
			'branch': branch,
			'out_of_stock': out_of_stock,
		}
		return render(request, self.template_name, context)

class StoreViewBills(StoreAdminRequiredMixin, TemplateView):
	template_name = "store/view_bills.html"

	def post(self, request):
		bill_id = request.POST['bill_id']
		
		try:
			order_set = OrderSet.objects.get(id=bill_id)
			return redirect('store:billView', bill_id)
		except OrderSet.DoesNotExist:
			return render(request, self.template_name)