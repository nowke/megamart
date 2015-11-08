from django.contrib import admin
from .models import Category, Product, ProductManager

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', )

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', )

class ProductManagerAdmin(admin.ModelAdmin):
	list_display = ('name', )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductManager, ProductManagerAdmin)