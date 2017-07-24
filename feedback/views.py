# -*- coding: UTF-8 -*-

from main.decorators import render_to
from feedback.forms import FeedbackForm


@render_to("feedback/feedback.html")
def feedback(request):
    """
    Страница с формой обратной связи
    """
    initial = {}
    if request.user.is_authenticated() and request.user.profile:
        initial = {
            'name': request.user.profile.name,
            'phone': request.user.profile.get_phone(),
            'email': request.user.email
        }

    feedback_form = FeedbackForm(request.POST or None, initial=initial)
    feedback_form_sending = False

    if request.method == 'POST' and request.POST.get('action') == FeedbackForm.action_text and feedback_form.is_valid():
        feedback_form.save()
        feedback_form = FeedbackForm()
        feedback_form_sending = True

    return {
        'feedback_form': feedback_form,
        'feedback_form_sending': feedback_form_sending,
    }
