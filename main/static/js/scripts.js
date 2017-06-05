function setBigImage(foto) {
    var image_conteiner = $(foto).closest('.thumbs').prev();
    image_conteiner.find('a').attr('href', $(foto).parent('.it').children('a').attr('href'));
    image_conteiner.find('img').attr('src', foto.src);
}

// function open_popup(id) {
//     $(id).show();
//     $('.overlay').show()
// }
// function close_popup() {
//     $('.popup').hide();
//     $('.overlay').hide()
// }
// $(function(){
//     $('.jq_open_popup').on('click', function(e){
//         e.preventDefault();
//         open_popup($(this).attr('href'))
//     })
//     $('.close, .overlay').on('click', function(e){
//         e.preventDefault();
//         close_popup()
//     })
//     $(document).keydown(function(e) {
//         if (e.keyCode == 27)
//             close_popup();
//     });
// })


$(function(){
    $('#jq-change-geo').on('click', function(e){
        e.preventDefault()
        console.log($(this).text())
    })
})


$(function(){
    $('.ajax-data-sender').on('click', function(e){
        e.preventDefault();
        var data = $(this).data();
        var url = $(this).closest('.ajax-data-sender-url').data('url');

        $.ajax({
            type: "POST",
            url: url,
            data: data
        }).done(function(data) {
            if(data.success) {
                console.log('success')
            }
            if(data.reload) {
                location.reload();
            }
        });
    })
})


var re = /([^&=]+)=?([^&]*)/g;
var decodeRE = /\+/g;  // Regex for replacing addition symbol with a space
var decode = function (str) {
    return decodeURIComponent(str.replace(decodeRE, " "));
};
$.parseParams = function (query) {
    var params = {}, e;
    while (e = re.exec(query)) {
        var k = decode(e[1]), v = decode(e[2]);
        if (k.substring(k.length - 2) === '[]') {
            k = k.substring(0, k.length - 2);
            (params[k] || (params[k] = [])).push(v);
        }
        else params[k] = v;
    }
    return params;
};

function select2_initial(el) {
    el.select2({
        ajax: {
            url: cities_filter_url,
            dataType: 'json',
            data: function (params) {
                return {
                    startswith: params.term, // search term
                    page: params.page
                };
            },
            processResults: function (data, params) {
              return {results: data.items};
            }
        },
        minimumInputLength: 1,
        language: "ru"
    }).select2('open').select2('close');
    el.on("select2:select", function() {
        $(this).select2('open').select2('close')
    });
    add_tooltip(el.next())
}

function select2_basic_initial(el) {
    el.select2({
        language: "ru",
        minimumResultsForSearch: Infinity
    }).select2('open').select2('close');
    el.on("select2:select", function() {
        $(this).select2('open').select2('close')
    });
    add_tooltip(el.next())
}

function add_tooltip(element) {
    element.tooltip({
        position: {
            my: "left",
            at: "left bottom+22",
            collision: "none"
        },
        using: function (position, feedback) {
            $(this).css(position);
            $("<span>")
                .addClass("am_tooltip")
                .addClass(feedback.vertical)
                .addClass(feedback.horizontal)
                .appendTo(this);
        },
        items: "input:not([id$=phone_0]):not([id$=phone_1]):not([id$=phone_2]), textarea, select, .select2.select2-container, .phone_split",
        content: function () {
            var element = $(this);

            if (element.is(".select2.select2-container")) {
                return $(this).prev().attr('placeholder')
            }
            if (element.is(".phone_split")) {
                return $(this).find('input:last').attr('placeholder')
            }
            if (element.is("input:not([id$=phone_0]):not([id$=phone_1]):not([id$=phone_2]):not(.select2-search__field)") || element.is("textarea") || element.is("select")) {
                return $(this).attr('placeholder')
            }
        },
        hide: {effect: "hide", duration: 1000}
    });
}

$(function() {
    var tooltip_selectors = ["input", "textarea", "select", ".select2"];
    for (var i in tooltip_selectors) {
        add_tooltip($(tooltip_selectors[i]))
    }
});

function modalFancyboxWithCKEditor(textarea_id, target) {
    // Функция отвечает за инит/дестрой редактора в модальном окне при открытии/закрытии окна
    // Иначе редактор в fancybox не будет работать
    // textarea_id - id текстового поля
    // target - обект открывающий fancybox, обычно ссылка

    var textarea = $(textarea_id);

    target.fancybox({
        speed : 0,
        beforeLoad:function(){
            if (CKEDITOR.instances[textarea.attr('id')] ) {
                CKEDITOR.instances[textarea.attr('id')].destroy();
                delete CKEDITOR.instances[textarea.attr('id')];
            }
            CKEDITOR.replace(textarea.attr('id'), textarea.data('config'));
        },
        beforeClose: function () {
            CKEDITOR.instances[textarea.attr('id')].destroy();
        }
    });
}

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};