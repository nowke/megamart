from django.views.generic.base import TemplateView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User

from .mixins import PmRequiredMixin
from .models import Category, Product

class PmHomeView(PmRequiredMixin, TemplateView):
	template_name = "product_manager/home.html"

	def get(self, request):
		categories = Category.objects.all()

		context = {
			'categories': categories,
		}
		return render(request, self.template_name, context)

class PmAddCategoryView(PmRequiredMixin, TemplateView):
	template_name = "product_manager/add_category.html"

	def post(self, request):
		title = request.POST['title']

		category_obj = Category(title=title)
		category_obj.save()

		if request.is_ajax():
			return JsonResponse({"success": True, "category_title": category_obj.title})

class PmCategoryView(PmRequiredMixin, TemplateView):
	template_name = "product_manager/category.html"

	def get(self, request, category_id):
		category_obj = Category.objects.get(id=category_id)

		context = {
			'category': category_obj,
		}

		return render(request, self.template_name, context)

class PmNewProductView(PmRequiredMixin, TemplateView):
	template_name = "product_manager/new_product.html"

	def get(self, request, category_id):
		category_obj = Category.objects.get(id=category_id)

		context = {
			'category': category_obj,
		}

		return render(request, self.template_name, context)

	def post(self, request, category_id):
		title = request.POST['title']
		price = request.POST['price']

		category_obj = Category.objects.get(id=category_id)
		product = Product(name=title, price=float(price), category=category_obj)
		product.save()

		if request.is_ajax():
			return JsonResponse({"success": True, "product_title": product.name})

class PmEditProductView(PmRequiredMixin, TemplateView):
	template_name = "product_manager/new_product.html"

	def get(self, request, product_id):
		product = Product.objects.get(id=product_id)

		context = {
			'product': product,
		}
		return render(request, self.template_name, context)

	def post(self, request, product_id):
		product = Product.objects.get(id=product_id)
		product.name = request.POST['title']
		product.price = float(request.POST['price'])
		product.save()

		if request.is_ajax():
			return JsonResponse({"success": True, "product_title": product.name})

class PmDeleteProductView(PmRequiredMixin, TemplateView):
	template_name = "product_manager/delete_product.html"

	def get(self, request, product_id):
		product = Product.objects.get(id=product_id)

		context = {
			'product': product,
		}
		return render(request, self.template_name, context)

	def post(self, request, product_id):
		product = Product.objects.get(id=product_id)
		product.delete()

		if request.is_ajax():
			return JsonResponse({"success": True})