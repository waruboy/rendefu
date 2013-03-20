# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NotifikasiTunda'
        db.create_table('surel_notifikasitunda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tujuan', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('judul', self.gf('django.db.models.fields.CharField')(max_length=141)),
            ('isi', self.gf('django.db.models.fields.TextField')()),
            ('dibuat', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('surel', ['NotifikasiTunda'])


    def backwards(self, orm):
        # Deleting model 'NotifikasiTunda'
        db.delete_table('surel_notifikasitunda')


    models = {
        'surel.notifikasitunda': {
            'Meta': {'object_name': 'NotifikasiTunda'},
            'dibuat': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isi': ('django.db.models.fields.TextField', [], {}),
            'judul': ('django.db.models.fields.CharField', [], {'max_length': '141'}),
            'tujuan': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
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