from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from carts.models import Cart
from .models import Order

@login_required
def my_orders(request):
	return HttpResponse("Your orders are displayed here")

@login_required
def new_order(request):
	user = request.user
	billing_address = user.userbillingaddress_set.last()
	mailing_address = user.usermailingaddress_set.last()
	cart_id = request.session.get('cart_id')
	cart = Cart.objects.get(id=cart_id)
	order_total = cart.get_total()
	context = {'billing_address': billing_address, 
			   'mailing_address': mailing_address,
			   'order_total': order_total
			   }

	if request.method == 'POST':
		card_num = request.POST['card_num']
		card_cvv = request.POST['card_cvv']
		card_exp = request.POST['card_exp']
		# Validate and do stuff with credit card

		order = Order(
			user=user,
			cart=cart,
			mailing_address=mailing_address,
			billing_address=billing_address,
			subtotal=cart.get_subtotal(),
			tax=cart.get_tax(),
			total=cart.get_total()
			)
		order.save()

		del request.session['cart_id']

		messages.add_message(request, messages.SUCCESS, 'Order submitted uccessfully.')
		return HttpResponseRedirect(reverse('my_orders'))
	return render(request, 'orders/new.html', context)