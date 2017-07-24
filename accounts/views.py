# -*- coding: UTF-8 -*-
import datetime

from livecamsbay.middleware import CurrentUser
from main.models import AbstractBaseClass
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.conf import settings
from django.db.models import Q, F
from django.db.models.aggregates import Count, Sum
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import View, TemplateView, ListView, DetailView, FormView, CreateView
from main.func import to_pagination

from accounts.decorators import validate_access
from accounts.models import Profile
# from articles.forms import ArticleImageFormSet
# from articles.models import Article
# from calendar_events.models import Event
# from calendar_events.forms import EventImageFormSet
# from calendar_events.serializers import EventPublicSerializer, EventPrivateSerializer
from main.decorators import render_to, render_to_json, has_edit
from accounts.forms import PasswordChangeForm
# from common.func import to_pagination
# from company.forms import OfferApprovedForm
# from django.utils import timezone
# from geo.models import Country
# from materials.forms import MaterialForm, MaterialArtificialForm, MaterialCatalogForm, MaterialImageFormSet
# from materials.models import MaterialCatalog, Material, MaterialProduction
# from offers.forms import OfferFormSet
# from orders.emails import order_closed, choice_performer_for_order
# from products.forms import ProductForm, ProductCatalogForm, ProductImageFormSet
# from products.models import ProductCatalog, Product, ProductCatalogMenu
# from services.forms import ServiceAddOrEditForm, ServiceImageFormSet
# from articles.forms import ArticleAddOrEditForm
from news.forms import NewsForm
from news.models import News
from accounts.models import FavoriteModel
from accounts.forms import FavoriteForm
# from notes.forms import NoteForm
# from notes.models import Note
# from offers.models import Offer
# from orders.forms import OrderDocumentForm, OrderCommentForm, OrderDocumentConfirmForm, OrderDocumentDeclineForm, \
#     OrderActionSetForm, OrderFinishUserConfirmForm, OrderRecallForm, OrderFileFormSet
# from orders.models import Order, OfferToOrder, OrderDocument
from private_messages.models import Message
# from services.models import Service, ServiceCatalog
# from tags.forms import MultipleChoiceTagForm
# from tags.models import Tag
from tickets.forms import MessageForm
from tickets.models import Ticket
# from works.forms import WorkForm, WorkCatalogForm, WorkImageFormSet
# from works.models import Work, WorkCatalog


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        _profile = self.request.user.profile
        context = super(ProfileView, self).get_context_data()
        context['company'] = _profile
        context['offers'] = settings.DEFAULT_IMAGE
        context['menu_catalogs'] = ''
        context['material_catalogs'] = ''
        context['material_elements_in_line'] = ''
        context['countries'] = ''
        context['productions'] = ''
        context['news_list'] = ''
        context['events'] = ''
        context['service_catalogs'] = ''
        context['work_catalog'] = ''
        context['testimonials'] = ''
        context['producers_count'] = ''
        return context

# @render_to("accounts/profile.html")
# @validate_access()
# def profile(request):
#     """
#     Отображение Профиля. Первая страница в личном кабинете.
#     """
#     _profile = request.user.profile
#     events = Event.objects.filter(public=True, certified=True, profile=_profile)
#     serializer = EventPublicSerializer(events, many=True)
#     import json
#     from django.core.serializers.json import DjangoJSONEncoder
#     from orders.models import OrderRecall
#     testimonials = OrderRecall.objects.filter(order__performer=_profile)
#     _profile.ave_rate = 0
#
#     if testimonials:
#         _profile.ave_rate = (
#             float(reduce(lambda x, y: x + y, map(lambda x: x.rate, testimonials))) /
#             testimonials.count() / 5 * 100)
#
#     return {
#         'company': _profile,
#         'offers': Offer.objects.filter(profile=_profile),
#         'menu_catalogs': ProductCatalogMenu.objects.all(),
#         'material_catalogs': {'get_children': MaterialCatalog.objects.filter(level=0)},
#         'material_elements_in_line': 3,
#         'countries': Country.objects.all(),
#         'productions': MaterialProduction.objects.all(),
#         'news_list': News.objects.filter(profile=_profile),
#         'events': json.dumps(serializer.data, cls=DjangoJSONEncoder),
#         'service_catalogs': ServiceCatalog.objects.all(),
#         'work_catalog': WorkCatalog.objects.filter(Q(profile=_profile) | Q(profile__isnull=True), Q(level=0)),
#         'testimonials': testimonials,
#         'producers_count': Profile.objects.producers().count()
#     }
#
#
@render_to("accounts/profile_edit.html")
@validate_access()
def profile_edit(request):
    """
    Отображение формы редактирования Профиля в личном кабинете
    """

    form_profile = request.user.profile.get_profile_account_form()(
        request.POST or None, request.FILES or None, instance=request.user.profile)

    phone_formset = Profile.get_profile_phone_formset()(request.POST or None, instance=request.user.profile)
    url_formset = Profile.get_profile_url_formset()(request.POST or None, instance=request.user.profile)
    email_formset = Profile.get_profile_email_formset()(request.POST or None, instance=request.user.profile)
    if request.user.profile.is_company():
        # contact_person_formset = Profile.get_profile_contact_person_formset()(
        #     request.POST or None, instance=request.user.profile)
        # director_form = Profile.get_profile_director_form()(
        #     request.POST or None, instance=request.user.profile.profiledirector)
        # bank_details_form = Profile.get_profile_bank_details_form()(
        #     request.POST or None, instance=request.user.profile.profilebankdetails)
        pass
    else:
        #contact_person_formset = Profile.get_profile_contact_person_formset()(request.POST or None)
        # director_form = Profile.get_profile_director_form()(request.POST or None)
        # bank_details_form = Profile.get_profile_bank_details_form()(request.POST or None)
        pass

    forms_errors = False
    if request.method == 'POST':
        if request.user.profile.is_user():
            if form_profile.is_valid() and phone_formset.is_valid():
                form_profile.save()
                phone_formset.save()
                return redirect('accounts:profile')
            else:
                forms_errors = True
        if request.user.profile.is_master():
            if form_profile.is_valid() and phone_formset.is_valid() and \
                    email_formset.is_valid() and url_formset.is_valid():
                form_profile.save()
                phone_formset.save()
                email_formset.save()
                url_formset.save()
                return redirect('accounts:profile')
            else:
                forms_errors = True
        # elif request.user.profile.is_company():
        #     if form_profile.is_valid() and phone_formset.is_valid() and email_formset.is_valid()\
        #             and contact_person_formset.is_valid() and director_form.is_valid()\
        #             and bank_details_form.is_valid() and url_formset.is_valid():
        #         form_profile.save()
        #         phone_formset.save()
        #         email_formset.save()
        #         url_formset.save()
        #         contact_person_formset.save()
        #         director = director_form.save(commit=False)
        #         director.profile = request.user.profile
        #         director.save()
        #         bank_details = bank_details_form.save(commit=False)
        #         bank_details.profile = request.user.profile
        #         bank_details.save()
        #         return redirect('accounts:profile')
        #     else:
        #         forms_errors = True

    return {
        'form_profile': form_profile,
        'phone_formset': phone_formset,
        'url_formset': url_formset,
        'email_formset': email_formset,
        'contact_person_formset': '',
        'director_form': '',
        'bank_details_form': '',

        'forms_errors': forms_errors,
    }


@render_to("accounts/password_change.html")
@validate_access()
def profile_change_password(request):
    """
    Отображение формы изменения пароля
    """
    password_change_form = PasswordChangeForm(data=request.POST or None, user=request.user)

    if request.method == 'POST':
        if password_change_form.is_valid():
            password_change_form.save()
            return redirect('accounts:profile_change_password_success')

    return {
        'password_change_form': password_change_form
    }


@render_to("accounts/password_change_success.html")
@validate_access()
def profile_change_password_success(request):
    """
    Отображение сообщения об успешний смене пароля
    """
    return {}


@render_to("accounts/order_add_or_edit.html")
@validate_access()
def order_add(request):
    """
    Отображение формы добавления нового заказа
    """
    return order_add_or_edit(request)


@render_to("accounts/order_add_or_edit.html")
@validate_access()
def order_edit(request, object_id=None):
    """
    Отображение формы редактирования заказа
    """
    get_object_or_404(Order, id=object_id, customer=request.user.profile)
    output = order_add_or_edit(request, order_id=object_id)

    return output


