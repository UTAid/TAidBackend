# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taid', '0002_auto_20150618_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='practical',
            name='course',
        ),
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='teachingassistant',
            name='practicals',
        ),
        migrations.RemoveField(
            model_name='teachingassistant',
            name='tutorials',
        ),
        migrations.RemoveField(
            model_name='tutorial',
            name='course',
        ),
        migrations.AlterField(
            model_name='course',
            name='pracs',
            field=models.ManyToManyField(to='taid.Practical', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='tuts',
            field=models.ManyToManyField(to='taid.Tutorial', blank=True),
        ),
        migrations.AlterField(
            model_name='practical',
            name='ta',
            field=models.ForeignKey(to='taid.Instructor'),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='ta',
            field=models.ForeignKey(to='taid.Instructor'),
        ),
    ]
