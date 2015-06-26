# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taid', '0003_auto_20150618_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('total', models.DecimalField(max_digits=6, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='GradeDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('value', models.DecimalField(max_digits=6, decimal_places=3)),
                ('assignment', models.ForeignKey(to='taid.Assignment')),
                ('parent', models.ForeignKey(related_name='subdefinitions', blank=True, to='taid.GradeDefinition', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('definitions', models.ManyToManyField(to='taid.GradeDefinition', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=6, decimal_places=3)),
                ('assignment', models.ForeignKey(to='taid.Assignment')),
                ('student', models.ForeignKey(to='taid.Student')),
            ],
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
    ]