@render_to_json
@validate_access()
def order_recall(request, object_id):
    """
    Обрабатывает отзыв заказкика об исполнителе.
    Отзыв можно оставить только в заказе с выбранным заказчиком.
    Форма для отправки accounts/templates/accounts/recall_form
    """
    if request.method == 'POST':
        from orders.models import OrderRecall
        from common.func import get_object_or_none
        recall = get_object_or_none(OrderRecall, order=object_id, order__customer=request.user.profile)
        order_recall_form = OrderRecallForm(request.POST, instance=recall)
        if order_recall_form.is_valid():
            order = Order.objects.filter(customer=request.user.profile).get(id=object_id)
            ob = order_recall_form.save(commit=False)
            ob.order = order
            ob.profile = order.performer
            ob.save()
            answer = HttpResponse(status=201)
            return answer

        else:
            # todo dnt do anything on client with this answer
            return {'errors': order_recall_form.errors}


def order_add_or_edit(request, order_id=None):
    """
    Метод для создания или редактирования заказа из личного кабинета.
    Если есть order_id, то редактирование, иначе создание.
    Метод вызывается из вьюх order_add и order_edit
    """
    if order_id:
        order = get_object_or_404(Order, pk=order_id, customer=request.user.profile)
        initial = {}
    else:
        order = Order()
        initial = {
            'name': request.user.profile.name,
            'email': request.user.email,
            'phone': request.user.profile.phone,
            'city': request.user.profile.city,
        }

    form = OrderAddOrEditForm(request.POST or None, instance=order, initial=initial)
    formset = OrderFileFormSet(request.POST or None, request.FILES or None, instance=order)

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save(user=request.user)
            formset.save()
            if order_id:
                return redirect(order.private_url)
            else:
                return redirect('accounts:order_add_success')
        else:
            return {'form': form, 'formset': formset}

    return {'form': form, 'formset': formset, 'order_id': order_id}


@render_to("accounts/order_add_success.html")
@validate_access()
def order_add_success(request):
    """
    Отображение сообщения, что заказ создан и отправлен на модерацию
    """
    return {}


# @validate_access()
# def order_view(request, object_id):
#     """
#     Отображение информации о заказе.
#     Создание предложения заказчику от исполнителя.
#     Выбор исполнителя.
#     Общение заказчика и исполнителя через систему чата.
#     """
#
#     order = get_object_or_404(Order, pk=object_id)
#
#     # Ставится статус, что заказ после какого либо изменения просмотрен второй стороной сделки
#     if order.customer == request.user.profile and order.quick_panel_status_customer == Order.QUICK_PANEL_NEW:
#         order.change_quick_panel_status_customer(status=Order.QUICK_PANEL_SHOW)
#     elif order.performer == request.user.profile and order.quick_panel_status_performer == Order.QUICK_PANEL_NEW:
#         order.change_quick_panel_status_performer(status=Order.QUICK_PANEL_SHOW)
#
#     # Ставится флаг просмотра всех предложений
#     if order.offertoorder_set.filter(viewed=False):
#         order.offertoorder_set.filter(viewed=False).update(viewed=True)
#
#     add_offer_to_order_form = AddOfferToOrderForm()
#     form_document = OrderDocumentForm(order=order, user=request.user)
#     form_comment = OrderCommentForm()
#     form_action = OrderActionSetForm()
#     finish_form = OrderFinishUserConfirmForm(instance=order)
#
#     if request.method == 'POST':
#         # клиент принял предложение
#         if not order.completed and request.POST.get('action', None) == OfferApprovedForm.action_text:  # Одобрениезаказа
#             offer_id = request.POST.get('id', None)
#             order.selected_offer(offer=get_object_or_404(OfferToOrder, id=offer_id))
#             choice_performer_for_order(order)
#             # формирование спецификации
#             #order.create_specification()
#             order.create_contract()
#
#         # исполнитель делает предложение
#         if not order.completed and request.POST.get('action', None) == AddOfferToOrderForm.action_text:
#             add_offer_to_order_form = AddOfferToOrderForm(request.POST)
#             if add_offer_to_order_form.is_valid():
#                 with transaction.atomic():
#                     add_offer_to_order_form.save(request, object_id, commit=True)
#                     order.send_private_message(
#                         template_name='add_new_offer_to_order',
#                         data={'order': order, 'url': order.accounts_url(), 'performer': request.user.profile},
#                         to=order.customer
#                     )
#
#                 return redirect(order.private_url)
#
#         # Возможные операции при выбранном исполнителе
#         if order.performer:
#             #  подтверждение документа
#             if request.POST.get('action') == OrderDocumentConfirmForm.action_text:
#                 document = OrderDocument.objects.get(id=request.POST.get('id'))
#                 customer_redirect_to_popup = False
#                 if request.user.profile == order.customer:
#                     document.customer_confirm()
#                     if order.get_act_of_work() and order.get_act_of_work().customer_confirmation_date:
#                         order.customer_finish_date = datetime.datetime.now()
#                         order.save()
#                         customer_redirect_to_popup = True
#                     else:
#                         return redirect(order.private_url)
#                 else:
#                     document.performer_confirm()
#                     if order.get_act_of_work() and order.get_act_of_work().performer_confirmation_date:
#                         order.performer_finish_date = datetime.datetime.now()
#                         order.save()
#                     return redirect(order.private_url)
#
#                 order.send_notification_document_confirm(request.user.profile, document)
#                 if customer_redirect_to_popup:
#                     popup = '?recall_popup=true'
#                     return redirect(order.private_url + popup)
#
#             #  отклонение документа
#             if request.POST.get('action') == OrderDocumentDeclineForm.action_text:
#                 document = OrderDocument.objects.get(id=request.POST.get('id'))
#                 if request.user.profile == order.customer:
#                     document.customer_decline()
#                 else:
#                     document.performer_decline()
#
#                 order.send_notification_document_decline(request.user.profile, document)
#
#                 return redirect(order.private_url)
#
#             # Добавление комментария или документа
#             if request.POST.get('action', None) == OrderActionSetForm.action_text:
#                 form_document = OrderDocumentForm(request.POST, request.FILES, order=order, user=request.user)
#                 form_comment = OrderCommentForm(request.POST, request.FILES)
#                 if form_document.is_valid() and form_comment.is_valid():
#                     with transaction.atomic():
#                         document = form_document.save(order=order) if request.FILES.get("file") else None
#
#                         # если прикреплен документ или комментарий не пустой
#                         # Бывает 3 валидные ситуации:
#                         # - есть комментарий
#                         # - есть документ
#                         # - есть комментарий и документ
#                         if document or form_comment.cleaned_data.get('text').strip():
#                             comment = form_comment.save(commit=False)
#
#                             comment.order = order
#
#                             if document:
#                                 comment.order_document = document
#
#                             if order.customer == request.user.profile:
#                                 comment.customer = request.user.profile
#                             else:
#                                 comment.performer = request.user.profile
#
#                             if not comment.text.strip():
#                                 comment.text = "Прикреплен файл (%s)" % document.file_type
#                             comment.save()
#
#                             #  отправляется сообщение собесседнику
#                             if comment.order_document:
#                                 order.send_notification_if_new_comment_with_document(comment, document)
#                             else:
#                                 order.send_notification_if_new_comment(comment)
#
#                             return redirect(order.private_url)
#
#         if request.POST.get('action') == OrderFinishUserConfirmForm.action_text:
#             finish_form = OrderFinishUserConfirmForm(request.POST, instance=order)
#             if finish_form.is_valid():
#                 finish_form.save(user=request.user)
#                 order_closed(order)
#                 popup = ''
#                 if not order.performer_finish_date:
#                     popup = '?recall_popup=true'
#                 return redirect(order.private_url + popup)
#
#     # todo not always need, add condition
#     from orders.models import OrderRecall
#     if order.customer == request.user.profile:
#         from common.func import get_object_or_none
#         recall = get_object_or_none(OrderRecall, order=object_id, order__customer=request.user.profile)
#         order_recall_form = OrderRecallForm(instance=recall)
#     else:
#         order_recall_form = None
#
#     if order.customer == request.user.profile:
#         order_offers = order.offertoorder_set.all()
#     else:
#         order_offers = order.offertoorder_set.filter(performer=request.user.profile)
#
#     context = {
#         'order': order,
#         'form': add_offer_to_order_form,
#         'offers': order_offers,
#         'comments': order.ordercomment_set.all() if order.is_party_transactions(request.user.profile) else None,
#         'form_comment': form_comment,
#         'form_document': form_document,
#         'form_action': form_action,
#         'finish_form': finish_form,
#         'recall_form': order_recall_form
#     }
#     return TemplateResponse(request, "accounts/order_view.html", context)


