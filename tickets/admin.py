# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db import transaction
from models import Ticket, Message as TicketMessage
from private_messages.models import Message
from tickets.emails import new_ticket_answer, ticket_closed


class TicketAdmin(admin.TabularInline):
    model = TicketMessage
    extra = 1
    readonly_fields = ['profile']


class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'date_start', 'first_message')
    list_display_links = ('is_active', 'date_start', 'first_message')
    inlines = [TicketAdmin]

    def date_start(self, obj):
        return obj.message_set.first().date if obj.message_set.exists() else None

    def first_message(self, obj):
        return obj.message_set.first().text[:20] if obj.message_set.exists() else ''

    def save_model(self, request, obj, form, change):
        if change:
            data = {'url': '../../' + obj.__class__.__name__.lower() + 's/',
                    'change_status': False}
            if 'is_active' in form.changed_data:
                data['active'] = obj.is_active
                data['change_status'] = True
            with transaction.atomic():
                message = Message()
                message.create_message_from_template(
                    template_name='ticket_answer',
                    data=data)
                message.save()
                message.send_to_profiles(profiles=[obj.profile])

            if 'is_active' in form.changed_data and not obj.is_active:
                ticket_closed(obj)

        super(TicketMessageAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        new = False
        for message in instances:
            if not message.id:
                new = True
                break
        if new:
            new_ticket_answer(message.ticket)
        formset.save()


admin.site.register(Ticket, TicketMessageAdmin)
