from django.contrib import admin
from .models import Category, Product

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', )

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)