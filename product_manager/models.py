from django.db import models

# Create your models here.
class Category(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

class Product(models.Model):
	name = models.CharField(max_length=150)
	price = models.FloatField()
	category = models.ForeignKey(Category)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = 'Products'