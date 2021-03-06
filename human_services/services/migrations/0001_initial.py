# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 00:46
from __future__ import unicode_literals

import common.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import parler.models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0002_auto_20171214_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', common.models.RequiredCharField(max_length=200, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')])),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='organizations.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(common.models.ValidateOnSaveMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ServiceTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='services.Service')),
            ],
            options={
                'verbose_name': 'service Translation',
                'db_table': 'services_service_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='servicetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
