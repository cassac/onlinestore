from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def user_login(request):
	return HttpResponse('log the user in')

def user_logout(request):
	return HttpResponse('log the user out')

def user_register(request):
	return HttpResponse('register the user')	