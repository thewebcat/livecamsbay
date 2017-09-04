# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Avg, Max
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from django_filters.views import FilterView
from main.decorators import set_views

from .filters import ModelsFilter

from .models import Model, Sex
from .models import CamService
from .models import CamSnapshot
from .models import Race
from .models import HairColor
from .models import BustSize
from .models import PublicArea

import urllib, json


# Create your views here.

class Catalogue(FilterView):
    template_name = 'index.html'
    model = Model
    filterset_class = ModelsFilter
    paginate_by = 25
    qs_count = 0

    @property
    def get_cam_service(self):
        cam_service = self.kwargs.get('cam_service')
        if cam_service:
            return cam_service
        else:
            return None

    @property
    def get_sex(self):
        sex = self.kwargs.get('sex')
        if sex:
            return sex
        else:
            return None

    def get_template_names(self):
        if not self.request.is_ajax():
            return [self.template_name]
        return ['models_content.html']

    def get_queryset(self):
        where = {}
        if self.get_cam_service:
            if self.get_cam_service == "all":
                pass
            else:
                try:
                    cam = CamService.objects.get(prefix=self.get_cam_service)
                except:
                    cam = None
                where.update({'cam_service': cam})
        if self.get_sex:
            try:
                sex = Sex.objects.get(code=self.get_sex)
            except:
                sex = None
            where.update({'sex': sex})
        queryset = Model.objects.filter(available=True).filter(**where).select_related(
            'sex', 'race', 'hair_color', 'bust_size', 'figure', 'public_area', 'cam_service').prefetch_related('speaks_language')
        self.qs_count = len(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Catalogue, self).get_context_data(**kwargs)
        # f = ModelsFilter(self.request.GET, queryset=self.queryset)
        # context['filter'] = f
        #context['models_count'] = len(Model.objects.filter(available=True))
        # context['max_age'] = max(price_list) if price_list else 1000
        # context['min_age'] = min(price_list) if price_list else 0
        context['max_age'] = 70
        context['min_age'] = 18
        context['race'] = Race.objects.all()
        context['hair_color'] = HairColor.objects.all()
        context['bust_size'] = BustSize.objects.all()
        context['public_area'] = PublicArea.objects.all()
        context['models_count'] = self.qs_count
        context['all_time'] = self.get_queryset().aggregate(max_time=Max('online_time'))
        return context

    def get(self, request, *args, **kwargs):
        response = super(Catalogue, self).get(request, *args, **kwargs)
        if request.is_ajax():
            response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
            response['Pragma'] = 'no-cache'
        return response

class ModelPage(DetailView):
    slug_field = 'name'
    template_name = 'model_page.html'
    model = Model

    def get_queryset(self):
        return Model.objects.prefetch_related('camsnapshot_set')

    @set_views(obj='model')
    def dispatch(self, request, *args, **kwargs):
        return super(ModelPage, self).dispatch(request, *args, **kwargs)