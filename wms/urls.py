from django.conf.urls import patterns, include, url
from django.contrib import admin
from wms import views
from wms.views import OrderListJson, SkuList, ClientList, OrderList, OrderDetailList, SkuLists, ChartList, \
    HomeView, TestFormView, gridlist, gridstack, dashboard

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
    url(r'^order_list_json/$', OrderListJson.as_view(), name='order_list_json'),
    url(r'^data_table/$', views.data_table, name='data_table'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'wms/login.html'}, name='login'),
    url(r'^graph/$', views.graph, name='graph'),
    url(r'^graph2/$', views.graph2, name='graph2'),
    url(r'^graph3/$', views.graph3, name='graph3'),
    url(r'^graph4/$', views.graph4, name='graph4'),
    url(r'^form/$', views.form, name='form'),
    url(r'^form2/$', views.form2, name='form2'),
    url(r'^form2/add_chart/$', views.add_chart, name='add_chart'),
    url(r'^form3/$', views.form3, name='form3'),
    url(r'^form3/new_chart/$', views.build_chart, name='new_chart'),
    url(r'^charts/$', views.charts, name='charts'),
    url(r'^logout/$', views.logout_page),
    url(r'^profile/$', views.profile),

    url(r'^sku_list/$', SkuList.as_view(), name='sku_list'),
    url(r'^sku_lists/$', SkuLists.as_view(), name='sku_lists'),
    url(r'^client_list/$', ClientList.as_view(), name='client_list'),
    url(r'^order_list/$', OrderList.as_view(), name='order_list'),
    url(r'^order_detail_list/$', OrderDetailList.as_view(), name='order_detail_list'),
    url(r'^chart_list/$', ChartList.as_view(), name='chart_list'),

    url(r'^home.html', HomeView.as_view(), name="home"),
    url(r'^test-form/$', TestFormView.as_view(), name="test-form"),
    url(r'^gridlist/$', views.gridlist, name='gridlist'),
    url(r'^gridstack/$', views.gridstack, name='gridstack'),


    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/get_chart_list/$', views.get_chart_list, name='get_chart_list'),
    url(r'^dashboard/build_chart/$', views.build_chart, name='build_chart'),
    url(r'^dashboard/add_dashboard/$', views.add_dashboard, name='add_dashboard'),
    url(r'^dashboard/get_dashboard/$', views.get_dashboard, name='get_dashboard'),
)