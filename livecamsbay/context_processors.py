from django.conf import settings


def get_settings(request):
    return {
        # 'WS_SERVER': settings.WS_SERVER,
        # 'WS_PORT': settings.WS_PORT,
        'NORECAPTCHA_SITE_KEY': settings.NORECAPTCHA_SITE_KEY,
        # 'UPLOAD_FILE_MAX_SIZE': settings.UPLOAD_FILE_MAX_SIZE,
        # 'RATE_TOOLTIPS': settings.RATE_TOOLTIPS,
    }


def get_cam_services(request):
    from main.models import CamService
    cam_services = CamService.objects.all()
    return {'cam_services': cam_services}