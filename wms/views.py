from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template import RequestContext, loader, Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth.models import User

@login_required
def index(request):
    return render_to_response('wms/main.html')

@login_required
def main(request):
    return render_to_response('wms/main.html', context_instance=RequestContext(request))
	
@login_required
def client(request):
    return render_to_response('wms/client.html', context_instance=RequestContext(request))
	
@login_required
def sku(request):
    return render_to_response('wms/sku.html', context_instance=RequestContext(request))
	
@login_required
def order(request):
    return render_to_response('wms/order.html', context_instance=RequestContext(request))
	
@login_required
def incoming(request):
    return render_to_response('wms/incoming.html', context_instance=RequestContext(request))
	
def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')