# @render_to("accounts/orders.html")
# @validate_access()
# def orders(request, f=None, t=None):
#     """
#     Отображение всех заказов.
#     Для исполнителей есть возможность просматривать все заказы и сортировать их, а заказчик видит только свои.
#     Args:
#         request:
#         f: состояния заказов (все, новые, активные, просмотренные и тд.). Значения должны соответствовать кортежам
#            incoming_filters and outgoing_filters, либо будет присвоено значение по умолчанию
#         t: тип заказов (входящие, исходящие). Значения должны соответствовать кортежу types, либо будет присвоено
#            значение по умолчанию
#
#     Returns:
#
#     """
#     types = ('incoming', 'outgoing')
#     incoming_filters = ('all', 'new', 'active', 'viewed', 'favorites', 'complete')
#     outgoing_filters = ('all', 'moderation', 'active', 'complete')
#
#     _profile = request.user.profile
#     if _profile.is_user():
#         t = 'outgoing'
#     else:
#         if t not in types:
#             t = 'incoming'
#
#     if t == 'incoming':
#         where = {'state': Order.STATE_PUBLISH}
#
#         if f not in incoming_filters:
#             f = 'new'
#
#         if f == 'active':
#             order_list = Order.objects.filter(
#                 Q(**where),
#                 Q(performer_finish_date__isnull=True),
#                 Q(id__in=OfferToOrder.objects.filter(performer=_profile).values_list('order_id', flat=True)),
#                 ~Q(customer=_profile))
#         elif f in ('new', 'viewed'):
#             ids = Order.objects.filter(
#                 Q(state=Order.STATE_PUBLISH),
#                 ~Q(customer=_profile),
#                 ~Q(completed=True)
#             ).values_list('id', flat=True)
#             content_type = ContentType.objects.get_for_model(Order)
#             views = ViewInstance.objects.filter(content_type=content_type.id, object_id__in=ids, profiles=_profile)\
#                 .values_list('object_id', flat=True)
#             if f == 'new':
#                 order_list = Order.objects.filter(id__in=ids).exclude(id__in=views)
#             else:
#                 order_list = Order.objects.filter(id__in=views)
#         elif f == "complete":
#             where.update({'performer': _profile})
#             order_list = Order.objects.filter(
#                 Q(**where),
#                 Q(performer_finish_date__isnull=False, customer_finish_date__isnull=False)
#             )
#         elif f == 'favorites':
#             return {'orders': None}
#         else:
#             order_list = Order.objects.filter(Q(**where), ~Q(customer=_profile))
#     else:
#         if f not in outgoing_filters:
#             f = 'all'
#         if f == 'active':
#             order_list = Order.objects.filter(Q(performer_finish_date__isnull=True) |
#                                               Q(customer_finish_date__isnull=True),
#                                               customer=_profile, state=Order.STATE_PUBLISH)
#         elif f == 'complete':
#             order_list = Order.objects.filter(customer=_profile, state=Order.STATE_PUBLISH,
#                                               performer_finish_date__isnull=False, customer_finish_date__isnull=False)
#         elif f == 'moderation':
#             order_list = Order.objects.filter(customer=_profile, state__in=[Order.STATE_DRAFT, Order.STATE_TO_PUBLISH],
#                                               moderator_finish_date__isnull=True)
#         else:
#             order_list = Order.objects.filter(customer=_profile)
#
#     return {
#         'orders': to_pagination(iter_object=order_list.order_by('-pk'), page=request.GET.get('page')),
#         'filter': f,
#         'type': t,
#     }


@render_to("accounts/favorite_list.html")
@validate_access()
def favorite_list(request):
    """
    Список заметок
    """
    return {
        'favorites': to_pagination(FavoriteModel.objects.filter(profile=request.user.profile), page=request.GET.get('page'))
    }


@render_to("accounts/favorite_add_or_edit.html")
@validate_access()
def favorite_add(request):
    """
    Добавление заметки
    """
    return favorite_add_or_edit(request, favorite_id=None)


@render_to("accounts/favorite_add_or_edit.html")
@validate_access()
def favorite_edit(request, object_id=None):
    """
    Редактирование заметки
    """
    output = favorite_add_or_edit(request, favorite_id=object_id)

    return output


def favorite_add_or_edit(request, favorite_id=None):
    """
    Метод для создания или редактирования заметки из личного кабинета.
    Если есть note_id, то редактирование, иначе создание.
    Метод вызывается из вьюх note_add и note_edit
    """
    initial = {}
    if favorite_id:
        favorite = get_object_or_404(FavoriteModel, id=favorite_id, profile=request.user.profile)
    else:
        import datetime
        favorite = FavoriteModel()
        initial = {}

    if request.method == 'POST':
        form = FavoriteForm(request.POST, instance=favorite)
        if form.is_valid():
            form.save()
            return redirect('accounts:favorite_list')
        else:
            return {'form': form}

    form = FavoriteForm(instance=favorite, initial=initial)
    return {'form': form}


@render_to("accounts/favorite_add_or_edit.html")
@validate_access()
def favorite_edit(request, object_id=None):
    """
    Редактирование заметки
    """
    output = favorite_add_or_edit(request, favorite_id=object_id)

    return output



@render_to("accounts/message_list.html")
@validate_access()
def message_list(request):
    """
    Список сообщений (автоматических уведомлений) в личном кабинете
    """
    messages = Message.objects.filter(message_recipient__profile=request.user.profile).order_by('-id')
    return {
        'messages': to_pagination(iter_object=messages, page=request.GET.get('page'))
    }


@render_to("accounts/message_view.html")
@validate_access()
def message_view(request, object_id):
    """
    Просмотр сообщения (автоматического уведомления)
    Есть такие сообщения, где не важно содержание и нужно переходить к определенной странице.
    (Оповещения о заказе, сразу ведут к странице заказа через redirect)
    """
    message = get_object_or_404(Message, id=object_id, message_recipient__profile=request.user.profile)
    if message.message_recipient.filter(viewed=False, profile=request.user.profile).exists():
        message.message_recipient.filter(viewed=False, profile=request.user.profile).update(viewed=True)

    obj = message.get_relation_object()
    if obj:
        return redirect(obj.accounts_url())

    return {
        'message': message,
    }


# @render_to('accounts/documents/list.html')
# @validate_access()
# def documents(request):
#     """
#     Список актуальных/утвержденных документов при работе с заказом.
#     """
#     return {
#         'documents': OrderDocument.objects.filter(Q(customer=request.user.profile) | Q(performer=request.user.profile),
#                                                   Q(customer_decline_date__isnull=True),
#                                                   Q(performer_decline_date__isnull=True, canceled_date__isnull=True))
#     }
#
#
# @render_to('accounts/bonuses/bonus_list.html')
# @validate_access(access_profiles=['c', 'm'])
# def bonus_list(request):
#     """
#     Страница бонусов(в разработке)
#     """
#     return {}
#
#
# @render_to("accounts/articles/articles.html")
# @validate_access(access_profiles=['c', 'm'])
# def articles(request):
#     """
#     Список всех статей пользователя
#     """
#     state = request.GET.get('state', '')
#     state_filter = {} if state == '' else {'state': state}
#     return {
#         "states": AbstractBaseClass.STATES,
#         "articles": Article.objects.filter(profile=request.user.profile, **state_filter),
#         "count_articles": Article.objects.filter(profile=request.user.profile).count(),
#     }
#
#
# @render_to("accounts/articles/article_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def article_add(request):
#     """
#     Добавление статьи
#     """
#     return article_add_edit(request)
#
#
# @render_to("accounts/articles/article_add_or_edit.html")
# @has_edit('article')
# @validate_access(access_profiles=['c', 'm'])
# def article_edit(request, object_id=None):
#     """
#     Редактирование статьи
#     """
#     article = Article.objects.get(id=object_id)
#     output = article_add_edit(request, article=article)
#
#     return output
#
#
# def article_add_edit(request, article=None):
#     """
#     Метод для создания или редактирования статьи из личного кабинета.
#     Если есть article, то редактирование, иначе создание.
#     Метод вызывается из вьюх article_add и article_edit
#     """
#     if not article:
#         article = Article()
#
#     multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=article)
#
#     form = ArticleAddOrEditForm(request.POST or None, request.FILES or None, instance=article)
#     formset = ArticleImageFormSet(request.POST or None, request.FILES or None, instance=article)
#     if request.method == 'POST':
#         if form.is_valid() and formset.is_valid():
#             with transaction.atomic():
#                 article = form.save(commit=False)
#                 article.profile = request.user.profile
#                 article.save()
#                 if multiple_choice_tag_form.is_valid():
#                     Tag.instance_update(article, multiple_choice_tag_form.save())
#
#                 # if 'action_save' in request.POST:
#                 #     article.mark_as_draft()
#                 # elif 'action_topublish' in request.POST:
#                 #     article.mark_as_to_published()
#                 # article.mark_as_published()
#                 article.save()
#                 formset.save()
#             return redirect('accounts:articles')
#         # else:
#         #     return {'form': form, 'formset': formset, 'multiple_choice_tag_form': multiple_choice_tag_form}
#
#     return {'article': article, 'form': form, 'formset': formset, 'multiple_choice_tag_form': multiple_choice_tag_form}
#
#
# @render_to("accounts/articles/article.html")
# @validate_access(access_profiles=['c', 'm'])
# def article_view(request, object_id):
#     """
#     Просмотр статьи
#     """
#     article = get_object_or_404(Article, pk=object_id, profile=request.user.profile)
#
#     return {
#         'article': article,
#         'count_articles': Article.objects.filter(profile=request.user.profile).count(),
#     }
#
#
@render_to("accounts/news/news_list.html")
@validate_access(access_profiles=['c', 'm'])
def news(request):
    """
    Просмотр списка новостей пользователя
    """
    state = request.GET.get('state', '')
    state_filter = {} if state == '' else {'state': state}
    return {
        "states": AbstractBaseClass.STATES,
        "list": News.objects.filter(profile=request.user.profile, **state_filter),
        "count_news": News.objects.filter(profile=request.user.profile).count(),
    }


