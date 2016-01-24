from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from carts.models import Cart
from .models import Order
from .utils import generate_order_id

@login_required
def my_orders(request):
	user = request.user
	context = {'orders': user.order_set.all }
	return render(request, 'orders/history.html', context)

@login_required
def new_order(request):
	user = request.user
	mailing_address = user.usermailingaddress_set.last()
	billing_address = user.userbillingaddress_set.last()
	cart_id = request.session.get('cart_id')
	cart = Cart.objects.get(id=cart_id)
	order_total = str(cart.get_total())
	stripe_total = order_total.replace('.', '')
	context = {'mailing_address': mailing_address,
			   'order_total': order_total,
			   'stripe_total': stripe_total
			   }
	if request.method == 'POST':
		if mailing_address is None or mailing_address.address1 == '':
			messages.add_message(request, messages.ERROR, '请提供自己的邮件地址')
			return HttpResponseRedirect(reverse('new_order'))		
		card_num = request.POST['card_num']
		card_cvv = request.POST['card_cvv']
		card_exp = request.POST['card_exp']
		# Validate and do stuff with credit card
		order = Order(
			user=user,
			cart=cart,
			mailing_address=mailing_address,
			# billing_address=billing_address,
 			order_id=generate_order_id(),
			subtotal=cart.get_subtotal(),
			tax=cart.get_tax(),
			total=cart.get_total()
			)

		order.save()

		del request.session['cart_id']
		del request.session['total_items']

		messages.add_message(request, messages.SUCCESS, 'Order submitted uccessfully.')
		return HttpResponseRedirect(reverse('my_orders'))
	if mailing_address is None or mailing_address.address1 == '':
		messages.add_message(request, messages.ERROR, '请提供自己的邮件地址')		
	return render(request, 'orders/new.html', context)