# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctores', '0002_auto_20151109_0103'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Doctor',
            new_name='Item',
        ),
    ]