@render_to("accounts/news/news_add_or_edit.html")
@validate_access(access_profiles=['c', 'm'])
def news_add(request):
    """
    Добавление новости
    """
    return news_add_edit(request)


@render_to("accounts/news/news_add_or_edit.html")
@has_edit('news')
@validate_access(access_profiles=['c', 'm'])
def news_edit(request, object_id=None):
    """
    редактирование новости
    """
    instance = get_object_or_404(News, id=object_id, profile=request.user.profile)
    output = news_add_edit(request, instance=instance)

    return output


def news_add_edit(request, instance=None):
    """
    Метод для создания или редактирования новости из личного кабинета.
    Если есть instance, то редактирование, иначе создание.
    Метод вызывается из вьюх news_add и news_edit
    """
    if not instance:
        instance = News()

    multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=instance)
    form = NewsForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            with transaction.atomic():
                instance = form.save(user=request.user, commit=True)
                if multiple_choice_tag_form.is_valid():
                    Tag.instance_update(instance, multiple_choice_tag_form.save())
                return redirect('accounts:news')

    return {'news': instance, 'form': form, 'multiple_choice_tag_form': multiple_choice_tag_form}
#
#
@render_to("accounts/news/news_view.html")
@validate_access(access_profiles=['c', 'm'])
def news_view(request, object_id):
    """
    Просмотр новости пользователя
    """
    instance = get_object_or_404(News, pk=object_id, profile=request.user.profile)

    return {
        'news': instance,
        'count_news': News.objects.filter(profile=request.user.profile).count(),
    }
