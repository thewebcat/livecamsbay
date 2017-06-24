# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from newsletter_email.forms import EmailSubscribeForm


@require_http_methods(["POST"])
def email_subscribe(request):
    """
    подписка на рассылку. Форма для подписки находится в футере
    """
    form_subscribe = EmailSubscribeForm(request.POST)
    if form_subscribe.is_valid():
        form_subscribe.save()
        return JsonResponse({'success': 'Вы подписались на рассылку'}, status=201)
    else:
        return JsonResponse({'error': form_subscribe.errors.values()}, status=400)
