# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table(u'core_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grade', self.gf('django.db.models.fields.IntegerField')()),
            ('age', self.gf('django.db.models.fields.IntegerField')()),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('LastName', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'core', ['Student'])

        # Adding model 'Teacher'
        db.create_table(u'core_teacher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('LastName', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'core', ['Teacher'])

        # Adding model 'Course'
        db.create_table(u'core_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('teachers', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Teacher'])),
            ('students', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Student'])),
        ))
        db.send_create_signal(u'core', ['Course'])

        # Adding model 'Lesson'
        db.create_table(u'core_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('isCompleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isStarted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('difficulty', self.gf('django.db.models.fields.IntegerField')()),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Teacher'], unique=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Student'], unique=True)),
        ))
        db.send_create_signal(u'core', ['Lesson'])

        # Adding model 'Snap'
        db.create_table(u'core_snap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stuff', self.gf('django.db.models.fields.TextField')()),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Lesson'], unique=True)),
        ))
        db.send_create_signal(u'core', ['Snap'])


    def backwards(self, orm):
        # Deleting model 'Student'
        db.delete_table(u'core_student')

        # Deleting model 'Teacher'
        db.delete_table(u'core_teacher')

        # Deleting model 'Course'
        db.delete_table(u'core_course')

        # Deleting model 'Lesson'
        db.delete_table(u'core_lesson')

        # Deleting model 'Snap'
        db.delete_table(u'core_snap')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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