from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
from django.db import models

class Product(models.Model):
	slug = AutoSlugField(('slug'), max_length=60, unique=True, populate_from=('title',))
	title = models.CharField(max_length=50)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='products/images/')
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return "<Image: %d - %s>" % (self.id, self.product.title)