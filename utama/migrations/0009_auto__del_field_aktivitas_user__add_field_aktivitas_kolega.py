# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Aktivitas.user'
        db.delete_column('utama_aktivitas', 'user_id')

        # Adding field 'Aktivitas.kolega'
        db.add_column('utama_aktivitas', 'kolega',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['utama.Kolega']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Aktivitas.user'
        db.add_column('utama_aktivitas', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Aktivitas.kolega'
        db.delete_column('utama_aktivitas', 'kolega_id')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'utama.aktivitas': {
            'Meta': {'object_name': 'Aktivitas'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kolega': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utama.Kolega']"}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'selesai': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'utama.kolega': {
            'Meta': {'object_name': 'Kolega'},
            'alamat': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ditambahkan': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kode': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organisasi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utama.Organisasi']"}),
            'tanggal_lahir': ('django.db.models.fields.DateField', [], {'null': "'True'", 'blank': "'True'"}),
            'telepon': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'utama.organisasi': {
            'Meta': {'object_name': 'Organisasi'},
            'aktif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anggota': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'through': "orm['utama.Status']", 'blank': 'True'}),
            'bergabung': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jenis': ('django.db.models.fields.CharField', [], {'default': "u'perunggu'", 'max_length': '10'}),
            'kode': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'utama.poinkontak': {
            'Meta': {'object_name': 'PoinKontak'},
            'aktivitas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utama.Aktivitas']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kolega': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utama.Kolega']"}),
            'kontak': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'waktu': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'utama.profil': {
            'Meta': {'object_name': 'Profil'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'panggilan': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'utama.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'masuk': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'organisasi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utama.Organisasi']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'anggota'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['utama']