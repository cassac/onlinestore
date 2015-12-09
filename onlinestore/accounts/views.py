from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (UserBillingAddressForm, UserMailingAddressForm,
	UserAccountInfoForm)
from .models import UserMailingAddress, UserBillingAddress

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

@login_required
def user_logout(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'You have successfuly logged out.')
	return HttpResponseRedirect(reverse('all_products'))

def user_register(request):
	return render(request, 'accounts/register.html')

@login_required
def user_billing_address(request):
	user = request.user
	initial = {}
	if user.userbillingaddress_set.first():
		address = user.userbillingaddress_set.last()
		initial['first_name'] = address.first_name
		initial['last_name'] = address.last_name			
		initial['address1'] = address.address1
		initial['address2'] = address.address2
		initial['city'] = address.city
		initial['state'] = address.state
		initial['zipcode'] = address.zipcode
		initial['phone'] = address.phone

	form = UserBillingAddressForm(initial=initial)
	context = {'form': form}

	if request.method == 'POST':
		f = UserBillingAddressForm(request.POST, instance=user)
		if f.is_valid():
			address = user.userbillingaddress_set.create()
			address.first_name = f.cleaned_data['first_name']
			address.last_name = f.cleaned_data['last_name']
			address.address1 = f.cleaned_data['address1']
			address.address2 = f.cleaned_data['address2']
			address.city = f.cleaned_data['city']
			address.state = f.cleaned_data['state']
			address.zipcode = f.cleaned_data['zipcode']
			address.phone = f.cleaned_data['phone']

			address.save()

		messages.add_message(request, messages.SUCCESS, 'Billing address updated.')

		return HttpResponseRedirect(reverse('user_billing_address'))

	return render(request, 'accounts/billingaddress.html', context)

@login_required
def user_mailing_address(request):
	user = request.user
	initial = {}
	if user.usermailingaddress_set.first():
		address = user.usermailingaddress_set.last()
		initial['first_name'] = address.first_name
		initial['last_name'] = address.last_name	
		initial['use_billing_address'] = address.use_billing_address
		initial['address1'] = address.address1
		initial['address2'] = address.address2
		initial['city'] = address.city
		initial['state'] = address.state
		initial['zipcode'] = address.zipcode
		initial['phone'] = address.phone

	form = UserMailingAddressForm(initial=initial)
	context = {'form': form}

	if request.method == 'POST':
		f = UserMailingAddressForm(request.POST, instance=user)
		if f.is_valid():
			address = user.usermailingaddress_set.create()
			address.first_name = f.cleaned_data['first_name']
			address.last_name = f.cleaned_data['last_name']
			address.use_billing_address = f.cleaned_data['use_billing_address']
			address.address1 = f.cleaned_data['address1']
			address.address2 = f.cleaned_data['address2']
			address.city = f.cleaned_data['city']
			address.state = f.cleaned_data['state']
			address.zipcode = f.cleaned_data['zipcode']
			address.phone = f.cleaned_data['phone']

			address.save()

		messages.add_message(request, messages.SUCCESS, 'Mailing address updated.')

		return HttpResponseRedirect(reverse('user_mailing_address'))

	return render(request, 'accounts/mailingaddress.html', context)	

@login_required
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

	if request.method == 'POST':
		f = UserAccountInfoForm(request.POST, instance=user)
		if f.is_valid():
			user.first_name = f.cleaned_data['first_name']
			user.last_name = f.cleaned_data['last_name']
			user.email = f.cleaned_data['email']
			user.username = f.cleaned_data['username']
			user.save()

		messages.add_message(request, messages.SUCCESS, 'Account info updated.')

		return HttpResponseRedirect(reverse('user_account_info'))

	return render(request, 'accounts/account.html', context)		