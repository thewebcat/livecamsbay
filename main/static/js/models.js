$(document).ready(function () {
    $('.add_to_favourites').ajaxForm({
        success: function(responseText) {
            console.log(responseText);
            $.fancybox.open({
                src  : '#add-to-favourites',
                type : 'inline',
            });
            if(responseText.action == 'add') {
                $('#add-to-favourites .call_order_form_success.remove-model').hide();
                $('#add-to-favourites .call_order_form_success.add-model').show();
                $('.add_to_favourites button[type=submit]').text('Удалить модель из избранного');
                $('.add_to_favourites').attr('action', '/favourites/remove/');

            } else if(responseText.action == 'remove') {
                $('#add-to-favourites .call_order_form_success.add-model').hide();
                $('#add-to-favourites .call_order_form_success.remove-model').show();
                $('.add_to_favourites button[type=submit]').text('Добавить модель в избраные');
                $('.add_to_favourites').attr('action', '/favourites/add/');
            }
            // $('#recall_form_popup .field-alert').removeClass('field-alert');
        }
    });
});