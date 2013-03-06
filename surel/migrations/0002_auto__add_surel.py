# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Surel'
        db.create_table('surel_surel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.TextField')()),
            ('recipient', self.gf('django.db.models.fields.TextField')()),
            ('body_plain', self.gf('django.db.models.fields.TextField')()),
            ('diterima', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('surel', ['Surel'])


    def backwards(self, orm):
        # Deleting model 'Surel'
        db.delete_table('surel_surel')


    models = {
        'surel.surel': {
            'Meta': {'object_name': 'Surel'},
            'body_plain': ('django.db.models.fields.TextField', [], {}),
            'diterima': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.TextField', [], {}),
            'sender': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['surel']