from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

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