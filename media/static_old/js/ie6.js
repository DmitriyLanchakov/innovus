$(function(){
  $("body").prepend(
    "<div id='ie6stop'>" +
      "<a href='#' class='cornerx' alt='Закрыть' title='Закрыть'></a>" +
      "<div class='browsers'>" +
        "<p><b>ВНИМАНИЕ!</b> Сайт может выглядеть некорректно.<br/> Причина этого &ndash; ваш <b>устаревший и небезопасный браузер</b>.<br/> Учтите, что это может стать причиной того, что ваша система может быть подвергнута атакам вредноностного кода<br/><b>Пожалуйста, обновите ваш браузер!</b></p>" +
        "<a href='http://www.mozilla-europe.org/ru/firefox/' class='firefox'>FireFox</a>" +
        "<a href='http://www.opera.com/browser/' class='opera'>Opera</a>" +
        "<a href='http://www.apple.com/ru/safari/download/' class='safari'>Safari</a>" +
        "<a href='http://www.google.com/chrome?hl=ru' class='chrome'>Google Chrome</a>" +
        "<a href='http://www.microsoft.com/rus/windows/internet-explorer/worldwide-sites.aspx' class='ie8'>Internet Explorer 8</a>" +
        "<div>Если Вы не уверены, что сможете самостоятельно обновить интернет-браузер, обратитесь в службу IT-поддержки</div>" +
      "</div>" +
    "</div>");
  $("#ie6stop .cornerx").live("click", function() {
    $('#ie6stop').remove();
    $('.minwidth').css('padding-top', '0');
    return false;
  });
  $("body").wrapInner("<div class='min-width'/>");
  $(".min-width").wrapInner("<div class='minwidth'/>");
})

