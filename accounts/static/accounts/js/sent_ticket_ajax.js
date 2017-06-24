$(document).ready(function() {
    $('.add_message_to_ticket').ajaxForm({
        url: '',
        type: 'post',
        success: function(responseText, statusText, xhr, $form) {
            var linkFile = '';
            if (responseText.file){
                linkFile = '<br><a style="margin-top: 10px; color: #417538;" href="'+
                        responseText.file +
                        '">Приложенный файл</a>'
            }
            $('<div class="message_user"><div class="ticket_date">' +
                responseText.date +
                '</div><div class="ticket_message">' +
                responseText.message +
                linkFile +
                '</div><div class="ticket_avatar"><img src="' +
                responseText.img + '' +
                '"></div></div>').insertBefore($form.parent());
            $form[0].reset();
            $form.find('input[name="file"]').change()
           }
        }
    );
});