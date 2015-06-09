from django import forms
from django.db import models
from django.forms import Media
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _, get_language
from fluent_contents.extensions import ContentPlugin, plugin_pool
from fluent_contents.forms import ContentItemForm
from geoposition.forms import GeopositionField, GeopositionWidget
from . import appsettings
from .models import MapItem


MAX_MAP_ZOOM = 23  # Deep zoom

class ZoomRangeWidget(forms.TextInput):
    """
    Range widget
    """
    input_type = 'range'
    min_value = 0
    max_value = MAX_MAP_ZOOM

    def build_attrs(self, extra_attrs=None, **kwargs):
        kwargs['min'] = self.min_value
        kwargs['max'] = self.max_value
        kwargs['onchange'] = 'this.siblings.innerHTML = this.value;'
        return super(ZoomRangeWidget, self).build_attrs(extra_attrs=extra_attrs, **kwargs)

    def render(self, name, value, attrs=None):
        input = super(ZoomRangeWidget, self).render(name, value, attrs=attrs)
        return format_html('{0}<span class="zoom-value">{1}</span>', input, value)


class InlineGeopositionWidget(GeopositionWidget):
    """
    Hide the Google Maps inline for now.
    """
    def format_output(self, rendered_widgets):
        return (
            u'<p class="geoposition">'
            u' <span>{0}: </span>{1}<br/>'
            u' <span>{2}: </span>{3}'
            u'</p>'
        ).format(
            _("latitude"), rendered_widgets[0],
            _("longitude"), rendered_widgets[1],
        )

    class Media:
        css = {'all': ('fluentcms_googlemaps/admin/geopositionwidget.css',)}


class InlineGeopositionField(GeopositionField):
    # Custom form field, to assign edited widget.
    def __init__(self, *args, **kwargs):
        super(InlineGeopositionField, self).__init__(*args, **kwargs)
        self.widget = InlineGeopositionWidget()


class MapItemForm(ContentItemForm):
    """
    Custom form for map item
    """
    center = InlineGeopositionField(label=_("Map center"))


@plugin_pool.register
class MapPlugin(ContentPlugin):
    """
    Plugin for adding a map to the site
    """
    model = MapItem
    form = MapItemForm
    category = _("Media")
    cache_output_per_language = True
    #filter_horizontal = ('groups',)
    render_template = 'fluentcms_googlemaps/maps/{style}.html'

    formfield_overrides = {
        # All zoom controls.
        # Standard zoom ends at 20, but some satellite image pushes it even further.
        # See: https://developers.google.com/maps/documentation/javascript/maxzoom
        # and http://www.wolfpil.de/v3/deep-zoom.html for examples
        models.PositiveSmallIntegerField: {
            'min_value': 0,
            'max_value': MAX_MAP_ZOOM,
            'widget': ZoomRangeWidget
        }
    }

    @property
    def frontend_media(self):
        # Language can differ per request, so this property is dynamic too.
        return Media(
            js = (
                "//maps.google.com/maps/api/js?sensor=false&language=" + get_language(),
            ) + tuple(appsettings.FLUENTCMS_GOOGLEMAPS_JS),
            css = appsettings.FLUENTCMS_GOOGLEMAPS_CSS,
        )

    def get_render_template(self, request, instance, **kwargs):
        """
        Auto select a rendering template using the "style" attribute
        """
        return [
            self.render_template.format(style=instance.style),
            self.render_template.format(style='default'),
        ]
