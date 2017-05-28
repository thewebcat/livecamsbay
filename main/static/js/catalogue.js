var $range = $("#range_price"),
    slider;
/*функция отображения слайдера цены*/
function show_range_slider() {
    $range.ionRangeSlider({
        type: 'double',
        step: 1,
        force_edges: true,
        postfix: " лет",
        prettify: true,
        onChange: function (obj) {      // callback, вызывается при каждом изменении состояния
            console.log(obj)
            $('input[name="min_age"]').val(obj.from);
            $('input[name="max_age"]').val(obj.to);

        },
        onUpdate: function (obj) {      // callback, вызывается при каждом изменении состояния
            console.log(obj)
            $('input[name="min_age"]').val(obj.from);
            $('input[name="max_age"]').val(obj.to);

        },

        onFinish: function (obj) {      // callback, вызывается при каждом изменении состояния

             $('input[name="min_age"]').trigger('blur');
        }
    });

    slider = $range.data("ionRangeSlider");
}

$(document).ready(function(){

    /*если js включен убираем кнопку сабмита формы*/
    // $('.left-menu form .btn-submit').hide();
    if($('#range_price').length>0){
        show_range_slider()
    }
    /*Инициализируем pjax при клике на страницы*/
    $(document).pjax('.pagination a', '#item-search',{"push":true,"replace":false,"timeout":5000,"scrollTo":330})
})