# -*- coding: utf-8 -*-
from datetime import datetime
from accounts.models import FavoriteModel, Profile
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from main.emails import model_went_online
from main.models import CamSnapshot, Model, BustSize, HairColor, Race, Sex
from update_api.views import load_api_data


class ChaturShowApi(TemplateView):
    template_name = 'api-update-log.html'
    cam, data = load_api_data('chatur')

    def get_context_data(self, **kwargs):
        context = super(ChaturShowApi, self).get_context_data(**kwargs)
        gender = []
        primary_language_key = []
        secondary_language_key = []
        weight = []

        for i in self.data:
            gender.append(i['gender'])
            primary_language_key.append(i['spoken_languages'])
            #secondary_language_key.append(i['secondary_language_key'])
            weight.append(i['tags'])
            context['gender'] = list(set(gender))
            context['primary_language_key'] = list(set(primary_language_key))

        return context


class ChaturUpdateApi(View):
    cam, data = load_api_data('chatur')

    def get(self, *args, **kwargs):

        changed_objects = []
        for i in self.data:
            if i['gender'] == u'f':
                sex = Sex.objects.get(code='w')
            elif i['gender'] == u'm':
                sex = Sex.objects.get(code='m')
            elif i['gender'] == u't':
                sex = Sex.objects.get(code='t')
            elif i['gender'] == u'c':
                sex = Sex.objects.get(code='w')
            else:
                sex = None

            try:
                check_online = Model.objects.get(name=self.cam.prefix + i['username'])
            except Model.DoesNotExist:
                check_online = None

            data = {
                'name': self.cam.prefix + i['username'],
                'display_name': i['username'],
                'profile_image': i['image_url'],
                'age': i['age'],
                'available': True,
                'cam_service': self.cam,
                'chat_url': i['chat_room_url'],
                'online_time': i['seconds_online'],
                'sex': sex,
                # 'race': race,
                # 'hair_color': hair,
                # 'bust_size': bust_penis_size,
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
                    # if p in favourites:
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
                snapshot_url=i['image_url'],
            )

        Model.objects.filter(cam_service__prefix='chatur').exclude(name__in=changed_objects).update(available=False,
                                                                                                   bay_online_time=None)
        return JsonResponse({'success': True})
