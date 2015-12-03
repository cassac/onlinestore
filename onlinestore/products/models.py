from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
from django.db import models

class Product(models.Model):
	slug = AutoSlugField(('slug'), max_length=60, unique=True, populate_from=('title',))
	title = models.CharField(max_length=50)
	description = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title