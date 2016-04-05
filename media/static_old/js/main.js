function flash(block_id) {
  $(block_id).stop(true, true).show();
  setTimeout("$('" + block_id + "').hide('slide', { 'direction': 'up' }, 200)", 3000);
};

(function($) {
  var cache = [];
  // Arguments are image paths relative to the current page.
  $.preLoadImages = function() {
    var args_len = arguments.length;
    for (var i = args_len; i--;) {
      var cacheImage = document.createElement("img");
      cacheImage.src = arguments[i];
      cache.push(cacheImage);
    }
  }
})(jQuery);

(function($){
  $.fn.shuffle = function() {
    return this.each(function() {
      var items = $(this).children();
      return (items.length) ? $(this).html($.shuffle(items)) : this;
    });
  };

  $.shuffle = function(arr) {
    for (
      var j, x, i = arr.length; i;
      j = parseInt(Math.random() * i),
      x = arr[--i], arr[i] = arr[j], arr[j] = x
    );
    return arr;
  };
})(jQuery);

$.fn.slidePersonInfo = function() {

  return this.each(function() {

    if (!$(this).length) return false;

    var block = $(this);

    var buttonPrev = $(".persons_button_prev", block);
    var linkPrev = buttonPrev.attr("href");
    var buttonNext = $(".persons_button_next", block);
    var linkNext = buttonNext.attr("href");
    var buttonMedium = $(".persons_button_medium", block);

    $("ul", block).wrap("<div class='persons_wrap'>");

    var offset = $(".persons_wrap ul").width();

    live_click();

    function prepareLinks(data) {
      buttonPrev.remove();
      buttonMedium.remove();
      buttonNext.remove();
      $(block).prepend(data["links"]);
      buttonPrev = $(".persons_button_prev", block);
      linkPrev = buttonPrev.attr("href");
      buttonNext = $(".persons_button_next", block);
      linkNext = buttonNext.attr("href");
      live_click();
    };

    function switch_info(data, direction) {
      if (linkPrev == "#") {
        buttonPrev.css({"cursor": "default", "background-position": "0 -22px"});
      } else {
        buttonPrev.css({"cursor": "pointer", "background-position": "0 0"});
      };
      if (linkNext == "#") {
        buttonNext.css({"cursor": "default", "background-position": "0 -22px"});
      } else {
        buttonNext.css({"cursor": "pointer", "background-position": "0 0"});
      };
      if (direction == "prev") {
        $(".persons_wrap", block).prepend(data["persons"]);
        $("ul", block).css("width", offset);
        $("ul:first", block).css("left", "-" + offset + "px");
        $("ul:last", block).animate({"left": "+=" + offset + "px"}, 1000, function() {
          $(this).remove();
        });
        $("ul:first", block).animate({"left": "+=" + offset + "px"}, 1000);
      }
      if (direction == "next") {
        $(".persons_wrap", block).append(data["persons"]);
        $("ul", block).css("width", offset);
        $("ul:last", block).css("left", $("ul:first", block).width());
        $("ul:first", block).animate({"left": "-=" + offset + "px"}, 1000, function() {
          $(this).remove();
        });
        $("ul:last", block).animate({"left": "-=" + offset + "px"}, 1000);
      };
    };

    function live_click() {

      buttonPrev.click(function(event) {
        if (linkPrev == "#")
          return false;
        event.preventDefault();
        $.ajax({
          url: linkPrev,
          async: false,
          cache: true,
          success: function(data) {
            prepareLinks(data);
            switch_info(data, "prev");
          }
        });
      });

      buttonNext.click(function(event) {
        if (linkNext == "#")
          return false;
        event.preventDefault();
        $.ajax({
          url: linkNext,
          async: false,
          cache: true,
          success: function(data) {
            prepareLinks(data);
            switch_info(data, "next");
          }
        });
      });
    };

  });

};

$.fn.getMoreInfo = function(url) {
  if (!$(this).length) return false;
  var block = this;
  $("ul", block).addClass("line_1");
  $(".bottom_button", block).click(function(event) {
    event.preventDefault();
    var page = parseInt($("ul:last", block).attr("class").replace("line_", "")) + 1;
    $.ajax({
      url: url,
      async: false,
      data: {"page": page},
      cache: true,
      success: function(data) {
        $("ul:last", block).after(data["text"]);
        $("ul:last", block).hide().addClass("line_" + page).slideDown(500);
        if (data["last"]) {
          $(".bottom_button", block).slideUp(function() {
            $(this).remove();
          });
        };
      }
    });
  });
};

