# -*- coding: UTF-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class AuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        try:
            user = user_model._default_manager.get(email=username)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            user_model().set_password(password)

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model._default_manager.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


class OneTimeAccess(AuthBackend):

    def authenticate(self, email=None, access_key=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model._default_manager.get(email=email, access_key=access_key, access_key_active=True)
            return user
        except user_model.DoesNotExist:
            pass
        return None


class EmailAccess(AuthBackend):
    def authenticate(self, user, **kwargs):
        return user
