# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Student.user_id'
        db.add_column(u'core_student', 'user_id',
                      self.gf('django.db.models.fields.IntegerField')(default=-1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Student.user_id'
        db.delete_column(u'core_student', 'user_id')


    models = {
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'students': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Student']"}),
            'teachers': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Teacher']"})
        },
        u'core.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCompleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isStarted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Student']", 'unique': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Teacher']", 'unique': 'True'})
        },
        u'core.snap': {
            'Meta': {'object_name': 'Snap'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Lesson']", 'unique': 'True'}),
            'stuff': ('django.db.models.fields.TextField', [], {})
        },
        u'core.student': {
            'LastName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'Meta': {'object_name': 'Student'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'grade': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.teacher': {
            'LastName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'Meta': {'object_name': 'Teacher'},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']