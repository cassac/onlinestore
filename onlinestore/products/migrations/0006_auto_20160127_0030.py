# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 00:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20160126_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size')], default='color', max_length=120),
        ),
    ]
