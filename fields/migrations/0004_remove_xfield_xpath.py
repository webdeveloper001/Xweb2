# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 02:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0003_url_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xfield',
            name='xpath',
        ),
    ]