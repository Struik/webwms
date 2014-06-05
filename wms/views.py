import json, datetime, qsstats, re
from django.core import serializers
from django.shortcuts import get_object_or_404, render, render_to_response
from wms.forms import MessageForm, ChartForm
from django.http import HttpResponseRedirect, HttpResponse
from annoying.decorators import render_to
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template import RequestContext, loader, Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from wms.models import Client, ReferredClients, Sku, Order, OrderDetail, Incoming, IncomingDetail, ChartType
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, TemplateView, ListView
from django.views.decorators.csrf import csrf_exempt
from qsstats import QuerySetStats
from django.db.models import Count
from collections import defaultdict
from wms.reports import ChartData
from django.contrib import messages
from collections import defaultdict
from django_datatables_view.base_datatable_view import BaseDatatableView
from braces.views import LoginRequiredMixin

import datatableview
from datatableview.views import DatatableView, XEditableDatatableView
from datatableview.utils import get_datatable_structure
from datatableview import helpers

def available_clients(user_id):
    return Client.objects.select_related('client').filter(referredclients__user=user_id)

@login_required
def index(request):
    return render_to_response('wms/main.html')

@login_required
def main(request):
    return render_to_response('wms/main.html', context_instance=RequestContext(request))

@login_required
def profile(request):
    return render_to_response('wms/profile.html', context_instance=RequestContext(request))


@csrf_exempt
@login_required
#@render_to('wms/order.html')#annoying-decorator
def order_detail(request):
    current_order_details=OrderDetail.objects.filter(order=request.POST.get('id'))
    return render_to_response('wms/order_detail.html', {'current_order_details':current_order_details}, context_instance=RequestContext(request))

