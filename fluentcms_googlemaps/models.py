from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.six import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from fluent_contents.models.mixins import CachedModelMixin
from fluent_contents.extensions import PluginImageField, PluginHtmlField
from fluent_contents.models import ContentItem
from . import appsettings


@python_2_unicode_compatible
class MarkerGroup(CachedModelMixin, models.Model):
    """
    Grouping of markers in a given category,
    """
    title = models.CharField(_("Title"), max_length=200)
    marker_image = PluginImageField(_("Marker image"))
    marker_zoom = models.PositiveSmallIntegerField(_("Zoom level on click"), default=7)

    class Meta:
        verbose_name = _("Marker Group")
        verbose_name_plural = _("Marker Groups")
        ordering = ('title',)

    def __str__(self):
        return self.title

    def clear_cache(self):
        # Called on save/delete by CachedModelMixin
        _clear_mapitem_cache()

    @property
    def url(self):
        return self.image.url if self.image else None

    @property
    def anchor(self):
        return (0,0)

    @property
    def origin(self):
        return (0,0)

    def to_dict(self):
        """
        Export the group data for the frontend.
        """
        return {
            'id': self.pk,
            'title': self.title,
            'icon': {
                'url': self.marker_image.url if self.marker_image else None,
                'width': self.marker_image.width if self.marker_image else 16,
                'height': self.marker_image.height if self.marker_image else 16,
                'marker_zoom': self.marker_zoom,
            },
            'markers': [
                marker.to_dict() for marker in self.markers.all()
            ],
        }


@python_2_unicode_compatible
class Marker(CachedModelMixin, models.Model):
    """
    A single point on the map
    """
    title = models.CharField(_("Title"), max_length=200)
    image = PluginImageField(_("Image"), blank=True)
    description = PluginHtmlField(_("Description"), blank=True)
    group = models.ForeignKey(MarkerGroup, related_name='markers', verbose_name=_("Group"), blank=True, null=True)
    location = GeopositionField(_("Location"))  # TODO: use different package?

    class Meta:
        verbose_name = _("Marker")
        verbose_name_plural = _("Markers")
        ordering = ('title',)

    def __str__(self):
        return self.title

    def clear_cache(self):
        # Called on save/delete by CachedModelMixin
        _clear_mapitem_cache()

    def to_dict(self, detailed=False):
        """
        Export the marker data for the frontend.

        :param expanded: Tell whether more detailed information should be added, for the detail page.
        :type expanded: bool
        """
        geoposition = self.location
        return {
            'id': self.pk,
            'title': self.title,
            'image': _image_to_dict(self, self.image),
            'description': self.description,
            'group_id': self.group_id,
            'location': [float(geoposition.latitude), float(geoposition.longitude)],
            #'click_zoom': 7,
            #cluster_weight
        }


def _image_to_dict(marker, image):
    if not image:
        return None

    return {
        'url': image.url,
        'html': render_to_string('fluentcms_googlemaps/marker_image.html', {'marker': marker, 'image': image})
    }


def _clear_mapitem_cache():
    MapItem.objects.all().clear_cache()


@python_2_unicode_compatible
class MapItem(ContentItem):
    """
    Content Item to add a map to a page.
    It can show different categories of markers.
    """
    title = models.CharField(_("Title"), max_length=200)
    style = models.CharField(_("Style"), max_length=200, choices=appsettings.FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES)
    groups = models.ManyToManyField(MarkerGroup, related_name='mapitems', verbose_name=_("Marker Groups"), db_table='contentitem_fluentcms_googlemaps_mapitem_groups')

    map_type_id = models.CharField(_("Map type"), max_length=50, choices=appsettings.FLUENTCMS_GOOGLEMAPS_TYPE_CHOICES, default='HYBRID')
    zoom = models.PositiveSmallIntegerField(_("Default zoom level"), default=1)
    min_zoom = models.PositiveSmallIntegerField(_("Minimum zoom level"), default=1)
    max_zoom = models.PositiveSmallIntegerField(_("Maximum zoom level"), default=12)
    center = GeopositionField(_("Map center"), default='0,0')
    show_clusters = models.BooleanField(_("Group nearby markers into clusters for larger zoom levels"), blank=True, default=False)

    class Meta:
        verbose_name = _("Map")
        verbose_name_plural = _("Maps")
        ordering = ('title',)

    def __str__(self):
        return force_text(self.title)

    def get_style_options(self):
        """
        Provide the options configured in the FLUENTCMS_GOOGLEMAPS_STYLES for the currently chosen style.
        """
        try:
            return next(v for k, v in appsettings.FLUENTCMS_GOOGLEMAPS_STYLES if k == self.style)
        except StopIteration:
            return {}

    def get_marker_data(self):
        """
        Provide the marker data for the frontend/template
        """
        result = []
        for group in self.groups.all().prefetch_related('markers'):
            result.append(group.to_dict())
        return result

    def get_map_options(self):
        """
        Return the visibility settings.
        These are translated into data-... attributes.
        """
        center = self.center
        # These attributes are translated into CamelCase when jQuery reads the data-.. attributes.
        return {
            'map_id': self.pk,
            'zoom': self.zoom,
            'min_zoom': self.min_zoom,
            'max_zoom': self.max_zoom,
            'center_lat': center.latitude,
            'center_lng': center.longitude,
            'map_type_id': self.map_type_id,
            'zoom_control_style': 'SMALL',
            'zoom_control': True,
            'street_view_control': False,
            'show_clusters': self.show_clusters,
            'static_url': settings.STATIC_URL,
            #cluster_image_path: '/static/fluentcms_googlemaps/img/m'
            #cluster_grid_size: 60
            #cluster_min_size: 2
            #cluster_max_zoom  (default max_zoom -1)
            #cluster_styles: {..}
            #cluster_average_center: False
        }
