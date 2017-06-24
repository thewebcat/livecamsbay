# from django.core.cache import cache
#
# from accounts.models import Profile
#
#
# def get_companies():
#     return cache.get_or_set('companies_ratings',
#                             lambda: Profile.objects.filter(completed=True, certified=True).exclude(role=Profile.ROLE_USER).order_by('-points'), 100)
#
#
# def get_positions():
#     return cache.get_or_set('company_position', lambda: {pr.id: index for index, pr in enumerate(get_companies())}, 100)