@login_required
def incoming(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    available_incomings=Incoming.objects.select_related('client').filter(holder=available_clients)
    return render_to_response('wms/incoming.html', {'available_incomings':available_incomings}, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def incoming_detail(request):
    current_incoming_details=IncomingDetail.objects.filter(incoming=request.POST.get('id'))
    return render_to_response('wms/incoming_detail.html', {'current_incoming_details':current_incoming_details}, context_instance=RequestContext(request))

@login_required
def graph(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    available_orders=Order.objects.select_related('client').filter(holder=available_clients)
    qsstats = QuerySetStats(available_orders, date_field='date_to_ship', aggregate=Count('id'))
    today = datetime.date.today()
    five_year_ago = today - datetime.timedelta(days=30)
    order_stats = qsstats.time_series(five_year_ago, today, interval='days')
    return render_to_response('wms/graph.html', {'order_stats':order_stats}, context_instance=RequestContext(request))

@login_required
def graph2(request):
    today = datetime.date.today()
    start_date= today - datetime.timedelta(days=30)
    end_date = today - datetime.timedelta(days=10)

    available_orders=Order.objects.all()
    qsstats = QuerySetStats(available_orders, date_field='date_to_ship', aggregate=Count('id'))
    order_stats = qsstats.time_series(start_date, end_date, interval='days')

    available_incomings=Incoming.objects.all()
    qsstats = QuerySetStats(available_incomings, date_field='date_to_ship', aggregate=Count('id'))
    incoming_stats = qsstats.time_series(start_date, end_date, interval='days')

    orders_by_holders = Order.objects.values("client_name").annotate(Count("id"))

    return render_to_response('wms/graph2.html', {'order_stats':order_stats,'incoming_stats':incoming_stats, 'orders_by_holders':orders_by_holders}, context_instance=RequestContext(request))

@login_required
def graph3(request):
    return render_to_response('wms/graph3.html', context_instance=RequestContext(request))

@login_required
def graph4(request):
    return render_to_response('wms/graph4.html', context_instance=RequestContext(request))

@csrf_exempt
@login_required
def add_chart(request):
    params = request.GET

    chart_params=defaultdict()
    chart_params_dict=('start_date', 'end_date', 'documents', 'chart_type')
    for chart_param in chart_params_dict:
        for param in params:
            if re.match(chart_param, param):
                chart_params[chart_param]=(params.getlist(param))

    if chart_params['chart_type'][0] == 'over_period':
        chart_data=ChartData.documents_over_period(chart_params)
    else:
        print('Received something else but over_period')

    return HttpResponse(json.dumps(chart_data), content_type='application/json')

@login_required
def form(request):
    return render(request, 'wms/form.html', {'form': MessageForm()})

@login_required
def form2(request):
    return render(request, 'wms/form2.html', {'form': ChartForm()})

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def data_table(request):
    #return render_to_response('wms/DataTable.html', context_instance=RequestContext(request))
    data = reverse('wms:order_list_json')
    print('111')
    print(data)
    print('222')
    return render_to_response(
        'wms/DataTable.html',
        {'data': data},
        context_instance=RequestContext(request),
    )

class OrderListJson(LoginRequiredMixin, BaseDatatableView):
    model = Order

    columns = ['sdid', 'date_to_ship', 'status']
    order_columns = ['sdid', 'date_to_ship', 'status']
    max_display_length = 200







@login_required
def client(request):
    data = reverse('wms:client_list')
    return render_to_response('wms/client.html', {'data': data}, context_instance=RequestContext(request))

@login_required
def sku(request):
    data = reverse('wms:sku_list')
    return render_to_response('wms/sku.html', {'data': data}, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def order(request):
    data = reverse('wms:order_list')
    detail_data=reverse('wms:order_detail_list')

    if request.method == 'POST' and request.is_ajax:
        params = request.POST
        # Create the URL query string and strip the last '&' at the end.
        data = ('%s?%s' % (reverse('wms:order_detail_list'), ''.join(
            ['%s=%s&' % (k, v) for k, v in params.items()])))\
            .rstrip('&')
        return HttpResponse(json.dumps(data), content_type='application/json')

    return render_to_response('wms/order_new.html', {'data': data, 'detail_data': detail_data}, context_instance=RequestContext(request))

class SkuList(LoginRequiredMixin, BaseDatatableView):
    model = Sku
    columns = ['id','sku_id','name','sdid']
    order_columns = ['id','sku_id','name','sdid']
    max_display_length = 500

    def get_initial_queryset(self):
        return self.model.objects.select_related('client').filter(holder=available_clients(self.request.user))

    def filter_queryset(self, filtered):
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            filtered = filtered.filter(name__icontains=sSearch)
        return filtered


class SkuLists(DatatableView):
    template_name = "wms/sku_new.html"
    model = Sku
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            'id',
            'sku_id',
            'name',
            'sdid',
        ],
        'ordering': ['id'],
    }

    def get_initial_queryset(self):
        return self.model.objects.select_related('client').filter(holder=available_clients(self.request.user))

class ClientList(LoginRequiredMixin, BaseDatatableView):
    model = Client
    columns = ['id','name','address','sdid']
    order_columns = ['id','name','address','sdid']
    max_display_length = 500

    def get_initial_queryset(self):
        return self.model.objects.select_related('client').filter(referredclients__user=self.request.user)

    def filter_queryset(self, filtered):
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            filtered = filtered.filter(name__icontains=sSearch)
        return filtered


class OrderList(LoginRequiredMixin, BaseDatatableView):
    model = Order
    columns = ['id', 'sdid', 'display_name', 'date_to_ship', 'status']
    order_columns = ['id', 'sdid', 'display_name', 'date_to_ship', 'status']
    max_display_length = 500

    def get_initial_queryset(self):
        return self.model.objects.select_related('client').filter(holder=available_clients(self.request.user))

    def filter_queryset(self, filtered):
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            filtered = filtered.filter(display_name__icontains=sSearch)
        return filtered

class OrderDetailList(LoginRequiredMixin, BaseDatatableView):
    model = OrderDetail
    columns = ['id', 'order_id', 'line', 'sku_id', 'sku_name', 'qty', 'planned', 'moved', 'packed', 'shiped']
    order_columns = ['id', 'order_id', 'line', 'sku_id', 'sku_name', 'qty', 'planned', 'moved', 'packed', 'shiped']
    max_display_length = 500

    def get_initial_queryset(self):
        return self.model.objects.all()

    def filter_queryset(self, qs):
        params = self.request.GET
        doc_id = params.get('doc_id', '')
        if doc_id:
            qs = qs.filter(order=doc_id)

        return qs