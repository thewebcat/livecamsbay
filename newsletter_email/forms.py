from django.forms import ModelForm

from newsletter_email.models import Email


class EmailSubscribeForm(ModelForm):
    class Meta:
        model = Email
        fields = ('email',)
