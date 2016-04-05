var Comment = function() {
    var MAXLENGTH = 1000; // @TODO откуда брать?
    var TEXTAREA = $('#id_content');
    var COUNTER = $('#tracker3');

    var signal = function(input, curlen, exceed)
    {
        if (exceed) {
            input.css({'border-color':'#E3867E'});
        }  else {
            input.css({'border-color':'#969696'});
        }

        COUNTER.get(0).innerHTML = curlen;
    }


    return {
        'init': function(textarea, maxlength, counter){
            TEXTAREA  = textarea;
            MAXLENGTH = maxlength;
            COUNTER   = counter;

            $(TEXTAREA).maxlength({
                maxCharacters : MAXLENGTH,
                status        : true,
                callbacks     : [signal]
            });

            //
            var commentList = $('#comments ul');
            var commentForm = $('#post-comment-form');
            var commentFormAction = commentForm.attr('action');

            var restoreFormDefault = function(){
                commentForm.attr('action', commentFormAction);
                $('#post-new-comment-container').append(commentForm);
            }

            commentForm.submit(function(e){
                var submitButton = $('#submit-comment');
                submitButton.attr('disabled', 'disabled');

                commentForm.addClass('progress');
                $('ul.errorlist').remove();
                $('li.error').removeClass('error');
                
                $.ajax(
                    {
                        type     : 'post',
                        dataType : 'json',
                        data     : commentForm.serialize(),
                        url      : commentForm.attr('action'),
                        success  : function(json, status, xhr){
                            if (json.success && json.comment) {
                                if (json.parent) {
                                    $('#comment-'+json.parent).after(json.comment);
                                } else {
                                    commentList.append(json.comment);
                                }
                                commentForm.find('textarea').blur().val('');
                                restoreFormDefault();

                            /* insert errors */
                            } else {
                                if (json.errors) {
                                    for (var i in json.errors) {
                                          $('#id_'+i).closest('LI').addClass('error');
                                          if ( i == "content" ){
                                            $('#id_'+i).closest('LI').before(json.errors[i]);
                                          }
                                          else {
                                            $('#id_'+i).before(json.errors[i]);
                                          }

                                    }
                                }
                            }
                        },

                        complete : function(xhr, status) {
                            commentForm.removeClass('progress');
                            submitButton.removeAttr('disabled');
                        }
                    }
                );

                // return not OpenID
                val = $('#id_openid-openid').val()
                if (! val) return false;
                return val && val.length > 0;
            });


            $('li a.comment-reply').live('click', function(e){
                var link = $(this);
                var comment = link.closest('li');

                comment.append(commentForm);
                commentForm.attr('action', link.attr('href'));
                commentForm.find('textarea').focus();

                return false;
            });


            /* переброс формы на место по клику на h2 New Comment */
            $('#post-new-comment-container h2').click(restoreFormDefault);


//            /* переклик anonymous-openid */
//            $('#openid').addClass('hide');
//            $('a.anonymous, a.openid').click(function(){
//                 var cls = $(this).attr('class');
//
//                 if (cls == 'anonymous') {
//                     $('#anonymous').removeClass('hide');
//                     $('a.anonymous').addClass('act_login');
//                     $('#openid').addClass('hide');
//                     $('a.openid').removeClass('act_login');
//                     $('#id_openid-openid').val('');
//                 } else if (cls == 'openid') {
//                     $('#anonymous').addClass('hide');
//                     $('a.anonymous').removeClass('act_login');
//                     $('#openid').removeClass('hide');
//                     $('a.openid').addClass('act_login');
//
//                     $('#id_anon-name').val('');
//                     $('#id_anon-email').val('');                     
//                     $('#id_anon-site_url').val('');
//                     }
//
//                 return false;
//            });

        }
    }
}