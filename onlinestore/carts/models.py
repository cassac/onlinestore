from decimal import Decimal 

from django.db import models
from django.core.urlresolvers import reverse

from products.models import Product, ProductVariation

class CartItem(models.Model):
	cart = models.ForeignKey('Cart', null=True, blank=True)
	product = models.ForeignKey(Product)
	variation = models.ManyToManyField(ProductVariation,blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<CartItem: %s>" % (self.product.title)

class Cart(models.Model):
	id = models.AutoField(primary_key=True)
	# products = models.ManyToManyField(Product)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<Cart: %d>" % (self.id)

	def get_subtotal(self):
		return Decimal(sum([p.price for p in self.products.all()]))

	def get_tax(self):
		two_places = Decimal(10) ** -2
		tax = self.get_subtotal() * Decimal(0.08)
		return tax.quantize(two_places)

	def get_total(self):
		two_places = Decimal(10) ** -2
		total = self.get_subtotal() + self.get_tax()
		return total.quantize(two_places)