from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse_lazy

from .models import MegaMartUser

login_link = reverse_lazy('login')

class CustomerRequiredMixin(object):

	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(CustomerRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view, login_url=login_link)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		try:
			customer = MegaMartUser.objects.get(user=request.user)
			return super(CustomerRequiredMixin, self).dispatch(request, *args, **kwargs)
		except MegaMartUser.DoesNotExist:
			raise Http404