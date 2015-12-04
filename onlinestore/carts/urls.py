from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_cart, name='get_cart'),
]