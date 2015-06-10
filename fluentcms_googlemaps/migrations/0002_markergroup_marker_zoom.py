# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluentcms_googlemaps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='markergroup',
            name='marker_zoom',
            field=models.PositiveSmallIntegerField(default=7, verbose_name='Zoom level on click'),
            preserve_default=True,
        ),
    ]
