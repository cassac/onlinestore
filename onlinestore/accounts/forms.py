from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import UserBillingAddress, UserMailingAddress

User = get_user_model()

class UserBillingAddressForm(ModelForm):
	class Meta:
		model = UserBillingAddress
		fields = ['first_name', 'last_name', 'address1', 'address2', 'city',
				'state', 'zipcode', 'phone']		

class UserMailingAddressForm(ModelForm):
	class Meta:
		model = UserMailingAddress
		fields = ['use_billing_address', 'first_name', 'last_name','address1',
				'address2', 'city', 'state', 'zipcode', 'phone']

class UserAccountInfoForm(ModelForm):
	class Meta:
		model = User
		fields = ['email', 'username', 'first_name', 'last_name']				