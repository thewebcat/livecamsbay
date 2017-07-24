# coding=utf-8
from django.forms import ClearableFileInput, CheckboxInput
from django.utils.encoding import force_text
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


thumbnail_options = {'crop': True}
thumbnail_options.update({'size': (129, 99)})


class ImageInput(ClearableFileInput):
    """
    Устаревшее
    """

    # template_with_initial = '%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    template_with_initial = '<div class="wrapper-image-input">%(initial)s %(clear_template)s<br />%(input)s</div>'

    # template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'
    template_with_clear = '<div>%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label></div>'

    # url_markup_template = '<a href="{0}">{1}</a>'
    url_markup_template = '<div class="photo1"><img src="{0}"></div>'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(self.url_markup_template,
                                                   get_thumbnailer(force_text(value)).get_thumbnail(thumbnail_options).url,
                                                   force_text(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)
