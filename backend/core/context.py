from django.conf import settings


def feature_flags(_request):
    return {
        'ENABLE_ADMIN': settings.ENABLE_ADMIN,
    }
