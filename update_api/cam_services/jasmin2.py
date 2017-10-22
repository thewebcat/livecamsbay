# -*- coding: utf-8 -*-
import json
import urllib

from datetime import datetime
from accounts.models import FavoriteModel, Profile
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from main.emails import model_went_online
from main.models import CamSnapshot, Model, BustSize, HairColor, Race, Sex, Figure, CamService
from update_api.views import load_api_data


class JasminShowApi(TemplateView):
    template_name = 'api-update-log.html'
    #cam, data = load_api_data('jasmin')

    def get_context_data(self, **kwargs):
        cam = CamService.objects.get(prefix='jasmin')
        response = urllib.urlopen(cam.api_url)
        data = json.loads(response.read())

        context = super(JasminShowApi, self).get_context_data(**kwargs)
        gender = []
        primary_language_key = []
        secondary_language_key = []
        weight = []
        hair_color = []
        height = []
        pubic_hair = []
        ethnicity = []
        sh_bust_penis_size = []

        for i in data['data']['models']:
            gender.append(i['category'])
            primary_language_key.append(i['details']['languages'])
            secondary_language_key.append(i['persons'][0]['sex'])
            weight.append(i['persons'][0]['body']['build'])
            hair_color.append(i['persons'][0]['body']['hairColor'])
            #pubic_hair.append(i['pubic_hair'])
            #ethnicity.append(i['ethnicity'])
            sh_bust_penis_size.append(i['persons'][0]['body']['breastSize'])

            context['gender'] = list(set(gender))
            context['primary_language_key'] = [x for x in primary_language_key]
            context['secondary_language_key'] = list(set(secondary_language_key))
            context['weight'] = list(set(weight))
            context['hair_color'] = list(set(hair_color))
            #context['pubic_hair'] = list(set(pubic_hair))
            #context['ethnicity'] = list(set(ethnicity))
            context['sh_bust_penis_size'] = list(set(sh_bust_penis_size))
        return context


class JasminUpdateApi(View):

    def get(self, *args, **kwargs):
        #cam, data = load_api_data('jasmin')
        cam = CamService.objects.get(prefix='jasmin2')
        response = urllib.urlopen(cam.api_url)
        cam_data = json.loads(response.read())

        changed_objects = []

        for i in cam_data['data']['models']:
            if i['persons'][0]['sex'] == u'female':
                sex = Sex.objects.get(code='w')
            elif i['persons'][0]['sex'] == u'male':
                sex = Sex.objects.get(code='m')
            elif i['persons'][0]['sex'] == u'hermaphrodite':
                sex = Sex.objects.get(code='t')
            elif i['persons'][0]['sex'] == u'shemale':
                sex = Sex.objects.get(code='t')
            elif i['persons'][0]['sex'] == u'transgendered':
                sex = Sex.objects.get(code='t')
            else:
                sex = None

            if i['ethnicity'] == u'white':
                race = Race.objects.get(code='white')
            elif i['ethnicity'] == u'latin':
                race = Race.objects.get(code='latin')
            elif i['ethnicity'] == u'ebony':
                race = Race.objects.get(code='black')
            elif i['ethnicity'] == u'asian':
                race = Race.objects.get(code='asian')
            else:
                race = None

            if i['persons'][0]['body']['hairColor'] == u'brown':
                hair = HairColor.objects.get(code='black')
            elif i['persons'][0]['body']['hairColor'] == u'black':
                hair = HairColor.objects.get(code='black')
            elif i['persons'][0]['body']['hairColor'] == u'other':
                hair = HairColor.objects.get(code='black')
            elif i['persons'][0]['body']['hairColor'] == u'blonde':
                hair = HairColor.objects.get(code='white')
            elif i['persons'][0]['body']['hairColor'] == u'blue':
                hair = HairColor.objects.get(code='white')
            elif i['persons'][0]['body']['hairColor'] == u'clown hair':
                hair = HairColor.objects.get(code='white')
            elif i['persons'][0]['body']['hairColor'] == u'orange':
                hair = HairColor.objects.get(code='red')
            elif i['persons'][0]['body']['hairColor'] == u'pink':
                hair = HairColor.objects.get(code='red')
            elif i['persons'][0]['body']['hairColor'] == u'auburn':
                hair = HairColor.objects.get(code='red')
            elif i['persons'][0]['body']['hairColor'] == u'fire red':
                hair = HairColor.objects.get(code='red')
            else:
                hair = None

            if i['persons'][0]['body']['breastSize'] == u'big':
                bust_size = BustSize.objects.get(code='big')
            elif i['persons'][0]['body']['breastSize'] == u'normal':
                bust_size = BustSize.objects.get(code='middle')
            elif i['persons'][0]['body']['breastSize'] == u'tiny':
                bust_size = BustSize.objects.get(code='small')
            elif i['persons'][0]['body']['breastSize'] == u'huge':
                bust_size = BustSize.objects.get(code='biggest')
            else:
                bust_size = None

            if i['persons'][0]['body']['build'] == u'skinny':
                figure = Figure.objects.get(code='s')
            elif i['persons'][0]['body']['build'] == u'petite':
                figure = Figure.objects.get(code='s')
            elif i['persons'][0]['body']['build'] == u'athletic':
                figure = Figure.objects.get(code='n')
            elif i['persons'][0]['body']['build'] == u'average':
                figure = Figure.objects.get(code='n')
            elif i['persons'][0]['body']['build'] == u'muscular':
                figure = Figure.objects.get(code='n')
            elif i['persons'][0]['body']['build'] == u'above average':
                figure = Figure.objects.get(code='c')
            elif i['persons'][0]['body']['build'] == u'obese':
                figure = Figure.objects.get(code='l')
            elif i['persons'][0]['body']['build'] == u'large':
                figure = Figure.objects.get(code='l')
            else:
                figure = None

            try:
                check_online = Model.objects.get(name=cam.prefix + i['performerId'])
            except Model.DoesNotExist:
                check_online = None

            data = {
                'name': cam.prefix + i['performerId'],
                'display_name': i['performerId'],
                'profile_image': i['profilePictureUrl']['size320x240'],
                'age': i['persons'][0]['age'],
                'available': True,
                'cam_service': cam,
                'chat_url': i['chatRoomUrl'],
                #'online_time': i['seconds_online'],
                'sex': sex,
                'race': race,
                'hair_color': hair,
                'bust_size': bust_size,
                'figure': figure,
            }

            Model.objects.update_or_create(
                name=cam.prefix + i['performerId'],
                defaults=data
            )

            profiles = Profile.objects.filter(role=Profile.ROLE_USER)
            favourites = FavoriteModel.objects.all()
            if not check_online:
                data.update({'bay_online_time': datetime.now()})
                print 'new'
            elif not check_online.bay_online_time:
                data.update({'bay_online_time': datetime.now()})
                print 'update'
                for p in profiles:
                    # if p in favourites:
                    model_went_online(p, check_online)
                    print 'sent'

            updated, created = Model.objects.update_or_create(
                name=cam.prefix + i['performerId'],
                defaults=data
            )
            if updated:
                changed_objects.append(updated)
            elif created:
                changed_objects.append(created)

        Model.objects.filter(cam_service__prefix='jasmin2').exclude(name__in=changed_objects).update(available=False,
                                                                                                   bay_online_time=None)
        return JsonResponse({'success': True})