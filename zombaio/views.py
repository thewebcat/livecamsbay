# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from livecamsbay.settings import ZOMBAIO_PASS
from accounts.models import Profile

import json

class GwView(View):
    def get(self, request, *args, **kwargs):
        auth = request.GET.get('ZombaioGWPass')
#        hash_str = request.user.profile.profilehash.hash_str
        if auth == ZOMBAIO_PASS:
            action = request.GET.get('Action')
            username = request.GET.get('username')
            password = request.GET.get('password')
            if action == 'get.path':
                return HttpResponse('')
            elif action == 'get.passfile':
                return HttpResponse('')
            elif action == 'user.add':
                try:
                    profile_hash = Profile.objects.get(user__email=username).profilehash.hash_str
                    if profile_hash == password:
                        return HttpResponse('OK|User added!')
                    else:
                        return HttpResponse('')
                except Profile.DoesNotExist:
                    return HttpResponse('')
            else:
                return HttpResponse('UNKNOW_ACTION|UNKNOW_ACTION')
        else:
            return HttpResponse('<h1>Zombaio Gateway 1.1</h1><h3>Authentication failed.</h3>', status=401)
# OK|User deleted!
# USER_DOES_NOT_EXIST | User does not exist!
