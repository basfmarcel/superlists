# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-06-19 14:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("lists", "0007_list_shared_with")]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="shared_with",
            field=models.ManyToManyField(
                null=True, related_name="shared_with", to=settings.AUTH_USER_MODEL
            ),
        )
    ]
