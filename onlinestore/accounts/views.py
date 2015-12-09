from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import (UserBillingAddressForm, UserMailingAddressForm,
	UserAccountInfoForm)

def user_login(request):
	if request.method == 'POST':
		username = request.POST['inputUsername']
		password = request.POST['inputPassword']
		
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, 'You have successfuly logged in.')
				return HttpResponseRedirect(reverse('all_products'))
			else:
				messages.add_message(request, messages.WARNING, 'Your account is not active.')
		else:
			messages.add_message(request, messages.ERROR, 'Username and/or password invalid.')

	return render(request, 'accounts/login.html')

def user_logout(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'You have successfuly logged out.')
	return HttpResponseRedirect(reverse('all_products'))

def user_register(request):
	return render(request, 'accounts/register.html')

def user_billing_address(request):
	user = request.user
	initial = {'first_name': user.first_name, 'last_name': user.last_name}
	if user.userbillingaddress_set.first():
		address = user.userbillingaddress_set.first()
		initial['address1'] = address.address1
		initial['address2'] = address.address2
		initial['city'] = address.city
		initial['state'] = address.state
		initial['zipcode'] = address.zipcode
		initial['phone'] = address.phone

	form = UserBillingAddressForm(
				initial=initial
			)
	context = {'form': form}
	return render(request, 'accounts/billingaddress.html', context)

def user_mailing_address(request):
	user = request.user
	initial = {'first_name': user.first_name, 'last_name': user.last_name}
	if user.usermailingaddress_set.first():
		address = user.usermailingaddress_set.first()
		initial['use_billing_address'] = address.use_billing_address
		initial['address1'] = address.address1
		initial['address2'] = address.address2
		initial['city'] = address.city
		initial['state'] = address.state
		initial['zipcode'] = address.zipcode
		initial['phone'] = address.phone
	form = UserMailingAddressForm()
	context = {'form': form}
	return render(request, 'accounts/mailingaddress.html', context)	

def user_account_info(request):
	user = request.user
	form = UserAccountInfoForm(
				initial={
					'first_name': user.first_name,
					'last_name': user.last_name,
					'username': user.username,
					'email': user.email,
				}
			)
	context = {'form': form}
	return render(request, 'accounts/account.html', context)		