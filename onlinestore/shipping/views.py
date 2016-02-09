import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def get_shipping_rates(request):
	if request.method == 'GET':
		rates = {
			'message': 'here are the rates...'
			}
		data = json.dumps(rates)
		return HttpResponse(data, content_type='application/json')


@csrf_exempt
def parse_easypost_event(request):
	if request.method == 'POST':
		new_event = {
			'message': 'here is the event data...'
			}
		data = json.dumps(new_event)
		return HttpResponse(data, content_type='application/json')