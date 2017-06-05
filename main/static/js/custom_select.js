$(function() {
    var custom_select_list = undefined
    $('select.custom-select').each(function () {
        currunt_select = $(this)
        select_width = $(this).width()
        select_height = $(this).height()

        custom_select_wrapper = $('<div />')
        custom_select_wrapper.addClass('custom-select-wrapper')

        custom_select = $('<div />')
        custom_select.addClass('custom-select')
        custom_select.addClass('jq_custom-select')
        custom_select.on('click', function () {
            $(this).next().toggleClass('custom-select-list-active')
        })

        custom_select_top = $('<div />')
        custom_select_top.addClass('custom-select-top')
        custom_select_top.css('line-height', select_height + 'px')

        custom_select_top.text($(this).find('option:selected').text())
        custom_select.append(custom_select_top)

        custom_select_list = $('<ul />')

        option_selected = $(this).find('option:selected')
        $(this).find('option').each(function () {
            li = $('<li />')
            if ($(this).text() == option_selected.text())
                li.addClass('custom-select-li-active')
            li.on('click', function () {
                currunt_select.find('option:contains(' + $(this).text() + ')').prop('selected', true)
                custom_select_top.text($(this).text())
                currunt_select.change()
                $(this).closest('.custom-select-list-active').toggleClass('custom-select-list-active')
                console.log($(this).closest('.custom-select-list-active'))
            })
            li.on('hover', function () {
                $(this).addClass('custom-select-li-active')
            })
            li.text($(this).text())
            custom_select_list.append(li)
        })

        custom_select_wrapper.append(custom_select)
        custom_select_list.find('li').mouseover(function () {
            custom_select_list.find('li').removeClass('custom-select-li-active')
            $(this).addClass('custom-select-li-active')
        })

        custom_select_wrapper.append(custom_select_list)

        $(this).hide()
        $(this).after(custom_select_wrapper)
    })
    if (custom_select_list != undefined) {
        custom_select_list.addClass('default-skin')
        custom_select_list.addClass('custom-select-list-active')
        custom_select_list.customScrollbar({
            hScroll: false,
            vScroll: true,
            preventDefaultScroll: true
        })
        custom_select_list.removeClass('custom-select-list-active')
    }
})