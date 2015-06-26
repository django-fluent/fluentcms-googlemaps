from django import forms
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from geoposition.forms import GeopositionWidget

# Standard zoom ends at 20, but some satellite image pushes it even further.
# See: https://developers.google.com/maps/documentation/javascript/maxzoom
# and http://www.wolfpil.de/v3/deep-zoom.html for examples
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
        kwargs['onchange'] = 'this.nextSibling.innerHTML = this.value;'
        return super(ZoomRangeWidget, self).build_attrs(extra_attrs=extra_attrs, **kwargs)

    def render(self, name, value, attrs=None):
        input = super(ZoomRangeWidget, self).render(name, value, attrs=attrs)
        return format_html('{0}<span class="zoom-value">{1}</span>', input, value)

    class Media:
        css = {'all': ('fluentcms_googlemaps/admin/zoomrangewidget.css',)}


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
