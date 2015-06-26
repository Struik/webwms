import json, datetime, qsstats, re, sqlalchemy, ast, sys
from django.core import serializers
from django.shortcuts import get_object_or_404, render, render_to_response
from wms.forms import MessageForm, ChartForm, NewChartForm, TestForm, TestModelForm
from django.http import HttpResponseRedirect, HttpResponse
from annoying.decorators import render_to
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.template import RequestContext, loader, Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from wms.models import Client, ReferredClients, Sku, Order, OrderDetail, Incoming, IncomingDetail, ChartType, Chartss, Dashboard, DashboardGroup
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
from wms.chart_data import Charts, get_chart_data
from wms.DjangoForms import ContactForm
from django.contrib.messages.views import SuccessMessageMixin


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datatableview
from datatableview.views import DatatableView, XEditableDatatableView
from datatableview.utils import get_datatable_structure
from datatableview import helpers

def available_clients(user_id):
    return Client.objects.select_related('client').filter(referredclients__user=user_id)

@login_required
def index(request):
    return render_to_response('wms/main.html')



def gridlist(request):
    return render_to_response('wms/gridlist.html')

def gridstack(request):
    return render_to_response('wms/gridstack.html')

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
    print('Fetching chart data')
    params = request.GET
    print(params)

    chart_params=defaultdict()
    chart_params_dict=('start_date', 'end_date', 'documents', 'chart_type', 'chart_interval')
    for chart_param in chart_params_dict:
        for param in params:
            if re.match(chart_param, param):
                chart_params[chart_param]=(params.getlist(param))


    if chart_params['chart_type'][0] == 'line_chart':
        chart_data=ChartData.documents_over_period(chart_params)
    elif chart_params['chart_type'][0] == 'columns':
        chart_data=ChartData.documents_over_period(chart_params)
    elif chart_params['chart_type'][0] == 'pie':
        chart_data=ChartData.documents_over_period(chart_params)
    else:
        print('Received something else but line_chart')

    print(chart_data)
    return HttpResponse(json.dumps(chart_data), content_type='application/json')

@csrf_exempt
@login_required
def build_chart(request):
    print('Fetching chart data')
    params = request.POST
    print(params)

    # print(11111)
    # chart_params=defaultdict()
    # print(22222)
    #
    # chart_params_dict=('start_date', 'end_date', 'documents', 'chart_type', 'chart_interval')
    # for chart_param in chart_params_dict:
    #     for param in params:
    #         if re.match(chart_param, param):
    #             chart_params[chart_param]=(params.getlist(param))
    # print(33333)
    # print(chart_params)
    # print(44444)
    # print(66666)
    # chart_req = ast.literal_eval(chart_params['chart_type'][0])
    # print(77777)
    # print(chart_req)
    # print(88888)
    # try:
    #     if chart_req['chart_type_id'] != 0:
    #         chart_object = Charts.get_chart_description(chart_req['chart_id'])
    #         start_date = datetime.datetime.strptime(chart_params['start_date'][0], '%d.%m.%Y')
    #         end_date = datetime.datetime.strptime(chart_params['end_date'][0], '%d.%m.%Y')
    #         grouping_type = chart_params['chart_interval'][0]
    #         chart_result = get_chart_data(chart_object, start_date, end_date, grouping_type)
    #     else:
    #         print('Received something else but over_period')
    # except:
    #     print(sys.exc_info())
    print('Collecting params')
    try:
        chart_object = Charts.get_chart_description(params['chart_descr[chart_id]'])
        start_date = datetime.datetime.strptime(params['chart_params[start_date]'], '%d.%m.%Y')
        end_date = datetime.datetime.strptime(params['chart_params[end_date]'], '%d.%m.%Y')
        grouping_type = params['chart_params[chart_interval]']
        chart_result = get_chart_data(chart_object, start_date, end_date, grouping_type)
    except:
        print(sys.exc_info())

    print(99999)
    print(chart_result)
    try:
        return HttpResponse(json.dumps(chart_result), content_type='application/json')
    except:
        print(sys.exc_info())

