Changelog
=========

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
