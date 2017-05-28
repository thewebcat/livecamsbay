$(document).ready(function(){
    /*если js включен убираем кнопку сабмита формы*/
    // $('.left-menu form .btn-submit').hide();
    // if($('#range_price').length>0){
    //     show_range_slider()
    // }
    /*Инициализируем pjax при клике на страницы*/
    $(document).pjax('.pagination a', '#item-search',{"push":true,"replace":false,"timeout":5000,"scrollTo":330})
})