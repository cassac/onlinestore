import os
import stripe

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from carts.models import Cart
from .models import Order
from .utils import generate_order_id

stripe.api_key = os.environ['STRIPE_SECRET_KEY']
stripe_pub_key = os.environ['STRIPE_PUBLISHABLE_KEY']

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
			   'stripe_total': stripe_total,
			   'stripe_pub_key': stripe_pub_key,
			   }
	if request.method == 'POST':
		stripe_token = request.POST['stripeToken']

		if mailing_address is None or mailing_address.address1 == '':
			messages.add_message(request, messages.ERROR, '请提供自己的邮件地址')
			return HttpResponseRedirect(reverse('new_order'))		

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

		try:
			charge = stripe.Charge.create(
					amount=stripe_total, # amount in cents, again
					currency="usd",
					source=stripe_token,
					description="cassac网店",
					metadata={"order_id": order.order_id}
				)
			if charge.status == 'succeeded':
				try:
					customer_email_address = charge.source.username # used for alipay charge
				except AttributeError:
					customer_email_address = charge.source.name # used for cc charge
				except:
					customer_email_address = None
			if customer_email_address is not None:
				send_mail(subject='CASSAC网店交易成功', 
						  message='谢谢您的光临。我们已收到您的订单了，会尽快发货！\n\n祝您今天愉快\n\nCASSAC网店', 
						  from_email=settings.EMAIL_HOST_USER,
						  recipient_list=[customer_email_address], 
						  fail_silently=False)
		except stripe.error.CardError as e:
			body = e.json_body
			err  = body['error']
			print("Status is: %s" % e.http_status)
			print("Type is: %s" % err['type'])
			print("Code is: %s" % err['code'])
			print("Param is: %s" % err['param'])
			print("Message is: %s" % err['message'])				

		order.save()
		
		del request.session['cart_id']
		del request.session['total_items']

		messages.add_message(request, messages.SUCCESS, 'Order submitted uccessfully.')
		return HttpResponseRedirect(reverse('my_orders'))
	if mailing_address is None or mailing_address.address1 == '':
		messages.add_message(request, messages.ERROR, '请提供自己的邮件地址')		
	return render(request, 'orders/new.html', context)