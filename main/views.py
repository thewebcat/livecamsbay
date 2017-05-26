# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, FormView
from django_filters.views import FilterView

from .filters import ModelsFilter

from .models import Model
from .models import CamService

import urllib, json


# Create your views here.

class Index(FilterView):
    template_name = 'index.html'
    model = Model
    filterset_class = ModelsFilter
    paginate_by = 25
    qs_count = 0

    def get_template_names(self):
        if not self.request.is_ajax():
            return [self.template_name]
        return ['index_ajax.html']

    def get_queryset(self):
        queryset = Model.objects.filter(available=True).select_related(
            'sex', 'race', 'hair_color', 'bust_size', 'figure', 'public_area').prefetch_related('speaks_language')
        self.qs_count = len(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        # f = ModelsFilter(self.request.GET, queryset=self.queryset)
        # context['filter'] = f
        #context['models_count'] = len(Model.objects.filter(available=True))
        context['models_count'] = self.qs_count
        return context


class UpdateApi(TemplateView):
    template_name = 'api-update-log.html'

    def get_context_data(self, **kwargs):
        url = 'https://ssl-tools.bongacams.com/promo.php?c=372807&type=api&api_v=1&api_type=json'
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        context = super(UpdateApi, self).get_context_data(**kwargs)
        cam = CamService.objects.get(pk=1)
        gender = []
        primary_language_key = []
        secondary_language_key = []
        weight = []
        hair_color = []
        height = []
        pubic_hair = []
        ethnicity = []
        context['girls'] = []
        Model.objects.all().update(available=False)
        # for item in models:
        #     item.available = False
        #     item.save()

        for i in data:
            if i['username'] == 'Alice_in_Love':
                context['json'] = u'username: {0}<br>'.format(i['username'])
                context['json'] += u'primary_language_key: {0}<br>'.format(i['primary_language_key'])
                context['json'] += u'weight: {0}<br>'.format(i['weight'])
                context['json'] += u'secondary_language_key: {0}<br>'.format(i['secondary_language_key'])
                context['json'] += u'hair_color: {0}<br>'.format(i['hair_color'])
                context['json'] += u'height: {0}<br>'.format(i['height'])
                context['json'] += u'pubic_hair: {0}<br>'.format(i['pubic_hair'])
                context['json'] += u'restricted_country_ids: {0}<br>'.format(i['restricted_country_ids'])
                context['json'] += u'primary_language: {0}<br>'.format(i['primary_language'])
                context['json'] += u'ethnicity: {0}<br>'.format(i['ethnicity'])
                context['json'] += u'display_name: {0}<br>'.format(i['display_name'])
                context['json'] += u'eye_color: {0}<br>'.format(i['eye_color'])
                context['json'] += u'members_count: {0}<br>'.format(i['members_count'])
                context['json'] += u'gender: {0}<br>'.format(i['gender'])
                context['json'] += u'display_age: {0}<br>'.format(i['display_age'])
                context['json'] += u'thumbnail_image_medium_live: {0} <img src="{0}" ><br>'.format(
                    i['profile_images']['thumbnail_image_medium_live'])
                context['json'] += u'thumbnail_image_medium: {0} <img src="{0}" ><<br>'.format(
                    i['profile_images']['thumbnail_image_medium'])

            gender.append(i['gender'])
            primary_language_key.append(i['primary_language_key'])
            secondary_language_key.append(i['secondary_language_key'])
            weight.append(i['weight'])
            hair_color.append(i['hair_color'])
            pubic_hair.append(i['pubic_hair'])
            ethnicity.append(i['ethnicity'])

            context['gender'] = list(set(gender))
            context['primary_language_key'] = list(set(primary_language_key))
            context['secondary_language_key'] = list(set(secondary_language_key))
            context['weight'] = list(set(weight))
            context['hair_color'] = list(set(hair_color))
            context['pubic_hair'] = list(set(pubic_hair))
            context['ethnicity'] = list(set(ethnicity))
            # context['primary_language_key'] = list(set(primary_language_key))
            # context['girls'].append(i['username'])
            data = {
                'name': cam.prefix + i['username'],
                'display_name': i['username'],
                'profile_image': i['profile_images']['thumbnail_image_medium'],
                'age': i['display_age'],
                'available': True if i['status'] == 1 else False,
                'cam_service': cam,
            }


            Model.objects.update_or_create(
                name=cam.prefix + i['username'],
                defaults=data
            )

        return context
