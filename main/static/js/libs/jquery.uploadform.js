/**
 * jQuery Formset 1.3-pre
 * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
 * @requires jQuery 1.2.6 or later
 *
 * Copyright (c) 2009, Stanislaus Madueke
 * All rights reserved.
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */
;(function($) {
    $.fn.uploadform = function(opts)
    {
        var options = $.extend({}, $.fn.uploadform.defaults, opts),
            $$ = $(this),

            ajaxSuccess = function(data, textStatus, jqXHR) {
                imageField.val(data.file);
                addPreview(imageField)
                removeMessageAlert(imageField)
            },

            ajaxError = function(jqXHR, textStatus, errorThrown) {
                addMessageAlert()
            },

            addMessageAlert = function() {
                var error_message = '<div class="message-alert"><i class="fa fa-exclamation-circle" aria-hidden="true"></i> Неверный формат файла или его размер больше ' + upload_file_max_size + ' мб.</div>';
                if(!imageField.prev().hasClass('message-alert')) {
                    imageField.before(error_message)
                }
            },

            removeMessageAlert = function(imageField) {
                if(imageField.prev().hasClass('message-alert')){
                    imageField.prev().remove()
                }
            },

            addPreview = function(inputField) {
                if(inputField.val()) {
                    addFileLabel.css('background-image', 'url(' + inputField.val().split('?')[1] + ')')
                } else {
                    addFileLabel.attr('style', '')
                }
            };

        if ($$.length) {
            var imageField = $$,
                addFileLabel, addFileInput, closestForm, formReset;
            // FIXME: Perhaps using $.data would be a better idea?

            addFileLabel = $('<label for="' + options.ajaxUploadFileId + '" class="ajax_upload_file_label photo add_file"></label>');
            addFileInput = $('<input type="file" id="' + options.ajaxUploadFileId + '" class="ajax_upload_file_input">');
            formReset = $('<form />');
            closestForm = $$.closest('form');
            // Otherwise, insert it immediately after the last form:
            imageField.after(addFileLabel);
            closestForm.after(formReset.append(addFileInput));

            addPreview(imageField)

            addFileInput.on('change', function(e){
                //{# Какой-то межанизм jQuery для возможности ajax'ом отправки файлов #}
                var data = new FormData();
                var error = false
                $.each( e.target.files, function(key, value)
                {
                    if(((options.allowedFileExtensions[0]) && options.allowedFileExtensions.indexOf(value.name.split('.').pop()) == -1) || value.size > upload_file_max_size*1024*1024) {
                        formReset[0].reset();
                        addMessageAlert()
                        error = true
                        return
                    }
                    data.append(key, value);
                });

                if(error)
                    return
                data.append('csrfmiddlewaretoken', closestForm.find('input[name="csrfmiddlewaretoken"]').val());

                $.ajax({
                    type: "POST",
                    url: upload_url,
                    data: data,
                    cache: false,
                    dataType: 'json',
                    processData: false, // Don't process the files
                    contentType: false, // Set content type to false as jQuery will tell the server its a query string request
                    success: ajaxSuccess,
                    error: ajaxError
                });
                formReset[0].reset();
            })

            imageField.change(function(){
                addPreview(imageField)
            })
        }

        return $$;
    };

    /* Setup plugin defaults */
    $.fn.uploadform.defaults = {
        ajaxUploadFileId: 'id-ajax-upload-one-file',
        allowedFileExtensions: ''
    };
})(jQuery);