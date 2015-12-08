from django.contrib import admin

from .models import Product, ProductImage

class ProductAdmin(admin.ModelAdmin):
	exclude = ("slug",)
	search_fields = ['title', 'description']
	list_display = ['title', 'price', 'updated']
	list_editable = ['price']
	list_filter = ['price']
	readonly_fields = ['updated']
	prepopulated_fields = {"slug": ("title",)}
	class Meta:
		model = Product

class ProductImageAdmin(admin.ModelAdmin):
	list_display = ['product', 'image', 'active', 'updated']
	list_editable = ['active']
	search_fields = ['image']
	class Meta:
		model = ProductImage

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
