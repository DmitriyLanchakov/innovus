$(function() {
  $("#header .auth .sign_up, #header .auth .sign_in").click(function() {
    $(location).attr("href", $(this).attr("href"));
  });
});

