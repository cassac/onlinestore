from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.all_products, name='all_products'),
    url(r'^product/$', views.single_product, name='single_product'),
]