# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_providers', '0004_auto_20171103_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovidertranslation',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]