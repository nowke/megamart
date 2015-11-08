from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'City'
		verbose_name_plural = 'Cities'

class Branch(models.Model):
	title = models.CharField(max_length=100)
	city = models.ForeignKey(City)
	address = models.TextField(max_length=256, default='')

	def __str__(self):
		return "%s, %s" % (self.title, self.city.name)

	class Meta:
		verbose_name = 'Branch'
		verbose_name_plural = 'Branches'

class StoreAdmin(models.Model):
	user = models.OneToOneField(User, unique=True)
	name = models.CharField(max_length=40)
	branch = models.OneToOneField(Branch)

	def __str__(self):
		return "%s - %s" % (self.name, self.branch.title)

	class Meta:
		verbose_name = 'Store Administrator'
		verbose_name_plural = 'Store Administrators'