from django.shortcuts import render, HttpResponse

def get_cart(request):
	return HttpResponse('this is the cart speaking')
