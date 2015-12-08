from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.my_orders, name='my_orders'),
    url(r'^new/$', views.new_order, name='new_order'),
]