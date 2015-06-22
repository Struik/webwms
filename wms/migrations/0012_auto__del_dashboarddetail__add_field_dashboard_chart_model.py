# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DashboardDetail'
        db.delete_table('wms_dashboarddetail')

        # Adding field 'Dashboard.chart_model'
        db.add_column('wms_dashboard', 'chart_model',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=2000),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'DashboardDetail'
        db.create_table('wms_dashboarddetail', (
            ('dashboard_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Dashboard'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chart_model', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('wms', ['DashboardDetail'])

        # Deleting field 'Dashboard.chart_model'
        db.delete_column('wms_dashboard', 'chart_model')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wms.chartss': {
            'Meta': {'db_table': "'wms_charts'", 'object_name': 'Chartss'},
            'chart_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'chart_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.ChartType']"}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'grouping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grouping_field': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'grouping_field_label': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'view_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'with_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'x_axis_field': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'x_axis_label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'y_axis_field': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'y_axis_label': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.charttype': {
            'Meta': {'object_name': 'ChartType'},
            'highchart_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.client': {
            'Meta': {'managed': 'False', 'db_table': "'web_client'", 'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'chart_model': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dashboard_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.DashboardGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.dashboardgroup': {
            'Meta': {'object_name': 'DashboardGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.incoming': {
            'Meta': {'managed': 'False', 'db_table': "'web_incoming'", 'object_name': 'Incoming'},
            'client_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date_to_ship': ('django.db.models.fields.DateField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.incomingdetail': {
            'Meta': {'managed': 'False', 'db_table': "'web_incoming_detail'", 'object_name': 'IncomingDetail'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'incoming': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Incoming']"}),
            'line': ('django.db.models.fields.IntegerField', [], {}),
            'qty': ('django.db.models.fields.IntegerField', [], {}),
            'received': ('django.db.models.fields.IntegerField', [], {}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Sku']"}),
            'sku_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.order': {
            'Meta': {'managed': 'False', 'db_table': "'web_order'", 'object_name': 'Order'},
            'client_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date_to_ship': ('django.db.models.fields.DateField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.orderdetail': {
            'Meta': {'managed': 'False', 'db_table': "'web_order_detail'", 'object_name': 'OrderDetail'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.IntegerField', [], {}),
            'moved': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Order']"}),
            'packed': ('django.db.models.fields.IntegerField', [], {}),
            'planned': ('django.db.models.fields.IntegerField', [], {}),
            'qty': ('django.db.models.fields.IntegerField', [], {}),
            'shiped': ('django.db.models.fields.IntegerField', [], {}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Sku']"}),
            'sku_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.referredclients': {
            'Meta': {'managed': 'False', 'object_name': 'ReferredClients'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'wms.sku': {
            'Meta': {'managed': 'False', 'db_table': "'web_sku'", 'object_name': 'Sku'},
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sku_id': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['wms']