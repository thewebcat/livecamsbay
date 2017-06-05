# coding=utf-8
from call_orders.forms import CallOrderForm
from common.decorators import render_to_json


@render_to_json
def call_order_send(request):
    """
    Ajax запрос из формы Заказать обратный звонок
    """
    call_order_sending = False
    fields = []

    call_order_form = CallOrderForm(request.POST or None, prefix='call_order')

    if request.method == 'POST' and request.POST.get('call_order-action') == CallOrderForm.action_text:

        if call_order_form.is_valid():
            call_order_form.save()
            call_order_sending = True
        else:
            fields = call_order_form.errors.keys()

    return {
        'success': call_order_sending,
        'fields': fields,
    }
