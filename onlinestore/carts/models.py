from decimal import Decimal 

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

	def get_total(self):
		two_places = Decimal(10) ** -2
		subtotal = sum([p.price for p in self.products.all()])
		withtax = Decimal(subtotal) * Decimal(1.08)
		total = withtax.quantize(two_places)
		return total