@csrf_exempt
@login_required
def add_dashboard(request):
    print('Fetching dashboard data for save')
    params = request.POST
    print(params)
    chart_model = json.loads(params['chart_model'])
    print(chart_model)

    dashboard_group_id = params['dashboard_group']
    dashboard_object = DashboardGroup.objects.get(id=dashboard_group_id)

    dashboard_name = params['dashboard_name']
    dashboard_comments = params['dashboard_comments']

    new_dashboard = Dashboard(name=dashboard_name, chart_model=chart_model, comments=dashboard_comments, dashboard_group=dashboard_object)
    new_dashboard.save()
    return HttpResponse(json.dumps({'data': 'data'}), content_type='application/json')

@csrf_exempt
@login_required
def get_dashboard(request):
    print('Fetching dashboard data for load')
    params = request.POST
    print(params)
    dashboard_id = params['dashboard_id']
    print(dashboard_id)
    try:
        print('Get dashboard object from DB')
        dashboard = Dashboard.objects.get(id=dashboard_id)
        chart_model = dashboard.chart_model
        print(chart_model)
        return HttpResponse( json.dumps({'chart_model': chart_model}), content_type='application/json')
    except:
        print(sys.exc_info())


@login_required
def form(request):
    return render(request, 'wms/form.html', {'form': MessageForm()})

@login_required
def form2(request):
    return render(request, 'wms/form2.html', {'form': ChartForm()})

@login_required
def form3(request):
    return render(request, 'wms/form3.html', {'form': NewChartForm()})
    #return render(request, 'wms/form3.html', {'form': ContactForm()})

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

@login_required
def charts(request):
    print(111)
    data = reverse('wms:chart_list')
    return render_to_response('wms/charts.html', {'data': data}, context_instance=RequestContext(request))

class ChartList(LoginRequiredMixin, BaseDatatableView):
    model = Chartss
    print(222)
    columns = ['id','chart_name','view_name','chart_type_id','x_axis_label','y_axis_label','x_axis_field',
               'y_axis_field','grouping','grouping_field','grouping_field_label','with_table','created']
    order_columns = ['id']
    max_display_length = 500

    def get_initial_queryset(self):
        print('Chart list:')
        print(self.model.objects.all())
        return self.model.objects.all()

    # def filter_queryset(self, filtered):
    #     sSearch = self.request.GET.get('sSearch', None)
    #     if sSearch:
    #         filtered = filtered.filter(name__icontains=sSearch)
    #     return filtered

class HomeView(TemplateView):
    template_name = 'wms/home.html'

class AjaxTemplateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

class TestFormView(SuccessMessageMixin, AjaxTemplateMixin, FormView):
    print('ooooooo')
    template_name = 'wms/test_form.html'
    form_class = TestModelForm
    success_url = reverse_lazy('wms:chart_list')
    success_message = "Way to go!"
    print('aaaaaaa')


    def form_valid(self, form):
        try:
            print('aaavvvvv')
            form.save()
            return super(TestFormView, self).form_valid(form)
        except:
            print('osososos')
            print(sys.exc_info())


@login_required
def dashboard(request):
    #return render_to_response('wms/dashboard.html')
    print('Fetching list of charts')
    try:
        chart_list = Charts.get_chart_names_dict()
    except:
        print(sys.exc_info())
    print('Chart list:')
    print(chart_list)
    #d = {"person": {"p":{"a":"1","b":"2"}}, {"z":{"a":"3","b":"4"}}}
    d = {"person": [{"first_name": "Joe", "last_name": "Johnson"}, {"first_name": "Oleg", "last_name": "Ole"}]}
    return render_to_response('wms/dashboard.html', chart_list, context_instance=RequestContext(request))

@login_required
def dashboard_list(request):
    print('Fetching list of dashboards')
    try:
        dashboard_list = Dashboard.objects.all().order_by("name")
        dashboard_groups = DashboardGroup.objects.all().order_by("dashboard_group_id")
    except:
        print(sys.exc_info())
    return render_to_response('wms/dashboards.html', {'dashboard_list': dashboard_list, 'dashboard_groups': dashboard_groups,}, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def get_chart_list(request):
    print('Fetching list of charts')
    try:
        chart_list = Charts.get_chart_names()
    except:
        print(sys.exc_info())
    print('Chart list:')
    print(chart_list)
    print('Returning chart list for ajax call')
    return HttpResponse(json.dumps(chart_list), content_type='application/json')

