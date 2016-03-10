from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (User, UserBillingAddressForm, UserMailingAddressForm,
	UserAccountInfoForm, UserRegistrationForm, UserLoginForm)
from .models import UserMailingAddress, UserBillingAddress

def user_register(request):
	form = UserRegistrationForm()

	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			username_exist = User.objects.filter(username=username).last()
			email_exist = User.objects.filter(email=email).first()

			if username_exist:
				messages.add_message(request, messages.ERROR, '用户名已注册过。请再选一个。')

			if email_exist:
				messages.add_message(request, messages.ERROR, '邮箱地址已注册过。')

			if form.cleaned_data['password'] == form.cleaned_data['password_confirm']\
				and not username_exist and not email_exist:
				new_user = User.objects.create(
					username=username,
					email=email)
				new_user.set_password(form.cleaned_data['password'])
				new_user.save()

				messages.add_message(request, messages.SUCCESS, '注册成功啦')
				return HttpResponseRedirect(reverse('all_products'))
			else:
				messages.add_message(request, messages.ERROR, "密码不一致")

	context = {'form': form}	
	return render(request, 'accounts/register.html', context)

def user_login(request):
	form = UserLoginForm()
	if request.method == 'POST':
		next_url = request.GET.get('next', '')
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, '成功登陆啦.祝你购物愉快!')
				return HttpResponseRedirect(next_url or reverse('all_products'))
			else:
				messages.add_message(request, messages.WARNING, '账户还没激活')
		else:
			messages.add_message(request, messages.ERROR, '用户名或密码有误')
	context = {'form': form}
	return render(request, 'accounts/login.html', context)

@login_required
def user_logout(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, '成功退出')
	return HttpResponseRedirect(reverse('all_products'))

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
def user_mailing_address(request, do_redirect=None):
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
	context = {'form': form, 'do_redirect': do_redirect}

	if request.method == 'POST':
		f = UserMailingAddressForm(request.POST, instance=user)
		if f.is_valid():
			address = user.usermailingaddress_set.create()
			address.first_name = f.cleaned_data['first_name']
			address.last_name = f.cleaned_data['last_name']
			# address.use_billing_address = f.cleaned_data['use_billing_address']
			address.address1 = f.cleaned_data['address1']
			address.address2 = f.cleaned_data['address2']
			address.city = f.cleaned_data['city']
			address.state = f.cleaned_data['state']
			address.zipcode = f.cleaned_data['zipcode']
			address.phone = f.cleaned_data['phone']

			address.save()

		messages.add_message(request, messages.SUCCESS, '邮件地址更新成功')

		if do_redirect == 'yes':
			return HttpResponseRedirect(reverse('new_order'))
		return HttpResponseRedirect(reverse('user_mailing_address', do_redirect))

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

		messages.add_message(request, messages.SUCCESS, '账户信息更新成功')

		return HttpResponseRedirect(reverse('user_account_info'))

	return render(request, 'accounts/account.html', context)		