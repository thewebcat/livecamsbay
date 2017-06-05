var $;

$ = jQuery;

$.fn.customSelect = function () {

    var Draw = function (element) {

        var current_select = $(element);
        var select_width = current_select.outerWidth();
        var select_height = current_select.outerHeight();

        var custom_select_wrapper = $('<div />');
        custom_select_wrapper.addClass('custom-select-wrapper');
        custom_select_wrapper.height(select_height);
        custom_select_wrapper.width(select_width);
        custom_select_wrapper.css('margin', current_select.css('margin'));
        custom_select_wrapper.css('padding', current_select.css('padding'));

        var custom_select = $('<div />');
        custom_select.addClass('custom-select');
        custom_select.addClass('jq_custom-select');
        custom_select.on('click', function () {
            $(this).next().toggleClass('custom-select-list-active')
        });

        var custom_select_top = $('<div />');
        custom_select_top.addClass('custom-select-top');
        custom_select_top.css('line-height', select_height + 'px');

        custom_select_top.text(current_select.find('option:selected').text());
        custom_select.append(custom_select_top);

        var custom_select_list = $('<ul />');

        var option_selected = $(this).find('option:selected');
        current_select.find('option').each(function () {
            var li = $('<li />');
            if ($(this).text() == option_selected.text())
                li.addClass('custom-select-li-active');
            li.on('click', function () {
                current_select.find('option:contains(' + $(this).text() + ')').prop('selected', true);
                custom_select_top.text($(this).text());
                current_select.change();
                $(this).closest('.custom-select-list-active').toggleClass('custom-select-list-active')
            });
            li.on('hover', function () {
                $(this).addClass('custom-select-li-active')
            });
            li.text($(this).text());
            custom_select_list.append(li)
        });

        custom_select_wrapper.append(custom_select);
        custom_select_list.find('li').mouseover(function () {
            $(this).parent().find('li.custom-select-li-active').removeClass('custom-select-li-active');
            $(this).addClass('custom-select-li-active')
        });

        custom_select_wrapper.append(custom_select_list);

        current_select.hide();
        current_select.after(custom_select_wrapper);

        var show_elements = custom_select_list.find('li').length;
        if (show_elements > 10)
            show_elements = 10;
        var custom_select_li_element = custom_select_list.find('li');
        var li_height = custom_select_li_element.outerHeight();
        custom_select_list.height(show_elements * li_height);

        if (custom_select_list != undefined) {
            custom_select_list.addClass('default-skin');
            custom_select_list.addClass('custom-select-list-active');
            custom_select_list.customScrollbar({
                hScroll: false,
                vScroll: true,
                preventDefaultScroll: true
            });
            custom_select_list.removeClass('custom-select-list-active')
        }
    };

    return this.each(function () {
        if(!$(this).next().hasClass('custom-select-wrapper')) {
            new Draw($(this));
        }
    });

};