# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('taid', '0003_auto_20150618_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='practical',
            name='event',
            field=models.ForeignKey(default=0, to='schedule.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tutorial',
            name='event',
            field=models.ForeignKey(default=0, to='schedule.Event'),
            preserve_default=False,
        ),
    ]
