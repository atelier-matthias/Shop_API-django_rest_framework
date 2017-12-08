# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 15:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20171206_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('order_product_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='ShopBucket',
            fields=[
                ('bucket_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('customer_uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_uuid', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.Product')),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='created',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='paid',
            new_name='date_paid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_uuid',
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='order_uuid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Order'),
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='product_uuid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.Product'),
        ),
    ]