$.fn.person_carousel = function() {
  var block = this;
  var height = 200;
  $("ul", block).shuffle();
  $("li", block).each(function() {
    if ($(this).innerHeight() > height) {
      height = $(this).innerHeight();
    }
  });
  $("li", block).css({
    "height": height,
    "margin": "0 0 10px 0"
  });
  $(block).jCarouselLite({
    btnPrev: $(block).prev(),
    btnNext: $(block).next(),
    auto: 20000,
    vertical: true,
    speed: 1500,
    visible: 2
  });
};

$.fn.history = function(url) {
  var block = this;
  var yaersBlock = 0;
  if ($("body").hasClass("ru")) {
    $("a", block).click(function(event) {
      event.preventDefault();
      yaersBlock = $("#archive_years");
      if (yaersBlock.length) {
        yaersBlock.slideToggle();
      } else {
        $.ajax({
          url: url,
          async: false,
          cache: true,
          success: function(data) {
            $(block).closest("#timeline").after(data);
            $(block).closest("#timeline").next().wrap("<div id='archive_years'></div>");
            $("#archive_years")
              .prepend("<a class='close_archive_years' href=''>close</a>")
              .wrapInner("<span class='tooltip_bottom'></span>")
              .prepend("<span class='tooltip_top'>&nbsp;</span>")
              .hide().slideDown(function() {
            });
            $(".close_archive_years").click(function(event) {
              event.preventDefault();
              $("#archive_years").slideUp();
            });
          }
        });
      };
    });
  };
};

(function($) {

  function slideLeft() {
    $("#registration .button").hide("blind", {direction: "horizontal"}, 150, function() {
      $(this).css({
        "background-color": "#f0fffb",
        "background-position": "-50px -7px",
        "border-top": "1px dotted #375125",
        "border-bottom": "1px dotted #375125"
      });
      $("a", this).text("").css({
        "height": "250px",
        "margin": "15px 15px 15px auto"
      });
      $(this).show("blind", {direction: "horizontal"}, 150);
    });
  };

  function slideRight(link_text) {
    $("#registration .button").hide("blind", {direction: "horizontal"}, 150, function() {
      $(this).css({
        "background-color": "transparent",
        "background-position": "0 -7px",
        "border-top": "none",
        "border-bottom": "none"
      });
      $("a", this).text(link_text).css({
        "margin": "5px 7px 15px auto"
      });
      $(this).show("blind", {direction: "horizontal"}, 150);
    });
  };

  function prepareLabels(block, offsetX, offsetY) {
    if (!$("#registration .login_info ." + block).length)
      return false;
    $("#registration .login_info .for_" + block).css({
      "position": "absolute",
      "top": $("#registration .login_info ." + block).position().top + offsetY,
      "left": $("#registration .login_info ." + block).position().left + offsetX
    });
    $("#registration .login_info .for_" + block).click(function() {
      $(this).hide();
      $("#registration .login_info input." + block).focus();
    });
    $("#registration .login_info input." + block).focus(function() {
      $("#registration .login_info .for_" + block).hide();
    }).blur(function() {
       if ($(this).val() == "")
         $("#registration .login_info .for_" + block).show();
    });
  };

  $.registrationBlock = function() {

    // удаляем весь блок, если находимся на форме регистрации
    if (location.pathname.indexOf("/profile/join/") > 0) {
      $("#registration").remove();
      return false;
    };

    // выходим, если блока нет, чтобы не возникали ошибки
    if (!$("#registration").length)
      return false;

    var show = false;
    var offset = $("#registration .form").width();
    var link_text = $("#registration .button a").text();
    $("#registration .button a").click(function(event) {
      event.preventDefault();
      if (!show) {
        slideLeft();
        if($.browser.msie && ($.browser.version == 6 || $.browser.version == 7)) {
          $("#registration .form").show("blind", {direction: "horizontal"});
        } else {
          $("#registration").animate({"right": "+="  + offset + "px"})
        };
        show = true;
      } else {
        slideRight(link_text);
        if($.browser.msie && ($.browser.version == 6 || $.browser.version == 7)) {
          $("#registration .form").hide("blind", {direction: "horizontal"});
        } else {
          $("#registration").animate({"right": "-=" + offset + "px"});
        };
        show = false;
      };
    });
    $("#registration .close").click(function(event) {
      event.preventDefault();
      slideRight(link_text);
      $("#registration").animate({"right": "-=" + offset + "px"});
      show = false;
    });
    $("#registration .left a").live("click" ,function(event) {
      var cls = $(this).parent().attr("class");
      if (cls != "participation") {
          event.preventDefault();
          $("#registration .left .selected").removeClass("selected").wrapInner("<a href=''></a>");
          $(this).parent().html($(this).html()).addClass("selected");
          $(this).remove();
          $("#registration .right div").hide();
          $("#registration ." + cls + "_info").show();
      }
    });

    if ($.browser.msie && $.browser.version == 6) {
      prepareLabels("login", 418, 108);
    } else if ($.browser.msie && $.browser.version == 7) {
      prepareLabels("login", 388, 108);
    } else {
      prepareLabels("login", 8, -18);
    };
    if ($("#registration .login_info .login").val() != "") $("#registration .login_info .for_login").hide();
    if ($.browser.msie && $.browser.version == 6) {
      prepareLabels("password", 418, 168);
    } else if ($.browser.msie && $.browser.version == 7) {
      prepareLabels("password", 388, 168);
    } else {
      prepareLabels("password", 8, -18);
    };
    if ($("#registration .login_info .password").val() != "") $("#registration .login_info .for_password").hide();

  };
})(jQuery);

