$(document).ready(function() {

  $("#id_hotel").change(function() {
    $("#id_room_class").html("");
    $("#id_room_number").html("");
    if ($(this).val()) {
      $.ajax({
        url: "/profile/hotel/classes/" + $(this).val() + "/",
        cache: true,
        success: function(data) {
          var html = "<option selected='selected' value=''></option>";
          $(data).each(function(index, element) {
            html += "<option value='" + element[0] + "'>" + element[1] + "</option>";
          });
          $("#id_room_class").html(html);
        }
      });
    };
  });

  $("#id_room_class").change(function() {
    $("#id_room_number").html("");
    if ($(this).val() && $("#id_hotel").val()) {
      $.ajax({
        url: "/profile/hotel/classes/" + $("#id_hotel").val() + "/" + $(this).val() + "/",
        cache: true,
        success: function(data) {
          var html = "<option selected='selected' value=''></option>";
          $(data).each(function(index, element) {
            html += "<option value='" + element["id"] + "'>" + element["value"] + "</option>";
          });
          $("#id_room_number").html(html);
        }
      });
    };
  });

  var datetime_format = "%d.%m.%Y %H:%M";
  var timeFormat = "24";

  if ($("body").hasClass("en")) {
    datetime_format = "%m-%d-%Y %I:%M %p";
    timeFormat = "12";
  }

  $("#id_arrival_date, #id_departure_date").dynDateTime({
    showsTime: true,
    ifFormat: datetime_format,
    timeFormat: timeFormat,
    align: "Br"
  }).attr("autocomplete", "off");

});

