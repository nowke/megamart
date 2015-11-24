from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from .models import ProductSet, Employee

# Register your models here.
class ProductSetAdmin(admin.ModelAdmin):
	list_display = ('prod_id', 'product', 'quantity', 'expiry_date')
	list_filter = [('expiry_date', DateRangeFilter), 'branch', 'branch__city',]

	def prod_id(self, obj):
		return obj.product_id
	prod_id.short_description = 'Id'

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('name', 'salary', 'branch')
	list_filter = ['branch__city', 'branch']
	list_display_links = ('name',)
	list_select_related = ('branch',)

admin.site.register(ProductSet, ProductSetAdmin)
admin.site.register(Employee, EmployeeAdmin)