from django.db import models
from django.conf import settings

from carts.models import Cart
        

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	cart = models.ForeignKey(Cart)
	subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True) 	

	def __str__(self):
		return "<Order: %d>" % (self.id)
		
