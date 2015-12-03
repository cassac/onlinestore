from django.shortcuts import render
from django.db.models import Q

from .models import Product

def all_products(request):
	products = Product.objects.all()
	context = {"products": products}
	return render(request, 'products/all.html', context)

def single_product(request, slug):
	product = Product.objects.get(slug=slug)
	context = {"product": product}
	return render(request, 'products/single.html', context)

def search_products(request):
	search_term = request.GET.get('term')
	search_results = Product.objects.filter(
					Q(title__icontains=search_term) |
					Q(description__icontains=search_term)
				)
	context = {"products": search_results,
			   "search_term": search_term}
	return render(request, 'products/all.html', context)