from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import LoginPageView, HomePageView, RegisterPageView, QueryView, AdminReportView
from .views import AdminHomeView, LogoutView, AdminBranchesView, AdminAddBranchView, AdminBranchDetailView
from .views import AdminEmployeeNewView, AdminEditEmployeeView, AdminStoreView, AdminDeleteEmployeeView, AdminStoreDeleteView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^login$', LoginPageView.as_view(), name='login'),
    url(r'^register$', RegisterPageView.as_view(), name='register'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    url(r'^q$', QueryView.as_view(), name='query'),

    # DB Admin views
    url(r'^administrator/home$', AdminHomeView.as_view(), name='admin_home'),
    url(r'^administrator/report$', AdminReportView.as_view(), name='report'),
    url(r'^administrator/branches$', AdminBranchesView.as_view(), name='admin_branches'),
    url(r'^administrator/branches/new$', AdminAddBranchView.as_view(), name='admin_add_branch'),
    url(r'^administrator/branches/(?P<branch_id>[0-9]+)$', AdminBranchDetailView.as_view(), name='admin_branch_detail'),

    url(r'^administrator/branches/(?P<branch_id>[0-9]+)/employees/new$', AdminEmployeeNewView.as_view(), name='admin_emp_new'),
    url(r'^administrator/branches/(?P<branch_id>[0-9]+)/employees/(?P<employee_id>[0-9]+)$', AdminEditEmployeeView.as_view(), name='admin_emp_edit'),
    url(r'^administrator/branches/(?P<branch_id>[0-9]+)/employees/(?P<employee_id>[0-9]+)/delete$', AdminDeleteEmployeeView.as_view(), name='admin_emp_delete'),

    url(r'^administrator/branches/(?P<branch_id>[0-9]+)/admin$', AdminStoreView.as_view(), name='admin_store_new'),
    url(r'^administrator/branches/(?P<branch_id>[0-9]+)/admin/delete$', AdminStoreDeleteView.as_view(), name='admin_store_delete'),

    url(r'^dashboard/', include('customer.urls', namespace='customer')),
    url(r'^manage_product/', include('product_manager.urls', namespace='product_manager')),
    url(r'^store/', include('admins.urls', namespace='store')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^silk/', include('silk.urls', namespace='silk')),
)