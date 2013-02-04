# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Speakerdeck'
        db.create_table('cmsplugin_speakerdeck', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('embed', self.gf('django.db.models.fields.TextField')()),
            ('width', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('ratio', self.gf('django.db.models.fields.CharField')(default='4:3', max_length=50, null=True, blank=True)),
            ('embed_as_is', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('presentations', ['Speakerdeck'])

        # Adding M2M table for field posts on 'Speakerdeck'
        db.create_table('presentations_speakerdeck_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('speakerdeck', models.ForeignKey(orm['presentations.speakerdeck'], null=False)),
            ('post', models.ForeignKey(orm['goscale.post'], null=False))
        ))
        db.create_unique('presentations_speakerdeck_posts', ['speakerdeck_id', 'post_id'])

        # Adding model 'Slideshare'
        db.create_table('cmsplugin_slideshare', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('embed', self.gf('django.db.models.fields.TextField')()),
            ('width', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('ratio', self.gf('django.db.models.fields.CharField')(default='4:3', max_length=50, null=True, blank=True)),
            ('embed_as_is', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('without_related_content', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('presentations', ['Slideshare'])

        # Adding M2M table for field posts on 'Slideshare'
        db.create_table('presentations_slideshare_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('slideshare', models.ForeignKey(orm['presentations.slideshare'], null=False)),
            ('post', models.ForeignKey(orm['goscale.post'], null=False))
        ))
        db.create_unique('presentations_slideshare_posts', ['slideshare_id', 'post_id'])

        # Adding model 'GooglePresentation'
        db.create_table('cmsplugin_googlepresentation', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('embed', self.gf('django.db.models.fields.TextField')()),
            ('width', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('ratio', self.gf('django.db.models.fields.CharField')(default='4:3', max_length=50, null=True, blank=True)),
            ('embed_as_is', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delay', self.gf('django.db.models.fields.SmallIntegerField')(default=3000)),
            ('autoplay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loop', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('presentations', ['GooglePresentation'])

        # Adding M2M table for field posts on 'GooglePresentation'
        db.create_table('presentations_googlepresentation_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('googlepresentation', models.ForeignKey(orm['presentations.googlepresentation'], null=False)),
            ('post', models.ForeignKey(orm['goscale.post'], null=False))
        ))
        db.create_unique('presentations_googlepresentation_posts', ['googlepresentation_id', 'post_id'])


    def backwards(self, orm):
        # Deleting model 'Speakerdeck'
        db.delete_table('cmsplugin_speakerdeck')

        # Removing M2M table for field posts on 'Speakerdeck'
        db.delete_table('presentations_speakerdeck_posts')

        # Deleting model 'Slideshare'
        db.delete_table('cmsplugin_slideshare')

        # Removing M2M table for field posts on 'Slideshare'
        db.delete_table('presentations_slideshare_posts')

        # Deleting model 'GooglePresentation'
        db.delete_table('cmsplugin_googlepresentation')

        # Removing M2M table for field posts on 'GooglePresentation'
        db.delete_table('presentations_googlepresentation_posts')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 4, 0, 0)'}),
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
        'goscale.post': {
            'Meta': {'object_name': 'Post'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
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
        'presentations.googlepresentation': {
            'Meta': {'object_name': 'GooglePresentation', 'db_table': "'cmsplugin_googlepresentation'"},
            'autoplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'delay': ('django.db.models.fields.SmallIntegerField', [], {'default': '3000'}),
            'embed': ('django.db.models.fields.TextField', [], {}),
            'embed_as_is': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['goscale.Post']", 'symmetrical': 'False'}),
            'ratio': ('django.db.models.fields.CharField', [], {'default': "'4:3'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'presentations.slideshare': {
            'Meta': {'object_name': 'Slideshare', 'db_table': "'cmsplugin_slideshare'"},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'embed': ('django.db.models.fields.TextField', [], {}),
            'embed_as_is': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['goscale.Post']", 'symmetrical': 'False'}),
            'ratio': ('django.db.models.fields.CharField', [], {'default': "'4:3'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'without_related_content': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'presentations.speakerdeck': {
            'Meta': {'object_name': 'Speakerdeck', 'db_table': "'cmsplugin_speakerdeck'"},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'embed': ('django.db.models.fields.TextField', [], {}),
            'embed_as_is': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['goscale.Post']", 'symmetrical': 'False'}),
            'ratio': ('django.db.models.fields.CharField', [], {'default': "'4:3'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['presentations']