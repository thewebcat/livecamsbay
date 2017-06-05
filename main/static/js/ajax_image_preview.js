$(function () {

    //{# Скрытое поле Джанги для определения количества переданных формсетов #}
    var total_forms_substring = 'TOTAL_FORMS';
    //{# Элемент в котором ведется подсчет количества передающихся формсетов #}
    var total_forms_element = undefined;
    //{# Регэксп для поиска любого числа, используется в замене числа в атрибутах элемента на +1 #}
    var reg = /\d+/g;
    //{# Атрибуты в которых нужно обновить числа при добавлении нового формсета #}
    var attributes = ['id', 'for', 'name']

    function form_callback(data, textStatus, jqXHR, el) {
        //{# класс котоый связывает нажимаемый элемент и формсет #}
        var parent_class = el.parent().attr('class')
        //{# клонирование последнего элемента для создания нового #}
        //var new_preview = $('.form-image-previews').find('.photo').last().clone()
        //{# если текущий элемент последний #}
        //if(parent_class == new_preview.children().attr('class')){
        //    //{# вычисляется число которое будет использоваться в классе нового элемента для нажатия #}
        //    var next_number = $('.formset-image-list').children().length;
        //    //{# меняется класс #}
        //    new_preview.find('div').attr('class', new_preview.find('div').attr('class').replace(reg, next_number));
        //    $('.formset-image-previews').append(new_preview)
        //}
        //{# у нажатого элемента меняется класс, чтобы он был больше не кликабельный #}
        var current_preview = $('.form-image-previews').find('.'+parent_class).parent()
        //current_preview.attr('class', 'photo1')
        //{# добавляется превьюшка #}
        current_preview.css('background-image', 'url("'+data.file+'")')

    }

    function formset_callback(data, textStatus, jqXHR, el) {
        //{# контейнер элемент #}
        var this_container = el.closest('.formset-image-container')
        //{# класс котоый связывает нажимаемый элемент и формсет #}
        var parent_class = el.parent().attr('class')
        //{# клонирование последнего элемента для создания нового #}
        var new_preview = this_container.find('.formset-image-previews').find('.photo').last().clone()
        //{# если текущий элемент последний #}
        if(parent_class == new_preview.children().attr('class')){
            //{# вычисляется число которое будет использоваться в классе нового элемента для нажатия #}
            var next_number = this_container.find('.formset-image-list').children().length;
            //{# меняется класс #}
            new_preview.find('div').attr('class', new_preview.find('div').attr('class').replace(reg, next_number));
            this_container.find('.formset-image-previews').append(new_preview)
        }
        //{# у нажатого элемента меняется класс, чтобы он был больше не кликабельный #}
        var current_preview = this_container.find('.formset-image-previews').find('.'+parent_class).parent()
        current_preview.attr('class', 'photo1')
        //{# добавляется превьюшка #}
        current_preview.css('background-image', 'url("'+data.file+'")')

    }
    //{# метод для обработки события change для полей file и последующей загрузки файла на сервер, #}
    //{# получения превьюшки, #}
    function stick_fileuploader_to(el, callback) {

        function wrap_callback(data, textStatus, jqXHR) {
            callback(data, textStatus, jqXHR, el)
        }

        el.on('change', function(e){
            //{# Какой-то межанизм jQuery для возможности ajax'ом отправки файлов #}
            var data = new FormData();
            $.each( e.target.files, function(key, value)
            {
                data.append(key, value);
            });

            $.ajax({
                type: "POST",
                url: upload_url,
                data: data,
                cache: false,
                dataType: 'json',
                processData: false, // Don't process the files
                contentType: false, // Set content type to false as jQuery will tell the server its a query string request
                success: wrap_callback,
                error: function(jqXHR, textStatus, errorThrown)
                {
                    console.log('ERRORS: ' + textStatus);
                }
            });
        })
    }

    if($('.formset-image-container').length>0) {

        $('.formset-image-container').each(function(){

            var this_container = $(this)

            //{# Элемент в котором ведется подсчет количества передающихся формсетов #}
            var total_forms_element = undefined;

            //{# Поиск поля для учета количества формсетов #}
            this_container.find('.formset-managment-form').children().each(function () {
                if ($(this).attr('id').indexOf(total_forms_substring) != -1)
                    total_forms_element = $(this)
            })
            //{# Уже имеющимся полям file назначается метод для ajax загрузки файлов #}
            this_container.find('.formset-image-list').find('input[type=file]').each(function () {
                stick_fileuploader_to($(this), formset_callback)
            })
            //{# Обработка нажатия на элемент для добавления нового файла #}
            this_container.find('.formset-image-previews').on('click', '.photo div', function () {
                //{# Если формсет с таким же классом пуст, то будет использоваться он #}
                //{# иначе будет создан новый формсет #}
                if ($('.formset-image-list .' + $(this).attr('class') + ' input[type=file]').val() == "") {

                } else {
                    //{# увеличивается счетчик формсетов на 1 при добавлении нового #}
                    total_forms_element.val(parseInt(total_forms_element.val()) + 1);
                    //{# вычисляется число которое будет использоваться в новом формсете в атрибутах #}
                    var next_number = this_container.find('.formset-image-list').children().length;
                    //{# формсет создается клонированием последнего #}
                    var formset_image = this_container.find('.formset-image-list').children().last().clone();
                    //{# изменяется класс с учетом замены текущего номера на следующий#}
                    formset_image.attr('class', formset_image.attr('class').replace(reg, next_number));
                    //{# изменяются все атрибуты с учетом замены текущего номера на следующий#}
                    formset_image.children().each(function () {
                        for (var i in attributes) {
                            if ($(this).attr(attributes[i]) != undefined)
                                $(this).attr(attributes[i], $(this).attr(attributes[i]).replace(reg, next_number))
                        }
                    })
                    //{# для поля file нового формсета назначается метод для ajax загрузки файлов #}
                    formset_image.find('input[type=file]').each(function () {
                        stick_fileuploader_to($(this), formset_callback)
                    })
                    //{# формсет добавляется на страницу #}
                    this_container.find('.formset-image-list').append(formset_image)
                    //{# для текущего элемента, который нажат, назначается класс такой же как у формсета, чтобы было легче искать элемент #}
                    $(this).attr('class', formset_image.attr('class'))
                }
                //{# триггер для нажатия на поле file #}
                this_container.find('.formset-image-list .' + $(this).attr('class') + ' input[type=file]').click()

            })
        })
    }
    if($('.form-image-element').length>0) {

        var form_image_element = $('.form-image-element')
        var form_image_previews = $('.form-image-previews')

        //{# Уже имеющимся полям file назначается метод для ajax загрузки файлов #}
        form_image_element.find('input[type=file]').each(function () {
            stick_fileuploader_to($(this), form_callback)
            $('.formset-image-list .' + $(this).attr('class') + ' input[type=file]').click()
        })

        form_image_previews.find('.form-image-input').on('click', function(){
            form_image_element.find('input[type=file]').click()
        })

    }


})