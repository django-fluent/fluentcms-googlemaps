import os

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from fluent_contents.tests.factories import create_content_item
from fluent_contents.tests.utils import render_content_items
from geoposition import Geoposition

try:
    from django.urls import reverse  # Django 1.10+
except ImportError:
    from django.core.urlresolvers import reverse

from fluentcms_googlemaps.models import MapItem, Marker, MarkerGroup


class MapTests(TestCase):
    """
    Testing private notes
    """

    def test_rendering(self):
        """
        Test the standard button
        """
        group = MarkerGroup.objects.create(title="Group 1", marker_image='')
        marker = Marker.objects.create(title="Marker 1", group=group, location=Geoposition(52, 6))

        item = create_content_item(MapItem, pk=1, title='test', style='default', center=Geoposition(3, 5))
        item.groups.add(group)
        output = render_content_items([item])

        self.assertTrue(output.html.count('<script '), 1)
        self.assertTrue(output.html.count('data-center-lng="5"'), 1)
        self.assertTrue(output.html.count('data-center-lat="3"'), 1)

    def test_api_view(self):
        marker = Marker.objects.create(title="Marker 1", location=Geoposition(52, 6))
        url = reverse('fluentcms-googlemaps-marker-detail')
        response = self.client.get("{url}?id={id}".format(url=url, id=marker.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marker 1')

    def test_markergroup_admin(self):
        group = MarkerGroup.objects.create(title="Group 1", marker_image='')
        admin = User.objects.create_superuser('map-admin', 'admin@example.com', 'testtest')
        self.client.login(username='map-admin', password='testtest')  # .force_login() exists as of Django 1.9
        response = self.client.get(reverse('admin:fluentcms_googlemaps_markergroup_change', args=(group.pk,)))
        self.assertContains(response, 'zoomrangewidget.css')

    def test_marker_admin(self):
        marker = Marker.objects.create(title="Marker 1", location=Geoposition(52, 6))
        admin = User.objects.create_superuser('map-admin', 'admin@example.com', 'testtest')
        self.client.login(username='map-admin', password='testtest')  # .force_login() exists as of Django 1.9
        response = self.client.get(reverse('admin:fluentcms_googlemaps_marker_change', args=(marker.pk,)))
        self.assertContains(response, 'Marker 1')

    def test_import_markers(self):
        group = MarkerGroup.objects.create(pk=2, title="Group 2")
        call_command(
            'import_markers',
            os.path.join(os.path.dirname(__file__), 'test.csv'),
        )
        self.assertEqual(Marker.objects.count(), 2)
        markers = sorted(Marker.objects.values_list('title', flat=True))
        self.assertEqual(markers, ['Test 1', 'Test 2'])
