# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='_person',
            name='ids',
        ),
        migrations.RemoveField(
            model_name='identification',
            name='person',
        ),
        migrations.AddField(
            model_name='student',
            name='ids',
            field=models.ManyToManyField(to='taid.Identification', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(to='taid.Instructor', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='pracs',
            field=models.ManyToManyField(related_name='course_pracs', to='taid.Practical', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='taid.Student', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='tuts',
            field=models.ManyToManyField(related_name='course_tuts', to='taid.Tutorial', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='courses',
            field=models.ManyToManyField(to='taid.Course', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(to='taid.Course', blank=True),
        ),
        migrations.AlterField(
            model_name='teachingassistant',
            name='practicals',
            field=models.ManyToManyField(to='taid.Practical', blank=True),
        ),
        migrations.AlterField(
            model_name='teachingassistant',
            name='tutorials',
            field=models.ManyToManyField(to='taid.Tutorial', blank=True),
        ),
    ]
