# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Charts'
        db.delete_table('wms_charts')

        # Adding model 'Chartss'
        db.create_table('wms_charts', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('chart_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('view_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('chart_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.ChartType'])),
            ('x_axis_label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('y_axis_label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('x_axis_field', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('y_axis_field', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('with_table', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('grouping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('grouping_field', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('grouping_field_label', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('wms', ['Chartss'])


    def backwards(self, orm):
        # Adding model 'Charts'
        db.create_table('wms_charts', (
            ('y_axis_field', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('x_axis_field', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('x_axis_label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('y_axis_label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('with_table', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chart_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.ChartType'])),
            ('view_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('chart_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('wms', ['Charts'])

        # Deleting model 'Chartss'
        db.delete_table('wms_charts')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wms.chartss': {
            'Meta': {'object_name': 'Chartss', 'db_table': "'wms_charts'"},
            'chart_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'chart_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.ChartType']"}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'grouping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grouping_field': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'grouping_field_label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'Meta': {'object_name': 'Client', 'db_table': "'web_client'", 'managed': 'False'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.incoming': {
            'Meta': {'object_name': 'Incoming', 'db_table': "'web_incoming'", 'managed': 'False'},
            'client_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date_to_ship': ('django.db.models.fields.DateField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.incomingdetail': {
            'Meta': {'object_name': 'IncomingDetail', 'db_table': "'web_incoming_detail'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'incoming': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Incoming']"}),
            'line': ('django.db.models.fields.IntegerField', [], {}),
            'qty': ('django.db.models.fields.IntegerField', [], {}),
            'received': ('django.db.models.fields.IntegerField', [], {}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Sku']"}),
            'sku_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.order': {
            'Meta': {'object_name': 'Order', 'db_table': "'web_order'", 'managed': 'False'},
            'client_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date_to_ship': ('django.db.models.fields.DateField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wms.orderdetail': {
            'Meta': {'object_name': 'OrderDetail', 'db_table': "'web_order_detail'", 'managed': 'False'},
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
            'Meta': {'object_name': 'ReferredClients', 'managed': 'False'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'wms.sku': {
            'Meta': {'object_name': 'Sku', 'db_table': "'web_sku'", 'managed': 'False'},
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sdid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sku_id': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['wms']