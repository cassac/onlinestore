import json
import easypost
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

easypost.api_key = settings.EASYPOST_API_KEY

def parse_shipping(name):
	word_list = []
	temp = ''
	upper_counter = 0

	for n in range(len(name)):

		if name[n].isupper() and upper_counter < 3:
			upper_counter += 1
		
			if len(temp) > 1:
				word_list.append(temp)
				temp = ''
		
		elif upper_counter == 3:
			return ' '.join(word_list)

		if len(word_list) < 3:
			temp += name[n]

	return [name[:12]]

def get_shipping_rates(request):
	if request.method == 'GET':

		user_address = request.user.usermailingaddress_set.last()

		if user_address == None or not user_address.is_complete():
			messages.add_message(request, messages.ERROR, '请提供邮件地址再结算')
			url = request.build_absolute_uri(reverse('user_mailing_address'))
			rates = {
				'redirect_to': url,
				}
			data = json.dumps(rates)
			return HttpResponse(data, status=302, content_type='application/json')

		try:
			# Create parcel for rate calculation
			parcel = easypost.Parcel.create(
			  length = 9, #inches
			  width = 6,
			  height = 2,
			  weight = 8, # ounces
			)
		except:
			rates = {
				'message': 'Error loading parcel'
				}
			data = json.dumps(rates)
			return HttpResponse(data, content_type='application/json')

		try:
			fromAddress = easypost.Address.create(
			  company = 'EasyPost',
			  street1 = '118 2nd Street',
			  street2 = '4th Floor',
			  city = 'San Francisco',
			  state = 'CA',
			  zip = '94105',
			  phone = '415-528-7555'
			)
		except:
			rates = {
				'message': 'Error loading fromAddress'
				}
			data = json.dumps(rates)
			return HttpResponse(data, content_type='application/json')

		try:
			toAddress = easypost.Address.create(
			  name = user_address.first_name +' '+user_address.last_name,
			  # company = 'Vandelay Industries',
			  street1 = user_address.address1,
			  stree2 = user_address.address2,
			  city = user_address.city,
			  state = user_address.state,
			  country = 'CN',
			  zip = user_address.zipcode,
			)
		except:
			rates = {
				'message': 'Error loading toAddress'
				}
			data = json.dumps(rates)
			return HttpResponse(data, content_type='application/json')			

		try:
			shipment = easypost.Shipment.create(
			  to_address = toAddress,
			  from_address = fromAddress,
			  parcel = parcel
			)
		except:
			rates = {
				'message': 'Error creating shipment object'
				}
			data = json.dumps(rates)
			return HttpResponse(data, content_type='application/json')	

		try:
			customs_item1 = easypost.CustomsItem.create(
			  description = 'T-shirt',
			  quantity = 1,
			  value = 11,
			  weight = 6,
			  hs_tariff_number = 610910,
			  origin_country = 'US'
			)
		except:
			rates = {
				'message': 'Error creating custom_item1'
				}
			data = json.dumps(rates)
			return HttpResponse(data, content_type='application/json')	

		try:
			customs_info = easypost.CustomsInfo.create(
			  eel_pfc = 'NOEEI 30.37(a)',
			  customs_certify = True,
			  customs_signer = 'Jarrett Streebin',
			  contents_type = 'gift',
			  customs_items = [customs_item1]
			)
		except:
			rates = {
				'message': 'Error creating customs_info'
				}
			data = json.dumps(rates)


		shipment = easypost.Shipment.create(
			to_address = toAddress,
			from_address = fromAddress,
			parcel = parcel,
			customs_info = customs_info,
		)

		shipping_rates = {}

		for option in shipment.rates:
			service_type = parse_shipping(option.service)
			shipping_rates[service_type] = {
					'rate': option.rate,
					'currency': option.currency,
					'rate_id': option.id,
				}
		data = json.dumps(shipping_rates)

		return HttpResponse(data, content_type='application/json')


@csrf_exempt
def parse_easypost_event(request):
	if request.method == 'POST':
		response_body = request.body.decode('utf-8')
		data = json.loads(response_body)
		print(data)
		return HttpResponse('ok', content_type='application/json')