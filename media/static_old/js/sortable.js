
jQuery(function(){
    var $ = jQuery;
    var table = $('table[cellspacing="0"]'); 
 
    $('tr', table).each(function(i){
        var tr = $(this);

        if (i == 0) {
            var td = $('<th>&nbsp;</th>');
            td.html('&nbsp;');    
            
        } else {
            var td = $('<td>&nbsp;</td>');
            td.addClass('handle');
            td.html('Хвать!');
            tr.attr('id',  'person-' + $('input[name="_selected_action"]', tr).val());
        }
        tr.prepend(td);
    });    
    
    $('tbody', table).sortable({
        handle : '.handle',
        items  : 'tr',
        update : function(){
            //window.location.pathname
            //window.location.search    '' || '?foo=bar'

            $.post(
                window.location.pathname + 'sort/' + window.location.search,
                $('tbody', table).sortable('serialize', {key: 'sort_order'}),
                function(json){},
                'json'
            );
        }
    });
});
