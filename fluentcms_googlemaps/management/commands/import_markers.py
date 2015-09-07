import codecs
import unicodecsv
from optparse import make_option
from django.core.management import BaseCommand, CommandError
from django.db import transaction
from django.template import Template, Context, TemplateSyntaxError
from fluentcms_googlemaps.models import MarkerGroup, Marker
from geopy import get_geocoder_for_service
from geopy.exc import GeopyError
import time


class Command(BaseCommand):
    """
    Import markers from a CSV file
    """
    args = "csv-file, ..."
    help = \
r"""
Import CSV data as markers.

The data can be converted into the database by using the options.
For example:

  manage.py import_markers \
    --name="{{ Name }}" \
    --geocode='{{ Address }} {{ Zipcode }} {{ City }} {{ County }}' \
    --description="<p>{{ Address }}<br>{{ Zipcode }} {{ City }}<br>{{ Country }}</p>"

Tip: export NL=$'\n' so you can use $NL in the strings for a newline.
"""
    option_list = BaseCommand.option_list + (
        make_option('--title', action='store', default='{{ name }}', help="A template that fills the name field"),
        make_option('--group', default='{{ group }}', help='A template that fills the group field'),
        make_option('--geocode', default='{{ address }}', help='A template that fills the address for Geocoding'),
        make_option('--description', default='{{ description }}', help='A template that fills the description field'),
        make_option('--image', default='', help='A template that fills the image field'),
        make_option('--dialect', default='excel'),
        make_option('--delimiter', default=','),
        make_option('--quotechar', default='"'),
        make_option('--geocoder', default='google'),
        make_option('--start-at', default=0, action='store', type='int'),
        make_option('--dry-run', action='store_true', default=False),
    )

    def handle(self, *args, **options):
        if not args:
            raise CommandError("Expected CSV filename to import")

        try:
            geocoder = get_geocoder_for_service(options['geocoder'])()
        except GeopyError as e:
            raise CommandError(str(e))

        dry_run = options['dry_run']
        start_at = options['start_at'] or 0

        for filename in args:
            # Not passing the utf-8 codec to codecs.open()
            # the file is opened in ascii, and unicodecsv performs the conversion.
            with codecs.open(filename, 'rb') as f:
                csv_data = unicodecsv.DictReader(f, dialect=options['dialect'], delimiter=options['delimiter'], quotechar=options['quotechar'])
                first = True
                marker_data = []
                row_num = 0
                for row in csv_data:
                    row_num += 1
                    if row_num < start_at:
                        continue

                    # Parse the row data
                    # Print first results immediately, for easy debugging
                    title = _format_field(options, 'title', row, allow_empty=not first)

                    if not first:
                        self.stdout.write('----')
                    self.stdout.write(u"Row:         {0}".format(row_num))
                    self.stdout.write(u"Name:        {0}".format(title))

                    # Parse the rest
                    geocode = _format_field(options, 'geocode', row, allow_empty=not first)
                    description = _format_field(options, 'description', row, allow_html=True, allow_empty=not first)
                    group_id = _format_field(options, 'group', row, allow_html=False, allow_empty=not first)
                    image = _format_field(options, 'image', row, allow_empty=True)

                    group = _get_group(group_id)

                    if not dry_run:
                        # Avoid exceeding rate limit on dry-run tests
                        if not first:
                            time.sleep(0.3)  # 300ms

                        try:
                            location = geocoder.geocode(geocode)
                        except GeopyError as e:
                            raise CommandError(str(e))
                        if not location:
                            raise CommandError("Unable to geocode: {0}".format(geocode))

                    self.stdout.write(u"Group:       {0}".format(group))
                    self.stdout.write(u"Geocode:     {0}".format(geocode))
                    if dry_run:
                        self.stdout.write(u"Location:    (not determined for dry-run)")
                    else:
                        self.stdout.write(u"Location:    ({0}, {1}) {2}".format(location.latitude, location.longitude, location))
                    self.stdout.write(u"Image:       {0}".format(image))
                    self.stdout.write(u"Description:\n{0}".format(description))
                    first = False

                    if not dry_run:
                        marker_data.append(Marker(
                            title=title,
                            image=image or '',
                            description=description,
                            group=group,
                            location=[location.latitude, location.longitude],
                        ))

                if dry_run:
                    continue

                self.stdout.write('----')
                self.stdout.write(u"Writing objects..")

                with transaction.atomic():
                    Marker.objects.bulk_create(marker_data)

                self.stdout.write(u"Done")



def _format_field(options, name, data, allow_html=False, allow_empty=False):
    template = options[name]
    try:
        result = Template(template).render(Context(data, autoescape=allow_html))
    except TemplateSyntaxError as e:
        raise CommandError("Invalid syntax for --{0}='{1}'\n{2}".format(name, template, e))
    if not result.strip() and not allow_empty:
        raise CommandError("No results for the '{0}' fields, please update --{0}. It currently uses '{1}'.".format(name, template))

    if allow_html:
        return result
    else:
        return unicode(result)

def _get_group(group_id):
    try:
        if group_id.isdigit():
            return MarkerGroup.objects.get(pk=int(group_id))
        else:
            return MarkerGroup.objects.get(title=group_id)
    except MarkerGroup.DoesNotExist:
        raise CommandError("Unable to find group '{0}'".format(group_id))
