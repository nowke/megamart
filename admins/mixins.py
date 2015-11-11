from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse_lazy

from .models import StoreAdmin

login_link = reverse_lazy('login')

class StoreAdminRequiredMixin(object):

	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(StoreAdminRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view, login_url=login_link)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		try:
			store_admin = StoreAdmin.objects.get(user=request.user)
			return super(StoreAdminRequiredMixin, self).dispatch(request, *args, **kwargs)
		except StoreAdmin.DoesNotExist:
			raise Http404