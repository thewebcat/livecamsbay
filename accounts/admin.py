# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.core.urlresolvers import resolve
from django.db.models import Q
from ckeditor.widgets import CKEditorWidget
from django.db import models

# from articles.models import Article
# from calendar_events.models import Event
# from custom_auth.models import User
from accounts.models import (
     Profile, ProfilePhone,
     ProfileEmail, ProfileUrl, FavoriteModel)
#
# from materials.models import MaterialCatalog, Material
# from news.models import News
# from notes.models import Note
# from offers.models import Offer
# from orders.models import Order, OrderRecall
# from products.models import ProductCatalog, Product
# from services.models import ServiceCatalog, Service
# from works.models import WorkCatalog, Work


# class ProfilePhoneInline(admin.TabularInline):
#     model = ProfilePhone
#     extra = 1
#
#
# class ProfileBankDetailsInline(admin.TabularInline):
#     model = ProfileBankDetails
#     extra = 1
#
#
# class ProfileContactPersonInline(admin.TabularInline):
#     model = ProfileContactPerson
#     extra = 1
#
#
# class ProfileDirectorInline(admin.TabularInline):
#     model = ProfileDirector
#     extra = 1
#
#
# class ProfileEmailInline(admin.TabularInline):
#     model = ProfileEmail
#     extra = 1
#
#
# class ProfileUrlInline(admin.TabularInline):
#     model = ProfileUrl
#     extra = 1
#
#
# class ProfileGradesInline(admin.TabularInline):
#     model = ProfileGrades
#     can_delete = False
#     fields = ('add_gem', )
#
#
# class NewsInline(admin.StackedInline):
#     model = News
#     extra = 0
#
#
# class NoteInline(admin.StackedInline):
#     model = Note
#     extra = 0
#
#
# class OfferInline(admin.StackedInline):
#     model = Offer
#     extra = 0
#
#
# class ProductInline(admin.StackedInline):
#     model = Product
#     extra = 0
#
#
# class OrderInline(admin.StackedInline):
#     model = Order
#     extra = 0
#
#
# class OrderRecallInline(admin.TabularInline):
#     model = OrderRecall
#     extra = 0
#
#
#
# class MaterialInline(admin.StackedInline):
#     model = Material
#     extra = 0
#
#
# class UserInline(admin.StackedInline):
#     model = User
#     extra = 0
#
#
# class WorkInline(admin.StackedInline):
#     model = Work
#     extra = 0
#
#
# class ArticleInline(admin.StackedInline):
#     model = Article
#     extra = 0
#
#
# class EventInline(admin.StackedInline):
#     model = Event
#     extra = 0
#
#
# # for catalogs
# class MixinInline(object):
#     extra = 0
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         id = resolve(request.path).args[0]
#         kwargs["queryset"] = self.model.objects.filter(Q(profile=id) | Q(profile=None))
#         return super(MixinInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
#
#
# class ProductCatalogInline(MixinInline, admin.StackedInline):
#     model = ProductCatalog
#
#
# class WorkCatalogInline(MixinInline, admin.StackedInline):
#     model = WorkCatalog
#
#
# class MaterialCatalogInline(MixinInline, admin.StackedInline):
#     model = MaterialCatalog
#
#
# class ServiceInline(MixinInline, admin.StackedInline):
#     model = Service
#
#
# class ServiceCatalogInline(MixinInline, admin.StackedInline):
#     model = ServiceCatalog
#
#
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
#     save_on_top = True
#     exclude = ('position', )
#     list_display = ('name', 'city', 'certified', 'state', 'provider', 'stoneworker', 'create_date_formated', 'position', 'point')
#     list_editable = ('certified', 'state', 'provider', 'stoneworker')
#     list_display_links = ('name',)
#     search_fields = ('name', )
#     list_filter = ('role', 'city')
#     formfield_overrides = {
#         models.TextField: {'widget': CKEditorWidget},
#     }
#     inlines = (ProfilePhoneInline, ProfileBankDetailsInline, ProfileContactPersonInline, ProfileDirectorInline,
#                ProfileEmailInline, ProfileUrlInline, ProfileGradesInline, OrderRecallInline)
#     # , ProductCatalogInline, ProductInline, WorkCatalogInline, MaterialCatalogInline, NewsInline, ServiceCatalogInline,
#     #  ServiceInline, NoteInline, OfferInline, MaterialInline, WorkInline, ArticleInline, EventInline
#
#     def create_date_formated(self, obj):
#         """
#         Метод возвращает форматированную дату создания профиля.
#         !*!*!
#             Возможно для универсальности стоит вывести данный метод в саму модель.
#             Так же отсутствует возможность сортировки.
#             ДОРАБОТАТЬ!
#         !*!*!
#         """
#         return obj.create_date.strftime('%d.%m.%Y')
#     create_date_formated.short_description = 'Create date'
#
# admin.site.register(Profile, ProfileAdmin)
@admin.register(FavoriteModel)
class FavoriteModelAdmin(admin.ModelAdmin):
    list_display = ('profile', 'model')