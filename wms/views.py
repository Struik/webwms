import json
import datetime, qsstats
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
from django.views.decorators.csrf import csrf_exempt
from qsstats import QuerySetStats
from django.db.models import Count
from collections import defaultdict
from wms.reports import ChartData
from django.contrib import messages


@login_required
def index(request):
    return render_to_response('wms/main.html')

@login_required
def main(request):
    return render_to_response('wms/main.html', context_instance=RequestContext(request))

@login_required
def profile(request):
    return render_to_response('wms/profile.html', context_instance=RequestContext(request))

@login_required
def client(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    return render_to_response('wms/client.html', {'available_clients':available_clients}, context_instance=RequestContext(request))

@login_required
def sku(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    available_sku=Sku.objects.select_related('client').filter(holder=available_clients)
    return render_to_response('wms/sku.html', {'available_sku':available_sku}, context_instance=RequestContext(request))

@login_required
def order(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    available_orders=Order.objects.select_related('client').filter(holder=available_clients)
    return render_to_response('wms/order.html', {'available_orders':available_orders}, context_instance=RequestContext(request))

# @csrf_exempt
# @login_required
# def order_detail(request):
#     current_order_details = serializers.serialize('json', OrderDetail.objects.filter(order=request.POST.get('id')))
#     return HttpResponse(json.dumps(current_order_details,
#             ensure_ascii=False), content_type='application/json')
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


# @login_required
# def graph2(request):
#     return render_to_response('wms/graph2.html', context_instance=RequestContext(request))

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

@login_required
def chart_data(request):
    data = {}
    params = request.GET
    today = datetime.date.today().strftime('%Y-%m-%d')
    chart_type = params.get('chartType','ignore')
    start_date = datetime.datetime.strptime(params.get('startDate') or (today), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(params.get('endDate') or (today), '%Y-%m-%d')
    if chart_type == 'documentsCount':
        available_orders=Order.objects.all()
        qsstats = QuerySetStats(available_orders, date_field='date_to_ship', aggregate=Count('id'))
        order_stats = qsstats.time_series(start_date, end_date, interval='days')

        data = {'dates': [], 'values': []}
        for item in order_stats:
            data['dates'].append(item[0].strftime('%d %b'))
            data['values'].append(item[1])
    else:
        type('Received something else but documentsCount')
    print(data)
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@login_required
def add_chart(request):
    params = request.GET

    today = datetime.date.today().strftime('%d.%m.%Y')
    chart_type = params.get('chart_type','ignore')

    if chart_type == 'over_period':
        chart_data=ChartData.documents_over_period(params.get('start_date'), params.get('end_date'), params.getlist('documents'))
    else:
        print('Received something else but over_period')

    print(chart_data)
    print(json.dumps(chart_data))
    return HttpResponse(json.dumps(chart_data), content_type='application/json')

@login_required
def form(request):
    return render(request, 'wms/form.html', {'form': MessageForm()})

@login_required
def form2(request):
    return render(request, 'wms/form2.html', {'form': ChartForm()})

# @login_required
# def graph(request):
#     queryset = Payment.objects.all()
#     # считаем количество платежей...
#     qsstats = QuerySetStats(queryset, date_field='datetime', aggregate=Count('id'))
#     # ...в день за указанный период
#     today = datetime.date.today()
#     five_year_ago = today - datetime.timedelta(days=5)
#     values = qsstats.time_series(five_year_ago, today, interval='days')
#     return render_to_response('wms/graph.html', {'order_stats': values})

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')