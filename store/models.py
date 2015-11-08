from django.db import models
from product_manager.models import Product
from admins.models import Branch

# Create your models here.
class ProductSet(models.Model):
	product = models.ForeignKey(Product)
	branch = models.ForeignKey(Branch)
	quantity = models.FloatField()
	expiry_date = models.DateField()
	min_quantity_retain = models.FloatField()

	def __str__(self):
		return "%s (x %s) - %s" % (self.product.name, str(self.quantity), self.branch.title)

	class Meta:
		verbose_name = 'Product Set'
		verbose_name_plural = 'Product Sets'

class Employee(models.Model):
	name = models.CharField(max_length=40)
	salary = models.PositiveIntegerField()
	phone = models.CharField(max_length=10, default='')
	branch = models.ForeignKey(Branch)

	def __str__(self):
		return "%s - %s" % (self.name, self.branch.title)

	class Meta:
		verbose_name = 'Employee'
		verbose_name_plural = 'Employees'