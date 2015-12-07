from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.my_cart, name='my_cart'),
    url(r'^remove/(?P<slug>[\w-]+)/$', views.remove_item, name='remove_item'),
]