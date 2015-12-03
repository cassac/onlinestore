from django.shortcuts import render
from .models import Product

def all_products(request):
	products = Product.objects.all()
	context = {"products": products}
	return render(request, 'products/all.html', context)

def single_product(request, slug):
	product = Product.objects.get(slug=slug)
	context = {"product": product}
	return render(request, 'products/single.html', context)