from django.db import models
from django.core.urlresolvers import reverse

from products.models import Product

class Cart(models.Model):
	id = models.AutoField(primary_key=True)
	products = models.ManyToManyField(Product)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<Cart: %d>" % (self.id)