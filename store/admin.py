from django.contrib import admin
from .models import ProductSet, Employee

# Register your models here.
class ProductSetAdmin(admin.ModelAdmin):
	list_display = ('product', 'quantity',)

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('name', 'salary', 'branch')

admin.site.register(ProductSet, ProductSetAdmin)
admin.site.register(Employee, EmployeeAdmin)