# -*- coding: utf-8 -*-
import json
import urllib

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from main.models import CamService, Model, Race, HairColor, BustSize, CamSnapshot, Sex, Figure


def load_api_data(service):
    cam = CamService.objects.get(prefix=service)
    response = urllib.urlopen(cam.api_url)
    return cam, json.loads(response.read())


class BongaShowApi(TemplateView):
    template_name = 'api-update-log.html'
    cam, data = load_api_data('bonga')

    def get_context_data(self, **kwargs):
        context = super(BongaShowApi, self).get_context_data(**kwargs)
        gender = []
        primary_language_key = []
        secondary_language_key = []
        weight = []
        hair_color = []
        height = []
        pubic_hair = []
        ethnicity = []
        sh_bust_penis_size = []

        for i in self.data:
            gender.append(i['gender'])
            primary_language_key.append(i['primary_language_key'])
            secondary_language_key.append(i['secondary_language_key'])
            weight.append(i['weight'])
            hair_color.append(i['hair_color'])
            pubic_hair.append(i['pubic_hair'])
            ethnicity.append(i['ethnicity'])
            sh_bust_penis_size.append(i['bust_penis_size'])

            context['gender'] = list(set(gender))
            context['primary_language_key'] = list(set(primary_language_key))
            context['secondary_language_key'] = list(set(secondary_language_key))
            context['weight'] = list(set(weight))
            context['hair_color'] = list(set(hair_color))
            context['pubic_hair'] = list(set(pubic_hair))
            context['ethnicity'] = list(set(ethnicity))
            context['sh_bust_penis_size'] = list(set(sh_bust_penis_size))
        return context


class BongaUpdateApi(View):
    cam, data = load_api_data('bonga')

    def get(self, *args, **kwargs):

        Model.objects.all().update(available=False)

        for i in self.data:
            if i['ethnicity'] == u'Европейское/Кавказское':
                race = Race.objects.get(code='white')
            elif i['ethnicity'] == u'Латиноамериканское':
                race = Race.objects.get(code='latin')
            elif i['ethnicity'] == u'Ближневосточное':
                race = Race.objects.get(code='west')
            elif i['ethnicity'] == u'Индийское':
                race = Race.objects.get(code='indian')
            elif i['ethnicity'] == u'Темнокожие':
                race = Race.objects.get(code='black')
            elif i['ethnicity'] == u'Азиатcкое':
                race = Race.objects.get(code='asian')
            else:
                race = None

            if i['hair_color'] == u'Тёмные':
                hair = HairColor.objects.get(code='black')
            elif i['hair_color'] == u'Светлые':
                hair = HairColor.objects.get(code='white')
            elif i['hair_color'] == u'Рыжие':
                hair = HairColor.objects.get(code='red')
            else:
                hair = None

            if i['bust_penis_size'] == u'Большая':
                bust_penis_size = BustSize.objects.get(code='big')
            elif i['bust_penis_size'] == u'Средняя':
                bust_penis_size = BustSize.objects.get(code='middle')
            elif i['bust_penis_size'] == u'Маленькая':
                bust_penis_size = BustSize.objects.get(code='small')
            elif i['bust_penis_size'] == u'Огромные':
                bust_penis_size = BustSize.objects.get(code='biggest')
            else:
                bust_penis_size = None

            data = {
                'name': self.cam.prefix + i['username'],
                'display_name': i['username'],
                'profile_image': i['profile_images']['thumbnail_image_medium'],
                'age': i['display_age'],
                'available': True if i['status'] == 1 else False,
                'cam_service': self.cam,
                'chat_url': i['chat_url_on_home_page'],
                'online_time': i['online_time'],
                'race': race,
                'hair_color': hair,
                'bust_size': bust_penis_size,
            }

            Model.objects.update_or_create(
                name=self.cam.prefix + i['username'],
                defaults=data
            )

            CamSnapshot.objects.create(
                model=Model.objects.get(name=self.cam.prefix + i['username']),
                snapshot_url=i['profile_images']['thumbnail_image_medium_live'],
            )

        return JsonResponse({'success': True})


class ChaturShowApi(TemplateView):
    template_name = 'api-update-log.html'
    cam, data = load_api_data('chatur')

    def get_context_data(self, **kwargs):
        context = super(ChaturShowApi, self).get_context_data(**kwargs)
        gender = []
        primary_language_key = []
        secondary_language_key = []
        weight = []
        hair_color = []
        height = []
        pubic_hair = []
        ethnicity = []
        sh_bust_penis_size = []

        for i in self.data:
            gender.append(i['gender'])
            primary_language_key.append(i['spoken_languages'])
            #secondary_language_key.append(i['secondary_language_key'])
            weight.append(i['tags'])
            #hair_color.append(i['hair_color'])
            #pubic_hair.append(i['pubic_hair'])
            #ethnicity.append(i['ethnicity'])
            #sh_bust_penis_size.append(i['bust_penis_size'])

            context['gender'] = list(set(gender))
            context['primary_language_key'] = list(set(primary_language_key))
            #context['secondary_language_key'] = list(set(secondary_language_key))
            #context['weight'] = list(set(weight))
            #context['hair_color'] = list(set(hair_color))
            #context['pubic_hair'] = list(set(pubic_hair))
            #context['ethnicity'] = list(set(ethnicity))
            #context['sh_bust_penis_size'] = list(set(sh_bust_penis_size))
        return context


class ChaturUpdateApi(View):
    cam, data = load_api_data('chatur')

    def get(self, *args, **kwargs):

        #Model.objects.all().update(available=False)

        for i in self.data:

            data = {
                'name': self.cam.prefix + i['username'],
                'display_name': i['username'],
                'profile_image': i['image_url'],
                'age': i['age'],
                'available': True,
                'cam_service': self.cam,
                'chat_url': i['chat_room_url'],
                'online_time': i['seconds_online'],
                # 'race': race,
                # 'hair_color': hair,
                # 'bust_size': bust_penis_size,
            }

            Model.objects.update_or_create(
                name=self.cam.prefix + i['username'],
                defaults=data
            )

            CamSnapshot.objects.create(
                model=Model.objects.get(name=self.cam.prefix + i['username']),
                snapshot_url=i['image_url'],
            )

        return JsonResponse({'success': True})


"""
Jasmin
"""
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
        cam = CamService.objects.get(prefix='jasmin')
        response = urllib.urlopen(cam.api_url)
        cam_data = json.loads(response.read())
        #Model.objects.all().update(available=False)

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

            # CamSnapshot.objects.create(
            #     model=Model.objects.get(name=self.cam.prefix + i['username']),
            #     snapshot_url=i['image_url'],
            # )

        return JsonResponse({'success': True})



"""
Xcams
"""
class XcamsShowApi(TemplateView):
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


class XcamsUpdateApi(View):

    def get(self, *args, **kwargs):
        #cam, data = load_api_data('jasmin')
        cam = CamService.objects.get(prefix='jasmin')
        response = urllib.urlopen(cam.api_url)
        cam_data = json.loads(response.read())
        #Model.objects.all().update(available=False)

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

            # CamSnapshot.objects.create(
            #     model=Model.objects.get(name=self.cam.prefix + i['username']),
            #     snapshot_url=i['image_url'],
            # )

        return JsonResponse({'success': True})