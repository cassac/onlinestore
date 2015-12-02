from django.shortcuts import render
from django.http import HttpResponse

def all_products(request):
	return render(request, 'products/all.html')

def single_product(request):
	return render(request, 'products/single.html')