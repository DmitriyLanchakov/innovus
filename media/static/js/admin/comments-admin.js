var CommentsAdmin = function(){
    var clickHandler = function(selector, callback) {
        $(selector).click(function(e){
            var item = $(this);
            $.get(
                item.attr('href'), {},
                function(json){
                    callback(item, json);
                },
                'json'
            );
            return false;
        });
    }

    return {
        init: function(){
            /* In post details */
            clickHandler('li.comment a.ban-ip-button',
                function(item, json) {
                    item.html(json.new_label);
                }
            );

            clickHandler('li.comment a.comment-approve-button',
                function(item, json) {
                    item.html(json.new_label);
                    var cmt = item.closest('li');
                    json.approved ? cmt.removeClass('blamed') : cmt.addClass('blamed');
                }
            );

            /* In comment list */
            clickHandler('tr a.approve-comment-button', function(item, json) {
                var search  = json.approved ? 'no' : 'yes';
                var replace = json.approved ? 'yes' : 'no';
                var img = $(item).closest('tr').find('img');
                var src = img.attr('src').replace(search, replace);
                img.attr('src', src);
                item.text(json.new_label);
            });

            clickHandler('tr a.ban-ip-button', function(item, json){
//                alert(json);
            });
        }
    }
};

