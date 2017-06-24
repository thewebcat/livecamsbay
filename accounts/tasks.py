# coding=utf-8
from django.db.models import Sum

from bulk_update.helper import bulk_update

from amigostone import celery
from accounts.models import Profile
from common.models import PointSystem


@celery.app.task(name='recalculate position')
def recalculate_position():
    profiles = Profile.objects.producers() \
        .annotate(points=Sum('pointaction__content_type__pointsystem__point')).order_by('-points')
    for i, v in enumerate(profiles):
        v.position = i + 1
    bulk_update(profiles, update_fields=['position'])

@celery.app.task(name='recalculate position 2')
def recalculate_position2():
    """
     Таск для пересчета рейтинга и позиций
    """
    # обнуляем позиции для всех компаний
    Profile.objects.update(position=None)

    profile_qs = Profile.objects.producers()
    ps_qs = PointSystem.objects.all()

    for profile in profile_qs:
        points = 0
        for ps in ps_qs:
            content = ps.model.model_class()
            if content.__name__ == type(profile).__name__:
                points += ps.point(profile)
            elif content.__name__ == 'ProfileBankDetails':
                for item in content.objects.filter(profile=profile):
                    points += ps.point(item)
                    #print "%s - %s" % (content.__name__, ps.point(item))
            elif content.__name__ == 'Order':
                points += content.objects.filter(performer=profile, completed=True).count() * ps.point()
            else:
                points += content.objects.filter(profile=profile, state=1).count() * ps.point()
        #print (profile, ' - ', points)
        profile.point = points

    bulk_update(profile_qs, update_fields=['point'])

    profiles = profile_qs.order_by('-point')
    for i, v in enumerate(profiles, 1):
        v.position = i

    bulk_update(profiles, update_fields=['position'])