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