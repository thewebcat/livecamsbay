$ = django.jQuery;

$(function () {
    $('#id_title, #id_keywords, #id_description').bind('input propertychange', function () {
        var textarea = $(this);
        updateHelp(textarea);
    });
    $('#id_title, #id_keywords, #id_description').each(function (i, textarea) {
        updateHelp($(textarea));
    });
});

function updateHelp(textarea) {
    var content = textarea.val();
    var help = textarea.next();
    var charsLimit = parseInt(help.text());
    var helpColor = content.length <= charsLimit ? 'green' : 'red';
    help.find('span').remove();
    help.append('<span style="color: '+helpColor+'"> '+content.length+'/'+charsLimit+' сим.</span>');
}
