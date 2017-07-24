# coding=utf-8
from django.http import JsonResponse
from tickets.emails import new_ticket
from tickets.forms import MessageForm


def add_new_ticket(request):
    """
    Ajax запрос на добавление нового тикета
    """
    if request.method == 'POST' and request.is_ajax():
        message_form = MessageForm(data=request.POST, files=request.FILES, profile=request.user.profile)
        if message_form.is_valid():
            message_form.save()
            new_ticket(request.user.profile)
            return JsonResponse({})
        else:
            return JsonResponse({'error': message_form.errors})
