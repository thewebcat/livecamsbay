$(function() {
    $('#for_recall_form').click(function(){
        $('#recall_form_popup').toggle()
    });
    $('#recall_form').ajaxForm(
        {
            success: function() {
                $('#recall_form_popup .call_order_form_success').show();
                // $('#recall_form_popup .field-alert').removeClass('field-alert');
            }
        }
    );
    function getUrlVars() {
        var vars = {};
        window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
            });
        return vars;
    }
    if(getUrlVars()['recall_popup']){
        $('#for_recall_form').click()
    };
});
