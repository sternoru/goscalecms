# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataSource'
        db.create_table('goscale_datasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('attributes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('goscale', ['DataSource'])

        # Adding model 'Post'
        db.create_table('goscale_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['goscale.DataSource'])),
            ('link', self.gf('django.db.models.fields.URLField')(db_index=True, max_length=200, null=True, blank=True)),
            ('permalink', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=250, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=250, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=250, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('categories', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=250, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attributes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('goscale', ['Post'])


    def backwards(self, orm):
        # Deleting model 'DataSource'
        db.delete_table('goscale_datasource')

        # Deleting model 'Post'
        db.delete_table('goscale_post')


    models = {
        'goscale.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'goscale.post': {
            'Meta': {'object_name': 'Post'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'data_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['goscale.DataSource']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'permalink': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['goscale']