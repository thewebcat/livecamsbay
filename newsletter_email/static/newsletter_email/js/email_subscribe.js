/**
 * Created by egor on 08.06.16.
 */
$(function(){
    function show_message(message){
         $.jGrowl(message, {
             position: 'bottom-left',
             group: 'popup_window'
         })
    }
    $('#email_subscribe').ajaxForm(
        {
            success: function(d){
                show_message(d['success']);
            },
            error: function(jqXHR){
                //$.jGrowl(JSON.parse(jqXHR.responseText)['error']);
                show_message(JSON.parse(jqXHR.responseText)['error']);
            }
        }
    )
});