#
#
# @render_to("accounts/calendar/calendar.html")
# @validate_access(access_profiles=['c', 'm'])
# def calendar(request):
#     """
#     Список мероприятий пользователя в виде календаря
#     """
#     import json
#     from django.core.serializers.json import DjangoJSONEncoder
#
#     state = request.GET.get('state', '')
#     state_filter = {} if state == '' else {'state': state}
#
#     events = Event.objects.filter(profile=request.user.profile, **state_filter)
#     serializer = EventPrivateSerializer(events, many=True)
#
#     return {
#         "states": AbstractBaseClass.STATES,
#         'events': json.dumps(serializer.data, cls=DjangoJSONEncoder)
#     }
#
#
# def calendar_event_list(request):
#     """
#     Была задумка сделать обычный список мероприятий (не реализовано, возможно и не нужно)
#     """
#     return None
#
#
# @render_to("accounts/calendar/calendar_event_add.html")
# @validate_access(access_profiles=['c', 'm'])
# def calendar_event_add(request):
#     """
#     Добавить меропроиятие
#     """
#     return calendar_event_add_edit(request)
#
#
# @render_to("accounts/calendar/calendar_event_add.html")
# @has_edit('event')
# @validate_access(access_profiles=['c', 'm'])
# def calendar_event_edit(request, object_id):
#     """
#     Редактировать мероприятие пользователя
#     """
#     event = get_object_or_404(Event, id=object_id, profile=request.user.profile)
#     output = calendar_event_add_edit(request, event)
#
#     return output
#
#
# def calendar_event_add_edit(request, event=None):
#     """
#     Метод для создания или редактирования мероприятия из личного кабинета.
#     Если есть event, то редактирование, иначе создание.
#     Метод вызывается из вьюх calendar_event_add и calendar_event_edit
#     """
#     from calendar_events.forms import EventForm
#     if not event:
#         event = Event()
#
#     multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=event)
#     form = EventForm(request.POST or None, instance=event)
#     formset = EventImageFormSet(request.POST or None, request.FILES or None, instance=event)
#
#     if request.method == 'POST':
#         if form.is_valid() and formset.is_valid():
#             with transaction.atomic():
#                 event = form.save(user=request.user)
#                 if multiple_choice_tag_form.is_valid():
#                     Tag.instance_update(event, multiple_choice_tag_form.save())
#                 formset.save()
#             return redirect('accounts:calendar')
#     return {'event': event, 'form': form, 'formset': formset, 'multiple_choice_tag_form': multiple_choice_tag_form}
#
#
# @render_to("accounts/calendar/calendar_event_view.html")
# @validate_access(access_profiles=['c', 'm'])
# def calendar_event(request, object_id):
#     """
#     Просмотр мероприятия пользователя
#     """
#     event_instance = get_object_or_404(Event, id=object_id, profile=request.user.profile)
#     return {
#         'event': event_instance,
#     }
#
#
# # CATALOGS
#
#
# def catalog_works_new(request):
#     """
#     Редирект на каталог работ.
#     """
#     return redirect('accounts:workcatalog_redirect')
#
#
# @render_to("accounts/works/works.html")
# @validate_access(access_profiles=['c', 'm'])
# def catalog_works_root_catalog(request):
#     """
#     Список корневого каталога работ. Содержит список дочерних каталогов.
#     """
#     return catalog_works_catalog(request, object_id=None)
#
#
# @render_to("accounts/works/works.html")
# @validate_access(access_profiles=['c', 'm'])
# def catalog_works_child_catalog(request, object_id=None):
#     """
#     Список дочернего каталога работ. Может содержать или список дочерних каталогов или список работ
#     """
#     catalog_instance = get_object_or_404(WorkCatalog, id=object_id)
#     output = catalog_works_catalog(request, object_id)
#     if isinstance(output, dict):
#         output.update({'breadcrumbs': catalog_instance.get_ancestors(include_self=True)})
#
#     return output
#
#
# def catalog_works_catalog(request, object_id=None):
#     """
#     Метод формарования ответа для вьюх catalog_works_root_catalog и catalog_works_child_catalog.
#     """
#     add_buttons = {}
#
#     if object_id:
#         current_catalog = get_object_or_404(WorkCatalog, id=object_id)
#         works = Work.objects.filter(profile=request.user.profile, work_catalog=current_catalog)
#         catalogs = None
#         add_buttons['add_catalog'] = False
#         add_buttons['add_work'] = True
#     else:
#         catalogs = WorkCatalog.objects.filter(Q(profile=None) | Q(profile=request.user.profile), level=0, parent__isnull=True)
#         works = None
#         add_buttons['add_catalog'] = True
#         add_buttons['add_work'] = False
#
#     list_catalog = {'works': works, 'catalogs': catalogs}
#     list_catalog.update(add_buttons)
#     return {
#         'list': list_catalog,
#         'form_catalog': WorkCatalogForm(hidden_catalog=object_id),
#         'form_work': WorkForm(hidden_catalog=object_id),
#         'formset_work': WorkImageFormSet(),
#         'multiple_choice_tag_form': MultipleChoiceTagForm(),
#     }
#
#
# @render_to("accounts/works/work.html")
# @validate_access(access_profiles=['c', 'm'])
# def catalog_work_view(request, object_id):
#     """
#     Отображение выбранной работы пользователя
#     """
#     work = get_object_or_404(Work, id=object_id, profile=request.user.profile)
#
#     return {
#         'work': work,
#         'breadcrumbs': work.work_catalog.get_ancestors(include_self=True)
#     }
#
#
# @render_to("accounts/works/work_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def work_add(request):
#     """
#     Добавление работы
#     """
#     return work_add_edit(request)
#
#
# @render_to("accounts/works/work_add_or_edit.html")
# @has_edit('work')
# @validate_access(access_profiles=['c', 'm'])
# def work_edit(request, object_id):
#     """
#     Редактирование работы пользователя
#     """
#
#     work = get_object_or_404(Work, id=object_id, profile=request.user.profile)
#     output = work_add_edit(request, work)
#     if isinstance(output, dict):
#         # todo add breadcrumbs
#         pass
#     return output
#
#
# def work_add_edit(request, work=None):
#     """
#     Метод для создания или редактирования работы из личного кабинета.
#     Если есть work, то редактирование, иначе создание.
#     Метод вызывается из вьюх work_add и work_edit
#     """
#     work = work if work else Work()
#
#     multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=work)
#     print request.POST
#     form = WorkForm(request.POST or None, instance=work)
#     formset = WorkImageFormSet(request.POST or None, instance=work)
#     if request.method == 'POST':
#         print form.errors
#         print form.cleaned_data
#         if form.is_valid() and formset.is_valid():
#             work = form.save(commit=False)
#             work.profile = request.user.profile
#             work.save()
#             formset.save()
#             if multiple_choice_tag_form.is_valid():
#                 Tag.instance_update(work, multiple_choice_tag_form.save())
#             return redirect(work.private_url)
#
#     return {
#         'work': work,
#         'form': form,
#         'formset': formset,
#         'multiple_choice_tag_form': multiple_choice_tag_form,
#         'breadcrumbs': work.work_catalog.get_ancestors(include_self=True) if work.id else None
#     }
#
#
# @render_to("accounts/works/work_catalog_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def work_catalog_add(request):
#     """
#     Добавление каталога работ
#     """
#     return work_catalog_add_edit(request)
#
#
# @render_to("accounts/works/work_catalog_add_or_edit.html")
# @has_edit('work_catalog')
# @validate_access(access_profiles=['c', 'm'])
# def work_catalog_edit(request, object_id):
#     """
#     Редактирование каталога работ пользователя
#     """
#     work_catalog = get_object_or_404(WorkCatalog, id=object_id, profile=request.user.profile)
#     output = work_catalog_add_edit(request, work_catalog)
#     if isinstance(output, dict):
#         # todo add breadcrumbs
#         pass
#     return output
#
#
# def work_catalog_add_edit(request, work_catalog=None):
#     """
#     Метод для создания или редактирования каталога работ из личного кабинета.
#     Если есть work_catalog, то редактирование, иначе создание.
#     Метод вызывается из вьюх work_catalog_add и work_catalog_edit
#     """
#
#     form = WorkCatalogForm(request.POST or None, instance=work_catalog)
#     if request.method == 'POST':
#         if form.is_valid():
#             print
#             work_catalog = form.save(commit=False)
#             work_catalog.profile = request.user.profile
#             work_catalog.save()
#             return redirect(work_catalog.private_url)
#
#     return {
#         'work_catalog': work_catalog,
#         'form': form,
#         'breadcrumbs': work_catalog.get_ancestors(include_self=True) if work_catalog else None
#     }
#
#
# @render_to("accounts/services/services.html")
# @validate_access(access_profiles=['c', 'm'])
# def services(request):
#     """
#     Список услуг пользователя
#     """
#     state = request.GET.get('state', '')
#     state_filter = {} if state == '' else {'state': state}
#     return {
#         "states": AbstractBaseClass.STATES,
#         "services": to_pagination(Service.objects.filter(profile=request.user.profile, **state_filter), page=request.GET.get('page'))
#     }
#
#
# @render_to("accounts/services/service_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def service_add(request):
#     """
#     Добавление услуги
#     """
#     return service_add_edit(request)
#
#
# @render_to("accounts/services/service_add_or_edit.html")
# @has_edit('service')
# @validate_access(access_profiles=['c', 'm'])
# def service_edit(request, object_id=None):
#     """
#     Редактирование услуги пользователя
#     """
#     service = get_object_or_404(Service, id=object_id, profile=request.user.profile)
#     output = service_add_edit(request, service=service)
#
#     return output
#
#
# def service_add_edit(request, service=None):
#     """
#     Метод для создания или редактирования услуги из личного кабинета.
#     Если есть service, то редактирование, иначе создание.
#     Метод вызывается из вьюх service_add и service_edit
#     """
#
#     if not service:
#         service = Service()
#
#     multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=service)
#
#     form = ServiceAddOrEditForm(request.POST or None, request.FILES or None, instance=service)
#     formset = ServiceImageFormSet(request.POST or None, request.FILES or None, instance=service)
#     if request.method == 'POST':
#         if form.is_valid() and formset.is_valid():
#             service = form.save(user=request.user)
#             if multiple_choice_tag_form.is_valid():
#                 Tag.instance_update(service, multiple_choice_tag_form.save())
#             formset.save()
#             return redirect('accounts:services')
#
#     return {'service': service, 'form': form, 'formset': formset, 'multiple_choice_tag_form': multiple_choice_tag_form}
#
#
# @render_to("accounts/services/service_view.html")
# @validate_access(access_profiles=['c', 'm'])
# def service_view(request, object_id=None):
#     """
#     Просмотр услуги
#     """
#     service = get_object_or_404(Service, id=object_id, profile=request.user.profile)
#
#     return {
#         'service': service,
#     }
#
#
# def catalog_products_new(request):
#     """
#     Редирект на каталог изделий
#     """
#     return redirect('accounts:productcatalog_redirect')
#
#
# @render_to("accounts/products/product_catalog_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def product_catalog_add(request):
#     """
#     Создание каталога изделий
#     """
#     return product_catalog_add_edit(request)
#
#
# @render_to("accounts/products/product_catalog_add_or_edit.html")
# @has_edit('product_catalog')
# @validate_access(access_profiles=['c', 'm'])
# def product_catalog_edit(request, object_id):
#     """
#     Редактирование каталога изделий
#     """
#     product_catalog = get_object_or_404(ProductCatalog, id=object_id, profile=request.user.profile)
#     output = product_catalog_add_edit(request, product_catalog)
#     if isinstance(output, dict):
#         # todo add breadcrumbs
#         pass
#     return output
#
#
# def product_catalog_add_edit(request, product_catalog=None):
#     """
#     Метод для создания или редактирования каталога изделий из личного кабинета.
#     Если есть product_catalog, то редактирование, иначе создание.
#     Метод вызывается из вьюх product_catalog_add и product_catalog_edit
#     """
#     form = ProductCatalogForm(request.POST or None, instance=product_catalog)
#     if request.method == 'POST':
#         if form.is_valid():
#             product_catalog = form.save(commit=False)
#             product_catalog.profile = request.user.profile
#             product_catalog.save()
#             return redirect(product_catalog.private_url)
#
#     return {
#         'product_catalog': product_catalog,
#         'form': form,
#         'breadcrumbs': product_catalog.get_ancestors(include_self=True) if product_catalog else None
#     }
#
#
# @render_to("accounts/products/products.html")
# @validate_access(access_profiles=['c', 'm'])
# def catalog_products_root_catalog(request):
#     """
#     Список корневого каталога изделий. Содержит список дочерних каталога
#     """
#     return catalog_products_catalog(request, object_id=None)
#
#
# @render_to("accounts/products/products.html")
# def catalog_products_child_catalog(request, object_id=None):
#     """
#     Список дочерних каталогов изделий. Может содержать или список дочерних каталогов или список изделий
#     """
#     catalog_instance = get_object_or_404(ProductCatalog, id=object_id)
#     output = catalog_products_catalog(request, object_id)
#     if isinstance(output, dict):
#         output.update({'breadcrumbs': catalog_instance.get_ancestors(include_self=True)})
#
#     return output
#
#
# def catalog_products_catalog(request, object_id=None):
#     """
#     Метод формарования ответа для вьюх catalog_products_root_catalog и catalog_products_child_catalog.
#     """
#
#     add_buttons = {}
#
#     if object_id:
#         current_catalog = get_object_or_404(ProductCatalog, id=object_id)
#         _catalogs = current_catalog.catalogs(profile=request.user.profile)
#         _products = current_catalog.products(profile=request.user.profile)
#         add_buttons['add_catalog'] = True if _catalogs.exists() else False
#         add_buttons['add_product'] = True if _products.exists() else False
#         if add_buttons.values().count(False) == len(add_buttons.values()):
#             add_buttons['add_catalog'] = add_buttons['add_product'] = True
#         if current_catalog.get_level() == 0:
#             add_buttons['add_product'] = False
#
#     else:
#         _catalogs = ProductCatalog.objects.filter(level=0, parent__isnull=True)
#         _products = None
#         add_buttons['add_catalog'] = add_buttons['add_product'] = False
#
#     list_catalog = {'products': _products, 'catalogs': _catalogs}
#     list_catalog.update(add_buttons)
#
#     return {
#         'list': list_catalog,
#         'form_catalog': ProductCatalogForm(hidden_catalog=object_id),
#         'form_product': ProductForm(hidden_catalog=object_id),
#         'formset_product': ProductImageFormSet(),
#         'multiple_choice_tag_form': MultipleChoiceTagForm()
#     }
#
#
# @render_to("accounts/products/product.html")
# @validate_access(access_profiles=['c', 'm'])
# def catalog_product_view(request, object_id):
#     """
#     Просмотр изделия
#     """
#     product = get_object_or_404(Product, id=object_id, profile=request.user.profile)
#
#     return {
#         'product': product,
#         'breadcrumbs': product.product_catalog.get_ancestors(include_self=True)
#     }
#
#
# @render_to("accounts/products/product_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def product_add(request):
#     """
#     Добавление изделия
#     """
#     return product_add_edit(request)
#
#
# @render_to("accounts/products/product_add_or_edit.html")
# @has_edit('product')
# @validate_access(access_profiles=['c', 'm'])
# def product_edit(request, object_id):
#     """
#     Редактирование изделия
#     """
#     product = get_object_or_404(Product, id=object_id, profile=request.user.profile)
#     output = product_add_edit(request, product)
#     if isinstance(output, dict):
#         # todo add breadcrumbs
#         pass
#     return output
#
#
# def product_add_edit(request, product=None):
#     """
#     Метод для создания или редактирования изделия из личного кабинета.
#     Если есть product, то редактирование, иначе создание.
#     Метод вызывается из вьюх product_add и product_edit
#     """
#     if not product:
#         product = Product()
#
#     multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=product)
#     form = ProductForm(request.POST or None, instance=product)
#     formset = ProductImageFormSet(request.POST or None, instance=product)
#     if request.method == 'POST':
#         if form.is_valid() and formset.is_valid():
#             product = form.save(commit=False)
#             product.profile = request.user.profile
#             product.save()
#             formset.save()
#             if multiple_choice_tag_form.is_valid():
#                 Tag.instance_update(product, multiple_choice_tag_form.save())
#             return redirect(product.private_url)
#
#     return {
#         'product': product,
#         'form': form,
#         'formset': formset,
#         'multiple_choice_tag_form': multiple_choice_tag_form,
#         'breadcrumbs': product.product_catalog.get_ancestors(include_self=True) if product and getattr(product, 'product_catalog', None) else None
#         # 'breadcrumbs': product.product_catalog.get_ancestors(include_self=True) if product and product.product_catalog else None
#     }
#
#
# def catalog_materials_new(request):
#     """
#     Редирект на каталог камней
#     """
#     return redirect('accounts:materialcatalog_redirect')
#
#
# @render_to("accounts/materials/material_catalog_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def material_catalog_add(request):
#     """
#     Добавление каталога камней
#     """
#     return material_catalog_add_edit(request)
#
#
# @render_to("accounts/materials/material_catalog_add_or_edit.html")
# @has_edit('material_catalog')
# @validate_access(access_profiles=['c', 'm'])
# def material_catalog_edit(request, object_id):
#     """
#     Редактирование каталога камней
#     """
#     material_catalog = get_object_or_404(MaterialCatalog, id=object_id, profile=request.user.profile)
#     output = material_catalog_add_edit(request, material_catalog)
#     if isinstance(output, dict):
#         # todo add breadcrumbs
#         pass
#     return output
#
#
# def material_catalog_add_edit(request, material_catalog=None):
#     """
#     Метод для создания или редактирования каталога камней из личного кабинета.
#     Если есть product_catalog, то редактирование, иначе создание.
#     Метод вызывается из вьюх material_catalog_add и material_catalog_edit
#     """
#     form = MaterialCatalogForm(request.POST or None, instance=material_catalog)
#     if request.method == 'POST':
#         if form.is_valid():
#             material_catalog = form.save(commit=False)
#             material_catalog.profile = request.user.profile
#             material_catalog.save()
#             return redirect(material_catalog.private_url)
#
#     return {
#         'material_catalog': material_catalog,
#         'form': form,
#         'breadcrumbs': material_catalog.get_ancestors(include_self=True) if material_catalog else None
#     }
#
#
# @render_to("accounts/materials/materials.html")
# @validate_access(access_profiles=['c', 'm'])
# def catalog_materials_root_catalog(request):
#     """
#     Список корневого каталога камней. Содержит список дочерних каталога
#     """
#     return catalog_materials_catalog(request)
#
#
# @render_to("accounts/materials/materials.html")
# def catalog_materials_child_catalog(request, object_id=None):
#     """
#     Список дочерних каталогов камней. Может содержать или список дочерних каталогов или список камней
#     """
#     current_catalog = get_object_or_404(MaterialCatalog, id=object_id)
#     output = catalog_materials_catalog(request, current_catalog)
#     if isinstance(output, dict):
#         output.update({'breadcrumbs': current_catalog.get_ancestors(include_self=True)})
#
#     return output
#
#
# def catalog_materials_catalog(request, current_catalog=None):
#     """
#     Метод формарования ответа для вьюх catalog_materials_root_catalog и catalog_materials_child_catalog.
#     """
#
#     class_form = MaterialForm
#     add_buttons = {}
#
#     if current_catalog:
#         catalogs = current_catalog.catalogs(profile=request.user.profile)
#         _materials = current_catalog.materials(profile=request.user.profile)
#         add_buttons['add_catalog'] = True if catalogs.exists() else False
#         add_buttons['add_material'] = True if _materials.exists() else False
#         if add_buttons.values().count(False) == len(add_buttons.values()):
#             add_buttons['add_catalog'] = add_buttons['add_material'] = True
#         if current_catalog.get_level() == 0:
#             add_buttons['add_catalog'] = add_buttons['add_material'] = False
#         class_form = MaterialForm if current_catalog.is_natural() else MaterialArtificialForm
#     else:
#         catalogs = MaterialCatalog.objects.filter(level=0, parent__isnull=True)
#         _materials = None
#         add_buttons['add_catalog'] = add_buttons['add_material'] = False
#
#     list_catalog = {'materials': _materials, 'catalogs': catalogs}
#     list_catalog.update(add_buttons)
#
#     return {
#         'list': list_catalog,
#         'form_catalog': MaterialCatalogForm(hidden_catalog=current_catalog.id if current_catalog else None),
#         'form_material': class_form(hidden_catalog=current_catalog.id if current_catalog else None),
#         'formset_material': MaterialImageFormSet(),
#         'multiple_choice_tag_form': MultipleChoiceTagForm()
#     }
#
#
# @render_to("accounts/materials/material.html")
# @validate_access(access_profiles=['c', 'm'])
# def material_view(request, object_id):
#     """
#     Просмотр камня
#     """
#     material = get_object_or_404(Material, id=object_id, profile=request.user.profile)
#
#     return {
#         'material': material,
#         'breadcrumbs': material.material_catalog.get_ancestors(include_self=True)
#     }
#
#
# @render_to("accounts/materials/material_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def material_natural_add(request):
#     """
#     Добавление натурального камня
#     """
#     return material_add_edit(request, natural=True)
#
#
# @render_to("accounts/materials/material_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def material_artificial_add(request):
#     """
#     Добавление искусственного камня
#     """
#     return material_add_edit(request, natural=False)
#
#
# @render_to("accounts/materials/material_add_or_edit.html")
# @has_edit('material')
# @validate_access(access_profiles=['c', 'm'])
# def material_edit(request, object_id):
#     """
#     Редактирование камня
#     """
#     material = get_object_or_404(Material, id=object_id, profile=request.user.profile)
#     # todo change product_id on product
#     output = material_add_edit(request, material.material_catalog.is_natural(), object_id)
#     if isinstance(output, dict):
#         # todo add breadcrumbs
#         pass
#     return output
#
#
# def material_add_edit(request, natural, object_id=None):
#     """
#     Метод для создания или редактирования камня из личного кабинета.
#     Если есть object_id, то редактирование, иначе создание.
#     Метод вызывается из вьюх material_natural_add, material_artificial_add и material_edit
#     """
#
#     if object_id:
#         material = get_object_or_404(Material, id=object_id)
#     else:
#         material = Material()
#         material.profile = request.user.profile
#
#     multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=material)
#     class_form = MaterialForm if natural else MaterialArtificialForm
#     form = class_form(request.POST or None, instance=material)
#     formset = MaterialImageFormSet(request.POST or None, instance=material)
#     if request.method == 'POST':
#         if form.is_valid() and formset.is_valid():
#             material = form.save(commit=False)
#             material.profile = request.user.profile
#             material.save()
#             formset.save()
#             if multiple_choice_tag_form.is_valid():
#                 Tag.instance_update(material, multiple_choice_tag_form.save())
#             return redirect(material.private_url)
#
#     return {
#         'material': material,
#         'form': form,
#         'formset': formset,
#         'multiple_choice_tag_form': multiple_choice_tag_form,
#         'breadcrumbs': material.material_catalog.get_ancestors(include_self=True) if object_id else None
#     }
#
#
# @render_to("accounts/offers/offers.html")
# @validate_access(access_profiles=['c', 'm'])
# def offers(request):
#     """
#     Список акций и предложений
#     """
#     state = request.GET.get('state', '')
#     state_filter = {} if state == '' else {'state': state}
#     return {
#         "states": AbstractBaseClass.STATES,
#         'offers': Offer.objects.filter(profile=request.user.profile, **state_filter)
#     }
#
#
# @render_to("accounts/offers/offer_add_or_edit.html")
# @validate_access(access_profiles=['c', 'm'])
# def offer_add(request):
#     """
#     Добавление акции или предложения
#     """
#     return offer_add_edit(request)
#
#
# @render_to("accounts/offers/offer_add_or_edit.html")
# @has_edit('offer')
# @validate_access(access_profiles=['c', 'm'])
# def offer_edit(request, object_id):
#     """
#     Редактирование акции или предложения
#     """
#     offer = get_object_or_404(Offer, id=object_id, profile=request.user.profile)
#     output = offer_add_edit(request, offer=offer)
#
#     return output
#
#
# def offer_add_edit(request, offer=None):
#     """
#     Метод для создания или редактирования акции или предложения из личного кабинета.
#     Если есть offer, то редактирование, иначе создание.
#     Метод вызывается из вьюх offer_add и offer_edit
#     """
#     from offers.forms import OfferForm
#     if not offer:
#         offer = Offer()
#
#     multiple_choice_tag_form = MultipleChoiceTagForm(request.POST or None, initial_object=offer)
#     form = OfferForm(request.POST or None,
#                      instance=offer,
#                      initial={'city': request.user.profile.city.id})
#     formset = OfferFormSet(request.POST or None, request.FILES or None, instance=offer)
#     if request.method == 'POST':
#         if form.is_valid() and formset.is_valid():
#             offer = form.save(user=request.user)
#             if multiple_choice_tag_form.is_valid():
#                 Tag.instance_update(offer, multiple_choice_tag_form.save())
#             formset.save()
#             return redirect('accounts:offers')
#
#     return {'offer': offer, 'form': form, 'formset': formset, 'multiple_choice_tag_form': multiple_choice_tag_form}
#
#
# @render_to("accounts/offers/offer_view.html")
# @validate_access(access_profiles=['c', 'm'])
# def offer_view(request, object_id):
#     """
#     Просмотр акции или предложения
#     """
#     offer_instance = get_object_or_404(Offer, pk=object_id, profile=request.user.profile)
#     return {
#         'offer': offer_instance,
#     }
#
#
# @render_to("accounts/companies/list.html")
# def companies_list(request):
#     """
#     Отображение страницы со списком компаний Поставщиков или Камнеобработчиков
#     На данный момент список компаний выводиться методом company_filter посредством Ajax
#     после загрузки шаблона list.html
#     """
#     from geo.forms import CityChoiceForm
#
#     url = request.build_absolute_uri()
#     company_type = "providers" if "providers" in url else "stoneworkers"
#
#     return {
#         'company_type': company_type,
#         'city_choice_form': CityChoiceForm()
#     }
#
#
# @render_to_json
# def companies_filter(request, page=None):
#     """
#     Ajax запрос для формирования списка компаний Поставщиков или Камнеобработчиков
#     """
#     output = {'result': {'object_list': [], 'paginator': {}}}
#     city_id = request.GET.get('city')
#     order = request.GET.get('order')
#
#     referer = request.META.get("HTTP_REFERER")
#
#     from accounts.serializers import OrderRatesSerializer
#
#     where = {"provider": True} if "providers" in referer else {"stoneworker": True}
#
#     companies = Profile.objects.producers().filter(**where).annotate(
#         orders=Count('performer__customer_finish_date'),
#         testimonials=Count('performer__orderrecall'),
#         city_title=F('city__title'),
#         ave_grade=Sum('performer__orderrecall__rate') / F('testimonials') / 5 * 100,
#         gems=F('profilegrades__gems') / 5 * 100)
#
#     if city_id:
#         companies = companies.filter(city__id=city_id)
#     if order == 'rate':
#         companies = companies.order_by('position')
#     elif order == 'orders':
#         companies = companies.order_by('-orders')
#     else:
#         companies = companies.order_by('-testimonials')
#     serializer = OrderRatesSerializer(companies, many=True)
#     paginate = to_pagination(serializer.data, page, 10)
#
#     if paginate.has_next():
#         next_page_url = reverse('companies:companies_filter_page', kwargs={'page': paginate.next_page_number()})
#     else:
#         next_page_url = None
#
#     output['producers_count'] = Profile.objects.producers().count()
#     output['result']['object_list'] = paginate.object_list
#     output['result']['paginator'] = {
#         'has_next': paginate.has_next(),
#         'next_page_url': next_page_url,
#         'next_page_number': paginate.next_page_number() if paginate.has_next() else None
#     }
#     return output
#
#
# @set_views(obj='company')
# def profile_public(request, slug):
#     """
#     Публичный профиль пользователя (компании или мвстера)
#     """
#     profile = get_object_or_404(Profile, slug=slug, role__in=[Profile.ROLE_COMPANY, Profile.ROLE_MASTER])
#
#     events = Event.objects.filter(public=True, certified=True, profile=profile)
#     serializer = EventPublicSerializer(events, many=True)
#     import json
#     from django.core.serializers.json import DjangoJSONEncoder
#     from orders.models import OrderRecall
#     testimonials = OrderRecall.objects.filter(order__performer=profile)
#     profile.ave_rate = 0
#     profile.rate = 0
#     if testimonials:
#         profile.ave_rate = (
#             float(reduce(lambda x, y: x + y, map(lambda x: x.rate, testimonials), 0)) /
#             testimonials.count() / 5 * 100)
#         profile.rate = float(reduce(lambda x, y: x + y, map(lambda x: x.rate, testimonials))) / testimonials.count()
#
#     context = {
#         'company': profile,
#         'offers': Offer.objects.filter(profile=profile).prefetch_related('offerimage_set'),
#         'menu_catalogs': ProductCatalogMenu.objects.all(),
#         'material_catalogs': {'get_children': MaterialCatalog.objects.filter(level=0, certified=True)},
#         'material_elements_in_line': 4,
#         'countries': Country.objects.all(),
#         'productions': MaterialProduction.objects.all(),
#         'news_list': News.objects.filter(profile=profile),
#         'events': json.dumps(serializer.data, cls=DjangoJSONEncoder),
#         'service_catalogs': ServiceCatalog.objects.all(),
#         'work_catalog': WorkCatalog.objects.filter(Q(profile=profile) | Q(profile__isnull=True), Q(level=0)),
#         'testimonials': testimonials,
#         'producers_count': Profile.objects.producers().count()
#     }
#     return TemplateResponse(request, "accounts/companies/profile.html", context)
#
#
# @render_to_json
# def ajax_catalog_products(request, catalog_id, page=None):
#     """
#     Ajax запрос для формирования отображения списка каталога изделий в личном или публичном профиле
#     """
#     output = {'result': {'object_list': [], 'paginator': {}}}
#     clist = {}
#     catalog = ProductCatalog.objects.get(id=catalog_id)
#     catalogs = ProductCatalog.objects.filter(parent=catalog)
#
#     if catalogs:
#         clist = {'catalogs': catalogs}
#         output.update({'catalog': True})
#     else:
#         _products = Product.objects.filter(product_catalog=catalog, certified=True)
#         if _products:
#             clist = {'products': _products}
#             output.update({'products': True})
#
#     if 'catalogs' in clist:
#         for c in clist['catalogs']:
#             for i in range(0, 9):
#                 output['result']['object_list'].append(
#                     {
#                         'id': c.id,
#                         'url': reverse('products:ajax_catalog_products', args=[c.id]),
#                         'image': c.image.get_thumbnail({'size': (150, 150), 'crop': True}).url,
#                         'title': c.title
#                     }
#                 )
#     elif 'products' in clist:
#         j = 0
#         output['result']['object_list'] = []
#         for p in clist['products']:
#             for i in range(0, 5):
#                 output['result']['object_list'].append(
#                     {
#                         'id': p.id,
#                         'url': reverse('products:ajax_products', args=[p.id]),
#                         'image': p.main_image.image.get_thumbnail({'size': (150, 150), 'crop': True}).url,
#                         'title': p.title,
#                         'break': False if j % 6 > 0 else True,
#                     }
#                 )
#                 j += 1
#
#         paginate = to_pagination(output['result']['object_list'], page, 18)
#         if paginate.has_next():
#             next_page_url = reverse('products:ajax_catalog_products_page', kwargs={'catalog_id': catalog_id,
#                                                                                    'page': paginate.next_page_number()})
#         else:
#             next_page_url = None
#         output['result']['object_list'] = paginate.object_list
#         output['result']['paginator'] = {
#             'has_next': paginate.has_next(),
#             'next_page_url': next_page_url,
#             'next_page_number': paginate.next_page_number() if paginate.has_next() else None
#         }
#
#     return output
#
#
# @render_to_json
# def ajax_products(request, product_id):
#     """
#     Ajax запрос для формирования отображения изделия в личном или публичном профиле
#     """
#     product = Product.objects.get(id=product_id)
#
#     output = {'result': {
#         'title': product.title,
#         'description': product.description,
#         'main_image': product.main_image.image.get_thumbnail({'size': (340, 340), 'crop': True}).url,
#         'images': list([image.image.get_thumbnail({'size': (340, 340), 'crop': True}).url for image in product.productimage_set.all()]),
#         'city': {'title': product.profile.city.title},
#         'category': {'title': product.product_catalog.title},
#         'company': {'title': product.profile.name, 'url': product.profile.public_url}
#     }}
#
#     return output
#
#
# def materials(request):
#     """
#     Вероятно устаревший метод.
#     """
#     catalogs = MaterialCatalog.objects.filter(level=0)
#
#     return {
#         'menu_catalogs': ProductCatalogMenu.objects.all(),
#         'catalogs': catalogs,
#         'countries': Country.objects.all(),
#         'productions': MaterialProduction.objects.all(),
#     }
#
#
# def products(request, catalog_id=None):
#     """
#     Вероятно устаревший метод.
#     """
#     # catalogs = ProductCatalog.objects.filter(company=None, parent__id=catalog_id)
#     catalogs = ProductCatalog.objects.filter(parent__id=catalog_id)
#     if not catalogs:
#         return {
#             'menu_catalogs': ProductCatalogMenu.objects.all(),
#             'catalogs': catalogs,
#         }
#     if not catalog_id:
#         # catalog = catalogs[0]
#         # return redirect('products:catalog_id', catalog_id=catalog.id)
#         catalog = None
#         _products = Product.objects.filter(certified=True)
#         # products = Product.objects.filter(certified=True, **filter_by_geo(request.session))
#     else:
#         catalog = ProductCatalog.objects.get(id=catalog_id)
#         _products = Product.objects.filter(product_catalog=catalog, certified=True)
#         # products = Product.objects.filter(product_catalog=catalog, certified=True, **filter_by_geo(request.session))
#
#     return {
#         'menu_catalogs': ProductCatalogMenu.objects.all(),
#         'catalogs': catalogs,
#         'products': to_pagination(iter_object=_products, page=request.GET.get('page')),
#         'current_catalog': catalog,
#     }
#
#
# @render_to_json
# def ajax_catalog_materias(request, page=None):
#     """
#     Ajax запрос для формирования отображения списка каталога камней в личном или публичном профиле
#     """
#     profile = None
#     if 'HTTP_REFERER' in request.META:
#         http_referer = request.META['HTTP_REFERER'].split(request.META['HTTP_HOST'])[1]
#         if http_referer == '/accounts/profile/':
#             profile = request.user.profile
#         else:
#             resolver_match = resolve(http_referer)
#             if resolver_match.url_name == 'profile_view':
#                 slug = resolver_match.kwargs.get('slug')
#                 profile = Profile.objects.get(slug=slug)
#
#     output = {'result': {'object_list': [], 'paginator': {}}, 'materials': True, 'mustache_id': ''}
#     parent = request.GET.get('parent')
#     catalog_ids = request.GET.getlist('catalog_id')
#     tag_ids = request.GET.getlist('tag_id', [])
#     country_id = request.GET.get('country', None)
#     production_id = request.GET.get('production', None)
#     tags = Tag.objects.filter(id__in=tag_ids)
#     material_elements_in_line = int(request.GET.get('material_elements_in_line', 4))
#
#     where = {'profile': profile}
#     if catalog_ids:
#         if len(catalog_ids) == 1:
#             child_catalogs = MaterialCatalog.objects.filter(parent_id__in=catalog_ids)
#             where.update({"material_catalog__in": child_catalogs})
#         else:
#             child_catalogs = MaterialCatalog.objects.filter(id__in=catalog_ids)
#             where.update({"material_catalog__in": child_catalogs})
#     elif parent:
#         # MaterialCatalog.objects.rebuild()
#         # print MaterialCatalog.objects.get(level=0, catalog_type=parent).get_descendants()
#         where.update({"material_catalog__in": MaterialCatalog.objects.get(level=0, catalog_type=parent).get_descendants()})
#     if country_id:
#         where.update({"country__id": country_id})
#     if production_id:
#         where.update({"production__id": production_id})
#     if tags:
#         material_list = Material.objects.filter(Q(tags__in=tags), **where)
#     else:
#         material_list = Material.objects.filter(**where)
#
#     paginate = to_pagination(material_list.distinct(), page, material_elements_in_line * 2)
#     j = 0
#     for material in paginate.object_list:
#         for i in range(0, 1):
#             output['result']['object_list'].append(
#                 {
#                     'id': material.id,
#                     'url': reverse('products:ajax_material', args=[material.id]),
#                     'image': material.main_image.get_thumbnail({'size': (250, 250), 'crop': True}).url,
#                     'title': material.title,
#                     'country': {'title': material.country.title},
#                     'color': material.get_color().title if material.get_color() else 'None',
#                     'break': False if j % material_elements_in_line > 0 else True,
#                 }
#             )
#             j += 1
#     output['result']['paginator'] = {
#         'has_next': paginate.has_next(),
#         'next_page_url': reverse('company:ajax_catalog_materias_page', kwargs={'page': paginate.next_page_number()}) if paginate.has_next() else None,
#         'next_page_number': paginate.next_page_number() if paginate.has_next() else None
#     }
#
#     output['mustache_id'] = '#catalog_materials_template'
#
#     return output
#
#
# @render_to_json
# def ajax_material(request, material_id):
#     """
#     Ajax запрос для формирования отображения камня в личном или публичном профиле
#     """
#     material = Material.objects.get(id=material_id)
#
#     output = {'result': {
#         'title': material.title,
#         'description': material.description,
#         'main_image': material.main_image.image.get_thumbnail({'size': (340, 340), 'crop': True}).url,
#         'images': list([image.image.get_thumbnail({'size': (340, 340), 'crop': True}).url for image in material.materialimage_set.all()]),
#         'city': {'title': material.profile.city.title if material.profile else 'None'},
#         'category': {'title': material.material_catalog.title},
#         'company': {'title': material.profile.name, 'url': material.profile.public_url if material.profile else {'title': 'None', 'url': 'None'}}
#     }}
#
#     return output
#
#
# @render_to_json
# def delete(request, data):
#     """
#     Общий метод для удаления контента пользователя.
#     Получает строку с данными, в которой указаны Название приложения, Название модели и Id элемента.
#     По полученным данным достает нужный экземпляр, проверяет его принадлежность текущему пользователю
#     и метит его как удаленный instance.mark_as_removed().
#     Сейчас instance.mark_as_removed() закомментирован, пока идет тест.
#     """
#     try:
#         app_name, app_model, pk = data.split(':')
#         from importlib import import_module
#         app = import_module(app_name)
#         if hasattr(app, 'models'):
#             models_py = getattr(app, 'models')
#             if hasattr(models_py, app_model):
#                 model = getattr(models_py, app_model)
#                 instance = model.objects.get(pk=pk, profile=request.user.profile)
#                 instance.mark_as_removed(commit=True)
#
#                 from django.db import models
#                 redirect_url = ''
#                 for field in instance._meta.fields:
#                     if isinstance(field, models.ForeignKey):
#                         getattr(instance, field.name)
#                         # todo: add redirect url
#                         redirect_url = '/'
#
#                 return {'success': True, 'next': redirect_url}
#     except:
#         pass
#
#     return {'success': False}
#
#
@render_to("accounts/tickets/list.html")
def tickets(request):
    """
    Отображение списка тикетов и ответов на них
    """
    _profile = request.user.profile
    _tickets = Ticket.objects.filter(profile=_profile)
    if request.method == 'GET':
        messages = _tickets.order_by('pk', 'message__date')\
            .values('pk', 'is_active', 'message__date', 'message__profile', 'message__text', 'message__file')
        return {'messages': messages}
    if request.method == 'POST':
        message_form = MessageForm(data=request.POST, files=request.FILES, profile=request.user.profile)
        if message_form.is_valid():
            new_message = message_form.save()
            if request.is_ajax():
                from django.http import JsonResponse
                img = _profile.get_avatar().generate_thumbnail({'size': (57, 56), 'crop': True}).url
                response = JsonResponse({'message': new_message.text,
                                         'date': timezone.localtime(new_message.date).strftime('%H:%M'),
                                         'img': img,
                                         'file': new_message.file.url if new_message.file else ''
                                         },
                                        status=201)
                return response
        return redirect('accounts:tickets')


@render_to("accounts/notifications/list.html")
def notifications_setting(request):
    """
    Отображение списка рассылок и их изменение
    """
    pr = request.user.profile
    if request.method == 'POST':
        pr.update_email_subs(request.POST.getlist('subs'))
    settings = pr.get_email_subs()
    return {'settings': settings}
