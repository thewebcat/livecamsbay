$(document).ready(function() {
    $('.ticket_button').click(function(event){
        event.preventDefault()
        function changeImg(e){
            var img = $(e).children('a').children('img');
            var tmp = img.attr('src');
            img.attr('src', img.data('href'));
            img.data('href', tmp);
        }
        function changeHiddenContent(e){
            var content = $(e).parent().parent().children('.ticket_content');
            content.slideToggle('300')
        }

        if ($(this).hasClass('active')){
            $(this).removeClass('active');
            changeImg(this);
            changeHiddenContent(this)
        }
        else {
            [].forEach.call($('.ticket_button'), function(e){
                if ($(e).hasClass('active')){
                    $(e).removeClass('active');
                    changeImg(e);
                    changeHiddenContent(e)
                }
            });
            $(this).addClass('active');
            changeImg(this);
            changeHiddenContent(this)
        }
}
    )

});
