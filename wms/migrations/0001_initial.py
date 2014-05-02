# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('wms_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wms_id', self.gf('django.db.models.fields.IntegerField')()),
            ('is_holder', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('wms', ['Client'])

        # Adding model 'ReferredClients'
        db.create_table('wms_referredclients', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Client'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('wms', ['ReferredClients'])

        # Adding model 'Sku'
        db.create_table('wms_sku', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('holder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Client'])),
        ))
        db.send_create_signal('wms', ['Sku'])

        # Adding model 'Order'
        db.create_table('wms_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('holder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Client'])),
        ))
        db.send_create_signal('wms', ['Order'])

        # Adding model 'OrderDetail'
        db.create_table('wms_orderdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Order'])),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Sku'])),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('wms', ['OrderDetail'])

        # Adding model 'Incoming'
        db.create_table('wms_incoming', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('holder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Client'])),
        ))
        db.send_create_signal('wms', ['Incoming'])

        # Adding model 'IncomingDetail'
        db.create_table('wms_incomingdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Incoming'])),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wms.Sku'])),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('wms', ['IncomingDetail'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('wms_client')

        # Deleting model 'ReferredClients'
        db.delete_table('wms_referredclients')

        # Deleting model 'Sku'
        db.delete_table('wms_sku')

        # Deleting model 'Order'
        db.delete_table('wms_order')

        # Deleting model 'OrderDetail'
        db.delete_table('wms_orderdetail')

        # Deleting model 'Incoming'
        db.delete_table('wms_incoming')

        # Deleting model 'IncomingDetail'
        db.delete_table('wms_incomingdetail')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wms.client': {
            'Meta': {'object_name': 'Client'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_holder': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wms_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'wms.incoming': {
            'Meta': {'object_name': 'Incoming'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'wms.incomingdetail': {
            'Meta': {'object_name': 'IncomingDetail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Incoming']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Sku']"}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        },
        'wms.order': {
            'Meta': {'object_name': 'Order'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'wms.orderdetail': {
            'Meta': {'object_name': 'OrderDetail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Order']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Sku']"}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        },
        'wms.referredclients': {
            'Meta': {'object_name': 'ReferredClients'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"})
        },
        'wms.sku': {
            'Meta': {'object_name': 'Sku'},
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wms.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sku_id': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['wms']