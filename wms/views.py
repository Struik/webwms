import json
import datetime, qsstats
from django.core import serializers
from django.shortcuts import get_object_or_404, render, render_to_response
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
from wms.models import Client, ReferredClients, Sku, Order, OrderDetail, Incoming, IncomingDetail, Payment
from django.views.decorators.csrf import csrf_exempt
from qsstats import QuerySetStats
from django.db.models import Count

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

# @login_required
# def graph(request):
#     available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
#     available_orders=Order.objects.select_related('client').filter(holder=available_clients)
#     qsstats = QuerySetStats(available_orders, date_field='date_to_ship', aggregate=Count('id'))
#     today = datetime.date.today()
#     year_ago = today - datetime.timedelta(days=365)
#     order_stats = qsstats.time_series(year_ago, today, interval='days')
#     return render_to_response('wms/graph.html', {'order_stats':order_stats}, context_instance=RequestContext(request))

@login_required
def graph(request):
    queryset = Payment.objects.all()
    # считаем количество платежей...
    qsstats = QuerySetStats(queryset, date_field='datetime', aggregate=Count('id'))
    # ...в день за указанный период
    today = datetime.date.today()
    five_year_ago = today - datetime.timedelta(days=5)
    values = qsstats.time_series(five_year_ago, today, interval='days')
    return render_to_response('wms/graph.html', {'order_stats': values})

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')