# -*- coding: utf-8 -*-
from datetime import datetime
from accounts.models import FavoriteModel, Profile
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from main.emails import model_went_online
from main.models import CamSnapshot, Model, BustSize, HairColor, Race, Sex
from update_api.views import load_api_data


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

        #Model.objects.filter(cam_service__prefix='bonga').update(available=False)
        changed_objects = []
        for i in self.data:
            if i['gender'] == u'Женщины':
                sex = Sex.objects.get(code='w')
            elif i['gender'] == u'Пара Женщина + Женщина':
                sex = Sex.objects.get(code='w')
            elif i['gender'] == u'Пара женщина + мужчина':
                sex = Sex.objects.get(code='w')
            else:
                sex = None

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

            try:
                check_online = Model.objects.get(name=self.cam.prefix + i['username'])
            except Model.DoesNotExist:
                check_online = None

            data = {
                'name': self.cam.prefix + i['username'],
                'display_name': i['username'],
                'profile_image': i['profile_images']['thumbnail_image_medium'],
                'age': i['display_age'],
                'available': True if i['status'] == 1 else False,
                'cam_service': self.cam,
                'chat_url': i['chat_url_on_home_page'],
                'online_time': i['online_time'],
                'sex': sex,
                'race': race,
                'hair_color': hair,
                'bust_size': bust_penis_size,
            }
            profiles = Profile.objects.filter(role=Profile.ROLE_USER)
            favourites = FavoriteModel.objects.all()
            if not check_online:
                data.update({'bay_online_time': datetime.now()})
                print 'new'
            elif not check_online.bay_online_time:
                data.update({'bay_online_time': datetime.now()})
                print 'update'
                for p in profiles:
                    #if p in favourites:
                        model_went_online(p, check_online)
                        print 'sent'

            updated, created = Model.objects.update_or_create(
                name=self.cam.prefix + i['username'],
                defaults=data
            )
            if updated:
                changed_objects.append(updated)
            elif created:
                changed_objects.append(created)

            CamSnapshot.objects.create(
                model=Model.objects.get(name=self.cam.prefix + i['username']),
                snapshot_url=i['profile_images']['thumbnail_image_medium_live'],
            )

        Model.objects.filter(cam_service__prefix='bonga').exclude(name__in=changed_objects).update(available=False, bay_online_time=None)

        return JsonResponse({'success': True})