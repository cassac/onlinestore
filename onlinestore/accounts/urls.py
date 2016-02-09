from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^mailing/$', views.user_mailing_address, name='user_mailing_address'), 
    url(r'^mailing/(?P<do_redirect>[-\w]+)$', views.user_mailing_address, name='user_mailing_address'),  
    url(r'^billing/$', views.user_billing_address, name='user_billing_address'), 
    url(r'^$', views.user_account_info, name='user_account_info'),            
]