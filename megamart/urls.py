from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import LoginPageView, HomePageView, RegisterPageView
from .views import AdminHomeView, LogoutView, AdminBranchesView, AdminAddBranchView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^login$', LoginPageView.as_view(), name='login'),
    url(r'^register$', RegisterPageView.as_view(), name='register'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    # DB Admin views
    url(r'^administrator/home$', AdminHomeView.as_view(), name='admin_home'),
    url(r'^administrator/branches$', AdminBranchesView.as_view(), name='admin_branches'),
    url(r'^administrator/branches/new$', AdminAddBranchView.as_view(), name='admin_add_branch'),

    url(r'^dashboard/', include('customer.urls', namespace='customer')),
    url(r'^manage_product/', include('product_manager.urls', namespace='product_manager')),
    url(r'^store/', include('store.urls', namespace='store')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^explorer/', include('explorer.urls')),
    # url(r'^silk/', include('silk.urls', namespace='silk')),
)