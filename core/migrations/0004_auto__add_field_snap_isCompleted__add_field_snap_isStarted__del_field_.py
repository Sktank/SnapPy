# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Snap.isCompleted'
        db.add_column(u'core_snap', 'isCompleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Snap.isStarted'
        db.add_column(u'core_snap', 'isStarted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Lesson.isCompleted'
        db.delete_column(u'core_lesson', 'isCompleted')

        # Deleting field 'Lesson.isStarted'
        db.delete_column(u'core_lesson', 'isStarted')


    def backwards(self, orm):
        # Deleting field 'Snap.isCompleted'
        db.delete_column(u'core_snap', 'isCompleted')

        # Deleting field 'Snap.isStarted'
        db.delete_column(u'core_snap', 'isStarted')

        # Adding field 'Lesson.isCompleted'
        db.add_column(u'core_lesson', 'isCompleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Lesson.isStarted'
        db.add_column(u'core_lesson', 'isStarted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'students'", 'symmetrical': 'False', 'to': u"orm['core.WebUser']"}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teachers'", 'symmetrical': 'False', 'to': u"orm['core.WebUser']"})
        },
        u'core.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WebUser']"})
        },
        u'core.snap': {
            'Meta': {'object_name': 'Snap'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCompleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isStarted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Lesson']"}),
            'stuff': ('django.db.models.fields.TextField', [], {})
        },
        u'core.webuser': {
            'LastName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'Meta': {'object_name': 'WebUser'},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userId': ('django.db.models.fields.IntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['core']