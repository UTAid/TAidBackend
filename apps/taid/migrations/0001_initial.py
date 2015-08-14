# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
                ('total', models.DecimalField(max_digits=6, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=254)),
                ('section_code', models.CharField(max_length=1, choices=[(b'F', b'Fall (First)'), (b'W', b'Winter (Second)'), (b'Y', b'Year (Both)')])),
                ('lecture_session', models.CharField(max_length=2, choices=[(b'FW', b'Fall and Winter'), (b'S', b'Summer')])),
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
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=6, decimal_places=3)),
                ('assignment', models.ForeignKey(to='taid.Assignment')),
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
            model_name='assignment',
            name='marks',
            field=models.ManyToManyField(related_name='student_marks', to='taid.Mark', blank=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='parent',
            field=models.ForeignKey(related_name='subparts', blank=True, to='taid.Assignment', null=True),
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
            model_name='mark',
            name='student',
            field=models.ForeignKey(to='taid.Student'),
        ),
        migrations.AddField(
            model_name='identification',
            name='student',
            field=models.ForeignKey(to='taid.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='taid.Student', blank=True),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='ta',
            field=models.ManyToManyField(to='taid.TeachingAssistant'),
        ),
        migrations.AddField(
            model_name='practical',
            name='ta',
            field=models.ManyToManyField(to='taid.TeachingAssistant'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(to='taid.Instructor', blank=True),
        ),
    ]
