from django.contrib import admin
from .models import City, Branch, StoreAdmin

# Register your models here.
class CityAdmin(admin.ModelAdmin):
	list_display = ('name', )

class BranchAdmin(admin.ModelAdmin):
	list_display = ('title',)

class StoreAdminAdmin(admin.ModelAdmin):
	list_display = ('name', )

admin.site.register(City, CityAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(StoreAdmin, StoreAdminAdmin)