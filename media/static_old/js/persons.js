var Publisher = function(url){
    var $ = jQuery;
    $(function(){
        $('#id_publish').click(function(){
            $('#id_publish_container').addClass('progress');
            $.ajax({
                type     : 'POST',
                dataType : 'json',
                data     : { object_id: $('#id_object_id').val() },
                url      : url,
                success  : function(json){
                
                },
                complete : function(){
                    $('#id_publish_container').removeClass('progress');
                }
            });
        });
    })
};

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
            $.post(
                '/admin/persons/person/sort/',
                $('tbody', table).sortable('serialize', {key: 'sort_order'}),
                function(json){},
                'json'
            );
        }
    });
});
