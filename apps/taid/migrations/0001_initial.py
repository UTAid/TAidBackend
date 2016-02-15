# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='_UniversityMember',
            fields=[
                ('university_id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='EnrollmentListFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datafile', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Identification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='MarkFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datafile', models.FileField(upload_to=b'')),
                ('assignment', models.ForeignKey(to='taid.Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Practical',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('total', models.DecimalField(max_digits=6, decimal_places=2)),
                ('assignment', models.ForeignKey(to='taid.Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='StudentListFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datafile', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='TAidEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='schedule.Event')),
            ],
            bases=('schedule.event',),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('event', models.ForeignKey(to='taid.TAidEvent')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('_universitymember_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid._UniversityMember')),
                ('student_number', models.CharField(max_length=10, blank=True)),
            ],
            bases=('taid._universitymember',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('_universitymember_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid._UniversityMember')),
            ],
            bases=('taid._universitymember',),
        ),
        migrations.AddField(
            model_name='practical',
            name='event',
            field=models.ForeignKey(to='taid.TAidEvent'),
        ),
        migrations.AddField(
            model_name='mark',
            name='rubric',
            field=models.ForeignKey(to='taid.Rubric'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='rubric_entries',
            field=models.ManyToManyField(related_name='rubric_entries', to='taid.Rubric', blank=True),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('teacher_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid.Teacher')),
            ],
            bases=('taid.teacher',),
        ),
        migrations.CreateModel(
            name='TeachingAssistant',
            fields=[
                ('teacher_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid.Teacher')),
            ],
            bases=('taid.teacher',),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='students',
            field=models.ManyToManyField(to='taid.Student', blank=True),
        ),
        migrations.AddField(
            model_name='practical',
            name='students',
            field=models.ManyToManyField(to='taid.Student', blank=True),
        ),
        migrations.AddField(
            model_name='mark',
            name='student',
            field=models.ForeignKey(to='taid.Student'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='students',
            field=models.ManyToManyField(to='taid.Student', blank=True),
        ),
        migrations.AddField(
            model_name='identification',
            name='student',
            field=models.ForeignKey(to='taid.Student'),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='ta',
            field=models.ManyToManyField(to='taid.TeachingAssistant', verbose_name=b'Teaching Assistant(s)', blank=True),
        ),
        migrations.AddField(
            model_name='practical',
            name='ta',
            field=models.ManyToManyField(to='taid.TeachingAssistant', verbose_name=b'Teaching Assistant(s)', blank=True),
        ),
        migrations.AddField(
            model_name='lecture',
            name='instructors',
            field=models.ManyToManyField(to='taid.Instructor', blank=True),
        ),
    ]
