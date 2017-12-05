# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('cash', 'cash'), ('payu', 'payu'), ('card', 'card')], default='cash', max_length=20),
        ),
    ]
