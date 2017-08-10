from __future__ import unicode_literals

from django.db import models
from django.forms import Media
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from fluent_contents.extensions import ContentPlugin, plugin_pool
from fluent_contents.forms import ContentItemForm
from geoposition.forms import GeopositionField

from . import appsettings
from .models import MapItem
from .widgets import InlineGeopositionWidget, ZoomRangeWidget


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
        models.PositiveSmallIntegerField: {
            'min_value': ZoomRangeWidget.min_value,
            'max_value': ZoomRangeWidget.max_value,
            'widget': ZoomRangeWidget
        }
    }

    def get_frontend_media(self, instance):
        """
        Provide FrontendMedia dynamically.
        It can differ per request and differ per style.
        :type instance: MapItem
        """
        style_options = instance.get_style_options()
        extra_js = style_options.get('extra_js', None)
        googlemaps_js = "//maps.google.com/maps/api/js?sensor=false&language={0}".format(get_language())
        if appsettings.GOOGLE_MAPS_API_KEY:
            googlemaps_js = "{0}&key={1}".format(googlemaps_js, appsettings.GOOGLE_MAPS_API_KEY)

        css = appsettings.FLUENTCMS_GOOGLEMAPS_CSS
        js = [googlemaps_js]
        js.extend(appsettings.FLUENTCMS_GOOGLEMAPS_JS)
        if extra_js:
            js.extend(extra_js)

        return Media(js=js, css=css)

    def get_render_template(self, request, instance, **kwargs):
        """
        Auto select a rendering template using the "style" attribute
        """
        templates = [
            self.render_template.format(style=instance.style),
            self.render_template.format(style='default'),
        ]

        # Allow defining a custom template in the settings for the chosen style.
        style_options = instance.get_style_options()
        template = style_options.get('template', None)
        if template:
            templates.insert(0, template)

        return templates
