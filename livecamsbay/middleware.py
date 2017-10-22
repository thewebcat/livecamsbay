# -*- coding: UTF-8 -*-
from accounts.models import FavoriteModel
from private_messages.models import MessageRecipient


class OfferCounterMiddleware(object):

    @staticmethod
    def process_request(request):
        if request.user.is_authenticated():
            pass
            # if not request.user.company:
            #     #request.offer_counter = Order.objects.filter(viewed__isnull=True).count()
            #     ids = Order.objects.filter(certified=True, completed=False).values_list("id", flat=True)
            #     request.offer_counter = OfferToOrder.objects.filter(order_id__in=ids, viewed=False).count()


class MessageCounterMiddleware(object):

    @staticmethod
    def process_request(request):
        if request.user.is_authenticated():
            request.message_counter = MessageRecipient.objects.filter(viewed=False, profile=request.user.profile).count()



class CurrentUser:
    profile = None
    user = None

    @staticmethod
    def process_view(request, *args):
        CurrentUser.profile = request.user.profile if hasattr(request.user, 'profile') else None
        CurrentUser.user = request.user


class QuickPanel(object):

    @staticmethod
    def process_request(request):
        request.active_models = ()
        if request.user.is_authenticated():
            profile = request.user.profile
            request.active_models = FavoriteModel.objects.filter(profile=profile, model__available=True)