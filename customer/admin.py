from django.contrib import admin
from .models import MegaMartUser, OrderSet, Order
# Register your models here.
class MegaMartUserAdmin(admin.ModelAdmin):
	list_display = ('name', 'phone', )

class OrderSetAdmin(admin.ModelAdmin):
	list_display = ('megamartuser', 'bill_amount', 'bill_date', 'branch',)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('product', 'quantity', 'total_amount', )

admin.site.register(MegaMartUser, MegaMartUserAdmin)
admin.site.register(OrderSet, OrderSetAdmin)
admin.site.register(Order, OrderAdmin)