from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import LoginPageView, HomePageView, RegisterPageView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^login$', LoginPageView.as_view(), name='login'),
    url(r'^register$', RegisterPageView.as_view(), name='register'),

    url(r'^dashboard/', include('customer.urls', namespace='customer')),
    url(r'^mainadmin/', include('admins.urls', namespace='mainadmin')),
    url(r'^manage_product/', include('product_manager.urls', namespace='product_manager')),
    url(r'^store/', include('store.urls', namespace='store')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^explorer/', include('explorer.urls')),
    # url(r'^silk/', include('silk.urls', namespace='silk')),
)
