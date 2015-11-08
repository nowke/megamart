from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse_lazy

from .models import ProductManager

login_link = reverse_lazy('login')

class PmRequiredMixin(object):

	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(PmRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view, login_url=login_link)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		try:
			product_manager = ProductManager(user=request.user)
			return super(PmRequiredMixin, self).dispatch(request, *args, **kwargs)
		except ProductManager.DoesNotExist:
			raise Http404