$.fn.eventsCarousel = function(url) {
  var block = this;
  if ($("li", block).size() == 1) {
    $(block).hide();
  };
  if ($("li", block).size() < 5) {
    $(block).prev().hide();
    $(block).next().hide();
  };
  $(block).jCarouselLite({
    btnPrev: $(block).prev(),
    btnNext: $(block).next(),
    speed: 500,
    visible: 4
  });
  $("a", block).live("click", function(event) {
    event.preventDefault();
    $("li", block).removeAttr("class");
    $("a[href='" + $(this).attr("href") + "']").parent().addClass("selected");
    $.ajax({
      url: url,
      async: false,
      cache: true,
      data: {event: $(this).closest("li").attr("id").replace("event_", "")},
      success: function(data) {
        var eventItem = $(block).closest("div.event_item");
        $(".item_info", eventItem).html(data.content);
        $(".event_video div", eventItem).html(data.media);
        $("#events .bottom_button").remove();
        $("#events").append(data.comments);
      }
    });
  });
};

$.fn.historyCarousel = function() {
  var block = this;
  if ($("li", block).size() == 1) {
    $(block).hide();
  };
  if ($("li", block).size() < 5) {
    $(block).prev().hide();
    $(block).next().hide();
  } else {
    $(block).jCarouselLite({
      btnPrev: $(block).prev(),
      btnNext: $(block).next(),
      speed: 500,
      visible: 4
    });
  };

  function updatePlayer(title, url) {
    var flashvars = {
      "uid": "videoplayer_mini",
      "comment": title,
      "st": "/media/static/css/video-ru-mini.txt",
      "file": url
    };
    var params = {
      id: "videoplayer_mini",
      allowFullScreen: "true",
      allowScriptAccess: "always",
      wmode: "transparent"
    };
    new swfobject.embedSWF("/media/static/flash/player.swf", "videoplayer_mini", "276", "221", "9.0.115", false, flashvars, params);
  };

  updatePlayer($(".selected a img", block).attr("alt"), $(".selected a", block).attr("href"));

  $("a", block).live("click", function(event) {
    event.preventDefault();
    $("li", block).removeAttr("class");
    $("a[href='" + $(this).attr("href") + "']").parent().addClass("selected");
    updatePlayer($(".selected a img", block).attr("alt"), $(".selected a", block).attr("href"));
  });
};

$.fn.fullVideoCarousel = function() {
  var block = this;
  if ($("li", block).size() < 9) {
    $(block).prev().hide();
    $(block).next().hide();
  } else {
    $(block).jCarouselLite({
      btnPrev: $(block).prev(),
      btnNext: $(block).next(),
      speed: 500,
      visible: 8
    });
  };

  function updatePlayer(title, url) {
    var flashvars = {
      "uid": "videoplayer_full",
      "comment": title,
      "st": "/media/static/css/video-ru-full.txt",
      "file": url
    };
    var params = {
      id: "videoplayer_full",
      allowFullScreen: "true",
      allowScriptAccess: "always",
      wmode: "transparent"
    };
    new swfobject.embedSWF("/media/static/flash/player.swf", "videoplayer_full", "510", "410", "9.0.115", false, flashvars, params);
  };

  updatePlayer($(".selected a img", block).attr("alt"), $(".selected a", block).attr("href"));

  $("a", block).live("click", function(event) {
    event.preventDefault();
    $("li", block).removeAttr("class");
    $("a[href='" + $(this).attr("href") + "']").parent().addClass("selected");
    updatePlayer($(".selected a img", block).attr("alt"), $(".selected a", block).attr("href"));
  });

};

