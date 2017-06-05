function ajax_load(url, data, callback, target) {
    $.ajax({
        type: 'get',
        url: url,
        data: data,
        success: function(responseText, statusText, xhr) {callback(responseText, statusText, xhr, target)}
    })
}

function set_jcarousel_control(el, target) {
    el
        .on('jcarouselcontrol:active', function () {
            $(this).removeClass('inactive');
        })
        .on('jcarouselcontrol:inactive', function () {
            $(this).addClass('inactive');
        })
        .jcarouselControl({
            // Options go here
            target: target
        });
}
function update_catalog_products(responseText, statusText, xhr, target){
    var tabscontent = target.closest('.tabscontent');
    if(target.hasClass('jq_top_catalogs')) {
        tabscontent.find('.jq_sub_catalogs_list').html('');
        tabscontent.find('.jq_catalog_elements_list').html('');
    }
    if(target.hasClass('jq_sub_catalogs')) {
        tabscontent.find('.jq_catalog_elements_list').html('');
    }

    var template, rendered;
    //console.log(responseText)
    //console.log("update_catalog_products")
    if(responseText.catalog){
        console.log('responseText.catalog')
        template = $('#catalog_template').html();
        rendered = Mustache.render(template, responseText);
        var jq_sub_catalogs_list = tabscontent.find('.jq_sub_catalogs_list');
        jq_sub_catalogs_list.html(rendered);
        jq_sub_catalogs_list.find('.profile_catalog_products_jcarousel').jcarousel();
        //console.log(jq_sub_catalogs_list);
        //console.log("-----------------");
        set_jcarousel_control(jq_sub_catalogs_list.find('.jcarousel-control-prev'), '-=1');
        set_jcarousel_control(jq_sub_catalogs_list.find('.jcarousel-control-next'), '+=1');
        // tabscontent.find('.jq_catalog_elements_list').html('');
    } else if (responseText.products) {
        console.log(responseText)
        //console.log('responseText.products')
        template = $('#catalog_products_template').html();
        rendered = Mustache.render(template, responseText);
        //console.log(target.prop("tagName"));
        if (target.prop("tagName") == 'A')
            // checking on responseText.products. If works without catalogs
            if (target.hasClass('jq_top_catalogs') && !responseText.products) {
                //console.log(tabscontent);
                // console.log("--1");
                tabscontent.find('.jq_sub_catalogs_list');
                tabscontent.find('.jq_sub_catalogs_list').html(rendered);
            } else if (target.hasClass('jq_sub_catalogs') || responseText.products) {
                if (target.hasClass('jq_next_page')) {
                    // console.log("--4");
                    tabscontent.find('.jq_catalog_elements_list').append(rendered);
                } else {
                    // console.log("--5");
                    tabscontent.find('.jq_catalog_elements_list').html(rendered);
                }
            } else {
                // console.log("--2");
                tabscontent.find('.jq_catalog_elements_list').append(rendered);
            }
        else {
            console.log("--3")
            tabscontent.find('.jq_catalog_elements_list').children().last().replaceWith(rendered);
        }
    } else if (responseText.materials) {
        //console.log('*************')
        //console.log(tabscontent)
        if (target.prop("tagName") == 'A') {
            template = $(responseText.mustache_id).html();
            rendered = Mustache.render(template, responseText);
            tabscontent.find('.jq_catalog_elements_list').append(rendered);
        } else {
            template = $(responseText.mustache_id).html();
            rendered = Mustache.render(template, responseText);
            tabscontent.find('.jq_catalog_elements_list').html(rendered);
        }
    } else if (responseText.services) {

        //console.log(responseText.services);

        if (target.prop("tagName") == 'A' && !target.hasClass('jq_top_catalogs')) {
            template = $(responseText.mustache_id).html();
            rendered = Mustache.render(template, responseText);
            tabscontent.find('.jq_catalog_elements_list').append(rendered);
        } else {
            template = $(responseText.mustache_id).html();
            rendered = Mustache.render(template, responseText);
            tabscontent.find('.jq_catalog_elements_list').html(rendered);
        }
    } else {
        tabscontent.find('.jq_sub_catalogs_list').html('');
        tabscontent.find('.jq_catalog_elements_list').html('');
    }
}

