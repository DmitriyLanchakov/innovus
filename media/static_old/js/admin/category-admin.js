var CategoryAdmin = function(){
    var formUrl = '';
    var categoryWrap = $('<div id="category-wrap" title="New category"></div>');
    var calendars = function() {
        $.datepicker.setDefaults(
            $.extend({showMonthAfterYear: false
                }, $.datepicker.regional['ru']));

            var dtpk = $('#filter-range-datapicker1, #filter-range-datapicker2, #filter-range-datapicker3');
            var flage = true
            dtpk.datepicker({
                dateFormat: 'yy-mm-dd',
                onClose: function(dateText, inst) {
                    flage=true;
                }
            });
            dtpk.click(function(){
                if (flage) {
                    var datapicker_width = parseInt($('#ui-datepicker-div').css('left')) - 20;
                    $('#ui-datepicker-div').css({'left':datapicker_width});
                    flage = false;
                }
            })        
            
            dtpk.attr('autocomplete', 'off')
        }
    var drawModalWindow = function() {
        if ($('body').find('#' + categoryWrap.attr('id')).size() < 1) {
            $('body').append(categoryWrap);


            /**
             * Fetch form code
             */
            $.get(formUrl, {}, function(html){
                categoryWrap.html(html);
                $('#category-addform').submit(function(e){
                    var form = $(this);
                    $('ul.errorlist', form).remove();
                    $.post(formUrl, form.serialize(),
                        function(json){
                            if (json.success) {
                                categoryWrap.dialog('close');
                                category = json.category;

                                var li    = $('<li />');
                                var label = $('<label />');
                                var input = $('<input type="checkbox" checked="checked" />');
                                var list  = $('div.form-row.category ul');

                                input.attr('value', category.id);
                                input.attr('id', 'id_category_'+ parseInt(list.find('li').size()+1));
                                input.attr('name', 'category');

                                label.append(input);
                                label.append(category.title);
                                li.append(label);
                                list.append(li);
                                li.effect("highlight", {color: '#008800'}, 2000);

                            } else {
                                for (var e in json.errors) {
                                    $('#id_' + e, form).before(json.errors[e]);
                                }
                            }
                        },
                       'json'
                   );
                   return false;
               })
            }, 'html');

            /**
             * Applies dialog wrapper
             */
            categoryWrap.dialog({
                modal     : true,
                width     : 300,
                resizable : false,
                draggable : false,
                autoOpen: false,
                height: 175
            });

    	    /* Dirty hack */
    	    $("div.ui-dialog").removeClass ("ui-widget ui-widget-content ui-corner-all")
	        $("div.ui-dialog-titlebar").removeClass ("ui-widget-header ui-corner-all ui-helper-clearfix")
        }

        categoryWrap.dialog('open');


    }

    return {
        init: function(url) {
            formUrl = url;
            $('div.form-row.category').append('<a href="#" id="qqqqq" class="button">Add</a>');
            calendars();
            $('#qqqqq').click(function(e){
                drawModalWindow();
                return false;
            });

        }
    }
}

