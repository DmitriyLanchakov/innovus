var ErrorHandler = function(){
    var _errors  = {};
    var _created = false;
    var _success = false;
    var _objectId = '';

    return {
        'addMessage': function(field, html) {
            _errors[field] = html;
        },

        'setSuccess': function(flag) {
            _success = flag;
        },

        'setObjectId': function(objectId) {
            _objectId = objectId;
        },

        'setCreated': function(flag){
            _created = flag;
        },

        'fire': function(){
            // Flag 'successfully' is enabled
            if (_success) {
                $('#inform').html('<p class="errornote green-note">Successfully</p>');
                $('#id_object_id').val(_objectId );

            // Some validation errors happens
            }
            else
            {
                $('#inform').html('<p class="errornote">ERROR</p>');

                for(var f in _errors) {
                    var row = $('.form-row.' + f); row.addClass('errors');
                    if (! $('.errorlist', row).get(0))
                    {
                        row.prepend(_errors[f]);
                    }
                }
            }

            var _form = $('#post_form');

            $(_form).removeAttr('target');
            $(_form).removeAttr('action');
            $('#inform p').fadeIn(300);
        }
    }
}

var Publisher = function(post_url){


    $('#id_publish').click(function(){
        var obj_id = $('#id_object_id').val()
        $('#id_publish_container').addClass('progress');
        $.post(post_url, {'object_id': obj_id}, function(data){
            $('#id_publish_container').removeClass('progress');
        });
    });

}

var PostAdmin = function(){
    var params = null;
//    var iframeName = 'hidden-target';
//    var iframe = $('<iframe name="' + iframeName + '" id="hidden-target" src="about:blank"></iframe>');
//    var form   = $('#post_form');
//    var inform = $('<div id="inform"></div>');
//    var action = '';

    var fixMarkUp = function()
    {
        var all_node = $('.datetime')
        for (var i=0;i<all_node.length;i++){
            $(all_node[i].firstChild).wrap('<span class="date_span"/>');
            $($(all_node[i]).find('br').get(0).nextSibling).wrap('<span class="time_span"/>');
        }
        $.datepicker.setDefaults(
                                $.extend({showMonthAfterYear: false
                                }, $.datepicker.regional['ru']));


        $('#id_public_from_0, #id_public_till_0').click(function(){
            var datapicker_width=parseInt($('#ui-datepicker-div').css('left'))-20;
            $('#ui-datepicker-div').css({'left':datapicker_width});
        })
        ;
        $('#id_public_from_0, #id_public_till_0').datepicker({
                                showOn: 'button',
                                buttonImage: '/media/admin/img/admin/icon_calendar.gif',
                                buttonImageOnly: true,
                                dateFormat: 'yy-mm-dd'
        });


        var nwq = $('.inline-related h3 b');
        for (var i=0;i<nwq.length;i++) { $($(nwq[i]).get(0).nextSibling).remove() }

    }

    var attachAdd = function(){
        var countAttaches = function() {
            return $('div.inline-related').size();
        }

        var container = $('div.inline-group');
        var first = container.find('div.inline-related');
        if (first.size() == 0) {
            return;
        }

        var html = '<div class="inline-related">' + first.html() + '</div>';
        html = html.replace(/&nbsp; #(\d+)/, '&nbsp;#%S');

        //<h3><b>Attachment:</b>&nbsp; #1

        container.append('<ul class="tools"><li><a class="add" href="">Add</a></li></ul>')
        container.find('a.add').click(function(e){
            var h = html;
            var c = countAttaches();
            h = h.replace('%s', c);
            h = h.replace('%S', c+1);

            var link = $(this);
            link.closest('ul').before(h);

            return false;
        })
    }


    return {
        init: function(prms)
        {
//            params = prms;
//            action = form.attr('action');
//            $('body').append(inform);
//            $('body').append(iframe);
//            $('input[name=_continue]').click(function()
//            {
//                $('div.form-row').removeClass('errors');
//                $('ul.errorlist').remove();
//                form.attr('action', params.url);
//                form.attr('target', iframeName);
//                form.submit();
//                form.removeAttr('action');
//                form.removeAttr('target');
//                return false;
//            });
           window.$ = window.jQuery
                    fixMarkUp();
//            attachAdd();
        }
    }
};

