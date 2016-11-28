Changelog
=========

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
