# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='_Person',
            fields=[
                ('utorid', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=254)),
                ('section', models.CharField(max_length=1, choices=[(b'F', b'Fall (First)'), (b'W', b'Winter (Second)'), (b'Y', b'Year (Both)')])),
                ('session', models.CharField(max_length=2, choices=[(b'FW', b'Fall and Winter'), (b'S', b'Summer')])),
                ('calendar', models.ForeignKey(to='schedule.Calendar')),
            ],
        ),
        migrations.CreateModel(
            name='Identification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=500)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Practical',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='schedule.Event')),
            ],
            bases=('schedule.event',),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='schedule.Event')),
            ],
            bases=('schedule.event',),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('_person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid._Person')),
            ],
            bases=('taid._person',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('_person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid._Person')),
                ('number', models.PositiveIntegerField()),
                ('ids', models.ManyToManyField(to='taid.Identification', blank=True)),
            ],
            bases=('taid._person',),
        ),
        migrations.AddField(
            model_name='course',
            name='pracs',
            field=models.ManyToManyField(to='taid.Practical', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='tuts',
            field=models.ManyToManyField(to='taid.Tutorial', blank=True),
        ),
        migrations.CreateModel(
            name='TeachingAssistant',
            fields=[
                ('instructor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid.Instructor')),
            ],
            bases=('taid.instructor',),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='ta',
            field=models.ForeignKey(to='taid.Instructor'),
        ),
        migrations.AddField(
            model_name='practical',
            name='ta',
            field=models.ForeignKey(to='taid.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(to='taid.Instructor', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='taid.Student', blank=True),
        ),
    ]
