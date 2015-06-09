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


Backend Configuration
---------------------

First make sure the project is configured for django-fluent-contents_.

Then add the following settings::

    INSTALLED_APPS += (
        'fluentcms_googlemaps',
    )

Add the following to ``urls.py``::

    urlpatterns = [
        ...

        url(r'^api/googlemaps/', include('fluentcms_googlemaps.urls')),
    ]

The database tables can be created afterwards::

    ./manage.py migrate

Now, the ``MapPlugin`` can be added to your ``PlaceholderField``
and ``PlaceholderEditorAdmin`` admin screens.


Frontend Configuration
----------------------

Make sure that all plugin media files are exposed by django-fluent-contents_::

    {% load frontend_contents_tags %}

    {% render_content_items_media %}

This tag should be placed at the bottom of the page, after all plugins are rendered.
For more configuration options - e.g. integration with django-compressor -
see the `template tag documentation <http://django-fluent-contents.readthedocs.org/en/latest/templatetags.html#frontend-media>`_.

CSS Code
~~~~~~~~

The stylesheet code is purposefully left out, since authors typically like to provide their own styling.

JavaScript Code
~~~~~~~~~~~~~~~

No configuration is required for the JavaScript integration.

By default, the plugin includes all required JavaScript code.

If needed, the includes resources can be changed by using the following settings::

    MAP_MARKERWITHLABEL_JS = "fluentcms_googlemaps/vendor/markerwithlabel.js"
    MAP_MARKERCLUSTERER_JS = "fluentcms_googlemaps/vendor/markerclusterer_compiled.js"
    MAPPLUGIN_JS = "fluentcms_googlemaps/js/mapplugin.js"

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
Also, you can create additional map styles and define these in ``FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES``.
The default is::

    FLUENTCMS_GOOGLEMAPS_STYLE_CHOICES = (
        ('default', _("Default")),
    )

The given key is used to locale a template named ``fluentcms_googlemaps/maps/{style}.html``.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-fluent-contents: https://github.com/edoburu/django-fluent-contents
