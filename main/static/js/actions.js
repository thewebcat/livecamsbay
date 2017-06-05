$(function () {
    $('.jq_show_delete_form').on('click', function(e){
        e.preventDefault();
        var form = $(this).closest('.jq_action_bar').find('.jq_action_delete_form')
        var container_action_bar = $(this).closest('.container_action_bar')
        if(container_action_bar.data('resize')==true)
            form.width(container_action_bar.width()).height(container_action_bar.height())
        form.show()
    });
    $('.jq_cancel_form').on('click', function(e){
        e.preventDefault();
        $(this).closest('.jq_action_delete_form').hide()
    })
    $('.jq_submit_form').on('click', function(e){
        e.preventDefault()
        var url = $(this).attr('href')
        var _this = $(this)
        $.ajax({
            url: url,
            cache: false
        })
        .done(function(json) {
            if(json.success) {
                if(json.next && _this.closest('.container_action_bar_visible').length) {
                    var next = $($('.breadcrumb')[$('.breadcrumb').length-2]).find('a').attr('href');
                    window.location = next
                } else {
                    _this.closest('.container_action_bar').hide(500, function () {
                        $(this).remove();
                    });
                }
            } else {
            }
        });
    })
});