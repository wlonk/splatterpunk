# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sheet'
        db.create_table('sheets_sheet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sheets', ['Sheet'])


    def backwards(self, orm):
        # Deleting model 'Sheet'
        db.delete_table('sheets_sheet')


    models = {
        'sheets.sheet': {
            'Meta': {'object_name': 'Sheet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['sheets']