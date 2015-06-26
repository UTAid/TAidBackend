# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taid', '0004_assignment_grade_gradedefinition_gradefile_mark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mark',
            old_name='grade',
            new_name='gradefile',
        ),
        migrations.AddField(
            model_name='grade',
            name='marks',
            field=models.ManyToManyField(to='taid.Mark'),
        ),
    ]
