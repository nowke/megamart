from django.contrib import admin
from .models import MegaMartUser, OrderSet, Order

class OrderSetInline(admin.TabularInline):
    model = OrderSet
    extra = 0

class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    raw_id_fields = ('product',)
    exclude = ('total_amount', )

# Register your models here.
class MegaMartUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', )
    inlines = [OrderSetInline]

class OrderSetAdmin(admin.ModelAdmin):
    list_display = ('megamartuser', 'bill_amount', 'bill_date', 'branch',)
    inlines = [OrderInline]

    def save_model(self, request, obj, form, change):
        obj.save()
        bill = 0
        for order in obj.order_set.all():
            bill += order.total_amount
        obj.bill_amount = bill
        obj.save()

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_amount', )
    exclude = ('total_amount',)

admin.site.register(MegaMartUser, MegaMartUserAdmin)
admin.site.register(OrderSet, OrderSetAdmin)
admin.site.register(Order, OrderAdmin)