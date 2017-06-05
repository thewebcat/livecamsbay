$(function(){
    var tag_container = $(".tag_container");
    var tag_container_form = tag_container.closest('form');
    tag_container.hide();
    tag_container.each(function() {

        var tags_controls = $('<div/>').addClass('tags_controls').attr('for_id', $(this).attr('id'));
        var tags_display  = $('<div/>').addClass('tags_display').addClass('jq_tags_display');
        var input_group   = $('<div/>').addClass('input-group');
        var input         = $('<div class="teg"><input type="text" placeholder="Введите тег"></div>');
        var button        = $('<div class="still jq_add_tag"></div>');
        input_group.append(input).append(button);
        tags_controls.append(tags_display).append(input_group);

        $(this).after(tags_controls);

        $(this).find("option").each(function() {
            $(this).prop('selected', true);
            tags_display.append($('<span>').html($(this).text() + " <span class=\"glyphicon glyphicon-remove jq_tag_remove\" aria-hidden=\"true\"></span>"))
        })
    });

    tag_container_form.on( "click", ".jq_add_tag", function() {
        var tags_controls = $( this).closest(".tags_controls");
        var tags_display = tags_controls.find(".jq_tags_display");
        var tag_input = tags_controls.find("input");
        var tag = tag_input.val();
        if($.trim(tag) == '')
            return false;
        var id_select = tags_controls.attr("for_id");

        if($('#'+id_select+' option[value="'+tag+'"]').length == 0) {

            $('#' + id_select).append($('<option>', {value: tag}).text(tag));
            $('#' + id_select + ' option').prop('selected', true);

            tags_display.append($('<span>').html(tag + " <span class=\"glyphicon glyphicon-remove jq_tag_remove\" aria-hidden=\"true\"></span>"))
        }
        tag_input.val("")
    });
    tag_container_form.on( "click", ".jq_tag_remove", function() {
        console.log("jq_tag_remove");
        var tags_controls = $( this).closest(".tags_controls");
        var id_select = tags_controls.attr("for_id");
        var tag_display = $(this).parent();
        var tag = $.trim(tag_display.text());

        $('#'+id_select+' option[value="'+tag+'"]').each(function() {
            $(this).remove();
            tag_display.remove()
        });
    })
});