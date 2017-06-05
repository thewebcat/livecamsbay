from call_orders.forms import CallOrderForm


def get_call_order_form(request):

    call_order_sending = False
    data = request.POST if request.POST.get('action') == CallOrderForm.action_text else None
    call_order_form = CallOrderForm(data, prefix='call_order')
    if data:
        if call_order_form.is_valid():
            call_order_form.save()
            call_order_sending = True
            call_order_form = CallOrderForm(prefix='call_order')

    return {
        'call_order_form': call_order_form,
        'call_order_sending': call_order_sending,
    }
