from django.contrib import admin

from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):

	class Meta:
		model = Cart

admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
	list_display = ['product','cart_id', 'color', 'size']
	filter_horizontal = ('variation',)
	class Meta:
		model = CartItem

admin.site.register(CartItem, CartItemAdmin)