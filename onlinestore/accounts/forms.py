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
		labels = {'first_name': '名字', 'last_name': '姓氏', 'address1': '地址第一行', 'address2': '地址第二行',
				 'city': '城市', 'state': '省份', 'zipcode': '邮编', 'phone': '电话'}
		fields = ['first_name', 'last_name','address1',
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