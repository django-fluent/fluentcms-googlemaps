from django.conf import settings
from django.utils.translation import ugettext_lazy as _

_js_min = "" if settings.DEBUG else ".min"

# Default values
MAP_MARKERWITHLABEL_JS = "fluentcms_googlemaps/vendor/markerwithlabel.js"
MAP_MARKERCLUSTERER_JS = "fluentcms_googlemaps/vendor/markerclusterer_compiled.js"
MAPPLUGIN_JS = "fluentcms_googlemaps/js/mapplugin.js"

FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES = (
    ('default', _("Default")),
)

FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES = (
    ('ROADMAP', _("Roadmap")),
    ('TERRAIN', _("Roadmap with terrain")),
    ('SATELLITE', _("Satellite")),
    ('HYBRID', _("Satellite with labels")),
)


## -- read the values from the settings.

FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES', FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES)
FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES', FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES)

# Allow overriding individual resources
MAP_MARKERWITHLABEL_JS = getattr(settings, 'MAP_MARKERWITHLABEL_JS', MAP_MARKERWITHLABEL_JS)
MAP_MARKERCLUSTERER_JS = getattr(settings, 'MAP_MARKERCLUSTERER_JS', MAP_MARKERCLUSTERER_JS)
MAPPLUGIN_JS = getattr(settings, 'MAPPLUGIN_JS', MAPPLUGIN_JS)

FLUENTCMS_GOOGLEMAPS_JS = (
    MAP_MARKERWITHLABEL_JS,
    MAP_MARKERCLUSTERER_JS,
    MAPPLUGIN_JS,
)

# Allow overriding the complete FrontendMedia definition
FLUENTCMS_GOOGLEMAPS_JS = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_JS', FLUENTCMS_GOOGLEMAPS_JS)
FLUENTCMS_GOOGLEMAPS_CSS = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_CSS', {})
