from __future__ import unicode_literals

import json

from django.template import Library
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

try:
    from django.urls import NoReverseMatch, reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch, reverse

register = Library()

_js_escapes = {
    ord('>'): '\\u003E',
    ord('<'): '\\u003C',
    ord('&'): '\\u0026',
    ord('\u2028'): '\\u2028',
    ord('\u2029'): '\\u2029',
}

# Add every ASCII character with a value less than 32.
_js_escapes.update((ord('%c' % z), '\\u%04X' % z) for z in range(32))


def escapejs_json(value):
    """Hex encodes characters for use in JavaScript strings."""
    return mark_safe(force_text(value).translate(_js_escapes))


@register.filter
def to_json(data):
    # Make sure HTML tags are not visible in the JSON output, but escaped to.
    return escapejs_json(json.dumps(data))


@register.simple_tag
def data_attrs(mapitem):
    """
    Generate the data-... attributes for a mapitem.
    """
    data_attrs = {}

    try:
        data_attrs['marker-detail-api-url'] = reverse('fluentcms-googlemaps-marker-detail')
    except NoReverseMatch:
        pass

    data_attrs.update(mapitem.get_map_options())
    return mark_safe(u''.join([
        format_html(u' data-{0}="{1}"', k.replace('_', '-'), _data_value(v))
        for k, v in data_attrs.items()
    ]))


def _data_value(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, int):
        return value
    else:
        return conditional_escape(value)
