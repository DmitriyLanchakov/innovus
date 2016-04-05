(function($,undefined) {
  $.fn.scrollable = function(params) {
    var settings = $.extend(
      {},
      {
        visible: 3, // count of visible elements
        interval: 0, // in seconds
        speed: 300, // in milliseconds
        prevClass: "prev",
        prevText: "prev",
        nextClass: "next",
        nextText: "next"
      },
      params);
    var container = $("ul", this);
    container.css({
      "position": "relative",
      "overflow": "hidden"
    });

    var containerWidth = container.outerWidth(true);

    var elements = $("li", container);
    elements.css({
      "width": containerWidth,
      "position": "absolute"
    });

    $(this).prepend("<a class='" + settings.prevClass + "' href='#'>" + settings.prevText + "</a>");
    $(this).append("<a class='" + settings.nextClass + "' href='#'>" + settings.nextText + "</a>");
    var buttonPrev = $("." + settings.prevClass, this);
    var buttonNext = $("." + settings.nextClass, this);

    var visibleHeight = 0;
    var verticalPosition = 0;
    $.each(elements, function(iterator, element) {
      $(element).css("top", verticalPosition);
      verticalPosition += $(element).outerHeight(true);
      if (iterator < settings.visible) {
        visibleHeight += $(element).outerHeight(true);
      }
    });
    container.height(visibleHeight);

    if (settings.interval) {
      setInterval(function() {
        buttonPrev.click();
      }, settings.interval * 1000);
    };

    buttonPrev.click(function() {
      elements = $("li", container);
      var last = $(elements.last()[0]);
      last.prependTo(container);
      elements = $("li", container);
      visibleHeight = 0;
      verticalPosition = 0 - last.outerHeight(true);
      $.each(elements, function(iterator, element) {
        $(element).css("top", verticalPosition);
        verticalPosition += $(element).outerHeight(true);
        if (iterator < settings.visible) {
          visibleHeight += $(element).outerHeight(true);
        }
      });
      elements.animate({
        top: "+=" + last.outerHeight(true)
      }, settings.speed, function(){
        container.height(visibleHeight);
      });
      return false;
    });

    buttonNext.click(function() {
      elements = $("li", container);
      var first = $(elements.first()[0]);
      elements.animate({
        top: "-=" + first.outerHeight(true)
      }, settings.speed, function(){
        first.appendTo(container);
        elements = $("li", container);
        visibleHeight = 0;
        verticalPosition = 0;
        $.each(elements, function(iterator, element) {
          $(element).css("top", verticalPosition);
          verticalPosition += $(element).outerHeight(true);
          if (iterator < settings.visible) {
            visibleHeight += $(element).outerHeight(true);
          }
        });
        container.height(visibleHeight);
      });
      return false;
    });
  };
})(jQuery);

