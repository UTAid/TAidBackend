# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('course', models.ForeignKey(to='taid.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('course', models.ForeignKey(to='taid.Course')),
            ],
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
            ],
            bases=('taid._person',),
        ),
        migrations.AddField(
            model_name='identification',
            name='person',
            field=models.ForeignKey(to='taid._Person'),
        ),
        migrations.AddField(
            model_name='course',
            name='pracs',
            field=models.ManyToManyField(related_name='course_pracs', to='taid.Practical'),
        ),
        migrations.AddField(
            model_name='course',
            name='tuts',
            field=models.ManyToManyField(related_name='course_tuts', to='taid.Tutorial'),
        ),
        migrations.AddField(
            model_name='_person',
            name='ids',
            field=models.ManyToManyField(to='taid.Identification'),
        ),
        migrations.CreateModel(
            name='TeachingAssistant',
            fields=[
                ('instructor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='taid.Instructor')),
                ('practicals', models.ManyToManyField(to='taid.Practical')),
            ],
            bases=('taid.instructor',),
        ),
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(to='taid.Course'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='courses',
            field=models.ManyToManyField(to='taid.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(to='taid.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='taid.Student'),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='ta',
            field=models.ForeignKey(to='taid.TeachingAssistant'),
        ),
        migrations.AddField(
            model_name='teachingassistant',
            name='tutorials',
            field=models.ManyToManyField(to='taid.Tutorial'),
        ),
        migrations.AddField(
            model_name='practical',
            name='ta',
            field=models.ForeignKey(to='taid.TeachingAssistant'),
        ),
    ]
