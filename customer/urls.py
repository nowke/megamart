from django.conf.urls import include, url

from .views import CustomerHomeView, CustomerOrderView

urlpatterns = [
	url(r'^home/$', CustomerHomeView.as_view(), name='home'),
	url(r'^home/(?P<order_set_id>[0-9]+)$', CustomerOrderView.as_view(), name='order'),
]