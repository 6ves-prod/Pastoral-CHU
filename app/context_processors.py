from django.conf import settings


def seo(request):
    return {
        "google_site_verification": settings.GOOGLE_SITE_VERIFICATION,
        "ga_measurement_id": settings.GA_MEASUREMENT_ID,
    }
