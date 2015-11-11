from django.views.generic.base import TemplateView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User

from collections import Counter

from .mixins import StoreAdminRequiredMixin
from .models import City, Branch, StoreAdmin
from store.models import ProductSet
from product_manager.models import Product, Category

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
