from django.conf import settings
from django.utils.translation import ugettext_lazy as _

_js_min = "" if settings.DEBUG else ".min"

# Default values
MAP_MARKERWITHLABEL_JS = "fluentcms_googlemaps/vendor/markerwithlabel.js"
MAP_MARKERCLUSTERER_JS = "fluentcms_googlemaps/vendor/markerclusterer_compiled.js"
MAPPLUGIN_JS = "fluentcms_googlemaps/js/mapplugin.js"
MAPSEARCH_JS = "fluentcms_googlemaps/js/mapsearch.js"

FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES = (
    ('ROADMAP', _("Roadmap")),
    ('TERRAIN', _("Roadmap with terrain")),
    ('SATELLITE', _("Satellite")),
    ('HYBRID', _("Satellite with labels")),
)


## -- read the values from the settings.

# Allow overriding individual resources
MAP_MARKERWITHLABEL_JS = getattr(settings, 'MAP_MARKERWITHLABEL_JS', MAP_MARKERWITHLABEL_JS)
MAP_MARKERCLUSTERER_JS = getattr(settings, 'MAP_MARKERCLUSTERER_JS', MAP_MARKERCLUSTERER_JS)
MAPPLUGIN_JS = getattr(settings, 'MAPPLUGIN_JS', MAPPLUGIN_JS)
MAPSEARCH_JS = getattr(settings, 'MAPSEARCH_JS', MAPSEARCH_JS)

FLUENTCMS_GOOGLEMAPS_JS = (
    MAP_MARKERWITHLABEL_JS,
    MAP_MARKERCLUSTERER_JS,
    MAPPLUGIN_JS,
)


FLUENTCMS_GOOGLEMAPS_STYLES = (
    ('default', {
        'title': _("Default"),
    }),
    ('search', {
        'title': _("Search field"),
        'extra_js': (
            MAPSEARCH_JS,   # = "fluentcms_googlemaps/js/mapsearch.js" by default.
        ),
    }),
)

# Backwards compatibility, create FLUENTCMS_GOOGLEMAPS_STYLES out of the old variable
FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES', None)
if FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES:
    FLUENTCMS_GOOGLEMAPS_STYLES = [
        (k, {'title': v}) for k, v in FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES
    ]


FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES', FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES)
FLUENTCMS_GOOGLEMAPS_STYLES = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_STYLES', FLUENTCMS_GOOGLEMAPS_STYLES)

# Allow overriding the complete FrontendMedia definition
FLUENTCMS_GOOGLEMAPS_JS = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_JS', FLUENTCMS_GOOGLEMAPS_JS)
FLUENTCMS_GOOGLEMAPS_CSS = getattr(settings, 'FLUENTCMS_GOOGLEMAPS_CSS', {})


# And with the new scheme of STYLES, provide the same form choices
# We'll have to do this somewhere, why not here.
if FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES is None:
    FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES = [(k, v['title']) for k, v in FLUENTCMS_GOOGLEMAPS_STYLES]
