.. image:: https://img.shields.io/travis/django-fluent/fluentcms-googlemaps/master.svg?branch=master
    :target: http://travis-ci.org/django-fluent/fluentcms-googlemaps
.. image:: https://img.shields.io/pypi/v/fluentcms-googlemaps.svg
    :target: https://pypi.python.org/pypi/fluentcms-googlemaps/
.. image:: https://img.shields.io/pypi/l/fluentcms-googlemaps.svg
    :target: https://pypi.python.org/pypi/fluentcms-googlemaps/
.. image:: https://img.shields.io/codecov/c/github/django-fluent/fluentcms-googlemaps/master.svg
    :target: https://codecov.io/github/django-fluent/fluentcms-googlemaps?branch=master

fluentcms-googlemaps
====================

A plugin for django-fluent-contents_ to show a Google Maps widget on a website.

This plugin is a work in progress.
It's already used in production, just know that there are two main area's that need improval:

* Use a better GeoPosition widget (e.g. by using a lightbox/popup)
* Make cluster icons configurable.


Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI::

    pip install fluentcms-googlemaps

**NOTE:** On Django 1.11, you'll have to install the following package first:

.. code-block:: bash

    pip -e git+https://github.com/philippbosch/django-geoposition.git@django-1.11#egg=django-geoposition

Since django-geoposition_ doesn't have a Django 1.11 compatible release yet.


Backend Configuration
---------------------

First make sure the project is configured for django-fluent-contents_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'geoposition',
        'fluentcms_googlemaps',
    )

    GOOGLE_MAPS_API_KEY = None  # Might be needed to define this.

Add the following to ``urls.py``:

.. code-block:: python

    urlpatterns = [
        ...

        url(r'^api/googlemaps/', include('fluentcms_googlemaps.urls')),
    ]

The database tables can be created afterwards:

.. code-block:: bash

    ./manage.py migrate

Now, the ``MapPlugin`` can be added to your ``PlaceholderField``
and ``PlaceholderEditorAdmin`` admin screens.


Frontend Configuration
----------------------

Make sure that all plugin media files are exposed by django-fluent-contents_:

.. code-block:: html+django

    {% load fluent_contents_tags %}

    {% render_content_items_media %}

This tag should be placed at the bottom of the page, after all plugins are rendered.
For more configuration options - e.g. integration with django-compressor -
see the `template tag documentation <https://django-fluent-contents.readthedocs.io/en/latest/templatetags.html#frontend-media>`_.

CSS Code
~~~~~~~~

The stylesheet code is purposefully left out, since authors typically like to provide their own styling.

JavaScript Code
~~~~~~~~~~~~~~~

No configuration is required for the JavaScript integration.

By default, the plugin includes all required JavaScript code.

If needed, the includes resources can be changed by using the following settings:

.. code-block:: python

    MAP_MARKERWITHLABEL_JS = "fluentcms_googlemaps/vendor/markerwithlabel.js"
    MAP_MARKERCLUSTERER_JS = "fluentcms_googlemaps/vendor/markerclusterer_compiled.js"
    MAPPLUGIN_JS = "fluentcms_googlemaps/js/mapplugin.js"
    MAPSEARCH_JS = "fluentcms_googlemaps/js/mapsearch.js"

    FLUENTCMS_GOOGLEMAPS_JS = (
        MAP_MARKERWITHLABEL_JS,
        MAP_MARKERCLUSTERER_JS,
        MAPPLUGIN_JS,
    )

    FLUENTCMS_GOOGLEMAPS_CSS = {}

If a value is defined as ``None``, it will be excluded from the frontend media.

HTML code
~~~~~~~~~

If needed, the HTML code can be overwritten by redefining ``fluentcms_googlemaps/maps/default.html``.
Also, you can create additional map styles and define these in ``FLUENTCMS_GOOGLEMAPS_STYLES``.
The default is:

.. code-block:: python

    FLUENTCMS_GOOGLEMAPS_STYLES = (
        ('default', {
            'title': _("Default"),
            'template': "fluentcms_googlemaps/maps/default.html",
        }),
        ('search', {
            'title': _("Search field"),
            'template': "fluentcms_googlemaps/maps/search.html",
            'extra_js': (
                MAPSEARCH_JS,   # = "fluentcms_googlemaps/js/mapsearch.js" unless MAPSEARCH_JS is redefined
            ),
        }),
    )

By default, the following templates are looked up:

* A explicitly defined ``template`` option in the ``FLUENTCMS_GOOGLEMAPS_STYLES``.
* A template named: ``fluentcms_googlemaps/maps/{style}.html``.
* The default; ``fluentcms_googlemaps/maps/default.html``.


Importing data
--------------

Marker data can be imported from CSV files, and receive geocoding too.
The ``import_markers`` command can be called with custom templates to map the CSV file data to marker fields.
For example:

.. code-block:: bash

    manage.py import_markers /stores.csv  --title='{{Name}}' --group=1 --geocode='{{Address}} {{Zipcode}} {{City}} {{County}}' --geocoder=google --description="<p>{{Address}}<br>{{Zipcode}} {{City}}<br>{% if County == 'NL'%}The Netherlands{% else %}{{County}}{% endif %}</p>"

It's recommended to add ``--dry-run`` first until all fields are properly filled.
The markers are created in a single transaction at the end of all parsing.


Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-geoposition: https://github.com/philippbosch/django-geoposition
.. _django-fluent-contents: https://github.com/django-fluent/django-fluent-contents
