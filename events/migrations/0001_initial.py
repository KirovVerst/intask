# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('is_public', models.BooleanField(default=False)),
                ('event_header', models.ForeignKey(related_name='event_header', default=None, to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('is_public', models.BooleanField(default=False)),
                ('event', models.ForeignKey(to='events.Event')),
                ('task_header', models.ForeignKey(related_name='task_header', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(to='events.Task'),
        ),
    ]
