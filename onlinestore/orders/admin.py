from django.contrib import admin

from .models import Order

class OrderAdmin(admin.ModelAdmin):
	exclude = ['created', 'subtotal', 'total']
	search_fields = ['id']
	list_display = ['id', 'subtotal', 'total']
	class Meta:
		model = Order

admin.site.register(Order, OrderAdmin)
