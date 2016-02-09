from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^rates/', views.get_shipping_rates, name='get_shipping_rates'),
    url(r'^events/', views.parse_easypost_event, name='parse_easypost_event'),
]