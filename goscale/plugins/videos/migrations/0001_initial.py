# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'YouKu'
        db.create_table('cmsplugin_youku', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('playlist', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('videos', ['YouKu'])

        # Adding M2M table for field posts on 'YouKu'
        db.create_table('videos_youku_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('youku', models.ForeignKey(orm['videos.youku'], null=False)),
            ('post', models.ForeignKey(orm['goscale.post'], null=False))
        ))
        db.create_unique('videos_youku_posts', ['youku_id', 'post_id'])


    def backwards(self, orm):
        # Deleting model 'YouKu'
        db.delete_table('cmsplugin_youku')

        # Removing M2M table for field posts on 'YouKu'
        db.delete_table('videos_youku_posts')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 3, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
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
        },
        'videos.youku': {
            'Meta': {'object_name': 'YouKu', 'db_table': "'cmsplugin_youku'"},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'playlist': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['goscale.Post']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['videos']