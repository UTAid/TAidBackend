# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('taid', '0004_auto_20150708_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='calendar',
            field=models.ForeignKey(default=0, to='schedule.Calendar'),
            preserve_default=False,
        ),
    ]
