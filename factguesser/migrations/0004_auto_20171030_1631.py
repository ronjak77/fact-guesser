# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-30 16:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factguesser', '0003_proposition_tosi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposition',
            name='code',
        ),
        migrations.RemoveField(
            model_name='proposition',
            name='linenos',
        ),
    ]