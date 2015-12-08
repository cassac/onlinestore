from django.contrib import admin

from .models import UserBillingAddress, UserMailingAddress


class UserBillingAddressAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['user', 'name', 'address1', 'state']	
	class Meta:
		model = UserBillingAddress

admin.site.register(UserBillingAddress, UserBillingAddressAdmin)

class UserMailingAddressAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['user', 'name', 'address1', 'state']	
	class Meta:
		model = UserMailingAddress

admin.site.register(UserMailingAddress, UserMailingAddressAdmin)