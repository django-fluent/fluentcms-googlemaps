from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from fluentcms_googlemaps.widgets import ZoomRangeWidget
from .models import MarkerGroup, Marker


class MarkerGroupAdmin(admin.ModelAdmin):
    """
    Admin for creating collections of markers.
    """
    list_display = ('title_column',)

    def title_column(self, object):
        if object.marker_image:
            return format_html(u'<span style="display: inline-block; min-width: 30px; vertical-align: middle;"><img src="{0}"></span> {1}', object.marker_image.url, object.title)
        else:
            return format_html(u'<span style="display: inline-block; min-width: 30px;"></span> {1}', object.title)
    title_column.allow_tags = True
    title_column.admin_order_field = 'title'
    title_column.short_description = _("Title")

    formfield_overrides = {
        # All zoom controls.
        models.PositiveSmallIntegerField: {
            'min_value': ZoomRangeWidget.min_value,
            'max_value': ZoomRangeWidget.max_value,
            'widget': ZoomRangeWidget
        }
    }


class MarkerAdmin(admin.ModelAdmin):
    """
    Admin for markers.
    """
    list_display = ('title', 'group',)
    list_filter = ('group',)
    list_select_related = True


admin.site.register(MarkerGroup, MarkerGroupAdmin)
admin.site.register(Marker, MarkerAdmin)
