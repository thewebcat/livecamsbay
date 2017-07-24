from functools import wraps

from email_sender.models import EmailSetting
from email_sender.tasks import sent_emails


EMAIL_ACTIONS = {}


def _set_action(name, desc):
    if name in EMAIL_ACTIONS:
        raise KeyError('this name already used')
    EMAIL_ACTIONS[name] = desc


def email_action_reg(f):
    if callable(f):
        _set_action(f.__name__, f.__name__)
        return get_and_sent_email(f)

    desc = f

    def wrapper(f):
        _set_action(f.__name__, desc)
        return get_and_sent_email(f)
    return wrapper


def get_and_sent_email(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        r = f(*args, **kwargs)
        profile = r[0]
        if EmailSetting.objects.filter(action=f.__name__, profiles=profile).exists():
            data = r[1]
            try:
                template = r[2]
            except IndexError:
                template = f.__name__
            sent_emails.delay(profile.get_actual_emails(), data, template)
    return wrapper


class EmailSenderDecorator(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        @wraps(self.f)
        def wrapper(*args, **kwargs):
            r = self.f(*args, **kwargs)
            profile = r[0]
            if EmailSetting.objects.filter(action=self.f.__name__, profiles=profile).exists():
                data = r[1]
                try:
                    template = r[2]
                except IndexError:
                    template = self.f.__name__
                sent_emails.delay(profile.get_actual_emails(), data, template)
        return wrapper
