from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
from django.db import models

class Product(models.Model):
	slug = AutoSlugField(('slug'), max_length=60, unique=True, populate_from=('title',))
	title = models.CharField(max_length=50)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	sale_price = models.DecimalField(decimal_places=2, max_digits=100,\
												null=True, blank=True)
	active = models.BooleanField(default=True)
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

class VariationManager(models.Manager):
	def all(self):
		return super(VariationManager, self).filter(active=True)

	def sizes(self):
		return self.all().filter(category='size').filter(active=True)

	def colors(self):
		return self.all().filter(category='color').filter(active=True)

VAR_CATEGORIES = (
	('color', 'color'),
	('size', 'size'),
	)

class ProductVariation(models.Model):
	product = models.ForeignKey(Product)
	category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='color')
	title = models.CharField(max_length=120)
	image = models.ForeignKey(ProductImage, null=True, blank=True)
	price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)
	length = models.IntegerField(null=False)
	width = models.IntegerField(null=False)
	height = models.IntegerField(null=False)
	objects = VariationManager()

	def __str__(self):
		return self.title