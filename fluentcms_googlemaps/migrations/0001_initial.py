# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import fluent_contents.models.mixins
import fluent_contents.extensions
from fluentcms_googlemaps import appsettings


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('style', models.CharField(max_length=200, verbose_name='Style', choices=appsettings.FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES)),
                ('map_type_id', models.CharField(default=b'HYBRID', max_length=50, verbose_name='Map type', choices=appsettings.FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES)),
                ('zoom', models.PositiveSmallIntegerField(default=1, verbose_name='Default zoom level')),
                ('min_zoom', models.PositiveSmallIntegerField(default=1, verbose_name='Minimum zoom level')),
                ('max_zoom', models.PositiveSmallIntegerField(default=12, verbose_name='Maximum zoom level')),
                ('center', geoposition.fields.GeopositionField(default=b'0,0', max_length=42, verbose_name='Map center')),
                ('show_clusters', models.BooleanField(default=False, verbose_name='Group nearby markers into clusters for larger zoom levels')),
            ],
            options={
                'ordering': ('title',),
                'db_table': 'contentitem_fluentcms_googlemaps_mapitem',
                'verbose_name': 'Map',
                'verbose_name_plural': 'Maps',
            },
            bases=('fluent_contents.contentitem',),
        ),
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('image', fluent_contents.extensions.PluginImageField(max_length=100, verbose_name='Image', blank=True)),
                ('description', fluent_contents.extensions.PluginHtmlField(verbose_name='Description', blank=True)),
                ('location', geoposition.fields.GeopositionField(max_length=42, verbose_name='Location')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Marker',
                'verbose_name_plural': 'Markers',
            },
            bases=(fluent_contents.models.mixins.CachedModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MarkerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('marker_image', fluent_contents.extensions.PluginImageField(max_length=100, verbose_name='Marker image')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Marker Group',
                'verbose_name_plural': 'Marker Groups',
            },
            bases=(fluent_contents.models.mixins.CachedModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='marker',
            name='group',
            field=models.ForeignKey(related_name='markers', verbose_name='Group', blank=True, to='fluentcms_googlemaps.MarkerGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mapitem',
            name='groups',
            field=models.ManyToManyField(related_name='mapitems', db_table=b'contentitem_fluentcms_googlemaps_mapitem_groups', verbose_name='Marker Groups', to='fluentcms_googlemaps.MarkerGroup'),
            preserve_default=True,
        ),
    ]
