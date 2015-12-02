from django.shortcuts import render

def all_products(request):
	context = {"products": "All products from context"}
	return render(request, 'products/all.html', context)

def single_product(request):
	context = {"product": "Single product from context"}
	return render(request, 'products/single.html', context)