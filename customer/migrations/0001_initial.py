# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_manager', '0001_initial'),
        ('admins', '0002_auto_20150927_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='MegaMartUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('phone', models.BigIntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MegaMart Customer',
                'verbose_name_plural': 'MegaMart Customers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('total_amount', models.FloatField()),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bill_amount', models.FloatField()),
                ('bill_date', models.DateTimeField()),
                ('branch', models.ForeignKey(to='admins.Branch')),
                ('megamartuser', models.ForeignKey(to='customer.MegaMartUser')),
            ],
            options={
                'verbose_name': 'Order Set',
                'verbose_name_plural': 'Order sets',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_set',
            field=models.ForeignKey(to='customer.OrderSet'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='product_manager.Product'),
        ),
    ]
