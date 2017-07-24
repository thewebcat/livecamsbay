# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context


class MixinSaveModelWithSeniorRights(object):
    """
    Миксин для Аккаунт наделеннного высшими правами,
    чтобы материалы отправленные на публикацию сразу публиковались
    """
    def save(self, *args, **kwargs):
        from amigostone.middleware import CurrentUser
        if CurrentUser.user.has_perm('custom_auth.account_with_senior_rights') and CurrentUser.profile:
            from common.models import AbstractBaseClass
            if hasattr(self, 'state') and self.state == AbstractBaseClass.STATE_TO_PUBLISH:
                self.state = AbstractBaseClass.STATE_PUBLISH

        super(MixinSaveModelWithSeniorRights, self).save(*args, **kwargs)

class MixinSaveModelAddPoint(MixinSaveModelWithSeniorRights):
    """
    Миксин для начисления балов пользователю за активность на сайте
    """

    def save(self, *args, **kwargs):
        super(MixinSaveModelAddPoint, self).save(*args, **kwargs)
        if hasattr(self, 'profile') and self.profile:
            from common.models import PointSystem, PointAction
            ps = PointSystem.objects.filter(model__model=self.__class__.__name__)
            if ps.exists() and self.state == self.STATE_PUBLISH:
                content_type = ContentType.objects.get_for_model(self)
                PointAction.objects.get_or_create(content_type=content_type, action_id=self.id, profile=self.profile)


class MixinForm(object):
    """
    Миксин для формы, для отображения ошибок в дизайне проекта
    """

    error_css_class = 'field-alert'

    def __init__(self, *args, **kwargs):
        super(MixinForm, self).__init__(*args, **kwargs)

    def show_errors(self):
        if not self.errors:
            return ""
        tmpl = """
        <ul class="errorlist">
          {% if form.non_field_errors %}
            {% for error in form.non_field_errors %}
                <li class="message-alert"><i class="fa fa-exclamation-circle" aria-hidden="true"></i> {{ error }}</li>
            {% endfor %}
          {% endif %}
          {% for field in form %}
            {% if field.errors %}
              {% for error in field.errors %}
                <li class="message-alert"><i class="fa fa-exclamation-circle" aria-hidden="true"></i> {{ field.label }}: {{ error }}</li>
              {% endfor %}
            {% endif %}
          {% endfor %}
        </ul>
        """
        return Template(tmpl).render(Context({'form': self}))
