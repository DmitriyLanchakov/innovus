$(function() {
  $("#post_comment_form #id_content").maxlength({
    maxCharacters : 1000,
    status        : true,
    callbacks     : [function(input, current_length, exceed) {
      $("#post_comment_form .comment_status").text(current_length);
    }]
  });

  $("#post_comment_form").submit(function() {

    var submitButton = $(".submit_comment", this);
    submitButton.attr("disabled", "disabled");
    var commentList;
    var commentForm = $('#post_comment_form');
    var commentFormAction = commentForm.attr('action');

    $("li.error", commentForm).removeClass("error");
    $("ul.errorlist", commentForm).remove();

    var restoreFormDefault = function() {
      commentForm.attr('action', commentFormAction);
      $('.comment_form h2').after(commentForm);
    };

    $.ajax({
      type: "post",
      dataType: "json",
      data: commentForm.serialize(),
      url: commentForm.attr("action"),
      success: function(json, status, xhr) {
        if (json.success) {
          if ($(".comments ul").length) {
            commentList = $(".comments ul");
          } else {
            $("<ul></ul>").appendTo($(".comments"));
            $(".comments p").remove();
            commentList = $(".comments ul");
          };
          if (json.parent) {
            $("#comment_" + json.parent).after(json.comment);
          } else {
            commentList.append(json.comment);
          };
          commentForm.find("textarea").val("");
          restoreFormDefault();
        } else {
          for (var i in json.errors) {
            $("#id_" + i).closest('li').addClass('error').after(json.errors[i]);
          };
        };
      },
      complete: function(xhr, status) {
        submitButton.removeAttr("disabled");
      }
    });
    return false;
  });

  $('.comments a.comment_reply').live('click', function(e){
    var link = $(this);
    var comment = link.closest('li');
    var commentForm = $("#post_comment_form");
    comment.append(commentForm);
    commentForm.attr('action', link.attr('href'));
    commentForm.find('textarea').focus();
    return false;
  });

});

