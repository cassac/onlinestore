import json
import easypost
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

easypost.api_key = settings.EASYPOST_API_KEY

def get_shipping_rates(request):
	if request.method == 'GET':

		try:
			# Create parcel for rate calculation
			parcel = easypost.Parcel.create(
			  length = 9, #inches
			  width = 6,
			  height = 2,
			  weight = 10, # ounces
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
			  name = 'George Costanza',
			  company = 'Vandelay Industries',
			  street1 = '1 E 161st St.',
			  city = 'Bronx',
			  state = 'NY',
			  zip = '10451'
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

		shipment = easypost.Shipment.create(
		  to_address = toAddress,
		  from_address = fromAddress,
		  parcel = parcel
		)

		shipping_rates = {}
		for option in shipment.rates:
			shipping_rates[option.service] = {
					'rate': option.rate,
					'currency': option.currency
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