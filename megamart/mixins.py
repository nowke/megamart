from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse_lazy

login_link = reverse_lazy('login')

class AdminRequiredMixin(object):

	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(AdminRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view, login_url=login_link)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_staff:
			return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404