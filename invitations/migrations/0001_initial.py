# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('text', models.TextField(blank=True, max_length=1000)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.EmailField(max_length=254)),
                ('event', models.ForeignKey(to='events.Event')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