$(function(){
    //console.log($("#catalog_products"));
    $("#catalog_products").tytabs({
        tabinit:"5",
        classcontent:"tabscontent_catalog",
        fadespeed:"fast"
    });
    //$('#catalog_products .tabs li a').on('click', function(e){
    //    e.preventDefault()
    //    console.log($(this).attr('href'))
    //    var url = $(this).attr('href')
    //    var data = {}
    //    $.ajax({
    //        type: 'get',
    //        url: url,
    //        data: data,
    //        success: function(responseText, statusText, xhr) {
    //            console.log(responseText)
    //        }
    //    })
    //})

function update_product_view(responseText, statusText, xhr, target){
    var tabscontent = target.closest('.tabscontent');
    var template = $('#product_view_template').html();
    var rendered = Mustache.render(template, responseText);
    var showed_element = $('<div/>');

    if(target.closest('ul').next().hasClass('jq_products_element_view')){
            //d.html(rendered)
            //target.closest('ul').next().html(d);
        target.closest('ul').next().html(rendered);
    } else {
        var hidden_element = target.closest('.jq_catalog_elements_list').find('.jq_products_element .jq_products_element_view');
        var products_element_view = $('<div />');
        products_element_view.addClass('jq_products_element_view');
        target.closest('ul').after(products_element_view);

        showed_element.hide();
        showed_element.html(rendered);
        products_element_view.html(showed_element);

        hidden_element.slideUp(function(){hidden_element.remove();});
        showed_element.slideDown()
    }

}





$('.jcarousel_menu').jcarousel();
$('.jcarousel_stone_list').jcarousel();

set_jcarousel_control($('.jcarousel-control-prev'), '-=1');
set_jcarousel_control($('.jcarousel-control-next'), '+=1');






$('.jcarousel_menu')
    .on('click', '.jq_top_catalogs', function(e){
        e.preventDefault();
        $('.jcarousel_menu').find('.jq_top_catalogs').removeClass('active');
        $(this).addClass('active');
        var tabscontent = $(this).closest('.tabscontent');
        var element_contains_prefix = tabscontent.find('.jq_root_catalog.active');
        var data = {};
        if(element_contains_prefix.length)
            data = $('#jq_filter'+element_contains_prefix.attr('id')).serializeArray();
            //$('.jq_sub_catalogs_list').html('');
        tmp_url = $(this).attr('href');
        ajax_load($(this).attr('href'), data, update_catalog_products, $(this));
    });
$('.jq_trigger_ajax_load_catalogs, .profile_list_elements, .jq_sub_catalogs_list')
        .on('click', 'a.jq_sub_catalogs', function(e){
            //console.log(".jq_catalog_products_element li a");
            var tabscontent = $(this).closest('.tabscontent');
            var element_contains_prefix = tabscontent.find('.jq_root_catalog.active');
            var data = {};
            if(element_contains_prefix.length)
                data = $('#jq_filter'+element_contains_prefix.attr('id')).serializeArray();
            e.preventDefault();
            $(this).closest('.jq_catalog_products_element').find('a.active').removeClass('active');
            $(this).addClass('active');
            // $(this).closest('.jq_catalog_products_element').nextAll().remove();
            tmp_url = $(this).attr('href');
            ajax_load($(this).attr('href'), data, update_catalog_products, $(this));
        })
        //.on('click', '.jq_next_page', function(e){
        //    e.preventDefault();
        //    console.log($(this).attr('href'))
        //    var data = {}
        //    ajax_load($(this).attr('href'), data, update_catalog_products, $(this));
        //})
        .on('click', '.jq_products_element li a', function(e){
            e.preventDefault();
            $(this).closest('.jq_catalog_elements_list').find('.jq_products_element a.active').parent().removeClass('active');
            $(this).closest('.jq_catalog_elements_list').find('.jq_products_element a.active').removeClass('active');

            $(this).addClass('active');
            $(this).parent().addClass('active');

            ajax_load($(this).attr('href'), '', update_product_view, $(this));
        });


    $('.jq_catalog_elements_list').on('click', '.jq_catalog_elements', function(e){
            e.preventDefault();
            $(this).closest('.jq_catalog_elements_list').find('.jq_products_element a.active').parent().removeClass('active');
            $(this).closest('.jq_catalog_elements_list').find('.jq_products_element a.active').removeClass('active');
            $(this).addClass('active');
            $(this).parent().addClass('active');

            ajax_load($(this).attr('href'), '', update_product_view, $(this));
        })
})


