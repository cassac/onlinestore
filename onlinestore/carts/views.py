from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product

def my_cart(request):
	# Initiate cart
	if 'total_items' not in request.session:
		request.session['total_items'] = 0

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

		if request.POST.get('_method') == 'put':
			quantities = [quantity for quantity in request.POST.getlist('quantity')]
			# print(dir(cart))
			for idx, cart_item in enumerate(cart.cartitem_set.all()):
				cart_item.quantity = quantities[idx]
				cart_item.save()

		else:
			product_slug = request.POST.get('product')
			quantity = request.POST.get('quantity')
			product = Product.objects.get(slug=product_slug)
			if product in cart.cartitem_set.all():
				messages.add_message(request, messages.ERROR, '此产品已加入购物车里')
			else:
				new_item = CartItem(cart=cart, product=product, 
					quantity=quantity)
				new_item.save()
				cart.cartitem_set.add(new_item)
				cart = Cart.objects.get(id=cart.id)
				total_items = int(request.session['total_items'])
				request.session['total_items'] = total_items + 1

		return HttpResponseRedirect(reverse('my_cart'))


def remove_item(request, cart_item_id):
	cart_id = request.session.get('cart_id')
	cart = Cart.objects.get(id=cart_id)
	cart_item = CartItem.objects.get(id=cart_item_id)
	cart.cartitem_set.remove(cart_item)
	cart.save()
	total_items = int(request.session['total_items'])
	request.session['total_items'] = total_items - 1
	messages.add_message(request, messages.SUCCESS, '产品被删除')
	return HttpResponseRedirect(reverse('my_cart'))