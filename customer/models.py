from django.db import models
from django.contrib.auth.models import User

from admins.models import Branch
from product_manager.models import Product

# Create your models here.
class MegaMartUser(models.Model):
	user = models.OneToOneField(User, unique=True)
	name = models.CharField(max_length=40)
	phone = models.BigIntegerField()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'MegaMart Customer'
		verbose_name_plural = 'MegaMart Customers'

class OrderSet(models.Model):
	megamartuser = models.ForeignKey(MegaMartUser)
	bill_amount = models.FloatField()
	bill_date = models.DateTimeField()
	branch = models.ForeignKey(Branch)

	def __str__(self):
		return "%s - %s on %s" % (self.megamartuser, self.branch, self.bill_date)

	class Meta:
		verbose_name = 'Order Set'
		verbose_name_plural = 'Order sets'

class Order(models.Model):
	order_set = models.ForeignKey(OrderSet)
	product = models.ForeignKey(Product)
	quantity = models.FloatField()
	total_amount = models.FloatField()

	def __str__(self):
		return "%s by %s on %s" % (self.product, self.order_set.megamartuser, self.order_set.bill_date)

	def save(self, *args, **kwargs):
		self.total_amount = self.product.price * self.quantity
		super(Order, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Order'
		verbose_name_plural = 'Orders'