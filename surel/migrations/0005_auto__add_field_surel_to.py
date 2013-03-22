# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Surel.to'
        db.add_column('surel_surel', 'to',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Surel.to'
        db.delete_column('surel_surel', 'to')


    models = {
        'surel.notifikasidikirim': {
            'Meta': {'object_name': 'NotifikasiDikirim'},
            'dikirim': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isi': ('django.db.models.fields.TextField', [], {}),
            'judul': ('django.db.models.fields.CharField', [], {'max_length': '141'}),
            'tujuan': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
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
            'sender': ('django.db.models.fields.TextField', [], {}),
            'to': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['surel']