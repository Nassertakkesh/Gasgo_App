# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-24 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GasgoApp', '0004_auto_20190924_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='gallons',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(blank=True, choices=[('87', 'Unleaded'), ('89', 'Plus'), ('91', 'Premium')], max_length=15, null=True),
        ),
    ]
