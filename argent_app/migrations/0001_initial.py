# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-08 13:30
from __future__ import unicode_literals

import argent_app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(default=argent_app.models.generate_uuid, max_length=80)),
                ('room_password', models.CharField(default='', max_length=40)),
                ('room_name', models.CharField(max_length=40)),
                ('host_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='Guest', max_length=80)),
                ('user_id', models.CharField(default=argent_app.models.generate_uuid, max_length=80)),
                ('is_temp', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='inroom',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='argent_app.User'),
        ),
        migrations.AddField(
            model_name='inroom',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='argent_app.Room'),
        ),
    ]
