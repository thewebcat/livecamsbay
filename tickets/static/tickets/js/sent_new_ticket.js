$(document).ready(function() {
    $('#add_new_ticket').ajaxForm(
        {
            url: '/add_new_ticket/',
            type: 'post',
            success: function() {
                $('#form_popup .call_order_form_success').show();
                $('#form_popup form')[0].reset();
                $('#form_popup .field-alert').removeClass('field-alert');
                setTimeout(function(){
                    //$('#form_popup .call_order_form_success').fadeOut(2000, function(){
                    $('#form_popup .call_order_form_success').fadeOut();
                    $('#form_popup').find('a.close').click();
                    //});
                }, 3000);
                //$('#form_popup').toggle('300');
                //console.log('Новый тикет открыт, ответ вы получите у себя в профиле');
            },
            error: function() {
                //$('#form_popup').toggle('300');
                //console.log('Нежданная ошибка, мы исправим, вскоре...')
            }
        }
    );
});
