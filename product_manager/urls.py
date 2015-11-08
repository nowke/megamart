from django.conf.urls import include, url

from .views import PmHomeView, PmAddCategoryView, PmCategoryView, PmNewProductView

urlpatterns = [
	url(r'^home/$', PmHomeView.as_view(), name='home'),
	url(r'^home/add_category$', PmAddCategoryView.as_view(), name='add_category'),
	url(r'^home/category/(?P<category_id>[0-9]+)$', PmCategoryView.as_view(), name='category'),
	url(r'^home/category/(?P<category_id>[0-9]+)/new$', PmNewProductView.as_view(), name='add_product'),
]