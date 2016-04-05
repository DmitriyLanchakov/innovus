var selected_input = [];

function toggle_search_input_label() {
  if ($("#search .search_input").val() == "" && $("#search .search_input")[0] != selected_input[0]) {
    $("#search .search_input_label").show();
  } else {
    $("#search .search_input_label").hide();
  };
};

function search_label() {
  $("#search .search_input")
  .focus(function() {
    toggle_search_input_label();
  })
  .blur(function() {
    selected_input = [];
    toggle_search_input_label();
  });
};

function toggle_sign() {
  $("#sign_container .sign_up_block .close, #sign_container .sign_in_block .close").click(function() {
    $("#sign_container .sign_up_block").hide();
    $("#sign_container .sign_in_block").hide();
    return false;
  });
  $("#header .auth .sign_up").click(function() {
    if ($("#sign_container .sign_in_block").is(":visible")) {
      $("#sign_container .sign_in_block").hide();
    };
    $("#sign_container .sign_up_block").toggle();
    return false;
  });
  $("#header .auth .sign_in").click(function() {
    if ($("#sign_container .sign_up_block").is(":visible")) {
      $("#sign_container .sign_up_block").hide();
    };
    $("#sign_container .sign_in_block").toggle();
    if ($("#sign_container .sign_in_block").is(":visible")) {
      $("#sign_container .sign_in_block #header_id_username").focus();
    };
    return false;
  });
};

function toggle_event_interviews() {
  $("#content .greeting .toggler .expander a").click(function() {
    var owner_block = $(".person_item", $(this).closest(".toggler")).attr("id");
    var expander = $(".expander", $(this).closest(".toggler"));
    var collapser = $(".collapser", $(this).closest(".toggler"));
    var interview = $(".hidden", $(this).closest(".toggler"));
    expander.slideToggle("fast");
    collapser.slideToggle("fast");
    interview.slideToggle("slow");
    $.scrollTo("#" + owner_block, 500, {offset: {top: -50 }});
    return false;
  });
  $("#content .greeting .toggler .collapser a").click(function() {
    var owner_block = $(".person_item", $(this).closest(".toggler")).attr("id");
    var expander = $(".expander", $(this).closest(".toggler"));
    var collapser = $(".collapser", $(this).closest(".toggler"));
    var interview = $(".hidden", $(this).closest(".toggler"));
    expander.slideToggle("fast");
    collapser.slideToggle("fast");
    interview.slideToggle("slow");
    $.scrollTo("#" + owner_block, 500, {offset: {top: -50 }});
    return false;
  });
};

function trigger_my_programm() {
  $("#content .my_events input.trigger").change(function() {
    if ($(this).attr("checked")) {
      $("td input[type=checkbox]", $(this).closest("table")).attr("checked", true);
    } else {
      $("td input[type=checkbox]", $(this).closest("table")).attr("checked", false);
    }
  });
};

function flash_notice() {
  $("#flash_notice p").stop(true, true).show();
  setTimeout("$('#flash_notice p').slideUp(function() { $(this).parent().remove(); });", 3000);
  $("#flash_notice p").click(function() {
    $(this).slideUp(function() {
      $(this).parent().remove();
    });
  });
};

function open_swf_material() {
  $(".type_swf a").click(function() {
    $("<div id='swf_material'></div>").appendTo("body").hide();
    var title = $(this).html();
    var url = $(this).attr("href");
    var flashvars = {
      "uid": "swf_material",
      "file": url
    };
    var params = {
      id: "swf_material",
      allowFullScreen: "true",
      allowScriptAccess: "always",
      wmode: "transparent"
    };
    $("#swf_material").dialog({
      width: 510,
      height: 470,
      modal: true,
      title: title,
      resizable: false,
      open: function() {
        new swfobject.embedSWF(url, "swf_material", "510", "410", "9.0.115", false, flashvars, params);
      }
    });
    return false;
  });
};

$(function() {
  flash_notice();
  $(":input").focus(function() {
    selected_input = $(this);
  });
  $("#header .auth a[rel=tipsy]").tipsy({
    gravity: "e",
    html: true,
    live: true,
    opacity: 1
  });
  $("#content .registration abbr").tipsy({
    gravity: 's',
    html: true,
    live: true,
    opacity: 1
  });
  $("#history_timeline li a").tipsy({
    gravity: 's',
    html: true,
    live: true,
    opacity: 1
  });
  toggle_search_input_label();
  search_label();
  toggle_sign();
  toggle_event_interviews();
  $("#content .event_details .speakers .to_comments").click(function() {
    $.scrollTo("#content .event_details .comments", 500, {offset: {top: -50 }});
    return false;
  });
  if (location.href.match("#to_comments")) {
    $.scrollTo("#content .comments", 500, {offset: {top: -50 }});
  };
  $(".program_print_version").click(function() {
    window.print();
    return false;
  });
  trigger_my_programm();
  open_swf_material();
});

