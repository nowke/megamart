from django.views.generic.base import TemplateView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from .mixins import CustomerRequiredMixin
from .models import MegaMartUser, OrderSet, Order

def getUser(user):
	customer = MegaMartUser.objects.get(user=user)
	return customer

class CustomerHomeView(CustomerRequiredMixin, TemplateView):
	template_name = "customer/home.html"

	def get(self, request):
		customer = getUser(request.user)
		context = {
			'customer': customer,
		}
		return render(request, self.template_name, context)

class CustomerOrderView(CustomerRequiredMixin, TemplateView):
	template_name = "customer/order.html"

	def get(self, request, order_set_id):
		order_set_obj = OrderSet.objects.get(id=order_set_id)
		context = {
			'order_set': order_set_obj,
		}
		return render(request, self.template_name, context)