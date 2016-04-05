function toggler(container) {
  $(container).each(function() {
    var block = this;
    var info = $(".hidden", block).removeClass("hidden").hide();
    var expander = $(".expander", block);
    var collapser = $(".collapser", block).wrap("<p></p>").css("margin", "0 0 20px 20px");

    $(expander).click(function(event) {
      event.preventDefault();
      if (info.html() == "") {
        $.ajax({
          url: $(expander).attr("href"),
          cache: true,
          success: function(data) {
            info.html(data.html).append($(collapser).clone());
            $(info).show();
            collapser = $(".collapser", block);
            $(collapser).show();
            $(expander).hide();
            doBigPicture();
          }
        });
      } else {
        if (!$("." + $(collapser).attr("class"), info).length)
          info.append($(collapser).clone());
        $(info).show();
        collapser = $(".collapser", block);
        $(collapser).show();
        $(expander).hide();
      };
    });

    $(collapser).live("click", function(event) {
      event.preventDefault();
      info.hide();
      $(collapser).hide();
      $(expander).show();
      $.scrollTo($(block), 200, {over: -0.2});
    });
  });
};

$(document).ready(function() {
  toggler(".toggler");
});
