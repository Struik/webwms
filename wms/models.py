import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=200)
    wms_id = models.IntegerField()
    is_holder = models.CharField(max_length=200)
	
    def __str__(self):
        return self.name
        
class ReferredClients(models.Model):
    user = models.ForeignKey(Client)
    client = models.ForeignKey(User)
    
class Sku(models.Model):
    sku_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
	
    def __str__(self):
        return self.name
    
class Order(models.Model):
    display_name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
	
    def __str__(self):
        return self.display_name

class OrderDetail(models.Model):
    order = models.ForeignKey(Order)
    sku = models.ForeignKey(Sku)
    units = models.IntegerField()
    
class Incoming(models.Model):
    display_name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
	
    def __str__(self):
        return self.display_name

class IncomingDetail(models.Model):
    inc = models.ForeignKey(Incoming)
    sku = models.ForeignKey(Sku)
    units = models.IntegerField()