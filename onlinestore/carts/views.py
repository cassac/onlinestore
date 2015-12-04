from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Cart
from products.models import Product

def my_cart(request):
	# Retrieves cart or creates one
	if request.session.get('cart_id'):
		cart_id = request.session.get('cart_id')
		cart = Cart.objects.get(id=cart_id)
	else:
		cart = Cart.objects.create()
		request.session['cart_id'] = cart.id

	if request.method == 'GET':
		context = {'cart': cart}
		return render(request, 'carts/mycart.html', context)

	if request.method == 'POST':
		product_slug = request.POST.get('add')
		product = Product.objects.get(slug=product_slug)
		cart.products.add(product)
		cart = Cart.objects.get(id=cart.id)
		context = {'cart': cart}
		return HttpResponseRedirect(reverse('my_cart'))
	