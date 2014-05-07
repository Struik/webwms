from django.conf.urls import patterns, include, url
from django.contrib import admin
from wms import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^index/$', views.index, name='index'),
	url(r'^main/$', views.main, name='main'),
	url(r'^client/$', views.client, name='client'),
	url(r'^sku/$', views.sku, name='sku'),
	url(r'^order/$', views.order, name='order'),
    url(r'^order_detail/$', views.order_detail, name='order_detail'),
	url(r'^incoming/$', views.incoming, name='incoming'),
    url(r'^incoming_detail/$', views.incoming_detail, name='incoming_detail'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'wms/login.html'}, name='login'),
    url(r'^graph/$', views.graph, name='graph'),
	url(r'^logout/$', views.logout_page),
    url(r'^profile/$', views.profile),
)