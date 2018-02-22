# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 00:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_serviceatlocation'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceatlocation',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service'),
        ),
        migrations.AddField(
            model_name='location',
            name='services',
            field=models.ManyToManyField(related_name='locations', through='locations.ServiceAtLocation', to='services.Service'),
        ),
    ]