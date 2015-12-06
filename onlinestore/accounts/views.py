from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def user_login(request):
	return render(request, 'accounts/login.html')

def user_logout(request):
	return render(request, 'accounts/logout.html')

def user_register(request):
	return render(request, 'accounts/register.html')	