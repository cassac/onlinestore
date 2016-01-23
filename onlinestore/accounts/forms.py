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
		labels = {'first_name': '名字', 'last_name': '姓氏', 'email': '邮箱地址', 'username': '用户名'}
		fields = ['email', 'username', 'first_name', 'last_name']

error_messages={'required': '必填'}

class UserRegistrationForm(forms.Form):	
	username = forms.CharField(error_messages=error_messages, widget=forms.TextInput(attrs={'placeholder': '用户名', 'class': 'form-control'}))
	email = forms.CharField(error_messages=error_messages, widget=forms.EmailInput(attrs={'placeholder': '邮箱地址', 'class': 'form-control'}))
	password = forms.CharField(error_messages=error_messages, widget=forms.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control'}))
	password_confirm = forms.CharField(error_messages=error_messages, widget=forms.PasswordInput(attrs={'placeholder': '再次输入密码', 'class': 'form-control'}))

class UserLoginForm(forms.Form):	
	username = forms.CharField(error_messages=error_messages, widget=forms.TextInput(attrs={'placeholder': '用户名', 'class': 'form-control'}))
	password = forms.CharField(error_messages=error_messages, widget=forms.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control'}))