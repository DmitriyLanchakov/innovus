/* ------------------------------------------------------------------------
  Class: ajaxIndicator
  Use: A unified solution for AJAX loader
  Version: 1.0
------------------------------------------------------------------------- */

(function($) {
  $.ajaxIndicator = {version: "1.0"};

  $.ajaxIndicator = function(settings) {
    settings = $.extend({
      className: ".ajaxIndicator",
      animationSpeed: "fast", /* fast/normal/slow/integer */
      bindAjax: true, /* true/false */
      delay: false, /* false OR time in milliseconds (ms) */
      loaderImage: "/img/ajax-loader.gif", /* Path to your loader gif */
      offset_top: 13, /* integer */
      offset_left: 10 /* integer */
    }, settings);

    var scrollPos = _getScroll();

    // Window/Keyboard events
    $(window).unbind("scroll").scroll(function() {
      scrollPos = _getScroll();
    });

    if(settings.bindAjax) {
      $(document).ajaxSend(function() {
        $.ajaxIndicator.show();
      });
      $(document).ajaxStop(function() {
        $.ajaxIndicator.hide();
      });
    }

    $.ajaxIndicator.show = function(delay){

      if ($(settings.className).length)
        return false;

      var loader = $("<div></div>").appendTo("body").hide();
      loader.addClass(settings.className.substr(1));

      // Build the loader image
      loader.append("<img src='" + settings.loaderImage + "'/>");

      // No png for IE6...sadly :(
      if($.browser.msie && $.browser.version == 6)
        loader.addClass("ai_ie6");

      $(document).click(function(e) {
        e = e ? e : window.event;
        $(loader).css({
          "left": e.clientX + settings.offset_left + scrollPos["scrollLeft"],
          "top": e.clientY + settings.offset_top + scrollPos["scrollTop"]
        });
      });

      // Show it!
      loader.fadeIn(settings.animationSpeed);

      $(document).mousemove(function(e){
        // Get the cursor position
        e = e ? e : window.event;
        $(loader).css({
          "left": e.clientX + settings.offset_left + scrollPos["scrollLeft"],
          "top": e.clientY + settings.offset_top + scrollPos["scrollTop"]
        });
      });

      var delay = (delay) ? delay : settings.delay;

      if (delay) {
        setTimeout(function() {
          $.ajaxIndicator.hide();
        }, delay);
      };
    };

    $.ajaxIndicator.hide = function(){
      $(settings.className).fadeOut(settings.animationSpeed, function(){
        $(this).remove();
      });
    };

    function _getScroll(){
      if (self.pageYOffset) {
        return {scrollTop:self.pageYOffset,scrollLeft:self.pageXOffset};
      } else if (document.documentElement && document.documentElement.scrollTop) { // Explorer 6 Strict
        return {scrollTop:document.documentElement.scrollTop,scrollLeft:document.documentElement.scrollLeft};
      } else if (document.body) {// all other Explorers
        return {scrollTop:document.body.scrollTop,scrollLeft:document.body.scrollLeft};
      };
    };

    return this;
  };

})(jQuery);
