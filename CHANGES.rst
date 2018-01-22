Changelog
=========

Version 1.4 (2018-01-22)
------------------------

* Fixed startup errors on Django 2.0.

Note that django-geoposition_ doesn't support Django 2.0 yet,
hence this package is not yet released as "v2.0".


Version 1.3 (2017-08-10)
------------------------

* Fixed ``import_markers`` usage for Django 1.10
* Fixed Python 3 compatibility.
* Fixed mising dependency to *django-wysiwyg* for the admin.
* Dropped Django 1.6 and 1.7 support, which is also not supported by django-geoposition_ 0.3.

**NOTE:** On Django 1.11, you'll have to install the following package first::

    pip -e git+https://github.com/philippbosch/django-geoposition.git@django-1.11#egg=django-geoposition


Version 1.2.7 (2017-05-05)
--------------------------

* Fixed admin error in Django 1.11.
  (note that the actual widget still needs updates, both in this package and django-geoposition_).


Version 1.2.6 (2016-11-25)
--------------------------

* Added ``GOOGLE_MAPS_API_KEY`` setting support.
  Allow configuring a Google Maps API key.


Version 1.2.5 (2016-03-17)
--------------------------

* Optimize appearance at admin page, avoid loading Google Maps API.


Version 1.2.4 (2015-10-02)
--------------------------

* Fix Django migrations to avoid unnecessary migrations when settings change.


Version 1.2.3 (2015-09-28)
--------------------------

* Fix 500 error when no ID parameter is passed.


Version 1.2.2 (2015-09-07)
--------------------------

* Improve utf-8 support for ``import_markers`` management command.
* Avoid 500 error when passing bad parameters to the API view.


Version 1.2.1
-------------

* Fixed packaging error with cluster PNG files missing.


Version 1.2
-----------

* Fixed ``ZoomRangeWidget`` number updating.
* Added ``manage.py import_markers`` script.


Version 1.1
-----------

* Added search support, fully customizable and overridable.
* Added new ``FLUENTCMS_GOOGLEMAPS_STYLES`` setting with ``template`` and ``extra_js`` options.
* Added ``marker_zoom`` setting to clusters
* Improve visual display of marker groups.
* Improve jQuery plugin interface, allow method calling with ``.mapPlugin("methodname", args..)``.


Version 1.0 (2015-06-09)
------------------------

* First release


.. _django-geoposition: https://github.com/philippbosch/django-geoposition
