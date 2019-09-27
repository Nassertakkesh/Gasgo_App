# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-24 22:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GasgoApp', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='GasgoApp.Driver'),
        ),
    ]
