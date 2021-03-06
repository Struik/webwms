from datetime import datetime
import json
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    sdid = models.CharField(max_length=200)
	
    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'web_client'
        
class ReferredClients(models.Model):
    id = models.IntegerField(primary_key=True)
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)

    class Meta:
        managed = False
        db_table = 'wms_referredclients'

class Sku(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Идентификатор")
    sku_id = models.CharField(max_length=200, verbose_name="Артикул")
    name = models.CharField(max_length=200, verbose_name="Наименование")
    holder = models.ForeignKey(Client, verbose_name="Владелец")
    sdid = models.CharField(max_length=200, verbose_name="Код товара")

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'web_sku'
    
class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    sdid = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
    client_name = models.CharField(max_length=200)
    date_to_ship = models.DateField()
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.display_name

    class Meta:
        managed = False
        db_table = 'web_order'

class OrderDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Order)
    line = models.IntegerField()
    sku = models.ForeignKey(Sku)
    sku_name = models.CharField(max_length=200)
    qty = models.IntegerField()
    planned = models.IntegerField()
    moved = models.IntegerField()
    packed = models.IntegerField()
    shiped = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'web_order_detail'

class Incoming(models.Model):
    id = models.IntegerField(primary_key=True)
    sdid = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
    client_name = models.CharField(max_length=200)
    date_to_ship = models.DateField()
    status = models.CharField(max_length=200)
	
    def __str__(self):
        return self.display_name

    class Meta:
        managed = False
        db_table = 'web_incoming'

class IncomingDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    incoming = models.ForeignKey(Incoming)
    line = models.IntegerField()
    sku = models.ForeignKey(Sku)
    sku_name = models.CharField(max_length=200)
    qty = models.IntegerField()
    received = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'web_incoming_detail'

class ChartType(models.Model):
    type = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    highchart_type = models.CharField(max_length=200)
    interval = models.CharField(max_length=200)

    def __str__(self):              # __unicode__ on Python 2
        return self.label

class Chartss(models.Model):
    id = models.IntegerField(primary_key=True)
    chart_name = models.CharField(max_length=200)
    view_name = models.CharField(max_length=200)
    chart_type = models.ForeignKey(ChartType)
    x_axis_label = models.CharField(max_length=200)
    y_axis_label = models.CharField(max_length=200)
    x_axis_field = models.CharField(max_length=200)
    y_axis_field = models.CharField(max_length=200)
    with_table = models.BooleanField(default=False)
    created = models.DateField(default=datetime.now)
    grouping = models.BooleanField(default=False)
    grouping_field = models.CharField(max_length=200, blank=True)
    grouping_field_label = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'wms_charts'

class DashboardGroup(models.Model):
    name = models.CharField(max_length=200)

class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    chart_model = models.CharField(max_length=2000)
    comments = models.CharField(max_length=200)
    dashboard_group = models.ForeignKey(DashboardGroup)



