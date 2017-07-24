from django.contrib import admin

from email_sender.models import EmailSetting, EmailGroup

admin.site.register(EmailSetting)
admin.site.register(EmailGroup)
