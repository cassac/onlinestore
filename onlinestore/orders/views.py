from django.shortcuts import render
from django.http import HttpResponse

def my_orders(request):
	return HttpResponse("Your orders are displayed here")

def new_order(request):
	return HttpResponse("This is your new order page")