(function($) {
  if (!$(this).length) return false;
  $.fn.tooltip = function(options) {
    options = $.extend({
     tooltipId: "tooltip",
     offsetX: 0,
     offsetY: 0
    }, options || {});
    return this.each(function() {
      var block = this;
      $("ul li a", this).hover(
      function() {
        if ($(this).closest("#timeline_top").length) // не отрабатываем на списке #timeline_top
          return false;
        $("<span id='" + options.tooltipId + "'>" +
            "<span class='tooltip_top'>&nbsp;</span>" +
            "<span class='tooltip_bottom'></span>" +
          "</span>").appendTo(block);
        var tip = $("#" + options.tooltipId, block);
        $(".tooltip_bottom", tip).html($(this).parent().attr("title"));
        $(this).parent().removeAttr("title");
        $(tip).css({
          "top": $(this).parent().offset().top + $(this).parent().height() + options.offsetY,
          "left": $(this).parent().offset().left + options.offsetX
        });
      }, function() {
        $(this).parent().attr("title", $(".tooltip_bottom", $("#" + options.tooltipId, block)).html());
        $("#" + options.tooltipId, block).remove();
      });
      $("ul.timeline_top li a").hover(function() {
        return false;
      });
    });
  };
})(jQuery);

function historyCarouselTooltip() {
  if (!$("#history_carousel").closest("#column").length)
    return false;
  $("#history_carousel").tooltip({
    tooltipId: "history_video_tooltip",
    offsetX: - $("#history_carousel").closest("#column").position().left - 202,
    offsetY: - $("#history_carousel").closest("#column").position().top + 2
  });
};

function doBigPicture() {

  var prevLabelText = "назад";
  var nextLabelText = "вперед";
  var infoLabelText = "Информация";
  var hideLabelText = "Закрыть";

  if ($("body").attr("class") == "en") {
    prevLabelText = "prev";
    nextLabelText = "next";
    infoLabelText = "Information";
    hideLabelText = "Close";
  };

  $(".forum_images a").bigPicture({
    "prevLabel": prevLabelText,
    "nextLabel": nextLabelText,
    "infoLabel": infoLabelText,
    "hideLabel": hideLabelText,
    "boxEaseFn": "easeInQuint",
    "boxEaseSpeed": 900,
    "enableInfo": true,
    "hideImageCount": true,
    "autoShowInfo": true,
    "infoEaseFn": "easeOutBack",
    "infoEaseSpeed": 500
  });
};

function broadcast() {
}

$(document).ready(function() {
  // предзагрузка картинок
  $.preLoadImages("/media/static/img/ajax_loader.gif");

  // индикатор отработки ajax'а
  $.ajaxIndicator({
    loaderImage: "/media/static/img/ajax_loader.gif"
  });
  // возвращать :json => {:first => true/false, :last => true/false, :text => "<ul><li>..."}
  $(".persons_main").slidePersonInfo();
  // TODO: url для нового на сайте
  // перепараметр - page, значение - 2,3,4...
  // возвращать :json => {:last => true/false, :text => "<ul><li>..."}
  $("#site_news").getMoreInfo("/ajax/news/site/");
  // TODO: url для новостей инноваций
  // перепараметр - page, значение - 2,3,4...
  // возвращать :json => {:last => true/false, :text => "<ul><li>..."}
  $("#innovation_news").getMoreInfo("/ajax/news/inno/");
  // карусель персон на просмотре
  $(".persons .jcarousel").person_carousel();
  // история форума
  $("#history_link").history("/ajax/archive_years/");
  // TODO: url события
  // перепараметр - event, значение - id события...
  // возвращать :json => {:media => "<img ... />" :content => "какой-то html-код"}
  $("#events_carousel .jcarousel").eventsCarousel("/ajax/events/");
  $("#events_carousel").tooltip({
    tooltipId: "events_tooltip",
    offsetX: -26,
    offsetY: 2
  });

  // карусель в истории
  $("#history_carousel .jcarousel").historyCarousel();
  historyCarouselTooltip();

  // карусель с большим видео
  $("#full_video_carousel .jcarousel").fullVideoCarousel();
  $("#full_video_carousel").tooltip({
    tooltipId: "full_video_tooltip",
    offsetX: -26,
    offsetY: 2
  });

  // подсказки на года в истории
  $("#timeline").tooltip({
    tooltipId: "history_years_tooltip",
    offsetX: -40
  });

  doBigPicture();

  $.registrationBlock();

  flash("ul.message");

  broadcast();

});

