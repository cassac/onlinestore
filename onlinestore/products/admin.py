from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
	exclude = ("slug",)
	list_display = ['title', 'description', 'created']
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)