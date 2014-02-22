# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebUser'
        db.create_table(u'core_webuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userId', self.gf('django.db.models.fields.IntegerField')()),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('LastName', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'core', ['WebUser'])

        # Adding model 'Course'
        db.create_table(u'core_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Course'])

        # Adding M2M table for field teachers on 'Course'
        m2m_table_name = db.shorten_name(u'core_course_teachers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'core.course'], null=False)),
            ('webuser', models.ForeignKey(orm[u'core.webuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'webuser_id'])

        # Adding M2M table for field students on 'Course'
        m2m_table_name = db.shorten_name(u'core_course_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'core.course'], null=False)),
            ('webuser', models.ForeignKey(orm[u'core.webuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'webuser_id'])

        # Adding model 'Lesson'
        db.create_table(u'core_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('isCompleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isStarted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('difficulty', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.WebUser'], unique=True)),
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
        # Deleting model 'WebUser'
        db.delete_table(u'core_webuser')

        # Deleting model 'Course'
        db.delete_table(u'core_course')

        # Removing M2M table for field teachers on 'Course'
        db.delete_table(db.shorten_name(u'core_course_teachers'))

        # Removing M2M table for field students on 'Course'
        db.delete_table(db.shorten_name(u'core_course_students'))

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
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'students'", 'symmetrical': 'False', 'to': u"orm['core.WebUser']"}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teachers'", 'symmetrical': 'False', 'to': u"orm['core.WebUser']"})
        },
        u'core.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCompleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isStarted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WebUser']", 'unique': 'True'})
        },
        u'core.snap': {
            'Meta': {'object_name': 'Snap'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Lesson']", 'unique': 'True'}),
            'stuff': ('django.db.models.fields.TextField', [], {})
        },
        u'core.webuser': {
            'LastName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'Meta': {'object_name': 'WebUser'},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userId': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']