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
            //console.log(obj)
            $('input[name="min_age"]').val(obj.from);
            $('input[name="max_age"]').val(obj.to);

        },
        onUpdate: function (obj) {      // callback, вызывается при каждом изменении состояния
            //console.log(obj)
            $('input[name="min_age"]').val(obj.from);
            $('input[name="max_age"]').val(obj.to);

        },

        onFinish: function (obj) {      // callback, вызывается при каждом изменении состояния

             $('input[name="min_age"]').trigger('blur');
        }
    });

    slider = $range.data("ionRangeSlider");
}

$(document).on('keyup','input[name="min_age"],input[name="max_age"]',function(e){
       if(e.keyCode == 13)
    {
        $(this).trigger("blur");
    }
})

$(document).on('blur', 'input[name="min_age"],input[name="max_age"]', function () {

    //console.log(slider)
    slider.update({
        from: parseInt($('input[name="min_age"]').val()),
        to: parseInt($('input[name="max_age"]').val())
    });
    $('.left-menu form').trigger('submit');
});

$(document).ready(function(){

    /*если js включен убираем кнопку сабмита формы*/
    // $('.left-menu form .btn-submit').hide();
    if($('#range_price').length>0){
        show_range_slider()
    }
    /*Инициализируем pjax при клике на страницы*/
    $(document).pjax('.pagination a', '#item-search',{"push":true,"replace":false,"timeout":5000,"scrollTo":0})
});

/*При клике на чекбоксы сабмитим форму для pjax*/
$(document).on('change','input[type=checkbox]',function(){
    $('.left-menu form').trigger('submit')
})

/*Если идет pjax запрос - выводим прелоадер*/
$(document).on('pjax:send', function() {
     $('#item-search').html('<div class="loading" ></div><br/><br/>')
    $("body").animate({
        scrollTop: 0
    }, "500", "swing")

});
/*Событие на сабмит формы pjax*/
$(document).on('submit', ".left-menu form", function (event) {$.pjax.submit(event, '#item-search', {"push":true,"replace":false,"timeout":5000,"scrollTo":false});});