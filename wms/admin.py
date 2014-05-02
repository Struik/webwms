from django.contrib import admin
from wms.models import Client, ReferredClients, Sku, Order, OrderDetail, Incoming, IncomingDetail

class RefClientInline(admin.TabularInline):
    model = ReferredClients
    extra = 1
	
class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None, 				 {'fields': ['wms_id']}),
        (None, 				 {'fields': ['is_holder']}),
    ]
    list_display = ('name', 'wms_id', 'is_holder')
    list_filter = ['name']
    search_fields = ['name']
    inlines = [RefClientInline]
	
class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 5
	
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['display_name']}),
        (None, 				 {'fields': ['holder']}),
    ]
    inlines = [OrderDetailInline]
	
class IncomingDetailInline(admin.TabularInline):
    model = IncomingDetail
    extra = 5
	
class IncomingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['display_name']}),
        (None, 				 {'fields': ['holder']}),
    ]
    inlines = [IncomingDetailInline]

admin.site.register(Client, ClientAdmin)
admin.site.register(Sku)
admin.site.register(Order, OrderAdmin)
admin.site.register(Incoming, IncomingAdmin)

# Register your models here.