function filter_data(){
    var element_contains_prefix = $('.jq_root_catalog.active');
    //console.log(element_contains_prefix.length);
    var data = {};
    var stone_data = {};
    if(element_contains_prefix.length) {
        var form = $('#jq_filter' + element_contains_prefix.attr('id'));
        var stone_form = $('#jq_stone_filter' + element_contains_prefix.attr('id'));
        data = form.serializeArray()
        stone_data = stone_form.serializeArray();
        data = data.concat(stone_data);
        data = data.concat({"name": "parent", "value":  element_contains_prefix.attr('id')});
        //console.log(data)
    }
    return data
}


function update_material_products(responseText, statusText, xhr, target){
    var tabscontent = target.closest('.jq_catalog_panel');
    var template, rendered;
    //console.log(responseText);
    template = $(responseText.mustache_id).html();
    rendered = Mustache.render(template, responseText);
    if(target.prop("tagName")=='A')
        tabscontent.find('.jq_catalog').append(rendered);
    else
        tabscontent.find('.jq_catalog').html(rendered);

}
function update_material(responseText, statusText, xhr, target){
    var tabscontent = target.closest('.tabscontent');
    var template = $('#material_view_template').html();
    var rendered = Mustache.render(template, responseText);
    var showed_element = $('<div/>');

    if(target.closest('.stone_breaker').next().hasClass('jq_products_element_view')){
        target.closest('.stone_breaker').next().html(rendered);
    } else {
        var hidden_element = target.closest('.jq_catalog_elements_list').find('.jq_products_element_view');
        var products_element_view = $('<div />');
        products_element_view.addClass('jq_products_element_view');
        target.closest('.stone_breaker').after(products_element_view);

        showed_element.hide();
        showed_element.html(rendered);
        products_element_view.html(showed_element);

        hidden_element.slideUp(function(){hidden_element.remove();});
        showed_element.slideDown()
    }
}

$(function () {
    $('.jq_catalog_elements_list').on('click', '.jq_next_page', function(e){
        e.preventDefault();
        var url = $(this).attr('href');
        var data = filter_data($(this));
        var form = $(this).closest('.contents').find('.jq_catalog_panel.active').find('form')
        if(form)
            data = form.serializeArray()
        else
            data = {}

        //console.log('next page');
        ajax_load(url, data, update_catalog_products, $(this));
    })
    .on('click', '.cube', function(e){
        e.preventDefault();
        var url = $(this).attr('href');
        var data = {};
        //console.log('cube click');
        ajax_load(url, data, update_material, $(this));
    })


});


function getUrlVars() {
    var vars = {};
    window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars;
}
$(function() {
    $('a[href="#catalog"]').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $('#anchor_catalog');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 120
                }, 300, function () {
                    target.find('a').click()
                });
            }
        }
    });
    $('a[href="#button_for_look_recalls"]').click(function (e) {
        e.preventDefault();
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $('#start_of_recalls');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 120
                });
            }
        }
    });
    if (getUrlVars()['to_recalls']) {
        $('a[href="#button_for_look_recalls"]').click()
    }
});


