from django.db import models
from django.conf import settings

from localflavor.cn.cn_provinces import CN_PROVINCE_CHOICES
# from localflavor.us.us_states import US_STATES

class UserBillingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address1 = models.CharField(max_length=200)
	address2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50, choices=CN_PROVINCE_CHOICES)
	zipcode = models.CharField(max_length=20)
	phone = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<UserBillingAddress: %d - %s>" % (self.user.id, self.user.username)

class UserMailingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	use_billing_address = models.BooleanField(default=False)
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	address1 = models.CharField(max_length=200, null=True, blank=True)
	address2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	state = models.CharField(max_length=50, choices=CN_PROVINCE_CHOICES, blank=True)
	zipcode = models.CharField(max_length=20, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<UserMailingAddress: %d - %s>" % (self.user.id, self.user.username)

	def is_complete(self):
		if not self.first_name or not self.last_name or not self.address1 or not self.city\
			or not self.state or not self.zipcode or not self.phone:
			return False
		return True

class UserStripe(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	stripe_id = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return "User: %d" & (self.user.email)

