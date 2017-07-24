# coding=utf-8
from django.core.urlresolvers import reverse
from main.func import build_absolute_uri

from email_sender.email_actions import email_action_reg
from tickets.models import Message


def get_tickets_url():
    return build_absolute_uri(reverse('accounts:tickets'))


@email_action_reg(u'Новый тикет создан')
def new_ticket(profile):
    return profile, {'name': profile.name, 'tickets_url': get_tickets_url()}


@email_action_reg(u'Ответ на тикет')
def new_ticket_answer(ticket):
    profile = ticket.profile
    last_user_message = Message.objects.filter(ticket=ticket.id, profile__isnull=False).order_by('date').last().text
    return profile, {'name': profile.name, 'ticket_message': last_user_message, 'tickets_url': get_tickets_url()}


@email_action_reg('Тикет закрыт')
def ticket_closed(ticket):
    profile = ticket.profile
    first_user_message = Message.objects.filter(ticket=ticket.id).order_by('date').first().text
    return profile, {'name': profile.name, 'ticket_message': first_user_message, 'tickets_url': get_tickets_url()}
