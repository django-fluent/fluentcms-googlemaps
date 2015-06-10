# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MarkerGroup.marker_zoom'
        db.add_column(u'fluentcms_googlemaps_markergroup', 'marker_zoom',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=7),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MarkerGroup.marker_zoom'
        db.delete_column(u'fluentcms_googlemaps_markergroup', 'marker_zoom')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fluent_contents.contentitem': {
            'Meta': {'ordering': "('placeholder', 'sort_order')", 'object_name': 'ContentItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'db_index': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contentitems'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['fluent_contents.Placeholder']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_fluent_contents.contentitem_set+'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        'fluent_contents.placeholder': {
            'Meta': {'unique_together': "(('parent_type', 'parent_id', 'slot'),)", 'object_name': 'Placeholder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'slot': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'fluentcms_googlemaps.mapitem': {
            'Meta': {'ordering': "('title',)", 'object_name': 'MapItem', 'db_table': "u'contentitem_fluentcms_googlemaps_mapitem'", '_ormbases': ['fluent_contents.ContentItem']},
            'center': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42'}),
            u'contentitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fluent_contents.ContentItem']", 'unique': 'True', 'primary_key': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mapitems'", 'symmetrical': 'False', 'db_table': "'contentitem_fluentcms_googlemaps_mapitem_groups'", 'to': u"orm['fluentcms_googlemaps.MarkerGroup']"}),
            'map_type_id': ('django.db.models.fields.CharField', [], {'default': "'HYBRID'", 'max_length': '50'}),
            'max_zoom': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '12'}),
            'min_zoom': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'show_clusters': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zoom': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        u'fluentcms_googlemaps.marker': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Marker'},
            'description': ('fluent_contents.extensions.PluginHtmlField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'markers'", 'null': 'True', 'to': u"orm['fluentcms_googlemaps.MarkerGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('fluent_contents.extensions.PluginImageField', [], {'max_length': '100', 'blank': 'True'}),
            'location': ('geoposition.fields.GeopositionField', [], {'max_length': '42'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'fluentcms_googlemaps.markergroup': {
            'Meta': {'ordering': "('title',)", 'object_name': 'MarkerGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marker_image': ('fluent_contents.extensions.PluginImageField', [], {'max_length': '100'}),
            'marker_zoom': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '7'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['fluentcms_googlemaps']