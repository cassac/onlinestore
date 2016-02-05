from django.contrib import admin

from .models import UserBillingAddress, UserMailingAddress, UserStripe


class UserBillingAddressAdmin(admin.ModelAdmin):
	search_fields = ['first_name', 'last_name']
	list_display = ['user', 'first_name', 'last_name', 'address1', 'state']	
	class Meta:
		model = UserBillingAddress

admin.site.register(UserBillingAddress, UserBillingAddressAdmin)

class UserMailingAddressAdmin(admin.ModelAdmin):
	search_fields = ['first_name', 'last_name']
	list_display = ['user', 'first_name', 'last_name', 'address1', 'state']		
	class Meta:
		model = UserMailingAddress

admin.site.register(UserMailingAddress, UserMailingAddressAdmin)

class UserStripeAdmin(admin.ModelAdmin):
	
	class Meta:
		model = UserStripe

admin.site.register(UserStripe, UserStripeAdmin)