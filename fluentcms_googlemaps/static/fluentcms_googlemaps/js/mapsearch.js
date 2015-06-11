/**
 * A simple user interface for the "search" map type,
 * this is built on top of the jQuery plugin interface that mapplugin.js provides.
 * Feel free to use any variation of this file in your own products to suit your needs.
 */
+function($){
  var $form;
  var $did_you_mean;

  $.fn.ready(function(){
    $form = $('.googlemaps-area-search');
    $did_you_mean = $(".did-you-mean");
    if($form.length == 0) return;

    $form.submit(onFormSubmit);
  });

  function onFormSubmit(event)
  {
    event.preventDefault();
    var address = this.q.value;
    var $maparea = $(this).closest('.map').find('.googlemaps-area');

    // Reset inputs
    $did_you_mean.hide();
    $form.find('.control-group-q').removeClass('error');

    if(address == '') {
      $maparea.mapPlugin('resetView');
    }
    else {
      $maparea.mapPlugin("showStartPage");
      $maparea.mapPlugin("search", {'address': address}, onSuccess, onMultipleResults, onError);
    }
  }


  function onSuccess(request, result)
  {
    var $maparea = $(this);
    $maparea.mapPlugin("zoomToResult", result);
    $form[0].q.value = result.formatted_address;
  }

  function onMultipleResults(request, results)
  {
    var $maparea = $(this);
    var $ul = $did_you_mean.find('ul');
    $ul.empty();

    $.each(results, function(i, result) { // bind 'result' to this closure.
      var $li = $('<li><a href="#"></a></li>');
      var $a = $li.find('a');
      $a.text(result.formatted_address);
      $a.click(function(event) {
        event.preventDefault();
        $maparea.mapPlugin("zoomToResult", result);
        $form[0].q.value = result.formatted_address;
        $did_you_mean.hide();
      });
      $li.appendTo($ul);
    });

    $did_you_mean.show();
  }

  function onError(request, status)
  {
    $form.find('.control-group-q').addClass('error');
  }

}(window.jQuery);
