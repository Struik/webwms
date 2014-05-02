from django.conf.urls import patterns, include, url
from django.contrib import admin
from wms import views
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.index, name='wms'),
    url(r'^wms/', include('wms.urls', namespace="wms")),
    url(r'^admin/', include(admin.site.urls)),
)