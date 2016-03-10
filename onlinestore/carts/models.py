from decimal import Decimal 

from django.db import models
from django.core.urlresolvers import reverse

from products.models import Product, ProductVariation

class CartItem(models.Model):
	cart = models.ForeignKey('Cart', null=True, blank=True)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(blank=False)
	variation = models.ManyToManyField(ProductVariation,blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<CartItem: %s>" % (self.product.title)

	def total_price(self):
		return self.quantity * self.product.price

	def color(self):
	# Display color variation
		return ', '.join([v.title for v in self.variation.filter(category='color').all()])

	def size(self):
	# Display size variation
		return ', '.join([v.title for v in self.variation.filter(category='size').all()])

class Cart(models.Model):
	id = models.AutoField(primary_key=True)
	shipping_rate = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
	shipping_rate_id = models.CharField(null=True, blank=True, max_length=200)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<Cart: %d>" % (self.id)

	def get_subtotal(self):
		return Decimal(sum([cart_item.total_price() for cart_item in self.cartitem_set.all()]))

	def get_tax(self):
		two_places = Decimal(10) ** -2
		tax = self.get_subtotal() * Decimal(0.08)
		return tax.quantize(two_places)

	def get_total(self):
		two_places = Decimal(10) ** -2
		total = self.get_subtotal() + self.get_tax()
		return total.quantize(two_places)

	def has_calculated_shipping(self):
		if not self.shipping_rate:
			return False
		return True