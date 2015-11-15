from django.contrib import admin
from .models import Category, Product, ProductManager
from store.models import ProductSet

# Register your models here.
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class ProductSetInline(admin.TabularInline):
    model = ProductSet
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', )
	inlines = [ProductInline]

class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'price', )
	list_filter = ['category']
	inlines = [ProductSetInline]
	search_fields = ['name']

class ProductManagerAdmin(admin.ModelAdmin):
	list_display = ('name', )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductManager, ProductManagerAdmin)