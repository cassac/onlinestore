from django.db import models
from django.conf import settings

from carts.models import Cart
from accounts.models import UserMailingAddress, UserBillingAddress

STATUS_CHOICES = (
		("Processing", "Processing"),
		("Cancelled", "Cancelled"),
		("Shipped", "Shipped"),
		("Returned", "Returned"),
		("Completed", "Completed")		
	)

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	cart = models.ForeignKey(Cart)
	mailing_address = models.ForeignKey(UserMailingAddress)
	billing_address = models.ForeignKey(UserBillingAddress, blank=True, null=True)
	order_id = models.CharField(max_length=10)	
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Processing")
	subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True) 	

	def __str__(self):
		return "<Order: %s>" % (self.order_id)