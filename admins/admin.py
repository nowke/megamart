from django.contrib import admin
from .models import City, Branch, StoreAdmin
from store.models import Employee

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1

class EmployeeInline(admin.StackedInline):
    model = Employee
    extra = 1

class StoreAdminInline(admin.StackedInline):
	model = StoreAdmin

# Register your models here.
class CityAdmin(admin.ModelAdmin):
	list_display = ('name', )
	inlines = [BranchInline]

class BranchAdmin(admin.ModelAdmin):
	list_display = ('title', 'city', 'address')
	list_filter = ['city']
	inlines = [StoreAdminInline, EmployeeInline]

class StoreAdminAdmin(admin.ModelAdmin):
	list_display = ('name', 'branch')
	list_filter = ['branch__city']

admin.site.register(City, CityAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(StoreAdmin, StoreAdminAdmin)