from django.conf.urls import include, url

from .views import StoreHomeView, StoreCategoryView, StoreAddProductView, StoreBillView, StoreBillGenView

urlpatterns = [
	url(r'^home/$', StoreHomeView.as_view(), name='home'),
	url(r'^home/add_product$', StoreAddProductView.as_view(), name='add_product'),
	url(r'^home/category/(?P<category_id>[0-9]+)$', StoreCategoryView.as_view(), name='category'),
	url(r'^home/bill$', StoreBillView.as_view(), name='bill'),
	url(r'^home/bill/(?P<order_set_id>[0-9]+)$', StoreBillGenView.as_view(), name='billView'),
]