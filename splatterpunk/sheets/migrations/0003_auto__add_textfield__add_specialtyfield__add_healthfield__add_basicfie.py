# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TextField'
        db.create_table('sheets_textfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheets.Sheet'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('sheets', ['TextField'])

        # Adding model 'SpecialtyField'
        db.create_table('sheets_specialtyfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheets.BasicField'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('sheets', ['SpecialtyField'])

        # Adding model 'HealthField'
        db.create_table('sheets_healthfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheets.Sheet'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('max', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('bashing', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('lethal', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('aggravated', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('sheets', ['HealthField'])

        # Adding model 'BasicField'
        db.create_table('sheets_basicfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheets.Sheet'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('max', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('sheets', ['BasicField'])

        # Adding model 'PointsField'
        db.create_table('sheets_pointsfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheets.Sheet'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('max', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('points', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('sheets', ['PointsField'])


    def backwards(self, orm):
        # Deleting model 'TextField'
        db.delete_table('sheets_textfield')

        # Deleting model 'SpecialtyField'
        db.delete_table('sheets_specialtyfield')

        # Deleting model 'HealthField'
        db.delete_table('sheets_healthfield')

        # Deleting model 'BasicField'
        db.delete_table('sheets_basicfield')

        # Deleting model 'PointsField'
        db.delete_table('sheets_pointsfield')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sheets.basicfield': {
            'Meta': {'object_name': 'BasicField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'max': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sheets.Sheet']"}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'sheets.healthfield': {
            'Meta': {'object_name': 'HealthField'},
            'aggravated': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'bashing': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'lethal': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'max': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sheets.Sheet']"})
        },
        'sheets.pointsfield': {
            'Meta': {'object_name': 'PointsField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'max': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'points': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sheets.Sheet']"})
        },
        'sheets.sheet': {
            'Meta': {'object_name': 'Sheet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sheets.specialtyfield': {
            'Meta': {'object_name': 'SpecialtyField'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sheets.BasicField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'sheets.textfield': {
            'Meta': {'object_name': 'TextField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sheets.Sheet']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['sheets']
