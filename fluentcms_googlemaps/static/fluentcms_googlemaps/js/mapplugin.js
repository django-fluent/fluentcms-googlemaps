+function($) {

  var $googleMapsAreas = $('.googlemaps-area');
  if($googleMapsAreas.length == 0) {
    return;
  }

  // NOTE: these are now duplicated with "impactmap.py" in Python
  var DEFAULT_CLUSTER_STYLES = [
    {
      url: '/static/fluentcms_googlemaps/img/m1.png',
      width: 53,
      height: 53,
      textSize: 11,
      textColor: '#333333',
      min_weight: Number.NEGATIVE_INFINITY,  // 1-9
      marker_zoom: 7
    },
    {
      url: '/static/fluentcms_googlemaps/img/m2.png',
      width: 56,
      height: 56,
      textSize: 11,
      textColor: '#333333',
      min_weight: 10,
      marker_zoom: 7    // 2 digits
    },
    {
      url: '/static/fluentcms_googlemaps/img/m3.png',
      width: 66,
      height: 66,
      textSize: 13,
      textColor: '#333333',
      min_weight: 100,   // 3 digits
      marker_zoom: 7
    },
    {
      url: '/static/fluentcms_googlemaps/img/m4.png',
      width: 78,
      height: 78,
      textSize: 14,
      textColor: '#333333',
      min_weight: 1000,  // 4 digits
      marker_zoom: 5
    },
    {
      url: '/static/fluentcms_googlemaps/img/m5.png',
      width: 90,
      height: 90,
      textSize: 17,
      textColor: '#333333',
      min_weight: 10000,  // 5 digits
      marker_zoom: 5
    }
  ];
  _enrichClusterIconsAsMarkerIcons(DEFAULT_CLUSTER_STYLES);


  function MapPlugin(area, options)
  {
    this.$area = $(area);
    this.gmap = null;
    this.options = $.extend({}, MapPlugin.DEFAULTS, this.$area.data(), options);
    this.options.defaultCenter = this.options.defaultCenter || new google.maps.LatLng(this.options.centerLat, this.options.centerLng);

    this.init();
  }

  MapPlugin.DEFAULTS = {
    centerLat: 0,
    centerLng: 0,
    zoom: 1,
    minZoom: 1,
    maxZoom: 12,    // amount that can be zoomed in.
    zoomControl: true,
    streetViewControl: false,
    mapTypeId: "HYBRID",
    zoomControlStyle: "SMALL",
    staticUrl: '/static/',
    showClusters: false,
    clusterMinSize: 2,
    clusterGridSize: 60,
    clusterMaxZoom: null,  // 1 less then maxZoom
    clusterStyles: DEFAULT_CLUSTER_STYLES,
    clusterAverageCenter: false
  };

  MapPlugin.prototype =
  {
    init: function MapPlugin_init()
    {
      var map_content = JSON.parse(this.$area.find('script.googlemaps-data').text());

      // Initialize the main map
      var mapMaxZoom = this.options.maxZoom;
      this.gmap = new google.maps.Map(this.$area.find('.googlemaps-widget').get(0), {
        center: this.options.defaultCenter,
        mapTypeId: google.maps.MapTypeId[this.options.mapTypeId],

        // nice default settings for compact embedding:
        zoom: this.options.zoom,
        minZoom: this.options.minZoom,
        maxZoom: mapMaxZoom,
        streetViewControl: this.options.streetViewControl,
        zoomControl: this.options.zoomControl,
        zoomControlOptions: {
          style: google.maps.ZoomControlStyle[this.options.zoomControlStyle]
        }
      });
      google.maps.event.addListener(this.gmap, 'click', $.proxy(this._onMapClick, this));
      google.maps.event.addListener(this.gmap, 'zoom_changed', $.proxy(this._onMapZoom, this));

      // Cluster manager
      if(this.options.showClusters) {
        this.markerCluster = new MarkerClusterer(this.gmap, [], {
          imagePath: this.options.clusterImagePath || (this.options.staticUrl + 'fluentcms_googlemaps/img/m'),
          minimumClusterSize: this.options.clusterMinSize,
          gridSize: this.options.clusterGridSize,
          maxZoom: this.options.clusterMaxZoom || (mapMaxZoom - 1),  // Always one less or you'll never see markers
          styles: this.options.clusterStyles,
          averageCenter: this.options.clusterAverageCenter
        });
        this.markerCluster.setCalculator(_getClusterStyle);
      }
      else {
        this.gmarkers = [];
      }

      // Add overlay
      this.$zoomBack = this.$area.find(".zoom-back");
      this.$zoomBack.hide().find('a').click($.proxy(this._onZoomBackClick, this));
      this.gmap.controls[google.maps.ControlPosition.TOP_LEFT].insertAt(0, this.$zoomBack.get(0));

      // Add markers
      this.initMarkers(map_content);
    },

    initMarkers: function MapPlugin_initMarkers(groups)
    {
      this.clearMarkers();

      for(var i = 0; i < groups.length; i++) {
        var group = groups[i];
        var icon = _createIcon(group.icon);
        var gmarkers = this._jsonToMarkers(group.markers, icon);
        this.addMarkers(gmarkers);
      }
    },

    clearMarkers: function MapPlugin_clearMarkers()
    {
      if(this.options.showClusters) {
        // Remove everything loaded in the clusterer
        this.markerCluster.clearMarkers();
      }
      else {
        // Remove all individual items
        for(var i = 0; i < this.gmarkers.length; i++) {
          this.gmarkers[i].setMap(null);
        }
        this.gmarkers = [];
      }
    },

    addMarkers: function MapPlugin_addMarkers(gmarkers)
    {
      if(this.options.showClusters) {
        // Let the clusterer dedide what to show.
        this.markerCluster.addMarkers(gmarkers);
      }
      else {
        // Add as individual items on the map.
        this.gmarkers = this.gmarkers.concat(gmarkers);
        for(var i = 0; i < gmarkers.length; i++) {
          gmarkers[i].setMap(this.gmap);
        }
      }
    },

    _onMapClick: function MapPlugin_onMapClick(event)
    {
      // event.latLng
      this.showStartPage();
    },

    _onMapZoom: function MapPlugin_onMapZoom(event)
    {
      var gmap = this.gmap;
      this.$zoomBack[gmap.getZoom() > gmap.minZoom ? 'show' : 'hide']();
    },

    _onZoomBackClick: function MapPlugin_onZoomBackClick(event) {
      event.preventDefault();
      event.target.blur();
      this.resetView();
    },

    _onMarkerClick: function MapPlugin_onMarkerClick(event, gmarker)
    {
      if(event.stop)
        event.stop();  // no bubbling to the map.

      this.zoomTo(gmarker.getPosition(), gmarker._click_zoom || 7);
      this._loadMarkerDetails(gmarker, false);
    },

    _loadMarkerDetails: function MapPlugin_fetchMarkerDetails(gmarker, move_map)
    {
      // URL is optional
      var url = this.options.markerDetailApiUrl;
      if(! url)
        return;

      var outer_this = this;
      $.ajax({
        url: url,
        data: {
          'map_id': this.options.mapId || 0,
          'id': gmarker._data.id
        },
        dataType: 'json'
      }).success(function(marker){
        outer_this.showMarkerDetails(marker);

        // Data is known afterwards, zoom to marker.
        if(move_map) {
          var icon_zoom = _getClusterIconForMarker(marker).marker_zoom;
          var center = new google.maps.LatLng(marker.location[0], marker.location[1]);
          outer_this.zoomTo(center, marker.click_zoom || icon_zoom);
        }
      });
    },

    _jsonToMarkers: function MapPlugin_jsonToMarkers(marker_data, icon)
    {
      var markers = [];
      for (var i = 0; i < marker_data.length; i++)
      {
        var marker = marker_data[i];
        var options = {
          position: new google.maps.LatLng(marker.location[0], marker.location[1]),
          icon: icon || _getClusterIconForMarker(marker),
          flat: true,

          // Markerwithlabel
          map: this.gmap,
          labelContent: marker.label || "",
          labelClass: "label", // the CSS class for the label
          labelAnchor: icon._labelAnchor,
          labelStyle: icon._labelStyle
        };
        if(!options.icon)
          delete options['icon'];
        var gmarker = new MarkerWithLabel(options);
        gmarker._data = marker;
        gmarker._click_zoom = marker.click_zoom || icon.marker_zoom;

        var outer_this = this;
        google.maps.event.addListener(gmarker, 'click', function(event){ outer_this._onMarkerClick(event, this); });
        markers.push(gmarker);
      }

      return markers;
    },

    /**
     * Plugin API: Reset the view to the original situation.
     */
    resetView: function MapPlugin_reset()
    {
      this.showStartPage();
      this.resetZoom();
    },

    /**
     * Plugin API: Reset the zoom level to the original situation.
     */
    resetZoom: function MapPlugin_zoomReset()
    {
      var gmap = this.gmap;
      gmap.setZoom(this.options.zoom || gmap.minZoom);
      gmap.panTo(this.options.defaultCenter);
    },

    /**
     * Plugin API: Show the opening page.
     */
    showStartPage: function MapPlugin_showStartPage()
    {
      // Switch panes
      $('.sidebar-pane').hide();
      $('.sidebar-pane.home').show();

      // Set location
      if(location.hash) {
        location.hash = '!';
      }
    },

    /**
     * Show the marker details in the sidebar
     */
    showMarkerDetails: function MapPlugin_showMarkerDetails(marker)
    {
      var $marker_detail = $('.marker-detail');

      // Switch panes
      $('.sidebar-pane').hide();
      $marker_detail.show();

      // Set location
      location.hash = '#!/marker/' + marker.id;

      // Fill values (already escaped server-side)
      $marker_detail.find('.marker-title').html(marker.title);
      $marker_detail.find('.marker-description').html(marker.description);
      $marker_detail.find('.marker-image').html(marker.image ? marker.image.html : '');
    },

    /**
     * Plugin API: search for an address.
     *
     * This finds possible locations based on the request.
     * The callbacks can be used to implement a user interface,
     * to display errors and handle multiple results.
     *
     * The onSuccess and onMultipleResults callbacks typically
     * call $(this).mapPlugin('zoomToResult', result) for a specific result.
     * When the success callback is not defined, the map zooms by default.
     *
     * Other methods of interest are:
     * - resetView
     * - showStartPage
     *
     * @param request The options defined in https://developers.google.com/maps/documentation/javascript/3.exp/reference#GeocoderRequest
     *                Typically {'address': "input text"}
     * @param onSuccess  Function called when there is a single result
     * @param onMultipleResults  Function called when there are multiple choices.
     * @param onError Function called when the geocoding failed.
     */
    search: function MapPlugin_search(request, onSuccess, onMultipleResults, onError)
    {
      if(request && !request.address && !request.components) throw new Error("Invalid geocoding request!");

      var gc = new google.maps.Geocoder();
      var outer_this = this;
      var area = this.$area[0];
      gc.geocode(request, function(results, status) {
        if(status != 'OK') {
          if(onError != null) onError.call(area, request, status);
        }
        else {
          if(results.length == 1) {
            if(onSuccess != null) onSuccess.call(area, request, results[0]);
            else  outer_this.zoomToResult(results[0]);
          }
          else {
            if(onMultipleResults != null) onMultipleResults.call(area, request, results);
          }
        }
      });
    },

    /**
     * Plugin API: Zoom and pan to a specific location.
     * @param latlng A `google.maps.LatLng` object.
     * @param minZoom The minimum zoom level the map should navigate to first.
     */
    zoomTo: function MapPlugin_zoomTo(latlng, minZoom)
    {
      if(minZoom != null && this.gmap.getZoom() < minZoom)
        this.gmap.setZoom(minZoom);

      this.gmap.panTo(latlng);
    },

    /**
     * Plugin API: Zoom to a Geocoder result
     * @param result
     */
    zoomToResult: function MapPlugin_zoomToGeocoderResult(result)
    {
      if (result.geometry.bounds) {
        this.gmap.fitBounds(result.geometry.bounds);
      }
      else {
        this.gmap.panTo(result.geometry.location);
        this.gmap.setZoom(18);
      }
    }
  };


  function _createIcon(icon) {
    if(! icon)
      return null;

    var cx = Math.floor(icon.width / 2);
    var cy = Math.floor(icon.height / 2);

    icon.size = new google.maps.Size(icon.width, icon.height);
    icon.anchor = new google.maps.Point(cx, cy);
    icon._labelAnchor = new google.maps.Point(cx, cy);   // is relative to anchor
    icon._labelStyle = {
      width: icon.width + "px",
      lineHeight: icon.height + 'px',
      fontSize: icon.textSize + "px",
      color: icon.textColor
    };
    return icon;
  }

  function _getMarkerWeight(marker) {
    // The standard clusterer counts every marker as 1.
    // For some projects, it's desired to have a custom weight value for each marker.
    // It could be that the marker already contains a number/price, etc.. so the cluster should add those up.
    return marker.cluster_weight != null ? marker.cluster_weight : 1;
  }

  function _getClusterStyle(markers) {
    var clusterWeight = 0;
    for (var i = 0; i < markers.length; i++) {
      var marker = markers[i];
      clusterWeight += _getMarkerWeight(marker);
    }

    var index = _getClusterStyleIndex(clusterWeight) + 1;

    return {
      text: clusterWeight,
      index: index
    };
  }

  function _getClusterStyleIndex(icon_weight) {
    for (var i = 0; i < DEFAULT_CLUSTER_STYLES.length; i++) {
      var style = DEFAULT_CLUSTER_STYLES[i];
      if(style.min_weight > icon_weight) {
        return i - 1;  // previous candidate was ok!
      }
    }

    // Largest cluster
    return DEFAULT_CLUSTER_STYLES.length - 1;
  }

  function _getClusterIconForMarker(marker)
  {
    // Because of _enrichClusterIconsAsMarkerIcons(),
    // the cluster style can also be used as marker icon.
    var clusterIndex = _getClusterStyleIndex(_getMarkerWeight(marker));
    return DEFAULT_CLUSTER_STYLES[clusterIndex];
  }

  function _enrichClusterIconsAsMarkerIcons(cluster_styles) {
    // NOTE: this is not a copy, editing the same object
    var marker_icons = cluster_styles;

    for (var i = 0; i < marker_icons.length; i++) {
      var icon = marker_icons[i];
      var cx = Math.floor(icon.width / 2);
      var cy = Math.floor(icon.height / 2);

      icon.size = new google.maps.Size(icon.width, icon.height);
      icon.anchor = new google.maps.Point(cx, cy);
      icon._labelAnchor = new google.maps.Point(cx, cy);   // is relative to anchor
      icon._labelStyle = {
        width: icon.width + "px",
        lineHeight: icon.height + 'px',
        fontSize: icon.textSize + "px",
        color: icon.textColor
      };
    }
    return marker_icons;
  }


  /**
   * jQuery Plugin definition
   */
  $.fn.mapPlugin = function(option) {
    // Can handle both {..} options and "methodName" arguments
    var action = typeof option == 'string' ? option : null;
    var actionArgs = action ? Array.prototype.splice.call(arguments, 1) : null;
    var options = action ? {} : option;
    var plugin_result = (action ? undefined : this);

    this.each(function(){
      // Instantiate data-object on load,
      // call method if a string was passed.
      var map = $(this).data('mapPlugin');
      if(map == null) $(this).data('mapPlugin', (map = new MapPlugin(this, options)));
      if(action) plugin_result = map[action].apply(map, actionArgs);
    });

    return plugin_result;
  };

  $.fn.ready(function(){
    $(".googlemaps-area.auto-enable").each(function() {
      var $this = $(this);
      $this.mapPlugin();
    });
  });

  // Use same jQuery as geoposition.js when loaded in the admin.
}(window.django ? window.django.jQuery : window.jQuery);
