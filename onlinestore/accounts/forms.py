from django import forms
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

class UserRegistrationForm(forms.Form):	
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
	password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))